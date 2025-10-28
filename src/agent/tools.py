from typing import List
from collections import Counter
import re
from langchain_core.tools import tool


@tool
def extract_entities(text: str) -> list[str]:
    """Extract Title-Case entities from text."""
    candidates = re.findall(r"(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", text)
    return list(dict.fromkeys(candidates))[:15]


@tool
def keyword_counts(text: str, top_k: int = 10, min_length: int = 2) -> list[dict]:
    """Return top-k keyword frequencies from text (language-agnostic, case-insensitive).
    
    Filters tokens by minimum length only, no language-specific stopwords.
    Works with any language using Unicode word characters.
    """
    tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+", text.lower())
    filtered = [t for t in tokens if len(t) >= min_length]
    counts = Counter(filtered).most_common(top_k)
    return [{"term": t, "count": c} for t, c in counts]


## Intentionally no IO tools here (no file/network access)


@tool
def calculate_stats(numbers: List[float]) -> dict:
    """Calculate statistics for numbers."""
    import statistics as st
    if not numbers:
        return {"error": "Empty"}
    return {
        "count": len(numbers),
        "mean": round(st.mean(numbers), 2),
        "median": round(st.median(numbers), 2),
        "stdev": round(st.stdev(numbers), 2) if len(numbers) > 1 else 0,
        "min": min(numbers),
        "max": max(numbers),
    }


@tool
def format_table(data: list[dict] | dict | None = None) -> str:
    """Format data as markdown table."""
    if not data:
        return "No data"
    if isinstance(data, dict):
        rows = [f"| {k} | {v} |" for k, v in data.items()]
        return "| Metric | Value |\n| --- | --- |\n" + "\n".join(rows)
    if isinstance(data, list) and data:
        headers = list(data[0].keys())
        hdr = "| " + " | ".join(headers) + " |"
        sep = "| " + " | ".join(["---"] * len(headers)) + " |"
        rows = [
            "| " + " | ".join(str(r.get(h, "")) for h in headers) + " |"
            for r in data
        ]
        return "\n".join([hdr, sep] + rows)
    return "Invalid data"
