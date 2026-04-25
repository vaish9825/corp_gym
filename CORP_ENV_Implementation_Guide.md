# CORP-ENV: Step-by-Step Implementation Guide
### OpenEnv Hackathon India 2026 — Build Plan for Claude Opus

---

## THE CORE THESIS (memorise this for the pitch)

> **EnterpriseOps-Gym** (ServiceNow, Mar 2026) proved frontier LLMs fail at 37% of enterprise tasks. The bottleneck is *planning*, not tool use. No RL training environment exists to fix it. **CORP-ENV** is that environment. We train a 7B model to maintain a shared context document across a long multi-agent episode — the exact capability that makes frontier models fail.

---

## WHAT WE ARE ACTUALLY BUILDING

One sentence: **An RL environment where a Master Agent must govern a shared Workspace Document across a long multi-turn corporate decision episode, coordinating frozen Worker Agents, while the document's integrity, completeness and coherence are what the reward is primarily measuring.**

The workspace document IS the product. Not the final answer. The journey of building and maintaining it is what gets rewarded.

This is different from EnterpriseOps-Gym (benchmark only) and from MARTI/Agent-R1 (code/math tasks). Nothing in OpenEnv Hub targets **shared-context governance in a business planning setting**.

---

## PART 0 — ARCHITECTURE DECISIONS (settle these first)

### 0.1 Why no `max_steps` as a hard cap

Long-horizon planning means the agent should not be penalised just for taking time. Instead:
- Use **token budget awareness**: state includes `tokens_used / token_budget`
- Use **milestone deadlines**: each subtask has an expected completion window
- Episode ends on: `finalize()` called, or token_budget exceeded, or all milestones missed
- Efficiency reward is based on milestone adherence, not raw step count

### 0.2 The Shared Workspace Document (SWD)

This is a persistent JSON document that the agent reads and writes every turn. It is the environment's core state. Every reward component references it.

```json
{
  "episode_id": "uuid",
  "scenario": "string",
  "phase": "discovery | analysis | decision | execution",
  "milestones": [
    {
      "id": "m1",
      "label": "string",
      "due_by_turn": 8,
      "status": "pending | in_progress | complete | missed",
      "owner": "agent_name | master",
      "output": null
    }
  ],
  "agent_reports": {
    "dev": null,
    "hr": null,
    "finance": null
  },
  "decisions": [],
  "conflicts_identified": [],
  "conflict_resolutions": [],
  "reasoning_log": [],
  "final_recommendation": null,
  "swd_version": 1
}
```

**Key insight**: The SWD version increments every write. Reward checks diff between versions to ensure meaningful updates (not just re-writing the same content).

### 0.3 Three Worker Agents (frozen)

All implemented as the same base model with different system prompts. Called via `delegate()`.

| Agent | Domain | Can conflict with |
|---|---|---|
| `dev_agent` | Technical feasibility, timelines, risk | `finance_agent` |
| `hr_agent` | Headcount, policy, compliance | `exec_agent` |
| `finance_agent` | Budget, ROI, cost projections | `dev_agent` |

### 0.4 Four Action Types

```
delegate(agent_id, task_description, milestone_id)
update_swd(json_patch)               # RFC 6902 JSON Patch
query_swd(jsonpath_expression)       # read-only, no reward
finalize(recommendation)
```

`query_swd` is free (no reward signal, no penalty) — it lets the agent re-read its own document without writing noise.

---

## PART 1 — TASK DESIGN

### Design Principle
- **Easy**: Zero-shot solvable. One agent, one phase, no conflicts. Teaches SWD format.
- **Medium**: Requires two agents, two phases, one reconcilable conflict.  
- **Hard**: Three agents, all four phases, contradictory intel, requires explicit conflict_resolution + phased plan. Designed to fail frontier models without training.

---

### TASK E1 — Product Launch Readiness Check

**Scenario**: As PM, a new feature is scheduled to launch in 48h. You must verify it is ready.

**Available agents**: `dev_agent`, `hr_agent`

