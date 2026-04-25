# inference.py — Master agent baseline for CORP-ENV (local Environment + OpenAI-compatible API)
#
# Uses the four action types: delegate, update_swd (JSON Patch), query_swd (JSONPath), finalize.

from __future__ import annotations

import argparse
import json
import os
import re
import textwrap
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from openai import OpenAI

from corp_env.models import CorpAction, CorpObservation
from server.environment import CorpEnvironment
from server.llm_env import openai_client_kwargs_master

load_dotenv()

MASTER_KWARGS = openai_client_kwargs_master()
MASTER_API_KEY = MASTER_KWARGS.get("api_key")
MODEL_NAME = os.getenv("CORP_MASTER_MODEL") or os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

BENCHMARK = "corp-env"
MAX_HISTORY_MESSAGES = 40
MAX_RETRIES = 5
RETRY_BASE_DELAY = 2

DEFAULT_TASKS = ["e1_launch_readiness", "m1_budget_reallocation", "h1_acquisition_defence"]

SYSTEM_PROMPT = textwrap.dedent(
    """\
    You are the Master Agent in CORP-ENV. You govern a Shared Workspace Document (SWD)
    shown in each observation. You coordinate frozen worker agents and maintain SWD
    integrity until you call finalize.

    Rules:
    1. Respond with ONLY a valid JSON object (no markdown fences).
    2. Include a "thought" key first (reasoning), then action fields matching CorpAction.
    3. action_type is one of: delegate, update_swd, query_swd, finalize.
    4. For delegate: set agent_id to one of the available_agents from the observation;
       payload is the task description for that worker. Optional: put milestone_id in metadata.
    5. For update_swd: payload is a JSON array (RFC 6902) of patch operations as a STRING.
    6. For query_swd: payload is a JSONPath expression (read-only).
    7. For finalize: payload is the final recommendation — for E1 use the string GO or NO_GO;
       for M1/H1 use a JSON object string with required keys from the task rubric.
    8. Use update_swd to append to decisions, conflicts_identified, conflict_resolutions,
       reasoning_log, and to advance phase when appropriate.

    JSON schema (fields besides optional metadata):
    {
      "thought": "string",
      "action_type": "delegate|update_swd|query_swd|finalize",
      "agent_id": "string or null",
      "payload": "string"
    }
    """
).strip()


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    err = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.3f} done={str(done).lower()} error={err}",
        flush=True,
    )


def log_end(task: str, steps: int, score: float, rewards: List[float]) -> None:
    rs = ",".join(f"{r:.3f}" for r in rewards)
    print(f"[END] task={task} steps={steps} score={score:.3f} rewards={rs}", flush=True)


class SwdTraceWriter:
    """Append SWD snapshots to a dedicated file (not mixed with console logs)."""

    def __init__(self, path: Optional[str], task_id: str) -> None:
        self.path = path.strip() if path else None
        self.task_id = task_id
        self._jsonl = bool(self.path and self.path.lower().endswith(".jsonl"))
        if not self.path:
            return
        p = Path(self.path)
        p.parent.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
        with p.open("a", encoding="utf-8") as f:
            f.write(
                f"\n{'=' * 72}\n"
                f"# CORP-ENV SWD trace | task={task_id} | started_utc={ts}\n"
                f"{'=' * 72}\n"
            )

    def write(
        self,
        *,
        phase: str,
        step_index: int,
        action: Optional[CorpAction],
        obs: CorpObservation,
    ) -> None:
        if not self.path:
            return
        action_blob: Dict[str, Any]
        if action is None:
            action_blob = {"note": "initial observation after reset"}
        else:
            action_blob = action.model_dump(mode="json", exclude_none=True)

        if self._jsonl:
            record = {
                "phase": phase,
                "step_index": step_index,
                "env_turn": obs.turn,
                "reward": obs.reward,
                "done": obs.done,
                "error": obs.error,
                "action": action_blob,
                "swd": obs.swd,
            }
            line = json.dumps(record, ensure_ascii=False)
            with Path(self.path).open("a", encoding="utf-8") as f:
                f.write(line + "\n")
            return

        with Path(self.path).open("a", encoding="utf-8") as f:
            f.write(
                f"\n--- {phase} step_index={step_index} env_turn={obs.turn} "
                f"reward={obs.reward} done={obs.done} ---\n"
            )
            f.write(f"action: {json.dumps(action_blob, indent=2, ensure_ascii=False)}\n")
            f.write(f"swd:\n{json.dumps(obs.swd, indent=2, ensure_ascii=False)}\n")


