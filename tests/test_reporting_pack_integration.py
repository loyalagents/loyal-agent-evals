import csv
import io
import json
from pathlib import Path

import yaml

from core.data_models import EvaluationItem, EvaluationResults, ScorerResult

from fdl_eval.reporting import build_headline_summary, results_to_csv, results_to_json
from fdl_eval.stage_identity import annotate_results_with_stage_identity


REPO_ROOT = Path(__file__).resolve().parents[1]


FRAME_PACKS = [
    (
        "eval_packs/fdl_frame_a_consumer.yaml",
        "Semantic Alignment",
        "stage_01_signal_extractor",
        "stage_05_semantic_alignment",
    ),
    (
        "eval_packs/fdl_frame_b_business.yaml",
        "Business Compliance Judge",
        "stage_01_signal_extractor",
        "stage_06_business_compliance_judge",
    ),
]


def _load_pack(relative_path):
    with open(REPO_ROOT / relative_path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _results_for_pack(pack_data):
    scores = []
    for stage in pack_data["pipeline"]:
        details = {}
        if stage["scorer"] != "llm_judge":
            details = {"applicable": False, "status": "N/A", "substantive": False}
        scores.append(
            ScorerResult(
                scorer_name=stage["scorer"],
                score=1.0,
                numeric_score=1.0,
                passed=True,
                reasoning=f"synthetic {stage['name']}",
                details=details,
            )
        )

    results = EvaluationResults(
        items=[
            EvaluationItem(
                id="integration-case",
                input="input",
                output="output",
                expected_output="expected",
                metadata={"fixture": "actual-pack-stage-order"},
                scores=scores,
            )
        ],
        config={"eval_pack": pack_data},
    )
    return annotate_results_with_stage_identity(results, pack_data)


def test_actual_frame_packs_preserve_duplicate_llm_judge_stages_in_exports():
    for pack_path, headline_name, signal_stage_id, headline_stage_id in FRAME_PACKS:
        results = _results_for_pack(_load_pack(pack_path))

        headline = build_headline_summary(results)
        payload = json.loads(results_to_json(results))
        csv_row = next(csv.DictReader(io.StringIO(results_to_csv(results))))

        llm_stages = [
            score["stage_name"]
            for score in payload["items"][0]["scores"]
            if score["scorer_name"] == "llm_judge"
        ]

        assert llm_stages == ["Signal Extractor", headline_name]
        assert headline["headline_stage_id"] == headline_stage_id
        assert headline["headline_stage_name"] == headline_name
        assert headline["scenario_level_items"] == 1
        assert headline["substantive_denominator"] == 1
        assert f"{signal_stage_id}__score" in csv_row
        assert f"{headline_stage_id}__score" in csv_row
        assert csv_row[f"{signal_stage_id}__scorer_name"] == "llm_judge"
        assert csv_row[f"{headline_stage_id}__scorer_name"] == "llm_judge"