**Phases**: discovery → decision

**SWD milestones**:
- M1 (turn ≤4): dev readiness confirmed in `agent_reports.dev`
- M2 (turn ≤7): HR sign-off on support staffing in `agent_reports.hr`
- M3 (turn ≤10): `final_recommendation` populated with go/no-go + reason

**Deterministic verification**:
```python
def verify_e1(swd):
    checks = {
        "dev_report_present": swd["agent_reports"]["dev"] is not None,
        "hr_report_present": swd["agent_reports"]["hr"] is not None,
        "final_rec_valid": swd["final_recommendation"] in ["GO", "NO_GO"],
        "reason_present": len(swd.get("decisions", [])) >= 1,
        "no_missed_milestones": all(
            m["status"] != "missed" for m in swd["milestones"]
        ),
        "swd_version_advanced": swd["swd_version"] >= 4,
    }
    return checks
```

**Why zero-shot solvable**: single path, no conflict, expected outputs are obvious from task description.

---

### TASK M1 — Cross-Department Budget Reallocation

**Scenario**: As CFO, engineering wants 40% more budget for infra. HR says headcount is at risk if cut. Finance has a fixed envelope. You must produce a phased reallocation plan.

**Available agents**: `dev_agent`, `hr_agent`, `finance_agent`

**Phases**: discovery → analysis → decision

**SWD milestones**:
- M1 (turn ≤5): All three agent_reports populated
- M2 (turn ≤10): At least one `conflicts_identified` entry (dev vs finance OR hr vs finance)
- M3 (turn ≤14): At least one `conflict_resolutions` entry matching a conflict id
- M4 (turn ≤18): `final_recommendation` includes "phase_1" and "phase_2" keys

**Deterministic verification**:
```python
def verify_m1(swd):
    final = swd.get("final_recommendation") or {}
    checks = {
        "all_agents_consulted": all(
            swd["agent_reports"].get(a) is not None 
            for a in ["dev", "hr", "finance"]
        ),
        "conflict_logged": len(swd.get("conflicts_identified", [])) >= 1,
        "conflict_resolved": len(swd.get("conflict_resolutions", [])) >= 1,
        "phased_plan": isinstance(final, dict) and "phase_1" in final and "phase_2" in final,
        "budget_constraint_acknowledged": any(
            "budget" in str(d).lower() for d in swd.get("decisions", [])
        ),
        "reasoning_documented": len(swd.get("reasoning_log", [])) >= 3,
    }
    return checks
```

---

### TASK H1 — Hostile Acquisition Defence (Frontier-Model Killer)

**Scenario**: As CEO, a competitor has made an acquisition offer at 2.3x current valuation. Three advisors have been consulted but their reports *contradict each other*.

**Injected intel conflicts (hard-coded in task)**:
- `dev_agent` says: "Our tech stack is 18 months ahead, acquirer cannot replicate it — hold out for 3.5x"
- `finance_agent` says: "Cash runway is 7 months at burn rate, board will not approve a 3.5x ask — realistic ceiling is 2.6x"  
- `hr_agent` says: "Key engineering talent has competing offers, 60% retention risk if deal drags past 90 days"

**No single agent is wrong.** The CEO must reconcile all three views into a recommendation that satisfies: timeline constraint (hr), financial reality (finance), and strategic positioning (dev).

**Phases**: all four (discovery → analysis → decision → execution)

**SWD milestones**:
- M1 (turn ≤6): All three agent_reports present
- M2 (turn ≤10): `conflicts_identified` contains ≥2 entries with cross-references to agents
- M3 (turn ≤15): `conflict_resolutions` contains entry with `resolution_type` field
- M4 (turn ≤20): `final_recommendation` contains `counter_offer`, `deadline`, `retention_plan`
- M5 (turn ≤22): `reasoning_log` contains ≥5 entries with distinct `turn` values

