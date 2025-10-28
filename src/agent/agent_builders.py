from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from agent.tools import (
    extract_entities,
    keyword_counts,
    calculate_stats,
    format_table,
)


def create_text_worker(model_name: str):
    """ReAct worker: inline text analysis (simple, no IO/web)."""
    model = ChatOpenAI(model=model_name)
    return create_agent(
        model,
        tools=[extract_entities, keyword_counts],
        system_prompt=(
            "You are a simple Text Analysis Agent. Work only on the text provided inline in the user's message.\n"
            "Use exactly these tools:\n"
            "- extract_entities(text): Title-Case entities.\n"
            "- keyword_counts(text, top_k, min_length): top-k keywords with counts (language-agnostic, filters by min_length only).\n"
            "Keep it simple: identify the text span (after 'text:' / quoted / full message), call the tools, and synthesize a concise final answer (2–4 bullets + lists). No IO/web."
        ),
    )


def create_data_worker(model_name: str):
    """ReAct worker: statistics + table formatting (always synthesize final answer)."""
    model = ChatOpenAI(model=model_name)
    return create_agent(
        model,
        tools=[calculate_stats, format_table],
        system_prompt=(
            "You are a Data Agent. Your job is to compute numeric statistics and present them clearly.\n"
            "When the user asks for statistics (keywords like 'stats', 'calculate stats', or a list of numbers):\n"
            "1) Parse a clean list of numbers from the request.\n"
            "2) Call calculate_stats(numbers).\n"
            "3) Call format_table(<stats_dict>) to produce a markdown table of the results.\n"
            "4) THEN write a concise final answer that includes: the table and 1-2 short insights (e.g., mean, range).\n"
            "Rules: ALWAYS include the computed values (never just acknowledge). NEVER respond with a generic sentence.\n"
            "If the input is invalid, explain what's wrong and suggest a corrected format."
        ),
    )
