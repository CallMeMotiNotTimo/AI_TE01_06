from __future__ import annotations

import logging

from .models import Goal, Plan, Task

LOGGER = logging.getLogger(__name__)


class PlannerAgent:
    name = "planner"

    def create_plan(self, goal: Goal, revision: int = 0) -> Plan:
        LOGGER.info("agent_step agent=planner action=create_plan revision=%s", revision)

        if "empty plan" in goal.text.lower():
            return Plan(goal=goal, tasks=[], revision=revision)

        focus = goal.text.strip().rstrip(".")
        revision_note = " revised" if revision else ""
        tasks = [
            Task(
                title=f"Map the goal{revision_note}",
                description=f"Clarify the outcome and success criteria for: {focus}.",
                priority=1,
                expected_output="A short description of the target outcome.",
            ),
            Task(
                title="Break the work into milestones",
                description=f"Split the goal into practical learning or delivery milestones for: {focus}.",
                priority=2,
                expected_output="A sequenced list of milestones.",
            ),
            Task(
                title="Create practice checkpoints",
                description=f"Add hands-on checkpoints that prove progress on: {focus}.",
                priority=3,
                expected_output="Practice tasks or checkpoints.",
            ),
            Task(
                title="Package the final plan",
                description=f"Turn the milestones and checkpoints into a concise final plan for: {focus}.",
                priority=4,
                expected_output="A final beginner-friendly plan.",
            ),
        ]
        return Plan(goal=goal, tasks=tasks, revision=revision)