**Deterministic verification** (rubric — each check independently scored):
```python
def verify_h1(swd):
    final = swd.get("final_recommendation") or {}
    resolutions = swd.get("conflict_resolutions", [])
    
    checks = {
        # Structural completeness (always deterministic)
        "all_agents_consulted": all(swd["agent_reports"].get(a) for a in ["dev","hr","finance"]),
        "multi_conflict_logged": len(swd.get("conflicts_identified", [])) >= 2,
        "conflict_explicitly_resolved": len(resolutions) >= 1,
        "resolution_has_type": any("resolution_type" in r for r in resolutions),
        "rich_reasoning_log": len(swd.get("reasoning_log", [])) >= 5,
        
        # Content checks (regex-based)
        "counter_offer_present": "counter_offer" in final,
        "deadline_present": "deadline" in final,
        "retention_addressed": "retention_plan" in final,
        "timeline_constraint_acknowledged": any(
            re.search(r"(7 month|runway|cash)", str(d), re.I)
            for d in swd.get("decisions", [])
        ),
        "no_single_agent_copied": _check_no_verbatim_copy(swd),
        
        # Phase completeness
        "all_phases_reached": swd.get("phase") == "execution",
        "swd_version_rich": swd["swd_version"] >= 8,
    }
    return checks

def _check_no_verbatim_copy(swd):
    """Penalise if final_recommendation is just copy-paste from one agent report."""
    final_str = str(swd.get("final_recommendation", "")).lower()
    for report in swd["agent_reports"].values():
        if report and len(report) > 50:
            # Check if >60% of 5-grams overlap (reward hacking guard)
            report_grams = set(_ngrams(report.lower(), 5))
            final_grams = set(_ngrams(final_str, 5))
            if report_grams and len(final_grams & report_grams) / len(report_grams) > 0.6:
                return False
    return True
```

**Why frontier models fail this without training**:
1. They collapse to one agent's view (missing prerequisite reconciliation)
2. They do not log reasoning per turn (no `reasoning_log` entries)
3. They populate `final_recommendation` without satisfying all three constraints simultaneously
4. They finish too early — `phase` never reaches "execution"

---

## PART 2 — REWARD FUNCTION

### Design principle
Every component is independently verifiable. LLM judge is one signal at low weight. No single component can be gamed without solving the actual task.

```python
def compute_reward(swd, verify_result, episode_metadata):
    # --- Component 1: Completion (0–1.0) weight 0.35 ---
    completion_checks = verify_result  # dict of bool
    completion = sum(completion_checks.values()) / len(completion_checks)

    # --- Component 2: SWD Coherence (0–1.0) weight 0.25 ---
    # Checks workspace structural integrity at this snapshot
    coherence = compute_swd_coherence(swd)
    
    # --- Component 3: Milestone Adherence (0–1.0) weight 0.20 ---
    milestones = swd["milestones"]
    completed_on_time = sum(
        1 for m in milestones 
        if m["status"] == "complete" and 
           episode_metadata["turn_completed"].get(m["id"], 999) <= m["due_by_turn"]
    )
    milestone_score = completed_on_time / max(len(milestones), 1)

    # --- Component 4: Reasoning Density (0–1.0) weight 0.10 ---
    # Did the agent log reasoning, not just outputs?
    log_entries = swd.get("reasoning_log", [])
    unique_turns = len(set(e.get("turn") for e in log_entries))
    reasoning_score = min(unique_turns / 5.0, 1.0)  # saturates at 5 unique turns

    # --- Component 5: LLM Judge (0–1.0) weight 0.10 ---
    # Only called at finalize(). Fast prompt, single yes/no per criterion.
    llm_score = call_llm_judge(swd) if episode_metadata["finalized"] else 0.0

    # --- Penalties (applied after weighted sum) ---
    penalties = 0.0
    penalties += episode_metadata.get("invalid_json_count", 0) * 0.15
    penalties += episode_metadata.get("wrong_agent_count", 0) * 0.10
    penalties += episode_metadata.get("token_budget_exceeded", False) * 0.20
    penalties += sum(
        0.08 for m in milestones if m["status"] == "missed"
    )

    raw = (
        0.35 * completion +
        0.25 * coherence +
        0.20 * milestone_score +
        0.10 * reasoning_score +
        0.10 * llm_score
    )
    
    return max(0.0, raw - penalties)


def compute_swd_coherence(swd):
    """
    Checks structural coherence of the SWD. All deterministic.
    Returns 0–1.
    """
    checks = []
    
    # Required keys present
    required = ["episode_id","scenario","phase","milestones","agent_reports",
                "decisions","conflicts_identified","conflict_resolutions",
                "reasoning_log","final_recommendation","swd_version"]
    checks.append(all(k in swd for k in required))
    
    # Phase is valid
    checks.append(swd.get("phase") in ["discovery","analysis","decision","execution"])
    
    # Every milestone has required keys
    milestone_keys = {"id","label","due_by_turn","status","owner","output"}
    checks.append(all(
        milestone_keys.issubset(m.keys()) for m in swd.get("milestones", [])
    ))
    
    # Conflict resolutions reference valid conflict IDs
    conflict_ids = {c.get("id") for c in swd.get("conflicts_identified", [])}
    checks.append(all(
        r.get("conflict_id") in conflict_ids 
        for r in swd.get("conflict_resolutions", [])
    ))
    
    # SWD version is monotonically increasing (check via episode_metadata in real impl)
    checks.append(isinstance(swd.get("swd_version"), int) and swd["swd_version"] >= 1)
    
    # Reasoning log entries have turn numbers
    checks.append(all(
        "turn" in e for e in swd.get("reasoning_log", [])
    ))
    
    return sum(checks) / len(checks)
```

