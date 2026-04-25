"""Resolve OpenAI-compatible API key and base URL per role (master, worker, judge)."""

from __future__ import annotations

import os
from typing import Any, Dict, Optional


def _first(*values: Optional[str]) -> Optional[str]:
    for v in values:
        if v is not None and str(v).strip() != "":
            return str(v).strip()
    return None


def openai_client_kwargs_master() -> Dict[str, Any]:
    """Credentials for the master model (inference loop)."""
    api_key = _first(
        os.getenv("CORP_MASTER_API_KEY"),
        os.getenv("HF_TOKEN"),
        os.getenv("OPENAI_API_KEY"),
        os.getenv("API_KEY"),
    )
    base_url = _first(
        os.getenv("CORP_MASTER_BASE_URL"),
        os.getenv("API_BASE_URL"),
        os.getenv("OPENAI_BASE_URL"),
    )
    return _kwargs(api_key, base_url)


def openai_client_kwargs_worker(canonical_agent_id: str) -> Dict[str, Any]:
    """
    Credentials for a frozen worker (dev_agent, hr_agent, finance_agent).

    Per-agent overrides use uppercase id with hyphens as underscores, e.g.:
    CORP_WORKER_DEV_AGENT_API_KEY, CORP_WORKER_DEV_AGENT_BASE_URL
    """
    suffix = canonical_agent_id.upper().replace("-", "_")
    api_key = _first(
        os.getenv(f"CORP_WORKER_{suffix}_API_KEY"),
        os.getenv("CORP_WORKER_DEFAULT_API_KEY"),
        os.getenv("OPENAI_API_KEY"),
        os.getenv("HF_TOKEN"),
        os.getenv("API_KEY"),
    )
    base_url = _first(
        os.getenv(f"CORP_WORKER_{suffix}_BASE_URL"),
        os.getenv("CORP_WORKER_DEFAULT_BASE_URL"),
        os.getenv("API_BASE_URL"),
        os.getenv("OPENAI_BASE_URL"),
    )
    return _kwargs(api_key, base_url)


def openai_client_kwargs_judge() -> Dict[str, Any]:
    """Credentials for the optional LLM judge (reward)."""
    api_key = _first(
        os.getenv("CORP_JUDGE_API_KEY"),
        os.getenv("OPENAI_API_KEY"),
        os.getenv("HF_TOKEN"),
        os.getenv("API_KEY"),
    )
    base_url = _first(
        os.getenv("CORP_JUDGE_BASE_URL"),
        os.getenv("API_BASE_URL"),
        os.getenv("OPENAI_BASE_URL"),
    )
    return _kwargs(api_key, base_url)


def _kwargs(api_key: Optional[str], base_url: Optional[str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if api_key:
        out["api_key"] = api_key
    if base_url:
        out["base_url"] = base_url
    return out


def worker_model_for(canonical_agent_id: str) -> str:
    suffix = canonical_agent_id.upper().replace("-", "_")
    return _first(
        os.getenv(f"CORP_WORKER_{suffix}_MODEL"),
        os.getenv("CORP_WORKER_DEFAULT_MODEL"),
        os.getenv("CORP_WORKER_MODEL"),
        os.getenv("MODEL_NAME"),
    ) or "Qwen/Qwen2.5-7B-Instruct"
