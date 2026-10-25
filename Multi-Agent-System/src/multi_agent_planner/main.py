from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .demo_tasks import DEFAULT_GOAL
from .logging_config import configure_logging
from .orchestrator import Orchestrator


def load_goal_from_file(path: Path) -> str:
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    goal = data.get("goal")
    if not isinstance(goal, str) or not goal.strip():
        raise ValueError("Goal file must contain a non-empty 'goal' string.")
    return goal


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a small multi-agent planning workflow.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="Run the workflow for a goal.")
    run.add_argument("--goal", help="Goal text to plan and execute.")
    run.add_argument("--goal-file", type=Path, help="Path to a JSON file containing a goal.")

    subparsers.add_parser("demo", help="Run the default demo goal.")
    return parser


def main() -> None:
    configure_logging()
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "demo":
        goal = DEFAULT_GOAL
    elif args.goal_file:
        goal = load_goal_from_file(args.goal_file)
    elif args.goal:
        goal = args.goal
    else:
        parser.error("Provide --goal or --goal-file.")

    run = Orchestrator().run(goal)
    print(json.dumps(run.to_dict(), indent=2))


if __name__ == "__main__":
    main()
