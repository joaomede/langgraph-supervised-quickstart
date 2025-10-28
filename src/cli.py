"""Interactive CLI for the supervised multi-agent system.

Two modes:
  - Interactive chat mode (default): conversational interface with context memory  
  - Single query mode (--query): one-shot inference

Usage:
    python -m cli                    # interactive chat
    python -m cli --query "..."      # single query
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.status import Status
from rich.text import Text
from rich.theme import Theme

from agent import build_system

# Custom theme for the CLI
CUSTOM_THEME = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "prompt": "bold blue",
    "assistant": "green",
    "user": "cyan",
    "header": "bold magenta",
})

console = Console(theme=CUSTOM_THEME)

# ASCII banner for visual appeal (optional)
ASCII_BANNER = """
   ╔═══════════════════════════════════════════════════════╗
   ║   🤖  Multi-Agent Supervisor System                   ║
   ║   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ║
   ║   Powered by LangGraph v1                             ║
   ║   Text Analysis • Data Analysis                       ║
   ╚═══════════════════════════════════════════════════════╝
"""


def _load_env() -> None:
    """Load environment variables from typical locations."""
    root = Path(__file__).resolve().parents[1]
    loaded = False

    env_path = root / ".env"
    if env_path.exists():
        load_dotenv(str(env_path))
        loaded = True

    cwd_env = Path.cwd() / ".env"
    if cwd_env.exists():
        load_dotenv(str(cwd_env))
        loaded = True

    if not loaded:
        example_path = root / ".env.example"
        if example_path.exists():
            load_dotenv(str(example_path))


def _check_env() -> bool:
    """Validate required environment variables."""
    missing: List[str] = []
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not openai_key or openai_key.lower() in {"your-openai-api-key-here", "changeme", "paste-here"}:
        missing.append("OPENAI_API_KEY")
    if not os.getenv("LANGSMITH_API_KEY"):
        console.print("[warning]⚠️  LANGSMITH_API_KEY is not set. Tracing will be limited.[/warning]")
    if missing:
        console.print(f"[error]✗ Missing required environment variables: {', '.join(missing)}[/error]")
        console.print("[info]💡 Hint: copy .env.example to .env and fill your keys.[/info]")
        return False
    return True


def _run_single_query(query: str) -> int:
    """Single query mode: run one inference and exit."""
    graph = build_system()
    
    # Display query
    console.print()
    console.print(Panel(
        Text(query, style="user"),
        title="[prompt]Query[/prompt]",
        border_style="blue",
        padding=(1, 2),
    ))
    
    # Process with status indicator
    with Status("[info]🤔 Processing...[/info]", console=console, spinner="dots"):
        result = graph.invoke(
            {"messages": [HumanMessage(content=query)]},
            config={"configurable": {"thread_id": "single-query"}},
        )
    
    response = result['messages'][-1].content
    
    # Display response with markdown rendering
    console.print()
    console.print(Panel(
        Markdown(response),
        title="[assistant]✨ Response[/assistant]",
        border_style="green",
        padding=(1, 2),
    ))
    console.print()
    
    return 0


def _run_interactive_chat() -> int:
    """Interactive chat mode: conversational interface with context memory."""
    graph = build_system()
    conversation_history: List[str] = []
    message_count = 0
    
    # Display elegant header (ASCII or Panel based on preference)
    console.print()
    
    if os.getenv("CLI_ASCII_BANNER", "").lower() == "true":
        # ASCII art banner for retro terminals
        console.print(Text(ASCII_BANNER, style="header"))
    else:
        # Modern panel header (default)
        header = Text("🤖 Multi-Agent Supervisor System", style="header", justify="center")
        subtitle = Text("Powered by LangGraph v1 | Text Analysis + Data Analysis Agents", style="dim italic", justify="center")
        
        console.print(Panel(
            Text.assemble(header, "\n", subtitle),
            border_style="magenta",
            padding=(1, 2),
        ))
    
    console.print()
    console.print("[info]💬 Interactive Chat Mode[/info]")
    console.print("[dim]Commands: 'exit'/'quit' to end | 'clear' to reset history | 'help' for tips[/dim]")
    console.print()
    
    try:
        while True:
            try:
                # Rich prompt with custom style
                user_input = Prompt.ask(
                    "[prompt]You[/prompt]",
                    console=console,
                ).strip()
            except EOFError:
                _show_goodbye(message_count)
                break
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in {"exit", "quit", "bye"}:
                _show_goodbye(message_count)
                break
            
            if user_input.lower() == "clear":
                console.clear()
                conversation_history.clear()
                message_count = 0
                console.print("[success]✓ Conversation history cleared.[/success]\n")
                continue
            
            if user_input.lower() == "help":
                _show_help()
                continue
            
            # Build context-aware query with conversation history
            if conversation_history:
                context = "\n".join(conversation_history[-10:])  # last 5 exchanges
                full_query = f"[Conversation context:\n{context}\n]\n\nCurrent query: {user_input}"
            else:
                full_query = user_input
            
            # Invoke agent with elegant status
            with Status("[info]🤔 Thinking...[/info]", console=console, spinner="dots"):
                try:
                    result = graph.invoke(
                        {"messages": [HumanMessage(content=full_query)]},
                        config={"configurable": {"thread_id": "interactive-chat"}},
                    )
                    response = result['messages'][-1].content
                except Exception as e:
                    console.print(f"\n[error]✗ Error: {str(e)}[/error]\n")
                    continue
            
            # Update conversation history
            message_count += 1
            conversation_history.append(f"User: {user_input}")
            conversation_history.append(f"Assistant: {response}")
            
            # Display response with markdown rendering and message counter
            console.print()
            console.print(Panel(
                Markdown(response),
                title=f"[assistant]🤖 Assistant[/assistant] [dim]│ Message #{message_count}[/dim]",
                border_style="green",
                padding=(1, 2),
            ))
            console.print()
    
    except KeyboardInterrupt:
        console.print()
        _show_goodbye(message_count)
    
    return 0


def _show_goodbye(message_count: int) -> None:
    """Display goodbye message with session statistics."""
    console.print()
    
    if message_count > 0:
        stats_text = Text.assemble(
            ("👋 Session ended\n\n", "info"),
            ("Messages exchanged: ", "dim"),
            (str(message_count), "success bold"),
        )
    else:
        stats_text = Text("👋 Goodbye!", style="info")
    
    console.print(Panel(
        stats_text,
        border_style="blue",
        padding=(1, 2),
    ))
    console.print()


def _show_help() -> None:
    """Display inline help information."""
    help_text = """
