from __future__ import annotations

import logging

from .models import Goal, ReviewResult, Task, TaskStatus

LOGGER = logging.getLogger(__name__)


class ReviewerAgent:
    name = "reviewer"

    def review(self, goal: Goal, tasks: list[Task], threshold: int) -> ReviewResult:
        LOGGER.info("agent_step agent=reviewer action=review task_count=%s", len(tasks))

        missing_pieces: list[str] = []
        suggestions = [
            "Turn the completed tasks into a calendar with daily checkpoints.",
            "Add one hands-on exercise for each major concept.",
        ]

        if not tasks:
            missing_pieces.append("The plan did not include any tasks.")

        failed_tasks = [task for task in tasks if task.status == TaskStatus.FAILED]
        if failed_tasks:
            missing_pieces.append(f"{len(failed_tasks)} task failed during execution.")

        completed_count = len([task for task in tasks if task.status == TaskStatus.COMPLETED])
        score = 5
        if not tasks:
            score = 1
        elif failed_tasks:
            score = 3
        elif completed_count < len(tasks):
            score = 3

        if "low score" in goal.text.lower():
            score = min(score, 2)
            missing_pieces.append("The low-score scenario was requested by the goal.")

        accepted = score >= threshold
        summary = (
            "The workflow produced a usable result."
            if accepted
            else "The workflow needs revision before it should be accepted."
        )

        return ReviewResult(
            score=score,
            accepted=accepted,
            missing_pieces=missing_pieces,
            suggestions=suggestions,
            summary=summary,
        )
