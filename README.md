# Urban Data Cleaning Pipeline

> Three-stage hybrid data cleaning pipeline — rule engine for deterministic operations, LLM Agent for fuzzy semantic judgment. Built on real 25,000-building urban survey data.

![Status: MVP](https://img.shields.io/badge/status-MVP-yellow)
![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

---

## Why This Exists

During the development of a city government 3D digital twin platform, I handled data from 4+ utility companies, 30+ community offices, and multiple CAD drawing sets. The data was messy:

- Field names varied across sources (same concept, 3+ different column names)
- 36% of properties were empty or meaningless (`null`, `''`, `无`)
- Coordinate systems were mixed (GCJ-02, WGS-84, BD-09)
- Building addresses had 5+ variant spellings for the same location
- Some CAD-extracted values were logically impossible (30-story building, built in 1985)

Traditional rule-based cleaning handles the deterministic cases. But fuzzy cases — "is `乌兰巴托东路15号院3号楼` the same building as `3号楼15号院`?" — are where LLM Agents excel.

## Architecture

```
Stage 1: Rule Engine              Stage 2: Agent Assist            Stage 3: Agent Audit
┌──────────────────┐            ┌──────────────────┐            ┌──────────────────┐
│ Field mapping     │            │ Address matching  │            │ Batch sample      │
│ Type inference    │            │ Value equivalence │            │ Anomaly report    │
│ Coordinate conv   │            │ Anomaly reasoning │            │ Confidence score  │
│ Regex dedup       │            │                   │            │ Human review queue│
│                   │            │                   │            │                   │
│ 100% code         │            │ LLM judged         │            │ LLM audited       │
│ Fast & reliable   │            │ Handles ambiguity  │            │ Quality assurance │
└──────────────────┘            └──────────────────┘            └──────────────────┘
         │                              │                              │
         ▼                              ▼                              ▼
   Cleaned data                   Fuzzy matches               Anomaly report
   + stats                        + suggestions               + confidence
```

## Features

- [x] **Stage 1 — Rule Engine**: field name mapping, type inference (9 types), coordinate conversion (GCJ-02 ↔ WGS-84), regex dedup, empty value strategies (drop/fill/keep)
- [x] **Stage 2 — Agent Assist**: address semantic matching (LLM judges fuzzy address equivalence) + anomaly pattern reasoning (LLM flags impossible data combos using domain knowledge)
- [ ] **Stage 3 — Agent Audit**: batch sampling → LLM review → anomaly report with confidence scores → human review queue
- [x] YAML-driven configuration — different data sources use different rules, no code changes needed
- [x] Prompt templates in `config/prompts/` — auditable, version-controlled AI instructions
- [x] Pipeline orchestrator with checkpoint support — resume from any stage

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Run with sample data
python src/pipeline.py --config config/sample.yaml --input data/samples/raw_sample.csv

# Output
# data/clean/cleaned_data.csv
# data/clean/cleaning_report.md
```

## Configuration Example

```yaml
# config/sample.yaml
source: "community_survey_2026"
input: "data/samples/raw_sample.csv"

field_mapping:
  "房号": "room_id"
  "户号": "household_id"
  "建筑结构": "structure_type"

type_rules:
  structure_type: "string"
  floor_count: "int"
  build_year: "int"

empty_strategy:
  structure_type: "fill_mode"   # Most common value
  remarks: "drop"               # Remove entirely
  floor_count: "keep"           # 0 is meaningful (single-story)

coordinate_columns: ["longitude", "latitude"]
coord_source: "GCJ-02"
coord_target: "WGS-84"
```

## Data Privacy

This project uses real urban survey data. **Raw data is never committed to this repository.** All demo data in `data/samples/` has been anonymized:
- Building addresses → generic labels
- Coordinate precision → truncated to 3 decimal places (~100m accuracy)
- Organization names → generic labels

## Tech Stack

- **Python 3.10+** (type hints throughout)
- **pandas** (tabular data), **geopandas** (spatial data)
- **Claude API / OpenAI API** (LLM Agent stages)
- **PyYAML** (configuration)
- **pytest** (testing)

## Project Status

**MVP (Day 1-2)**: Stage 1 rule engine working end-to-end with sample data.
**In progress**: Stage 2 Agent Assist integration, Stage 1 edge cases.

---

> Built by [QinJiojio](https://github.com/QinJiojio) · Part of a 3-project portfolio for AI/FDE roles
> Related: [kashgar-urban-digital-twin](https://github.com/QinJiojio/kashgar-urban-digital-twin)
