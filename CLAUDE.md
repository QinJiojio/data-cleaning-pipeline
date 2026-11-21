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

## TODO — Remaining Work

### Priority 1: Make Pipeline Runnable (2-3 hours)

- [ ] **API key wiring**: Replace `NotImplementedError` in `address_matcher.py` and `anomaly_detector.py` with actual Anthropic API calls (10 lines each, format already documented in comments)
- [ ] **Sample data**: Create `data/samples/raw_sample.csv` with 100-500 anonymized rows. Use the 8 representative fields from `config/sample.yaml`. Anonymization: addresses → generic labels, coordinates → 3 decimal places
- [ ] **Stage 1 rule engine modules**: Extract validated logic from cesium-mvp into standalone Python modules:
  - [ ] `src/rule_engine/header_detector.py` — 3-mode detection (double-row / prefix / flat)
  - [ ] `src/rule_engine/type_inference.py` — 9-type auto-detection with boolean normalization
  - [ ] `src/rule_engine/empty_strategy.py` — drop / fill_mode / keep
  - [ ] `src/rule_engine/coord_converter.py` — GCJ-02 ↔ WGS-84 ↔ BD-09
  - [ ] `src/rule_engine/geojson_cleaner.py` — topology repair + degenerate fragment removal
- [ ] **Wire `_run_stage1/2/3` in `pipeline.py`** to actually call the modules above
- [ ] **Report generation**: `src/report/generate.py` — Markdown report with before/after stats + Agent findings

### Priority 2: Polish (2-3 hours)

- [ ] `requirements.txt` with exact versions (pandas, geopandas, pyyaml, anthropic, pytest)
- [ ] `Makefile` with targets: `make run`, `make test`, `make clean`
- [ ] pytest tests for stage 1 modules (happy path + edge cases)
- [ ] `docs/` with architecture diagram + data flow description
- [ ] Demo GIF/screenshot in README of pipeline running end-to-end

### Priority 3: Agent Enhancement (future)

- [ ] Agent 3 audit: batch sampling with confidence scores + human review queue
- [ ] Few-shot examples in prompts from real matching history
- [ ] Streaming output for large batch processing

### What NOT to do

- Do NOT add LangChain/LlamaIndex — overkill for 2 Agent calls, adds dependency weight
- Do NOT make a web UI — CLI is sufficient for showcase
- Do NOT handle every edge case — this is a showcase, not production software

## Related Repos

- `kashgar-urban-digital-twin` — The 3D platform this data pipeline was built for (full source)
- `cesium-mvp` — Private production repo (not public)


## 跨机同步仓库声明（2026-11-21）

- 本仓库是**跨机同步仓库**：远端 `github.com/QinJiojio/data-cleaning-pipeline`，A/B 两机各持一份 clone（路径一致协议，禁止改名/移动）
- **开工**：`git pull`；若 `git log @{u}..HEAD` 非空先补推上次遗漏
- **收工**：commit + push 并**确认 push 成功**（失败=改动未送达，下次会话补推）；提交信息用 `<类型>:<中文摘要>`（feat/fix/docs/chore/wip）
- 冲突保留双方条目，不确定即停问用户；**禁止 force push**
- 纪律全文见 `_galaxia` 仓库（CLAUDE.md 通信协议 + 指导书 §3.6）