### LLM Judge prompt (fast, one call per episode)

```python
LLM_JUDGE_PROMPT = """
You are evaluating a corporate decision document. Answer each question with YES or NO only.

DOCUMENT:
{swd_json}

TASK GOAL:
{task_goal}

QUESTIONS:
1. Does the final_recommendation address all three key stakeholder concerns present in the scenario?
2. Are the conflict_resolutions logically consistent with the agent_reports provided?
3. Does the reasoning_log show evidence of iterative thinking (not just a single dump)?

Respond in this exact format:
Q1: YES/NO
Q2: YES/NO  
Q3: YES/NO
"""

def call_llm_judge(swd, task_goal):
    # Use small fast model (Qwen2.5-7B-Instruct) not the training model
    response = call_model(LLM_JUDGE_PROMPT.format(
        swd_json=json.dumps(swd, indent=2)[:3000],  # truncate for speed
        task_goal=task_goal
    ))
    # Parse with regex — never trust free-form output for reward
    yes_count = len(re.findall(r"Q\d: YES", response))
    return yes_count / 3.0
```

---

## PART 3 — SFT DATA STRATEGY

### Why SFT first (cold start)

Research across QuarkMedSearch, KLong, and EigenData all confirm the same pattern:
> **SFT → RL outperforms RL alone** because without SFT, the model doesn't know the action format, SWD schema, or delegation protocol. Zero-reward rollouts are wasted compute.

Target: **~20% baseline success on E1 before starting RL**. SFT gets you there.

### What data to use (three sources, all free)

#### Source A: Synthetic Oracle Trajectories (primary, ~300 examples)

Generate using Claude Opus 4 (or GPT-4.1) as the oracle. For each task:
1. Feed the task state and SWD schema
2. Ask oracle to produce a complete multi-turn trajectory
3. Run verifier — keep only trajectories where `verify_result` passes all checks
4. Store as `(prompt, trajectory)` pairs

**Format** (multi-turn chat):
```json
{
  "messages": [
    {"role": "system", "content": "You are a Master Agent in CORP-ENV..."},
    {"role": "user", "content": "<state>{...}</state>\n<swd>{...}</swd>"},
    {"role": "assistant", "content": "<think>I need to first understand...</think>\n<action>delegate(dev_agent, 'Assess technical feasibility', 'm1')</action>"},
    {"role": "user", "content": "<action_result>dev_agent returned: {...}</action_result>\n<swd>{updated...}</swd>"},
    {"role": "assistant", "content": "<think>Dev report received. Now I need HR...</think>\n<action>update_swd({...})</action>"},
    ...
  ]
}
```

