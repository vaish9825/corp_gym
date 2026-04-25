"""Shared Workspace Document (SWD) schema, JSON Patch apply, and validation helpers."""

from __future__ import annotations

import copy
import uuid
from typing import Any, Dict, List, Optional, Tuple

import jsonpatch

REQUIRED_TOP_LEVEL = (
    "episode_id",
    "scenario",
    "phase",
    "milestones",
    "agent_reports",
    "decisions",
    "conflicts_identified",
    "conflict_resolutions",
    "reasoning_log",
    "final_recommendation",
    "swd_version",
)

VALID_PHASES = frozenset({"discovery", "analysis", "decision", "execution"})

MILESTONE_KEYS = frozenset({"id", "label", "due_by_turn", "status", "owner", "output"})


def new_episode_id() -> str:
    return str(uuid.uuid4())


def deep_clone_swd(swd: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(swd)


def ensure_agent_report_keys(swd: Dict[str, Any]) -> None:
    ar = swd.setdefault("agent_reports", {})
    for k in ("qa", "dev", "hr", "finance"):
        ar.setdefault(k, None)


def validate_milestone_shapes(swd: Dict[str, Any]) -> bool:
    for m in swd.get("milestones", []) or []:
        if not isinstance(m, dict) or not MILESTONE_KEYS.issubset(m.keys()):
            return False
    return True


def validate_swd_structure(swd: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    for k in REQUIRED_TOP_LEVEL:
        if k not in swd:
            return False, f"missing key: {k}"
    if swd.get("phase") not in VALID_PHASES:
        return False, "invalid phase"
    if not isinstance(swd.get("swd_version"), int):
        return False, "swd_version must be int"
    if not validate_milestone_shapes(swd):
        return False, "invalid milestone shape"
    ensure_agent_report_keys(swd)
    return True, None


def apply_json_patch(swd: Dict[str, Any], patch_ops: List[Any]) -> None:
    """Apply RFC 6902 JSON Patch in-place; increments swd_version on success."""
    patch = jsonpatch.JsonPatch(patch_ops)
    patch.apply(swd, in_place=True)
    swd["swd_version"] = int(swd.get("swd_version", 0)) + 1


def try_apply_json_patch(
    swd: Dict[str, Any], patch_ops: List[Any]
) -> Tuple[Dict[str, Any], Optional[str]]:
    """
    Apply patch to a deep copy; on success returns mutated document and None error.
    On failure returns original snapshot and error message (caller restores if needed).
    """
    snapshot = deep_clone_swd(swd)
    try:
        apply_json_patch(snapshot, patch_ops)
        ok, err = validate_swd_structure(snapshot)
        if not ok:
            return swd, err or "structure invalid after patch"
        if not resolutions_reference_valid_conflicts(snapshot):
            return swd, "conflict_resolutions reference unknown conflict id"
        return snapshot, None
    except jsonpatch.JsonPatchException as e:
        return swd, str(e)


def conflict_ids_from_swd(swd: Dict[str, Any]) -> set:
    out = set()
    for c in swd.get("conflicts_identified", []) or []:
        if isinstance(c, dict) and c.get("id") is not None:
            out.add(c["id"])
    return out


def resolutions_reference_valid_conflicts(swd: Dict[str, Any]) -> bool:
    ids = conflict_ids_from_swd(swd)
    for r in swd.get("conflict_resolutions", []) or []:
        if not isinstance(r, dict):
            return False
        cid = r.get("conflict_id")
        if cid is not None and cid not in ids:
            return False
    return True
