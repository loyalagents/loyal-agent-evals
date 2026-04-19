# Phase 7 Full Rerun Command Log

Run root: `reports/final-rerun-20260419T065448Z`

Gate 3 status before rerun: green with REVIEWER, BREAKER, and VERIFIER repair signoffs recorded in Dropbox `phase_6_review.md`.

## Frame A

```bash
set -a
source /Users/dazzagreenwood/Documents/GitHub/lake_merritt/.env
set +a
PYTHONPATH=/Users/dazzagreenwood/Documents/GitHub/lake_merritt /tmp/loyal-agent-evals-mini-sprint-venv/bin/python run_evaluation.py --pack eval_packs/fdl_frame_a_consumer.yaml --output-dir reports/final-rerun-20260419T065448Z/frame_a
```

## Frame B

Frame B command is intentionally documented here before execution, per Phase 7 ordering.

```bash
set -a
source /Users/dazzagreenwood/Documents/GitHub/lake_merritt/.env
set +a
PYTHONPATH=/Users/dazzagreenwood/Documents/GitHub/lake_merritt /tmp/loyal-agent-evals-mini-sprint-venv/bin/python run_evaluation.py --pack eval_packs/fdl_frame_b_business.yaml --output-dir reports/final-rerun-20260419T065448Z/frame_b
```
