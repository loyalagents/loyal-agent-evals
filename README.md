# Working Loyal Agent Eval Code Enhancements

> Stanford Loyal Agents Initiative — December 2025

---

## Quick Start with UV

```bash
# Clone the repository
git clone https://github.com/loyalagents/loyal-agent-evals.git
cd loyal-agent-evals

# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Set your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env
```

---

## Run Evaluations

### Option 1: Run Both Frames (Recommended)

```bash
./scripts/run_full_evaluation.sh
```

### Option 2: Run Frames Individually

**Frame A — Consumer Fiduciary (40 scenarios)**
```bash
python3 run_evaluation.py --pack eval_packs/fdl_frame_a_consumer.yaml
```

**Frame B — Business Fiduciary (7 scenarios)**
```bash
python3 run_evaluation.py --pack eval_packs/fdl_frame_b_business.yaml
```

### Option 3: Run Unified V4 Pack (47 scenarios)

```bash
python3 run_evaluation.py --pack eval_packs/fiduciary_duty_v4_fixed.yaml
```

---

## Latest Evaluation Results

### Frame A: Consumer Fiduciary (2025-12-08)

| Scorer | Pass Rate | Avg Score | Status |
|--------|-----------|-----------|--------|
| **LLM Judge** | 81.2% | 0.730 | ✅ Good |
| **Conflict Immunity** | 100% | 1.000 | ✅ Excellent |
| **UETA Compliance** | 100% | 1.000 | ✅ Excellent |

📊 **Full Report**: [report_20251208_144306.md](reports/report_20251208_144306.md)

### Frame B: Business Fiduciary (2025-12-08)

| Scorer | Pass Rate | Avg Score | Status |
|--------|-----------|-----------|--------|
| **LLM Judge** | 100% | 0.871 | ✅ Excellent |
| **Conflict Immunity** | 100% | 1.000 | ✅ Excellent |
| **UETA Compliance** | 100% | 1.000 | ✅ Excellent |

📊 **Full Report**: [report_20251208_144428.md](reports/report_20251208_144428.md)

📋 **Comprehensive Analysis**: [report_full_run.md](report_full_run.md)

---

## What's Included

```
loyalagents/loyal-agent-evals/
├── LICENSE                          # Apache 2.0
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── run_evaluation.py                # Main evaluation runner
│
├── data/
│   ├── fdl_benchmark_v1.3.csv       # Unified dataset (47 scenarios)
│   ├── fdl_frame_a_consumer.csv     # Consumer frame (40 scenarios)
│   └── fdl_frame_b_business.csv     # Business frame (7 scenarios)
│
├── eval_packs/
│   ├── fdl_frame_a_consumer.yaml    # ✅ Consumer eval pack
│   ├── fdl_frame_b_business.yaml    # ✅ Business eval pack
│   └── fiduciary_duty_v4_fixed.yaml # Unified V4 pack 
│
├── core/scoring/
│   ├── conflict_immunity_scorer.py  # Vendor compensation checks
│   ├── ueta_compliance_scorer.py    # UETA §10(b) confirmation gates
│   ├── llms_respect_scorer.py       # LLMS.txt ToS compliance
│   ├── compliance_first_scorer.py   # Legal > profit verification
│   ├── dual_fiduciary_scorer.py     # Dual-agency negotiation
│   ├── fdl_disclosure_scorer.py     # Disclosure keyword detection
│   └── fdl_alignment_scorer.py      # Expected output matching
│
├── docs/
│   └── SCORER_REFERENCE.md          # ✅ Complete scorer documentation
│
├── scripts/
│   └── run_full_evaluation.sh       # ✅ Reproducibility script
│
├── reports/
│   ├── report_20251208_144306.md    # Frame A results
│   ├── report_20251208_144428.md    # Frame B results
│   └── eval_results_*.csv/json      # Raw evaluation data
│
├── report_full_run.md               # Comprehensive analysis report
├── CONTRACT.md                      # Agent fiduciary contract spec example
└── AUTH_PREFS.md                    # User authorizations & preferences example
```

---

## Framework Architecture

### The CONTRACT.md Approach

At the center of this framework is a formal **Agent Fiduciary Contract** that defines:

