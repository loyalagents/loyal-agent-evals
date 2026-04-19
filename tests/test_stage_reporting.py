import csv
import io
import json

from core.data_models import EvaluationItem, EvaluationResults, ScorerResult

from fdl_eval.reporting import (
    build_headline_summary,
    generate_summary_report,
    headline_failure_items,
    results_to_csv,
    results_to_json,
)
from fdl_eval.stage_identity import annotate_results_with_stage_identity


def _pack(final_stage_name="Semantic Alignment"):
    return {
        "name": "Synthetic FDL Pack",
        "pipeline": [
            {"name": "Signal Extractor", "scorer": "llm_judge", "config": {}},
            {"name": final_stage_name, "scorer": "llm_judge", "config": {}},
            {"name": "Conflict Immunity", "scorer": "conflict_immunity", "config": {}},
        ],
    }


def _item(index, final_passed=True, final_score=1.0):
    return EvaluationItem(
        id=f"case-{index:03d}",
        input=f"input {index}",
        output=f"output {index}",
        expected_output=f"expected {index}",
        metadata={"group": "synthetic"},
        scores=[
            ScorerResult(
                scorer_name="llm_judge",
                score=0.75,
                numeric_score=0.75,
                passed=True,
                reasoning="signals extracted",
            ),
            ScorerResult(
                scorer_name="llm_judge",
                score=final_score,
                numeric_score=final_score,
                passed=final_passed,
                reasoning="headline judge",
            ),
            ScorerResult(
                scorer_name="conflict_immunity",
                score=1.0,
                numeric_score=1.0,
                passed=True,
                reasoning="not applicable",
                details={"applicable": False, "status": "N/A", "substantive": False},
            ),
        ],
    )


def _results(count, final_stage_name="Semantic Alignment"):
    results = EvaluationResults(
        items=[_item(index) for index in range(1, count + 1)],
        config={"eval_pack": _pack(final_stage_name)},
    )
    return annotate_results_with_stage_identity(results, _pack(final_stage_name))


def test_frame_a_headline_denominator_is_scenario_level_not_stage_level():
    results = _results(40, "Semantic Alignment")

    headline = build_headline_summary(results)
    report = generate_summary_report(results)

    assert headline["headline_stage_name"] == "Semantic Alignment"
    assert headline["scenario_level_items"] == 40
    assert headline["substantive_denominator"] == 40
    assert "Scenarios scored: 40" in report
    assert "Stage-level denominators count scorer-stage outputs, not scenarios." in report


def test_frame_b_headline_denominator_is_scenario_level_not_stage_level():
    results = _results(7, "Business Compliance Judge")

    headline = build_headline_summary(results)
    report = generate_summary_report(results)

    assert headline["headline_stage_name"] == "Business Compliance Judge"
    assert headline["scenario_level_items"] == 7
    assert headline["substantive_denominator"] == 7
    assert "Scenarios scored: 7" in report


def test_csv_export_preserves_duplicate_llm_judge_stage_outputs():
    results = _results(1)

    csv_text = results_to_csv(results)
    row = next(csv.DictReader(io.StringIO(csv_text)))

    assert row["stage_01_signal_extractor__scorer_name"] == "llm_judge"
    assert row["stage_02_semantic_alignment__scorer_name"] == "llm_judge"
    assert row["stage_01_signal_extractor__score"] == "0.75"
    assert row["stage_02_semantic_alignment__score"] == "1.0"


def test_stage_identity_maps_lake_merritt_llm_judge_display_name():
    pack_data = {
        "name": "Synthetic FDL Pack",
        "pipeline": [
            {"name": "Signal Extractor", "scorer": "llm_judge", "config": {}},
            {"name": "Conflict Immunity", "scorer": "conflict_immunity", "config": {}},
            {"name": "Semantic Alignment", "scorer": "llm_judge", "config": {}},
        ],
    }
    results = EvaluationResults(
        items=[
            EvaluationItem(
                id="display-name",
                input="input",
                output="output",
                expected_output="expected",
                scores=[
                    ScorerResult(
                        scorer_name="LLM Judge",
                        score=0.75,
                        numeric_score=0.75,
                        passed=True,
                        reasoning="signals extracted",
                    ),
                    ScorerResult(
                        scorer_name="conflict_immunity",
                        score=1.0,
                        numeric_score=1.0,
                        passed=True,
                        reasoning="not applicable",
                        details={"applicable": False, "status": "N/A", "substantive": False},
                    ),
                    ScorerResult(
                        scorer_name="LLM Judge",
                        score=0.9,
                        numeric_score=0.9,
                        passed=True,
                        reasoning="headline judge",
                    ),
                ],
            )
        ],
        config={"eval_pack": pack_data},
    )
    annotate_results_with_stage_identity(results, pack_data)

    payload = json.loads(results_to_json(results))
    headline = build_headline_summary(results)
    csv_row = next(csv.DictReader(io.StringIO(results_to_csv(results))))

    scores = payload["items"][0]["scores"]
    assert scores[0]["stage_id"] == "stage_01_signal_extractor"
    assert scores[0]["stage_scorer"] == "llm_judge"
    assert scores[2]["stage_id"] == "stage_03_semantic_alignment"
    assert scores[2]["stage_scorer"] == "llm_judge"
    assert headline["substantive_denominator"] == 1
    assert headline["missing_outputs"] == 0
    assert headline["passed"] == 1
    assert csv_row["stage_01_signal_extractor__scorer_name"] == "LLM Judge"
    assert csv_row["stage_03_semantic_alignment__scorer_name"] == "LLM Judge"
    assert "unmapped_01_llm_judge__score" not in csv_row


