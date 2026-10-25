from __future__ import annotations

import logging

from .config import Settings, load_settings
from .executor_agent import ExecutorAgent
from .models import AgentMessage, Goal, Plan, ReviewResult, WorkflowRun
from .planner_agent import PlannerAgent
from .reviewer_agent import ReviewerAgent
from .task_store import TaskStore

LOGGER = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or load_settings()
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent(self.settings)
        self.reviewer = ReviewerAgent()
        self.store = TaskStore()

    def run(self, goal_text: str) -> WorkflowRun:
        goal = Goal(text=goal_text)
        handoffs: list[AgentMessage] = []
        notes: list[str] = []

        handoffs.append(self._handoff("orchestrator", "planner", "Create a plan."))
        plan = self.planner.create_plan(goal)
        if not plan.tasks:
            notes.append("Planner returned no tasks.")

        self.store.add_many(plan.tasks)
        self._execute_plan(plan, handoffs)

        handoffs.append(self._handoff("executor", "reviewer", "Review completed tasks."))
        review = self.reviewer.review(goal, self.store.all(), self.settings.review_threshold)

        revision_count = 0
        if not review.accepted and plan.tasks:
            revision_count = 1
            notes.append("Review score was below threshold; one revision cycle was triggered.")
            handoffs.append(self._handoff("reviewer", "planner", "Revise the plan once."))
            plan = self.planner.create_plan(goal, revision=1)
            self.store = TaskStore()
            self.store.add_many(plan.tasks)
            self._execute_plan(plan, handoffs)
            handoffs.append(self._handoff("executor", "reviewer", "Review revised tasks."))
            review = self.reviewer.review(goal, self.store.all(), self.settings.review_threshold)

        LOGGER.info("workflow_complete accepted=%s score=%s", review.accepted, review.score)
        return WorkflowRun(
            goal=goal,
            plan=Plan(goal=goal, tasks=self.store.all(), revision=plan.revision),
            review=review,
            handoffs=handoffs,
            revision_count=revision_count,
            notes=notes,
        )

    def _execute_plan(self, plan: Plan, handoffs: list[AgentMessage]) -> None:
        handoffs.append(self._handoff("planner", "executor", "Execute planned tasks."))
        for task in plan.tasks:
            executed = self.executor.execute(task)
            self.store.update(executed)

    def _handoff(self, sender: str, receiver: str, content: str) -> AgentMessage:
        LOGGER.info("agent_handoff sender=%s receiver=%s", sender, receiver)
        return AgentMessage(sender=sender, receiver=receiver, content=content)
