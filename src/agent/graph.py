import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

from agent.agent_builders import create_text_worker, create_data_worker


def build_system():
    """Build single-mode supervisor graph: LLM + ToolNode (agent handoffs)."""
    return build_system_tools_mode()


def _make_handoff_tool(agent_graph, *, name: str, description: str):
    def _handoff(task: str) -> str:
        # Ensure the worker agent gets a proper HumanMessage to trigger its ReAct loop
        result = agent_graph.invoke({"messages": [HumanMessage(content=task)]})
        msg = result["messages"][-1]
        return getattr(msg, "content", str(msg))

    _handoff.__name__ = name
    _handoff.__doc__ = description
    return tool(_handoff)


def build_system_tools_mode():
    """Supervisor LLM with agent handoff via tools (supports parallel tool calls)."""
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    text_agent = create_text_worker(model_name)
    data_agent = create_data_worker(model_name)

    transfer_to_text = _make_handoff_tool(
        text_agent,
        name="transfer_to_text",
        description=(
            "Send a subtask to text_agent (inline text analysis: extract entities and keyword frequencies; no IO)"
        ),
    )
    transfer_to_data = _make_handoff_tool(
        data_agent,
        name="transfer_to_data",
        description=(
            "Send a subtask to data_agent (numeric stats and data/table formatting)"
        ),
    )

    def _bind(model: ChatOpenAI):
        return model.bind_tools([transfer_to_text, transfer_to_data])

    SUP_PROMPT = (
        "You are the Supervisor in the langgraph-supervised-quickstart project (https://github.com/joaomede/langgraph-supervised-quickstart).\n"
        "This is a minimal multi-agent system for educational purposes. Your role is to manage specialist agents and route tasks efficiently.\n\n"
        
        "=== AVAILABLE AGENTS ===\n"
        "1. TEXT AGENT (transfer_to_text)\n"
        "   - Capabilities: Entity extraction, keyword frequency analysis\n"
        "   - Tools: extract_entities (finds Title-Case entities), keyword_counts (top-k word frequencies, language-agnostic)\n"
        "   - Use when: User asks to extract entities, find keywords, analyze text content\n"
        "   - Example: 'Extract entities from: Microsoft and Google'\n\n"
        
        "2. DATA AGENT (transfer_to_data)\n"
        "   - Capabilities: Statistical analysis, data formatting\n"
        "   - Tools: calculate_stats (mean, median, stdev, min, max), format_table (markdown tables)\n"
        "   - Use when: User provides numbers, asks for statistics, needs data visualization\n"
        "   - Example: 'Calculate stats for: 10, 20, 30, 40, 50'\n\n"
        
        "=== YOUR RESPONSIBILITIES ===\n"
        "- When asked 'what can you do?', explain your role and describe both agents with examples\n"
        "- Route text analysis tasks to TEXT AGENT via transfer_to_text\n"
        "- Route numerical/statistical tasks to DATA AGENT via transfer_to_data\n"
        "- For mixed requests (text + numbers), you MAY call both tools in parallel\n"
        "- Synthesize agent results into a clear, concise final answer\n"
        "- If user mentions text/file but doesn't provide it, ask them to paste the content inline\n\n"
        
        "=== CONSTRAINTS ===\n"
        "- NO file I/O, NO web access, NO external resources\n"
        "- Work only with inline text and numbers provided by the user\n"
        "- Keep responses concise and focused\n"
    )

    model = ChatOpenAI(model=model_name)
    llm = _bind(model)
    tools_node = ToolNode([transfer_to_text, transfer_to_data])

    def supervisor_llm(state: MessagesState):
        msgs = state["messages"]
        if not msgs or (msgs and getattr(msgs[0], "type", getattr(msgs[0], "role", "")) != "system"):
            msgs = [{"role": "system", "content": SUP_PROMPT}] + msgs
        resp = llm.invoke(
            msgs,
            config={"run_name": "supervisor_llm", "tags": ["orchestrator", "tools-mode"]},
        )
        return {"messages": [resp]}

    def route_after_llm(state: MessagesState):
        last = state["messages"][-1]
        tool_calls = getattr(last, "tool_calls", None)
        return "tools" if tool_calls else END

    builder = StateGraph(MessagesState)
    builder.add_node("llm", supervisor_llm)
    builder.add_node("tools", tools_node)
    builder.add_edge(START, "llm")
    builder.add_conditional_edges("llm", route_after_llm, {"tools": "tools", END: END})
    builder.add_edge("tools", "llm")
    return builder.compile(checkpointer=MemorySaver())
