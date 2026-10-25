from __future__ import annotations

from .models import Task


class TaskStore:
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def add_many(self, tasks: list[Task]) -> None:
        for task in tasks:
            self._tasks[task.id] = task

    def update(self, task: Task) -> None:
        self._tasks[task.id] = task

    def all(self) -> list[Task]:
        return list(self._tasks.values())