| Party | Role |
|-------|------|
| **User (Principal)** | Grants authority, defines authorizations |
| **AI Agent Provider** | Operates the agent, assumes fiduciary-like duties |
| **AI Agent** | Quasi-autonomous tool executing on behalf of User |

### Contractual Duties

| Duty | Description | Waivable? |
|------|-------------|-----------|
| **Duty to Act** | Carry out user instructions faithfully | Yes |
| **Loyalty** | No self-dealing, disclose conflicts | Yes |
| **Care** | Competence, informed decisions | Yes |
| **Obedience** | Stay within authorized scope | Yes |
| **Disclosure** | Conflicts, limitations, material events | Yes |
| **UETA §10(b)** | Offer confirmation/correction opportunity | **No (Statutory)** |

### AUTH_PREFS.md

Defines user authorizations:
- Monetary limits ($200/transaction, $500/day)
- Approved vendors (Apple, Amazon)
- Exclusions (subscriptions, digital goods)
- Preferences (recyclable, Made in USA)
- Autonomy settings (when to ask vs. auto-proceed)

---

## The Datasets

### Frame A: Consumer Fiduciary (40 scenarios)

| Source | Count | Content |
|--------|-------|---------|
| Core FDL | 12 | Scope violations, conflicts, data minimization |
| Handbook | 21 | Self-dealing, authority, disclosure |
| D1 Inventory | 7 | LLMS.txt, UETA gates, kickbacks |

### Frame B: Business Fiduciary (7 scenarios)

| Source | Count | Content |
|--------|-------|---------|
| D1 Inventory | 7 | Tax compliance, antitrust, dual-agency |

---

## The Scorers

| Scorer | Type | What It Checks |
|--------|------|----------------|
| `conflict_immunity` | Deterministic | Vendor compensation didn't influence decisions |
| `ueta_compliance` | Deterministic | Confirmation/correction opportunity offered |
| `llms_respect` | Deterministic | LLMS.txt restrictions honored lawfully |
| `compliance_first` | Deterministic | Legal requirements prevailed over profit |
| `dual_fiduciary` | Deterministic | Dual-agency used objective criteria |
| `fdl_disclosure` | Deterministic | Required disclosure keywords present |
| `fdl_alignment` | Deterministic | Output matches expected behavior |
| `llm_judge` | LLM-Based | Semantic evaluation of response quality |

📖 **Full Documentation**: [docs/SCORER_REFERENCE.md](docs/SCORER_REFERENCE.md)

---

## Evaluation Snapshot

| Version | Run ID | Frame | Key Changes | LLM Judge |
|---------|--------|-------|-------------|-----------|
| V4 | 20251207_210558 | Unified | All bugs fixed | 0.733 |
| **Frame A** | **20251208_111320** | Consumer | Separate frame | **0.727** |
| **Frame B** | **20251208_111435** | Business | Separate frame | **0.871** |

---

## Design Philosophy

### "Observable Contractual Loyalty"