**Key**: Use `<think>...</think>` tags before every action. This teaches the model to reason before acting — critical for long-horizon tasks.

#### Source B: AgentInstruct / Hermes Tool-Calling Data (warm-up format only)

Use `NousResearch/hermes-function-calling-v1` or similar to teach the model action format syntax before environment-specific SFT. ~500 examples, 1 epoch only.

HuggingFace datasets to look at:
- `NousResearch/hermes-function-calling-v1` — multi-turn tool calling
- `Jofthomas/hermes-function-calling-thinking-V1` — has `<think>` tags already
- `DeepNLP/Agent-RL-Open-Dataset` — real agent rollouts with reward labels

#### Source C: Trajectory Splitting for Long Episodes (KLong technique)

H1 episodes will be 20+ turns. Context window becomes an issue during SFT. Solution:
- Split each long trajectory into overlapping sub-trajectories of 8–10 turns
- Each sub-trajectory includes the current SWD snapshot as context
- Train on sub-trajectories independently — the SWD provides the shared memory

```python
def split_trajectory(trajectory, window=10, overlap=3):
    """
    trajectory: list of (user_msg, assistant_msg) pairs
    Returns list of sub-trajectory dicts, each with SWD snapshot as context
    """
    splits = []
    for i in range(0, len(trajectory) - window + 1, window - overlap):
        chunk = trajectory[i:i+window]
        swd_at_start = chunk[0]["swd_snapshot"]
        splits.append({
            "context_swd": swd_at_start,
            "messages": chunk
        })
    return splits
```

### SFT Training Config

```python
# Recommended: Qwen2.5-7B-Instruct as base
# On H100 (8-12hr window), 3hr segments

sft_config = SFTConfig(
    model_name="Qwen/Qwen2.5-7B-Instruct",
    dataset_path="./sft_data/combined.jsonl",
    max_seq_length=8192,           # enough for 10-turn episodes with SWD
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-5,
    num_train_epochs=2,
    warmup_ratio=0.05,
    lora_r=64,
    lora_alpha=128,
    lora_target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
    save_steps=50,
    logging_steps=10,
    # Critical: mask tool outputs so gradients only flow through agent decisions
    dataset_kwargs={"mask_assistant_prefix": False}
)

# Estimated time on 1x H100: ~45min for 300 examples x 2 epochs
```

---

## PART 4 — RL TRAINING

### Algorithm: GRPO (preferred over PPO)

GRPO eliminates the value model — simpler infrastructure, same quality. Group 8 rollouts per prompt, compute relative advantages.

```python
grpo_config = GRPOConfig(
    model_name="./sft_checkpoint",   # start from SFT, not base
    reward_funcs=[compute_reward],
    num_generations=8,               # rollouts per prompt (GRPO group size)
    max_new_tokens=512,              # per action, not per episode
    temperature=0.7,
    learning_rate=1e-6,              # lower than SFT
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,
    kl_coef=0.02,                    # light KL penalty to base model
    # Token masking: don't backprop through tool outputs or SWD snapshots
    response_template="<action>",
)
```

### Curriculum schedule

```
Phase 1 (steps 0–150):   E1 only — 100%
Phase 2 (steps 150–400): E1 50% / M1 50%
Phase 3 (steps 400+):    E1 20% / M1 50% / H1 30%
```

Switch phases when: mean episode reward on current phase ≥ 0.5

### Token budget (not max_steps)

```python
TOKEN_BUDGETS = {
    "easy":   4096,
    "medium": 8192,
    "hard":   16384
}
# Episode ends when tokens_generated > budget
# Budget utilisation included in efficiency reward
```

### Reward hacking guards (must implement before training)

