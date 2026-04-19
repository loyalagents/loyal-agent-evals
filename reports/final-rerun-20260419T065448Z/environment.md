# Phase 7 Rerun Environment

Run root: `reports/final-rerun-20260419T065448Z`

Generated UTC:
- Frame A report: `2026-04-19 06:58:11`
- Frame B report: `2026-04-19 06:58:58`

Source:
- Loyal Agent Evals source commit: `6db3ed6ee31dd22a0082f800b034267ceb240723`
- Lake Merritt dependency path: `/Users/dazzagreenwood/Documents/GitHub/lake_merritt`
- Lake Merritt commit: `1869919493ce4904ad88afe85ebfc3e8e68b1ee7`
- `PYTHONPATH`: `/Users/dazzagreenwood/Documents/GitHub/lake_merritt`
- Virtualenv Python: `/tmp/loyal-agent-evals-mini-sprint-venv/bin/python`
- Python version: `Python 3.11.13`

Package versions resolved through `importlib.metadata`:
- `openai==2.32.0`
- `pydantic==2.13.2`
- `pytest==9.0.3`
- `PyYAML==6.0.3`
- `python-dotenv==1.2.2`
- `anyio==4.13.0`
- `httpx==0.28.1`

Model identifiers in the eval packs:
- Frame A data generation config: `openai/gpt-4o-mini`, temperature `0.5`
- Frame A Signal Extractor: `openai/gpt-4o-mini`, temperature `0.1`
- Frame A Semantic Alignment: `openai/gpt-4o`, temperature `0.2`
- Frame B data generation config: `openai/gpt-4o-mini`, temperature `0.5`
- Frame B Signal Extractor: `openai/gpt-4o-mini`, temperature `0.1`
- Frame B Business Compliance Judge: `openai/gpt-4o`, temperature `0.2`

API key handling:
- `OPENAI_API_KEY` was loaded from `/Users/dazzagreenwood/Documents/GitHub/lake_merritt/.env`.
- The key value is not recorded in this artifact.

Validation checks:
- Focused/current suite after the Phase 7 mapper repair: `28 passed, 6 warnings`.
- Full rerun logs contain no `Disallowed expression node: Call` messages.
- Frame A headline denominator is `40`, with `33` passed, `7` failed, `0` errors, and `0` missing headline outputs.
- Frame B headline denominator is `7`, with `7` passed, `0` failed, `0` errors, and `0` missing headline outputs.
- Specialized scorer stages appear in fixed outputs:
  - Frame A: `LLMS.txt Respect` / `llms_respect`
  - Frame B: `Compliance First` / `compliance_first`
  - Frame B: `Dual Fiduciary` / `dual_fiduciary`

Known local guardrails:
- Sprint evidence is stored under Dropbox only, not repo `docs/evidence`.
- Repo `docs/evidence` deletion entries remain an unstaged cleanup/history-curation surface and are not part of the Phase 7 commits.
- No push was performed.
