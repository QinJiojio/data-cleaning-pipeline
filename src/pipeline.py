"""
Three-stage hybrid data cleaning pipeline orchestrator.

Stage 1 (Rule Engine): Deterministic cleaning — field mapping, type inference,
  coordinate conversion, regex dedup. 100% code, fast & reliable.

Stage 2 (Agent Assist): LLM-powered fuzzy judgment — address matching, value
  equivalence, anomaly reasoning. Handles cases rules cannot express.

Stage 3 (Agent Audit): Batch LLM quality review — anomaly reports with
  confidence scores, human review queue for borderline cases.

Checkpoint files at each stage allow resuming or re-running individual stages.
"""

from pathlib import Path
from typing import Optional

import yaml


def run_pipeline(
    config_path: str | Path,
    resume_from: Optional[str] = None,
) -> dict:
    """
    Run the full data cleaning pipeline.

    Args:
        config_path: Path to YAML configuration file
        resume_from: Stage to resume from ("stage1", "stage2", "stage3")

    Returns:
        Dict with cleaning statistics and report path
    """
    config = _load_config(config_path)

    stats = {"input_rows": 0, "output_rows": 0, "stage1_changes": 0, "stage2_changes": 0, "stage3_changes": 0}

    # Stage 1: Rule Engine
    if resume_from is None or resume_from == "stage1":
        print("[Stage 1] Rule Engine — deterministic cleaning...")
        stats["stage1_changes"] = _run_stage1(config, stats)
        print(f"  → {stats['stage1_changes']} records modified")

    # Stage 2: Agent Assist
    if resume_from in (None, "stage1", "stage2"):
        print("[Stage 2] Agent Assist — fuzzy semantic judgment...")
        stats["stage2_changes"] = _run_stage2(config, stats)
        print(f"  → {stats['stage2_changes']} records modified by Agent")

    # Stage 3: Agent Audit
    if resume_from in (None, "stage1", "stage2", "stage3"):
        print("[Stage 3] Agent Audit — batch quality review...")
        stats["stage3_changes"] = _run_stage3(config, stats)
        print(f"  → {stats['stage3_changes']} issues flagged")

    # Generate report
    report_path = _generate_report(config, stats)
    print(f"\n✓ Pipeline complete. Report: {report_path}")

    return stats


def _load_config(path: str | Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def _run_stage1(config: dict, stats: dict) -> int:
    """
    Stage 1: Deterministic rule-based cleaning.

    Modules applied:
    1. header_detector — identify header mode (double-row / prefix / flat)
    2. type_inference — auto-detect 9 data types
    3. field_mapper — standardize field names across sources
    4. empty_strategy — handle null/empty/placeholder values
    5. coord_converter — GCJ-02 ↔ WGS-84 ↔ BD-09
    6. geojson_cleaner — topology repair, degenerate fragment cleanup
    7. dedup — multi-field deduplication
    """
    # TODO: Wire up actual modules
    return 0


def _run_stage2(config: dict, stats: dict) -> int:
    """
    Stage 2: LLM Agent for fuzzy semantic judgment.

    Uses: agent/address_matcher.py, agent/anomaly_detector.py
    """
    # TODO: Wire up Agent modules
    return 0


def _run_stage3(config: dict, stats: dict) -> int:
    """
    Stage 3: LLM Agent batch audit for quality assurance.
    """
    # TODO: Wire up Agent modules
    return 0


def _generate_report(config: dict, stats: dict) -> str:
    """
    Generate cleaning report (Markdown) comparing input vs output.
    """
    report_path = config.get("output_dir", "data/clean") + "/cleaning_report.md"
    # TODO: Generate actual report
    return report_path


if __name__ == "__main__":
    import sys

    config = sys.argv[1] if len(sys.argv) > 1 else "config/sample.yaml"
    run_pipeline(config)