```python
REWARD_HACKING_CHECKS = [
    # 1. Finalize() without populating SWD is penalised
    lambda swd, ep: -0.3 if ep["finalized"] and swd["swd_version"] < 4 else 0,
    
    # 2. Calling same agent twice in a row without SWD update in between
    lambda swd, ep: -0.1 * ep.get("consecutive_same_agent_calls", 0),
    
    # 3. final_recommendation is verbatim copy of agent report (see _check_no_verbatim_copy)
    lambda swd, ep: -0.25 if not _check_no_verbatim_copy(swd) else 0,
    
    # 4. update_swd that decreases swd_version (tampering)
    lambda swd, ep: -0.5 if ep.get("version_decreased", False) else 0,
    
    # 5. Reasoning log is identical across turns (copy-paste reasoning)
    lambda swd, ep: -0.15 if _reasoning_log_is_duplicated(swd) else 0,
]
```

---

## PART 5 — OPENENV IMPLEMENTATION

### File structure

```
corp_env/
├── openenv.yaml              # manifest
├── server/
│   ├── __init__.py
│   ├── environment.py        # main Environment class
│   ├── tasks/
│   │   ├── e1_launch_readiness.py
│   │   ├── m1_budget_reallocation.py
│   │   └── h1_acquisition_defence.py
│   ├── agents/
│   │   ├── dev_agent.py
│   │   ├── hr_agent.py
│   │   └── finance_agent.py
│   ├── reward.py             # all reward components
│   ├── swd.py                # SWD validation + helpers
│   └── verifiers.py          # per-task verification functions
├── client/
│   ├── __init__.py
│   └── client.py             # HTTPEnvClient subclass
└── Dockerfile
```

### openenv.yaml

```yaml
name: corp-env
version: 0.1.0
description: >
  Multi-agent corporate decision environment for training long-horizon planning
  via shared workspace document governance. Targets the planning capability gap
  exposed by EnterpriseOps-Gym (ServiceNow, 2026).
author: your-team
themes: [multi-agent, long-horizon-planning]
tasks: [e1_launch_readiness, m1_budget_reallocation, h1_acquisition_defence]
reward_range: [-1.0, 1.0]
observation_space: json
action_space: structured_text
```

### Core environment class skeleton

