import csv
import io
import json
import sys
from pathlib import Path

from core.data_models import EvaluationItem, EvaluationResults

from fdl_eval.reporting import build_stage_summary, results_to_csv, results_to_json
from fdl_eval.stage_identity import annotate_results_with_stage_identity


SCORER_DIR = Path(__file__).resolve().parents[1] / "core" / "scoring"
sys.path.insert(0, str(SCORER_DIR))

from compliance_first_scorer import ComplianceFirstScorer
from dual_fiduciary_scorer import DualFiduciaryScorer
from llms_respect_scorer import LLMSRespectScorer


GATE3_PACK = {
    "name": "Gate 3 Negative Sanity Probe",
    "pipeline": [
        {"name": "LLMS.txt Respect", "scorer": "llms_respect", "config": {}},
        {"name": "Compliance First", "scorer": "compliance_first", "config": {}},
        {"name": "Dual Fiduciary", "scorer": "dual_fiduciary", "config": {}},
    ],
}


def _item(observable_signals):
    return EvaluationItem(
        id="gate3-negative-probe",
        input="input",
        output="output",
        expected_output="expected",
        metadata={"observable_signals": observable_signals},
    )


def _llms_respect_failure():
    return LLMSRespectScorer().score(
        _item(
            "llms_txt_parsed=false;"
            "tos_restriction_detected=true;"
            "lawful_alt_used=false"
        ),
        {},
    )


def _compliance_first_failure():
    return ComplianceFirstScorer().score(
        _item(
            "legal_requirement_detected=true;"
            "compliance_prevailed=false;"
            "policy_override=false"
        ),
        {},
    )


def _dual_fiduciary_failure():
    return DualFiduciaryScorer().score(
        _item(
            "dual_fiduciary_recognized=true;"
            "objective_criteria_proposed=false;"
            "mutual_disclosure=true;"
            "narrow_agreement=true"
        ),
        {},
    )


def test_gate3_llms_respect_fail_trigger_surfaces_failure():
    result = _llms_respect_failure()

    assert result.passed is False
    assert result.details["applicable"] is True
    assert result.details["status"] == "FAIL"


def test_gate3_compliance_first_fail_trigger_surfaces_failure():
    result = _compliance_first_failure()

    assert result.passed is False
    assert result.details["applicable"] is True
    assert result.details["status"] == "FAIL"


def test_gate3_dual_fiduciary_fail_trigger_surfaces_failure():
    result = _dual_fiduciary_failure()

    assert result.passed is False
    assert result.details["applicable"] is True
    assert result.details["status"] == "FAIL"


def test_gate3_failures_surface_in_machine_readable_and_reportable_outputs():
    results = EvaluationResults(
        items=[
            EvaluationItem(
                id="gate3-export-probe",
                input="input",
                output="output",
                expected_output="expected",
                scores=[
                    _llms_respect_failure(),
                    _compliance_first_failure(),
                    _dual_fiduciary_failure(),
                ],
            )
        ],
        config={"eval_pack": GATE3_PACK},
    )
    annotate_results_with_stage_identity(results, GATE3_PACK)

    payload = json.loads(results_to_json(results))
    csv_row = next(csv.DictReader(io.StringIO(results_to_csv(results))))
    stage_summary = {
        stage["stage_id"]: stage for stage in build_stage_summary(results)
    }

    exported_scores = {
        score["scorer_name"]: score for score in payload["items"][0]["scores"]
    }
    for scorer_name in ("llms_respect", "compliance_first", "dual_fiduciary"):
        assert exported_scores[scorer_name]["passed"] is False
        assert exported_scores[scorer_name]["applicable"] is True
        assert exported_scores[scorer_name]["status"] == "FAIL"

    for stage_id in (
        "stage_01_llms_txt_respect",
        "stage_02_compliance_first",
        "stage_03_dual_fiduciary",
    ):
        assert csv_row[f"{stage_id}__passed"] == "false"
        assert csv_row[f"{stage_id}__applicable"] == "true"
        assert csv_row[f"{stage_id}__status"] == "FAIL"
        assert stage_summary[stage_id]["failed"] == 1
        assert stage_summary[stage_id]["passed"] == 0
        assert stage_summary[stage_id]["not_applicable_outputs"] == 0
