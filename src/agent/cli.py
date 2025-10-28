"""CLI for the supervised quickstart.

Usage: pass your query as a single argument. No built-in demos.

Reads .env from project root and validates required environment variables.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agent.graph import build_system


def _load_env() -> None:
    """Load environment variables from typical locations.

    Priority:
    1) Project root .env (two levels up from this file in src layout)
    2) Current working directory .env
    3) Project root .env.example (fallback for defaults)
    """
    # Project root in src layout: repo/ (one level above this file's parent)
    # __file__ = repo/src/cli.py -> parents[1] == repo
    root = Path(__file__).resolve().parents[1]
    loaded = False

    # 1) repo/.env
    env_path = root / ".env"
    if env_path.exists():
        load_dotenv(str(env_path))
        loaded = True

    # 2) CWD/.env (useful when installed in editable mode or running from a different dir)
    cwd_env = Path.cwd() / ".env"
    if cwd_env.exists():
        load_dotenv(str(cwd_env))
        loaded = True

    # 3) repo/.env.example as last-resort defaults
    if not loaded:
        example_path = root / ".env.example"
        if example_path.exists():
            load_dotenv(str(example_path))


def _check_env() -> bool:
    missing: List[str] = []
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not openai_key or openai_key.lower() in {"your-openai-api-key-here", "changeme", "paste-here"}:
        missing.append("OPENAI_API_KEY")
    if not os.getenv("LANGSMITH_API_KEY"):
        print("Warning: LANGSMITH_API_KEY is not set. Tracing will be limited.")
    if missing:
        print("Error: missing required environment variables: " + ", ".join(missing))
        print("Hint: copy .env.example to .env and fill your keys.")
        return False
    return True


def entrypoint(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv
    _load_env()
    if not _check_env():
        return 1

    graph = build_system()

    if len(argv) <= 1:
        print(
            "Usage:\n"
            "  PYTHONPATH=src python -m cli \"<your query>\"\n"
            "or (if installed):\n"
            "  lgsq \"<your query>\"\n\n"
            "Examples:\n"
            "  PYTHONPATH=src python -m cli \"Analyze the text: 'OpenAI and LangGraph enable agents.' and compute stats for: 2, 4, 6\"\n"
            "  lgsq \"Compute stats for: 10, 20, 30\"\n"
        )
        return 2

    query = " ".join(argv[1:])
    print(f"\n=== Query ===\n{query}")
    result = graph.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"configurable": {"thread_id": "cli"}},
    )
    print(f"\n=== Response ===\n{result['messages'][-1].content}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(entrypoint())
