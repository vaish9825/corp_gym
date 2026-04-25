"""Cross-episode memory store for master and worker sub-agents.

Layout on disk (under ``CORP_MEMORY_DIR``, default ``.corp_memory/``)::

    workers/<task_id>/<slot_id>/turns.jsonl      # every delegate call
    workers/<task_id>/<slot_id>/episodes.jsonl   # one line per finalized episode
    master/<task_id>.jsonl                        # one line per finalized episode

All writes are JSONL append-only. Memory is disabled entirely when the
environment variable ``CORP_MEMORY_DISABLED`` is set to a truthy value, or when
``CORP_MEMORY_DIR`` resolves to an empty / unwritable path.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


def _is_disabled() -> bool:
    return os.getenv("CORP_MEMORY_DISABLED", "").lower() in ("1", "true", "yes")


def memory_root() -> Optional[Path]:
    if _is_disabled():
        return None
    raw = os.getenv("CORP_MEMORY_DIR", ".corp_memory").strip()
    if not raw:
        return None
    return Path(raw)


_SAFE_RE = re.compile(r"[^A-Za-z0-9_.-]+")


def _safe(s: str) -> str:
    return _SAFE_RE.sub("_", s)[:80] or "unknown"


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _append_jsonl(path: Path, record: Dict[str, Any]) -> None:
    try:
        _ensure_parent(path)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        # Memory is best-effort; never break the environment loop on IO errors.
        return


def _read_jsonl_tail(path: Path, n: int) -> List[Dict[str, Any]]:
    if not path.exists() or n <= 0:
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    out: List[Dict[str, Any]] = []
    for line in lines[-n:]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _worker_dir(task_id: str, slot_id: str) -> Optional[Path]:
    root = memory_root()
    if root is None:
        return None
    return root / "workers" / _safe(task_id) / _safe(slot_id)


def _master_path(task_id: str) -> Optional[Path]:
    root = memory_root()
    if root is None:
        return None
    return root / "master" / f"{_safe(task_id)}.jsonl"


def append_worker_turn(
    *,
    task_id: str,
    slot_id: str,
    episode_id: str,
    turn: int,
    user_prompt: str,
    response: str,
) -> None:
    d = _worker_dir(task_id, slot_id)
    if d is None:
        return
    _append_jsonl(
        d / "turns.jsonl",
        {
            "ts": time.time(),
            "episode_id": episode_id,
            "turn": turn,
            "user_prompt": user_prompt,
            "response": response,
        },
    )


def append_worker_episode(
    *,
    task_id: str,
    slot_id: str,
    episode_id: str,
    summary: str,
    verifier_pass_rate: float,
    score: float,
) -> None:
    d = _worker_dir(task_id, slot_id)
    if d is None:
        return
    _append_jsonl(
        d / "episodes.jsonl",
        {
            "ts": time.time(),
            "episode_id": episode_id,
            "summary": summary,
            "verifier_pass_rate": round(float(verifier_pass_rate), 3),
            "score": round(float(score), 3),
        },
    )


def append_master_episode(
    *,
    task_id: str,
    episode_id: str,
    role: str,
    master_tier: str,
    final_recommendation: Any,
    score: float,
    milestone_counts: Dict[str, int],
    notes: Optional[str] = None,
) -> None:
    p = _master_path(task_id)
    if p is None:
        return
    _append_jsonl(
        p,
        {
            "ts": time.time(),
            "episode_id": episode_id,
            "role": role,
            "master_tier": master_tier,
            "final_recommendation": final_recommendation,
            "score": round(float(score), 3),
            "milestone_counts": milestone_counts,
            "notes": notes or "",
        },
    )


def load_recent_worker_memory(
    task_id: str,
    slot_id: str,
    *,
    n_episodes: int = 3,
) -> List[Dict[str, Any]]:
    """Return the last ``n_episodes`` episode summaries for this worker slot."""
    d = _worker_dir(task_id, slot_id)
    if d is None:
        return []
    return _read_jsonl_tail(d / "episodes.jsonl", n_episodes)


def load_episode_turns(
    task_id: str,
    slot_id: str,
    episode_id: str,
) -> List[Dict[str, Any]]:
    """Return this episode's prior worker turns (for replay as chat history)."""
    d = _worker_dir(task_id, slot_id)
    if d is None:
        return []
    rows = _read_jsonl_tail(d / "turns.jsonl", 200)
    return [r for r in rows if r.get("episode_id") == episode_id]


def format_past_experience_block(
    episodes: List[Dict[str, Any]], *, max_chars: int = 800
) -> str:
    if not episodes:
        return ""
    lines = ["Prior experience (most recent last):"]
    for ep in episodes:
        summary = str(ep.get("summary", "")).strip()
        pr = ep.get("verifier_pass_rate")
        piece = f"- episode {str(ep.get('episode_id', ''))[:8]}"
        if pr is not None:
            piece += f" pass_rate={pr}"
        if summary:
            piece += f": {summary}"
        lines.append(piece)
    block = "\n".join(lines)
    if len(block) > max_chars:
        block = block[: max_chars - 3] + "..."
    return block


def load_recent_master_episodes(
    task_id: str, *, n_episodes: int = 3
) -> List[Dict[str, Any]]:
    p = _master_path(task_id)
    if p is None:
        return []
    return _read_jsonl_tail(p, n_episodes)