```python
from openenv import Environment
from dataclasses import dataclass
import json, re, uuid

@dataclass
class CorpAction:
    action_type: str          # "delegate" | "update_swd" | "query_swd" | "finalize"
    agent_id: str | None
    payload: str              # task_description OR json_patch OR jsonpath OR recommendation

@dataclass  
class CorpObservation:
    task_description: str
    role: str
    available_agents: list[str]
    swd: dict                 # current workspace document
    agent_last_output: dict | None
    tokens_used: int
    token_budget: int
    turn: int

class CorpEnvironment(Environment):
    
    def reset(self, task_id=None):
        task_id = task_id or self._sample_task()
        task = TASKS[task_id]
        self.swd = task.initial_swd()
        self.task = task
        self.turn = 0
        self.tokens_used = 0
        self.episode_metadata = {
            "task_id": task_id,
            "invalid_json_count": 0,
            "wrong_agent_count": 0,
            "consecutive_same_agent_calls": 0,
            "last_agent": None,
            "finalized": False,
            "version_decreased": False,
            "turn_completed": {}
        }
        return CorpObservation(
            task_description=task.description,
            role=task.role,
            available_agents=task.available_agents,
            swd=self.swd,
            agent_last_output=None,
            tokens_used=0,
            token_budget=task.token_budget,
            turn=0
        )

    def step(self, action: CorpAction):
        self.turn += 1
        step_reward = 0.0
        done = False
        agent_output = None

        # --- Parse and validate action ---
        if action.action_type == "delegate":
            if action.agent_id not in self.task.available_agents:
                step_reward -= 0.10
                self.episode_metadata["wrong_agent_count"] += 1
            else:
                # Check consecutive same agent
                if action.agent_id == self.episode_metadata["last_agent"]:
                    self.episode_metadata["consecutive_same_agent_calls"] += 1
                else:
                    self.episode_metadata["consecutive_same_agent_calls"] = 0
                self.episode_metadata["last_agent"] = action.agent_id
                agent_output = self._call_worker(action.agent_id, action.payload)
                # Append to SWD agent_reports
                self.swd["agent_reports"][action.agent_id] = agent_output

        elif action.action_type == "update_swd":
            try:
                patch = json.loads(action.payload)
                old_version = self.swd["swd_version"]
                self._apply_patch(patch)
                if self.swd["swd_version"] < old_version:
                    self.episode_metadata["version_decreased"] = True
                    step_reward -= 0.5
                # Validate SWD coherence after patch
                coherence = compute_swd_coherence(self.swd)
                step_reward += 0.05 * coherence  # small per-step signal
            except (json.JSONDecodeError, KeyError) as e:
                step_reward -= 0.15
                self.episode_metadata["invalid_json_count"] += 1

        elif action.action_type == "query_swd":
            # Free action — no reward signal, just return data
            pass

        elif action.action_type == "finalize":
            self.swd["final_recommendation"] = action.payload
            self.episode_metadata["finalized"] = True
            verify_result = self.task.verifier(self.swd)
            terminal_reward = compute_reward(
                self.swd, verify_result, self.episode_metadata
            )
            step_reward += terminal_reward
            done = True

        # Check milestone completion
        self._update_milestone_status()

        # Check token budget
        if self.tokens_used > self.task.token_budget:
            step_reward -= 0.20
            done = True

        obs = CorpObservation(
            task_description=self.task.description,
            role=self.task.role,
            available_agents=self.task.available_agents,
            swd=self.swd,
            agent_last_output=agent_output,
            tokens_used=self.tokens_used,
            token_budget=self.task.token_budget,
            turn=self.turn
        )

        return obs, step_reward, done, {}
    
    def _call_worker(self, agent_id, task_description):
        """Call frozen worker agent with role-specific system prompt."""
        system_prompt = WORKER_PROMPTS[agent_id]
        # Inject conflict intel for H1
        if self.task.task_id == "h1" and agent_id in self.task.intel_injections:
            task_description += f"\n\nCONFIDENTIAL CONTEXT: {self.task.intel_injections[agent_id]}"
        return call_model(system_prompt, task_description, max_tokens=400)
```

---

## PART 6 — TRAINING INFRASTRUCTURE

### H100 session plan (3hr segments)

**Session 1 (3hr) — Environment validation**
- Deploy env to HF Space
- Run 50 episodes with GPT-4.1-mini as agent (baseline)
- Record: success rates, common failure modes, average reward
- Fix bugs before touching training

**Session 2 (3hr) — SFT**
- Generate 200–300 oracle trajectories with Claude Opus / GPT-4.1
- Filter to passing-verifier examples only (~60–70% pass rate expected)
- Run SFT on Qwen2.5-7B-Instruct
- Checkpoint every 50 steps
- Validate: run 20 episodes post-SFT, ensure E1 success > 20%

**Session 3 (3hr) — RL Phase 1 (E1 + M1)**
- Start from SFT checkpoint
- GRPO, curriculum Phase 1→2
- Monitor: per-component reward columns, not just total
- Save best checkpoint by E1+M1 success rate

**Session 4 (3hr, if available) — RL Phase 2 (add H1)**
- Continue from best Phase 1→2 checkpoint  
- Curriculum Phase 2→3
- Generate before/after trajectory examples for H1
- Export final model

### Monitoring (what to track)

```python
# Log these per training step
metrics = {
    "reward/total": ...,
    "reward/completion": ...,
    "reward/swd_coherence": ...,
    "reward/milestone_adherence": ...,
    "reward/reasoning_density": ...,
    "reward/llm_judge": ...,
    "penalty/invalid_json": ...,
    "penalty/wrong_agent": ...,
    "success_rate/e1": ...,
    "success_rate/m1": ...,
    "success_rate/h1": ...,
    "swd/avg_version_at_finalize": ...,    # tracks SWD richness
    "swd/avg_conflict_resolutions": ...,   # tracks reasoning depth
}
```

