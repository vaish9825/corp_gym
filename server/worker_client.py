"""Call frozen worker LLMs (or deterministic stubs for CI / offline)."""

from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

from server.agents.prompts import WORKER_PROMPTS
from server.llm_env import openai_client_kwargs_worker, worker_model_for

STUB_OUTPUTS = {
    "dev_agent": (
        "Dev readiness: feature branch merged, canary healthy, load tests within SLO. "
        "Residual risk: third-party API quota — mitigation: cache + backoff."
    ),
    "hr_agent": (
        "HR sign-off: on-call roster staffed for launch window; contingent workers briefed. "
        "Policy check: overtime pre-approved for T-48h window only."
    ),
    "finance_agent": (
        "Finance: launch opex within Q envelope; contingency fund intact. "
        "ROI breakeven projected at 10 weeks post-launch under base case."
    ),
}


def call_model_stub(canonical_id: str, task_description: str) -> str:
    base = STUB_OUTPUTS.get(
        canonical_id,
        f"{canonical_id} acknowledges: {task_description[:200]}",
    )
    if task_description:
        return f"{base}\n\n(Task focus: {task_description[:400]})"
    return base


def call_worker_model(
    canonical_agent_id: str,
    task_description: str,
    *,
    max_tokens: int = 400,
) -> str:
    if os.getenv("CORP_STUB_WORKERS", "").lower() in ("1", "true", "yes"):
        return call_model_stub(canonical_agent_id, task_description)

    kwargs = openai_client_kwargs_worker(canonical_agent_id)
    if not kwargs.get("api_key"):
        return call_model_stub(canonical_agent_id, task_description)

    model = worker_model_for(canonical_agent_id)
    system = WORKER_PROMPTS.get(
        canonical_agent_id,
        "You are a concise corporate advisor. Plain prose only.",
    )
    client = OpenAI(**kwargs)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": task_description},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )
    return (resp.choices[0].message.content or "").strip()
