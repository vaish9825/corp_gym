"""Task definition base class for CORP-ENV."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class CorpTask(ABC):
    task_id: str
    description: str
    role: str
    available_agents: List[str]
    token_budget: int
    intel_injections: Dict[str, str]

    def __init__(self) -> None:
        self.intel_injections = {}

    @abstractmethod
    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        raise NotImplementedError

    @abstractmethod
    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        """Return True when milestone objective is satisfied."""
        raise NotImplementedError
