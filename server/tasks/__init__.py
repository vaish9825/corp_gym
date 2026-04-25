"""Registered CORP-ENV tasks."""

from __future__ import annotations

from typing import Dict

from server.tasks.base import CorpTask
from server.tasks.e1_launch_readiness import E1LaunchReadinessTask
from server.tasks.h1_acquisition_defence import H1AcquisitionDefenceTask
from server.tasks.m1_budget_reallocation import M1BudgetReallocationTask

TASKS: Dict[str, CorpTask] = {
    "e1_launch_readiness": E1LaunchReadinessTask(),
    "m1_budget_reallocation": M1BudgetReallocationTask(),
    "h1_acquisition_defence": H1AcquisitionDefenceTask(),
}

__all__ = ["TASKS", "CorpTask"]
