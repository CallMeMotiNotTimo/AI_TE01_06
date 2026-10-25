from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4


class TaskStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(slots=True)
class Goal:
    text: str


@dataclass(slots=True)
class Task:
    title: str
    description: str
    priority: int
    expected_output: str
    status: TaskStatus = TaskStatus.PENDING
    output: str | None = None
    error: str | None = None
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass(slots=True)
class Plan:
    goal: Goal
    tasks: list[Task]
    revision: int = 0


@dataclass(slots=True)
class AgentMessage:
    sender: str
    receiver: str
    content: str


@dataclass(slots=True)
class ReviewResult:
    score: int
    accepted: bool
    missing_pieces: list[str]
    suggestions: list[str]
    summary: str


@dataclass(slots=True)
class WorkflowRun:
    goal: Goal
    plan: Plan
    review: ReviewResult
    handoffs: list[AgentMessage]
    revision_count: int
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        for task in data["plan"]["tasks"]:
            task["status"] = str(task["status"])
        return data
