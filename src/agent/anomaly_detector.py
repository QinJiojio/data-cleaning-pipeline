"""
Agent 2: Anomaly Pattern Reasoning

Uses LLM to flag logically impossible data combinations that rule-based
validation would miss. Rule engines can check ranges (floor_count > 0) but
cannot apply domain knowledge (30-story buildings didn't exist in 1985 Kashgar).

Example anomalies the Agent catches:
  {floor_count: 30, build_year: 1985, city: "Kashgar"} → "30-story residential
    buildings were not constructed in Kashgar in 1985. Likely data entry error."
  {area_m2: 2000, usage: "residential", floor_count: 1} → "Single-story 2000m²
    residential unit is unusual. Might be a public facility misclassified."
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class AnomalyReport:
    row_index: int
    field: str
    value: Any
    severity: str  # "high", "medium", "low"
    reasoning: str
    suggested_action: str


ANOMALY_PROMPT = """You are a data quality auditor for a Chinese city government's
urban survey dataset. You have domain knowledge about:
- Building construction history in Xinjiang (Kashgar region)
- Typical residential building characteristics in northwest China
- Common data entry errors in government surveys

Review this data row and flag any logically impossible or highly suspicious combinations.
Focus on what RULES cannot catch — use your domain knowledge.

Data row:
{row_json}

Context:
- City: Kashgar, Xinjiang
- Most residential buildings: 1-6 floors (older areas), 6-18 floors (newer areas)
- Buildings >18 floors were rare before 2010, extremely rare before 2000
- Typical residential unit: 50-150 m²
- Single-story 2000m² "residential" is almost certainly a misclassified facility

Output ONLY valid JSON array:
[{{"field": "field_name", "value": actual_value, "severity": "high|medium|low",
   "reasoning": "why this is suspicious", "suggested_action": "what to check"}}]

If nothing is suspicious, output: []
"""


def detect(
    row: dict[str, Any],
    row_index: int = 0,
    api_key: Optional[str] = None,
    model: str = "claude-fable-5",
) -> list[AnomalyReport]:
    """
    Analyze a single data row for domain-knowledge anomalies.

    Args:
        row: Dict of field_name → value
        row_index: Position in the dataset (for reporting)
        api_key: Anthropic API key
        model: Claude model

    Returns:
        List of AnomalyReport objects (empty if nothing suspicious)
    """
    import json

    prompt = ANOMALY_PROMPT.format(row_json=json.dumps(row, ensure_ascii=False))

    # Placeholder: replace with actual API call
    # headers = {
    #     "x-api-key": api_key,
    #     "anthropic-version": "2023-06-01",
    #     "content-type": "application/json",
    # }
    # body = {
    #     "model": model,
    #     "max_tokens": 512,
    #     "messages": [{"role": "user", "content": prompt}],
    # }
    # response = requests.post(
    #     "https://api.anthropic.com/v1/messages",
    #     headers=headers,
    #     json=body,
    #     timeout=10,
    # )
    # anomalies = json.loads(response.json()["content"][0]["text"])

    # return [AnomalyReport(
    #     row_index=row_index,
    #     field=a["field"],
    #     value=a["value"],
    #     severity=a["severity"],
    #     reasoning=a["reasoning"],
    #     suggested_action=a["suggested_action"],
    # ) for a in anomalies]

    raise NotImplementedError(
        "Replace this placeholder with your LLM API call."
    )


def batch_detect(
    rows: list[dict[str, Any]],
    sample_size: int = 50,
    api_key: Optional[str] = None,
    model: str = "claude-fable-5",
) -> list[AnomalyReport]:
    """
    Sample rows and run anomaly detection in batch.

    For large datasets (25K rows), running Agent per-row is too expensive.
    Instead: sample ~50 rows, run batch detection, use results to inform
    rule-engine improvements for the remaining rows.

    Args:
        rows: All data rows
        sample_size: Number of rows to sample for Agent analysis
        api_key: Anthropic API key
        model: Claude model

    Returns:
        List of AnomalyReport objects for sampled rows
    """
    import random

    if len(rows) > sample_size:
        sample = random.sample(rows, sample_size)
    else:
        sample = rows

    reports = []
    for i, row in enumerate(sample):
        row_reports = detect(row, row_index=i, api_key=api_key, model=model)
        reports.extend(row_reports)

    return reports


# ── Self-Test ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("Anomaly Detector Agent — self test")
    print("=" * 50)

    test_rows = [
        {
            "floor_count": 30,
            "build_year": 1985,
            "structure_type": "砖混",
            "city": "Kashgar",
        },
        {
            "area_m2": 2000,
            "usage": "住宅",
            "floor_count": 1,
            "structure_type": "砖混",
        },
        {
            "floor_count": 6,
            "build_year": 2010,
            "structure_type": "砖混",
            "area_m2": 80,
        },  # Normal — should produce no anomalies
    ]

    for i, row in enumerate(test_rows):
        print(f"\nRow {i}: {row}")
        print("Expected anomalies:")
        if row.get("floor_count") == 30 and row.get("build_year") == 1985:
            print("  ⚠️ 30-story building in 1985 Kashgar — highly suspicious")
        if row.get("area_m2") == 2000 and row.get("usage") == "住宅":
            print("  ⚠️ 2000m² single-story 'residential' — likely misclassification")

    print("\n✓ Test cases ready. Implement API call to run.")
