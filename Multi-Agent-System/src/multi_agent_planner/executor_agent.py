from __future__ import annotations

import json
import logging
import urllib.request

from .config import Settings
from .models import Task, TaskStatus

LOGGER = logging.getLogger(__name__)


class ExecutorAgent:
    name = "executor"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def execute(self, task: Task) -> Task:
        LOGGER.info("agent_step agent=executor action=execute task_id=%s", task.id)
        task.status = TaskStatus.IN_PROGRESS

        if "fail execution" in task.description.lower():
            task.status = TaskStatus.FAILED
            task.error = "Mock failure triggered by task description."
            return task

        if self.settings.mode == "llm" and self.settings.openai_api_key:
            task.output = self._execute_with_llm(task)
        else:
            task.output = self._execute_in_mock_mode(task)

        task.status = TaskStatus.COMPLETED
        return task

    def _execute_in_mock_mode(self, task: Task) -> str:
        return (
            f"{task.title}: {task.expected_output} "
            f"Mock result based on '{task.description}'."
        )

    def _execute_with_llm(self, task: Task) -> str:
        payload = {
            "model": self.settings.openai_model,
            "messages": [
                {
                    "role": "system",
                    "content": "Complete the task in a concise, beginner-friendly way.",
                },
                {
                    "role": "user",
                    "content": f"{task.description}\nExpected output: {task.expected_output}",
                },
            ],
        }
        request = urllib.request.Request(
            f"{self.settings.openai_base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]