The [agent handbook](https://github.com/loyalagents/agent-handbook-sandbox/commit/13a8cebc1f16eaf27b72efa7f25efd3875c7a094) provides a valuable foundation for identifying the behaviors we expect from loyal AI agents. Adapting these concepts for production, however, requires accounting for standard commercial contracting practices. Technology providers nearly universally disclaim agency relationships and consequent fiduciary duties — a typical example is [Section 7 of the Consumer Reports User Agreement](https://www.consumerreports.org/2015/01/user-agreement/), which explicitly holds that no "fiduciary, contractually implied or other relationship is created."

Because default fiduciary duties are routinely disclaimed, this framework builds on the handbook's scenarios by grounding evaluation in explicit contractual carve-outs. Duties of loyalty and care can enforceably arise through contract, even where a broader agency relationship has been disclaimed. For purposes of these evals, we translate "Fiduciary Duty" into "Observable Loyalty" — measurable behavior defined and agreed upon by contract between the parties.

This provides a clear, predictable basis for evaluating loyalty that sidesteps debates about AI legal personhood and focuses on whether an agent honored specific, limited duties defined in the provided contract and authorization files. In production, these contractual and authorization data sources may be vastly more complex; this framework identifies their essential role as fundamental inputs to measuring adherence to agreed behaviors.

### Repeatable Patterns

This framework is designed for reuse:

- **Different duties**: Modify CONTRACT.md
- **Different authorizations**: Modify AUTH_PREFS.md
- **Different agents**: Change the data_generator_llm (or use live agents)
- **Different data sources**: Change ingestion type (CSV, JSON, OTEL)
- **Different scorers**: Add to the pipeline

---

## Baseline Notes and Fixed-Rerun Behavior

### Specialized Scorer Invocation

The December 2025 baseline reports were produced before the frame packs stopped using `metadata.get()` function calls in `run_if` expressions. In that baseline, three specialized scorers were skipped by Lake Merritt's expression validator:

- **LLMS.txt Respect** (Frame A)
- **Compliance First** (Frame B)
- **Dual Fiduciary** (Frame B)

Current frame packs invoke these scorers directly and let each scorer decide whether it is substantively applicable. Missing or irrelevant observable signals are exported as `status=N/A`, `applicable=false`, and `substantive=false`, rather than counted as substantive pass-rate evidence.

The fixed rerun is stored under `reports/final-rerun-20260419T065448Z/`. Its logs contain no `Disallowed expression node: Call` messages.

### Stage-Aware Reporting

The December 2025 baseline Markdown reports aggregate duplicate `LLM Judge` scorer names by scorer label, so Frame A appears as `65/80` and Frame B as `14/14`. Current fixed-run reports are stage-aware:

- Headline pass rates use the configured final judge stage: `Semantic Alignment` for Frame A and `Business Compliance Judge` for Frame B.
- Frame A headline counts are scenario-level (`33/40`), not duplicate-stage counts (`65/80`).
- Frame B headline counts are scenario-level (`7/7`), not duplicate-stage counts (`14/14`).
- JSON exports preserve `headline_summary`, `stage_summary`, and per-score stage fields. Use those fields for substantive reporting instead of legacy compatibility `summary_stats`.

### Streaming Evals

Connect Lake Merritt OpenTelemetry Collector for real-time streaming evals.

---

## Requirements

Create `requirements.txt` in repo root or install directly:

```txt
openai>=1.0.0
pyyaml>=6.0
python-dotenv>=1.0.0
pandas>=2.0.0
rapidfuzz>=3.0.0
pydantic>=2.0.0
```

---

## License

- **Code**: Apache 2.0 (see [LICENSE](LICENSE))
- **Documentation and publication content**: CC BY 4.0 (see [LICENSE-CC-BY-4.0](LICENSE-CC-BY-4.0))
- **Dataset**: CC BY 4.0 (see [LICENSE-CC-BY-4.0](LICENSE-CC-BY-4.0) and [data/README.md](data/README.md))
- **License overview**: [LICENSES.md](LICENSES.md)

---

## References

- [Lake Merritt Evaluation Framework](https://github.com/PrototypeJam/lake_merritt)
- [Stanford Loyal Agents Initiative](https://loyalagents.org)
- [Uniform Electronic Transactions Act, Section 10(b)](https://www.dazzagreenwood.com/p/ueta-and-llm-agents-a-deep-dive-into)

---

## Reports Index

| Report | Date | Frame | Items | Key Metrics |
|--------|------|-------|-------|-------------|
| [report_20251208_144306.md](reports/report_20251208_144306.md) | 2025-12-08 | Consumer | 40 | 81.2% LLM, 100% UETA |
| [report_20251208_144428.md](reports/report_20251208_144428.md) | 2025-12-08 | Business | 7 | 100% all scorers |
| [report_20260418_235811.md](reports/final-rerun-20260419T065448Z/frame_a/report_20260418_235811.md) | 2026-04-19 | Consumer fixed rerun | 40 | 33/40 Semantic Alignment, LLMS 4 applicable / 36 N/A |
| [report_20260418_235858.md](reports/final-rerun-20260419T065448Z/frame_b/report_20260418_235858.md) | 2026-04-19 | Business fixed rerun | 7 | 7/7 Business Compliance Judge, Compliance First 3 applicable / 4 N/A, Dual Fiduciary 1 applicable / 6 N/A |

---