def test_json_export_preserves_stage_identity_and_applicability_fields():
    results = _results(1)

    payload = json.loads(results_to_json(results))
    scores = payload["items"][0]["scores"]

    assert scores[0]["stage_id"] == "stage_01_signal_extractor"
    assert scores[0]["stage_name"] == "Signal Extractor"
    assert scores[1]["stage_id"] == "stage_02_semantic_alignment"
    assert scores[1]["stage_name"] == "Semantic Alignment"
    assert scores[2]["stage_id"] == "stage_03_conflict_immunity"
    assert scores[2]["applicable"] is False
    assert scores[2]["status"] == "N/A"
    assert scores[2]["substantive"] is False


def test_csv_export_marks_inapplicable_rows_as_not_substantive():
    results = _results(1)

    row = next(csv.DictReader(io.StringIO(results_to_csv(results))))

    assert row["stage_03_conflict_immunity__applicable"] == "false"
    assert row["stage_03_conflict_immunity__status"] == "N/A"
    assert row["stage_03_conflict_immunity__substantive"] == "false"
    assert row["stage_03_conflict_immunity__passed"] == "true"


def test_status_only_na_exports_as_not_applicable():
    results = EvaluationResults(
        items=[
            EvaluationItem(
                id="status-only-na",
                input="input",
                output="output",
                expected_output="expected",
                scores=[
                    ScorerResult(
                        scorer_name="llm_judge",
                        score=1.0,
                        numeric_score=1.0,
                        passed=True,
                        details={"status": "N/A"},
                    ),
                    ScorerResult(
                        scorer_name="llm_judge",
                        score=1.0,
                        numeric_score=1.0,
                        passed=True,
                    ),
                ],
            )
        ],
        config={"eval_pack": _pack()},
    )
    annotate_results_with_stage_identity(results, _pack())

    csv_row = next(csv.DictReader(io.StringIO(results_to_csv(results))))
    payload = json.loads(results_to_json(results))

    assert csv_row["stage_01_signal_extractor__status"] == "N/A"
    assert csv_row["stage_01_signal_extractor__applicable"] == "false"
    assert csv_row["stage_01_signal_extractor__substantive"] == "false"
    assert payload["items"][0]["scores"][0]["status"] == "N/A"
    assert payload["items"][0]["scores"][0]["applicable"] is False
    assert payload["items"][0]["scores"][0]["substantive"] is False


def test_missing_headline_stage_output_is_counted_as_error():
    results = EvaluationResults(
        items=[
            EvaluationItem(
                id="missing-headline",
                input="input",
                output="output",
                expected_output="expected",
                scores=[
                    ScorerResult(
                        scorer_name="llm_judge",
                        score=0.75,
                        numeric_score=0.75,
                        passed=True,
                    )
                ],
            )
        ],
        config={"eval_pack": _pack()},
    )
    annotate_results_with_stage_identity(results, _pack())

    headline = build_headline_summary(results)
    csv_row = next(csv.DictReader(io.StringIO(results_to_csv(results))))
    report = generate_summary_report(results)

    assert headline["headline_stage_id"] == "stage_02_semantic_alignment"
    assert headline["scenario_level_items"] == 1
    assert headline["substantive_denominator"] == 0
    assert headline["errors"] == 1
    assert headline["missing_outputs"] == 1
    assert headline["failures"][0]["id"] == "missing-headline"
    assert csv_row["stage_02_semantic_alignment__score"] == ""
    assert "Missing headline outputs: 1" in report


def test_headline_failure_list_deduplicates_by_scenario_id():
    item = _item(1, final_passed=False, final_score=0.2)
    results = EvaluationResults(items=[item], config={"eval_pack": _pack()})
    annotate_results_with_stage_identity(results, _pack())

    duplicate_failure = ScorerResult(
        scorer_name="llm_judge",
        score=0.1,
        numeric_score=0.1,
        passed=False,
        reasoning="duplicate failed headline score",
        details={
            "stage_id": "stage_02_semantic_alignment",
            "stage_name": "Semantic Alignment",
            "stage_index": 2,
            "applicable": True,
            "status": "FAIL",
            "substantive": True,
        },
    )
    item.scores.append(duplicate_failure)

    failures = headline_failure_items(results, "stage_02_semantic_alignment")

    assert len(failures) == 1
    assert failures[0]["id"] == "case-001"