## 💡 Quick Help

**Available Commands:**
- `exit`, `quit`, `bye` — End the chat session
- `clear` — Clear conversation history
- `help` — Show this help message

**Tips:**
- The system has **two specialized agents**:
  - 🔤 **Text Agent**: Extract entities, analyze keywords
  - 📊 **Data Agent**: Calculate statistics, format tables
- Try **multi-turn conversations** — context is preserved!
- Example queries:
  - *"Extract entities from: Microsoft and Azure"*
  - *"Calculate stats for: 10, 20, 30, 40, 50"*
  - *"What were the entities in my last query?"* (uses context)
"""
    console.print()
    console.print(Panel(
        Markdown(help_text),
        title="[header]Help & Tips[/header]",
        border_style="blue",
        padding=(1, 2),
    ))
    console.print()


def entrypoint(argv: list[str] | None = None) -> int:
    """Main entry point: interactive chat or single query mode."""
    argv = argv if argv is not None else sys.argv
    _load_env()
    if not _check_env():
        return 1

    # Parse mode
    if len(argv) > 1 and argv[1] in {"--query", "-q"}:
        # Single query mode
        if len(argv) <= 2:
            console.print("[error]Usage: python -m cli --query \"<your query>\"[/error]")
            return 2
        query = " ".join(argv[2:])
        return _run_single_query(query)
    elif len(argv) > 1 and argv[1] not in {"--help", "-h"}:
        # Legacy: treat any args as a single query
        query = " ".join(argv[1:])
        return _run_single_query(query)
    elif len(argv) > 1 and argv[1] in {"--help", "-h"}:
        console.print(Panel(
            Markdown(__doc__ or "No documentation available."),
            title="[header]Help[/header]",
            border_style="blue",
        ))
        return 0
    else:
        # Interactive chat mode (default)
        return _run_interactive_chat()


if __name__ == "__main__":
    raise SystemExit(entrypoint())
