"""Task definition base class for CORP-ENV."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Literal, Optional

from server.agents.personas import AgentSlot


Difficulty = Literal["easy", "medium", "hard"]
MasterTier = Literal["fresher", "senior", "executive"]


class CorpTask(ABC):
    task_id: str
    description: str
    role: str
    difficulty: Difficulty
    master_tier: MasterTier
    agent_slots: List[AgentSlot]
    token_budget: int
    intel_injections: Dict[str, str]

    def __init__(self) -> None:
        self.intel_injections = {}

    @property
    def available_agents(self) -> List[str]:
        """Derived slot-id list shown to the master agent."""
        return [s.id for s in self.agent_slots]

    def get_slot(self, slot_id: str) -> Optional[AgentSlot]:
        for s in self.agent_slots:
            if s.id == slot_id:
                return s
        return None

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