def extract_json(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```\s*$", "", cleaned)
    cleaned = cleaned.strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    start = cleaned.find("{")
    if start == -1:
        raise ValueError("No JSON object found")
    depth = 0
    in_string = False
    escape_next = False
    for i in range(start, len(cleaned)):
        c = cleaned[i]
        if escape_next:
            escape_next = False
            continue
        if c == "\\" and in_string:
            escape_next = True
            continue
        if c == '"' and not escape_next:
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(cleaned[start : i + 1])
    raise ValueError("Unbalanced braces")


def parse_action(raw_text: str) -> CorpAction:
    d = extract_json(raw_text)
    d.pop("thought", None)
    return CorpAction.model_validate(d)


def build_observation_message(step: int, obs: CorpObservation) -> str:
    parts = [
        f"--- Step {step} ---",
        f"Role: {obs.role}",
        f"Task: {obs.task_description}",
        f"Available agents: {', '.join(obs.available_agents)}",
        f"Turn: {obs.turn}  tokens_used: {obs.tokens_used}/{obs.token_budget}",
        f"SWD:\n{json.dumps(obs.swd, indent=2)[:12000]}",
    ]
    if obs.agent_last_output:
        parts.append(f"Last worker output:\n{obs.agent_last_output[:4000]}")
    if obs.query_result is not None:
        parts.append(f"Query result: {json.dumps(obs.query_result)[:2000]}")
    if obs.error:
        parts.append(f"Error: {obs.error}")
    parts.append(f"Reward (last step): {obs.reward}")
    parts.append("Respond with your next JSON action.")
    return "\n".join(parts)


def trim_history(messages: list, max_messages: int = MAX_HISTORY_MESSAGES) -> None:
    while len(messages) > max_messages:
        messages.pop(1)


def run_episode(
    client: OpenAI,
    task_id: str,
    max_steps: int,
    swd_trace: Optional[SwdTraceWriter],
) -> tuple[float, int, List[float]]:
    os.environ["CORP_TASK_ID"] = task_id
    os.environ.setdefault("CORP_STUB_WORKERS", "1")

    env = CorpEnvironment()
    rewards: List[float] = []
    total = 0.0
    steps = 0

    log_start(task=task_id, env=BENCHMARK, model=MODEL_NAME)
    obs = env.reset(task_id=task_id)
    if swd_trace:
        swd_trace.write(phase="after_reset", step_index=0, action=None, obs=obs)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_observation_message(0, obs)},
    ]

    for step in range(1, max_steps + 1):
        if obs.done:
            break
        trim_history(messages)
        raw_text = None
        for attempt in range(MAX_RETRIES):
            try:
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=2048,
                )
                raw_text = (completion.choices[0].message.content or "").strip()
                break
            except Exception as exc:
                exc_s = str(exc)
                if ("429" in exc_s or "rate" in exc_s.lower()) and attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_BASE_DELAY * (2**attempt))
                    continue
                print(f"[ERROR] {exc}", flush=True)
                log_end(task_id, step, total, rewards)
                return total, step, rewards

        if raw_text is None:
            continue

        messages.append({"role": "assistant", "content": raw_text})
        try:
            action = parse_action(raw_text)
            alog = action.model_dump_json(exclude_none=True)
        except Exception as exc:
            action = CorpAction(action_type="query_swd", payload="$.phase")
            alog = f"PARSE_ERROR: {exc}"
            messages.append(
                {
                    "role": "user",
                    "content": f"Invalid JSON action: {exc}. Fix and output only JSON.",
                }
            )

        obs = env.step(action)
        rewards.append(float(obs.reward or 0.0))
        total += float(obs.reward or 0.0)
        steps = step
        log_step(step, alog[:200], float(obs.reward or 0.0), obs.done, obs.error)
        if swd_trace:
            swd_trace.write(phase="after_step", step_index=step, action=action, obs=obs)
        messages.append({"role": "user", "content": build_observation_message(step, obs)})
        if obs.done:
            break

    log_end(task_id, steps, total, rewards)
    return total, steps, rewards


def deterministic_e1_smoke(swd_trace: Optional[SwdTraceWriter] = None) -> None:
    """Offline smoke: E1 solved with stub workers (no master LLM)."""
    os.environ["CORP_TASK_ID"] = "e1_launch_readiness"
    os.environ["CORP_STUB_WORKERS"] = "1"
    env = CorpEnvironment()
    obs = env.reset(task_id="e1_launch_readiness")
    if swd_trace:
        swd_trace.write(phase="after_reset", step_index=0, action=None, obs=obs)
    seq = [
        CorpAction(action_type="delegate", agent_id="dev_agent", payload="Assess launch readiness"),
        CorpAction(action_type="delegate", agent_id="hr_agent", payload="Staffing sign-off"),
        CorpAction(
            action_type="update_swd",
            payload=json.dumps(
                [{"op": "add", "path": "/decisions/-", "value": {"summary": "Ready with mitigations"}}]
            ),
        ),
        CorpAction(action_type="finalize", payload="GO"),
    ]
    total = 0.0
    rlist: List[float] = []
    for i, act in enumerate(seq, start=1):
        obs = env.step(act)
        r = float(obs.reward or 0.0)
        total += r
        rlist.append(r)
        log_step(i, act.action_type, r, obs.done, obs.error)
        if swd_trace:
            swd_trace.write(phase="after_step", step_index=i, action=act, obs=obs)
    log_end("e1_launch_readiness", len(seq), total, rlist)


def main() -> None:
    parser = argparse.ArgumentParser(description="CORP-ENV baseline master agent")
    parser.add_argument(
        "--tasks",
        type=str,
        default=",".join(DEFAULT_TASKS),
        help="Comma-separated task ids",
    )
    parser.add_argument("--max-steps", type=int, default=30, help="Max steps per episode")
    parser.add_argument(
        "--swd-trace",
        type=str,
        default=os.getenv("CORP_SWD_TRACE_FILE", ""),
        help="Append SWD evolution to this file (.jsonl recommended). Overrides CORP_SWD_TRACE_FILE.",
    )
    args = parser.parse_args()

    trace_path = (args.swd_trace or "").strip() or None

    if not MASTER_API_KEY:
        print(
            "No master API key (set CORP_MASTER_API_KEY or HF_TOKEN / OPENAI_API_KEY) - "
            "running deterministic E1 smoke only. Set keys to run the LLM master on --tasks.",
            flush=True,
        )
        tw = SwdTraceWriter(trace_path, "e1_launch_readiness") if trace_path else None
        deterministic_e1_smoke(swd_trace=tw)
        return

    client = OpenAI(**MASTER_KWARGS)
    for tid in [t.strip() for t in args.tasks.split(",") if t.strip()]:
        ms = args.max_steps * 2 if tid == "h1_acquisition_defence" else args.max_steps
        tw = SwdTraceWriter(trace_path, tid) if trace_path else None
        run_episode(client, tid, max_steps=ms, swd_trace=tw)


if __name__ == "__main__":
    main()