---

## PART 7 — DEMO AND STORY

### The three-slide story (for the pitch)

**Slide 1 — The problem**
> EnterpriseOps-Gym (ServiceNow, Mar 2026): best frontier model gets 37.4% on enterprise tasks. Failure mode: planning, not tool use. No RL training env exists to fix this.

**Slide 2 — The environment**  
> Show the SWD growing over a single H1 episode. Turn 1: empty. Turn 8: three agent reports, two conflicts logged. Turn 18: conflict resolved, phased plan, reasoning log with 6 entries. The document tells the story.

**Slide 3 — The result**
> Baseline (no training): 35% on E1, ~5% on H1. After SFT + RL: 70%+ on E1, 25%+ on H1. The reward curve goes up. The SWD gets richer. The agent learned to maintain shared context.

### Before/after trajectory for H1

Show side by side:
- **Baseline**: calls one agent, copies their report, calls finalize. SWD version 2. Score: 0.12.
- **Trained**: calls all three agents, logs conflicts, produces resolution with type field, writes phased recommendation with all three constraints addressed. SWD version 11. Score: 0.71.

---

## PART 8 — COMMON FAILURE MODES TO WATCH

| Failure | Symptom | Fix |
|---|---|---|
| Zero reward on H1 from the start | Agent can't format actions | Run SFT first; don't start RL on H1 |
| Reward hacks finalize() early | SWD version = 1 at terminal | Add version check penalty |
| Reasoning log identical every turn | Low reasoning_density reward | Add n-gram diversity check to log |
| Agent copies one report verbatim | `_check_no_verbatim_copy` fires | Increase penalty; add to SFT negative examples |
| SWD version goes backwards | `version_decreased` flag | Hard penalty -0.5; fix in env step() |
| Token budget gaming | Agent writes tiny SWD updates | Minimum content-length check on patches |
| LLM judge gets gamed | High judge score, low completion | Keep judge weight at 0.10; trust deterministic checks |

---

## QUICK REFERENCE: COSTS AND COMPUTE

| Item | Estimate |
|---|---|
| Oracle trajectory generation (300 eps × Claude Opus) | ~$8–12 of $60 budget |
| SFT on H100 (2hr) | 1 session |
| RL Phase 1 (E1+M1, 3hr) | 1 session |
| RL Phase 2 (add H1, 3hr) | 1 session |
| Baseline eval + debug session | 1 session |
| **Total H100 sessions needed** | **4 × 3hr = 12hr** (fits exactly) |
| HF Space hosting | Free tier |
| Remaining HF credits for inference | ~$48–52 |

---

## FOR CLAUDE OPUS — EXACT TASK LIST TO GENERATE

When you feed this to Claude Opus for task planning, ask it to produce:

1. `task_e1.py` — E1 task class with `initial_swd()`, `verifier()`, worker prompts
2. `task_m1.py` — M1 task class with conflict injection
3. `task_h1.py` — H1 task class with three conflicting intel strings
4. `environment.py` — Full CorpEnvironment implementing OpenEnv base class
5. `reward.py` — All five reward components + penalty system
6. `swd.py` — SWD validator, patch applier, version manager
7. `generate_sft_data.py` — Oracle trajectory generator + verifier filter
8. `train_sft.py` — Unsloth + TRL SFTTrainer config
9. `train_rl.py` — GRPO config + curriculum controller
10. `eval.py` — Baseline + post-training evaluation with per-task metrics
11. `plot_results.py` — Reward curves + success rate bars (labelled axes, PNG output)
12. `client.py` — OpenEnv HTTPEnvClient subclass
13. `openenv.yaml` — Valid manifest
14. `Dockerfile` — For HF Space deployment
15. `README.md` — Problem, environment, results, links

---

*CORP-ENV Implementation Guide v1.0 — OpenEnv Hackathon India 2026*
