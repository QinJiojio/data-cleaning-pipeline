"""
Agent 1: Address Semantic Matching

Uses LLM to determine whether two differently-written addresses refer to the
same building. Rule-based regex cannot handle the combinatorial explosion of
Chinese address variants (character reordering, abbreviation, local naming).

Example matches the Agent handles:
  "乌兰巴托东路15号院3号楼" vs "3号楼 15号院" → YES (reordered)
  "团结路23号" vs "团结路25号" → NO (different number)
  "解放南路188号" vs "解放路188号" → YES (omitted "南")
  "东湖小区2栋" vs "东湖小区2号楼" → YES (equivalent suffix)
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests  # or anthropic SDK


@dataclass
class MatchResult:
    matches: bool
    confidence: float
    reasoning: str


PROMPT = """You are a data cleaning assistant specialized in Chinese urban addresses.
Determine whether two addresses refer to the SAME building.

Rules:
- Building number swapping (e.g., "15号院3号楼" vs "3号楼15号院") → SAME
- Directional suffix omission (e.g., "解放南路" vs "解放路") in same numbered street → SAME
- Different numbers on the same street → DIFFERENT
- Same community name + same building number despite different suffixes (栋/号楼/幢) → SAME
- Different community names → DIFFERENT (low confidence if ambiguous)

Output ONLY valid JSON: {"matches": true/false, "confidence": 0.0-1.0, "reasoning": "brief explanation in English"}

Address A: {addr_a}
Address B: {addr_b}
"""


def match(
    addr_a: str,
    addr_b: str,
    api_key: Optional[str] = None,
    model: str = "claude-fable-5",
) -> MatchResult:
    """
    Compare two addresses and return match result with confidence.

    Args:
        addr_a: First address string
        addr_b: Second address string
        api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        model: Claude model to use

    Returns:
        MatchResult with match status, confidence (0.0-1.0), and reasoning
    """
    import json

    prompt = PROMPT.format(addr_a=addr_a, addr_b=addr_b)

    # Using requests directly (no framework dependency)
    # Replace with your preferred LLM client
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": model,
        "max_tokens": 256,
        "messages": [{"role": "user", "content": prompt}],
    }

    # Placeholder: replace with actual API call
    # response = requests.post(
    #     "https://api.anthropic.com/v1/messages",
    #     headers=headers,
    #     json=body,
    #     timeout=10,
    # )
    # result = json.loads(response.json()["content"][0]["text"])

    raise NotImplementedError(
        "Replace this placeholder with your LLM API call. "
        "See comments above for the Anthropic API format."
    )


# ── Batch Processing ──────────────────────────────────────────

def batch_match(
    pairs: list[tuple[str, str]],
    api_key: Optional[str] = None,
    model: str = "claude-fable-5",
    batch_size: int = 10,
) -> list[MatchResult]:
    """
    Match multiple address pairs in batches.

    Args:
        pairs: List of (addr_a, addr_b) tuples
        api_key: Anthropic API key
        model: Claude model
        batch_size: Number of pairs per API call (grouped into one prompt)

    Returns:
        List of MatchResult, one per input pair
    """
    results = []
    for i in range(0, len(pairs), batch_size):
        batch = pairs[i : i + batch_size]
        # Batch into a single prompt: "Compare these N pairs..."
        # grouped_prompt = build_batch_prompt(batch)
        # batch_results = call_llm(grouped_prompt)
        # results.extend(batch_results)
        pass
    return results


# ── Self-Test ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("Address Matcher Agent — self test")
    print("=" * 50)

    test_cases = [
        ("乌兰巴托东路15号院3号楼", "3号楼 15号院", True),
        ("团结路23号", "团结路25号", False),
        ("解放南路188号", "解放路188号", True),
        ("东湖小区2栋", "东湖小区2号楼", True),
    ]

    for a, b, expected in test_cases:
        print(f"\nA: {a}\nB: {b}")
        print(f"Expected: {'MATCH' if expected else 'DIFFERENT'}")
        print(f"Agent: [API call placeholder]")

    print("\n✓ Test cases ready. Implement API call to run.")
