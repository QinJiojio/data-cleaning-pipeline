# CLAUDE.md — Urban Data Cleaning Pipeline

> Three-stage data cleaning pipeline with LLM Agent augmentation. Built on real-world urban survey data from a city government project.

## Project Purpose

Demonstrate data engineering capability for FDE/AI engineering roles:
1. **Stage 1 (Rule Engine)**: Deterministic cleaning — field mapping, type inference, coordinate conversion, dedup
2. **Stage 2 (Agent Assist)**: LLM-powered fuzzy semantic judgment — address matching, value equivalence, anomaly reasoning
3. **Stage 3 (Agent Audit)**: Batch LLM review — anomaly reports with confidence scores

## Architecture

```
config/
├── field_mapping.yaml     ← Field name standardization rules
├── type_inference.yaml    ← Type detection patterns
└── cleaning_rules.yaml    ← Per-data-source cleaning rules

data/
├── raw/                   ← Raw data (gitignored — contains sensitive real data)
├── clean/                 ← Cleaned outputs
└── samples/               ← Anonymized sample data for public demo

src/
├── pipeline.py            ← Entry point
├── rule_engine/           ← Stage 1: deterministic cleaning
├── agent/                 ← Stage 2+3: LLM agent integration
└── report/                ← Cleaning report generation

tests/

docs/
```

## Key Rules

### Data Privacy (CRITICAL)
- **NEVER commit raw data**. `data/raw/` and any file with real building addresses are gitignored
- All demo data must be anonymized: addresses → generic labels, coordinates → truncated to 3 decimal places
- Review every commit diff before pushing — no real data should ever reach GitHub

### Code Quality
- Python 3.10+, type hints on all public functions
- Each stage output is a checkpoint file — pipeline can resume from any stage
- YAML-driven configuration — no hardcoded field names or cleaning rules

### Project Focus
- This is a showcase project. Prioritize clean architecture, clear documentation, and demonstrable results over exhaustive edge case handling
- Every feature should have a corresponding entry in the cleaning report
- Agent prompts should be in a separate `prompts/` directory for easy review and iteration

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Data | pandas, geopandas |
| LLM | Claude API / OpenAI API |
| Config | YAML |
| Report | Markdown + HTML (jinja2) |
| Testing | pytest |
| Types | mypy |

## Related Repos

- `kashgar-urban-digital-twin` — The 3D platform this data pipeline was built for (full source)
- `cesium-mvp` — Private production repo (not public)
