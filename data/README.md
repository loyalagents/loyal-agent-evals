# Dataset

This directory contains the Loyal Agent Evals test dataset developed under the
Stanford Loyal Agents Initiative.

## License

The dataset files in this directory are licensed under the Creative Commons
Attribution 4.0 International License (CC BY 4.0). See
[../LICENSE-CC-BY-4.0](../LICENSE-CC-BY-4.0).

## Files

- `fdl_frame_a_consumer.csv` — 40 consumer-fiduciary scenarios
- `fdl_frame_b_business.csv` — 7 business-fiduciary scenarios
- `fdl_benchmark_v1.3.csv` — 47 unified scenarios across both frames

## Provenance

- Frame A (40): Core FDL (12), Handbook (21), D1 Inventory (7)
- Frame B (7): D1 Inventory (7)

## Schema

- `fdl_benchmark_v1.3.csv`: `id`, `input`, `expected_output`, `metadata`
- `fdl_frame_a_consumer.csv` and `fdl_frame_b_business.csv`: `id`, `input`,
  `expected_output`, `metadata`, `frame`, `has_explanation`,
  `llms_txt_parsed`, `legal_requirement_detected`,
  `dual_fiduciary_recognized`

## Suggested Attribution

Greenwood, D. (2026). Loyal Agent Evals Dataset. Stanford Loyal Agents
Initiative. https://github.com/loyalagents/loyal-agent-evals
