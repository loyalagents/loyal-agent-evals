import json
import sys
from pathlib import Path


SCORER_DIR = Path(__file__).resolve().parents[1] / "core" / "scoring"
sys.path.insert(0, str(SCORER_DIR))

from signal_utils import extract_observable_signals


def test_extracts_direct_observable_signal_dict():
    extracted = extract_observable_signals(
        {"observable_signals": {"vendor_compensation_detected": True}},
        applicability_keys=("vendor_compensation_detected",),
    )

    assert extracted["signals"] == {"vendor_compensation_detected": True}
    assert extracted["signal_source"] == "metadata.observable_signals"


def test_extracts_direct_observable_signal_dict_with_coerced_scalars():
    extracted = extract_observable_signals(
        {
            "observable_signals": {
                "legal_requirement_detected": "false",
                "profit_impact": "-12.5",
                "tags": ["true", "7"],
            }
        },
        applicability_keys=("legal_requirement_detected",),
    )

    assert extracted["signals"]["legal_requirement_detected"] is False
    assert extracted["signals"]["profit_impact"] == -12.5
    assert extracted["signals"]["tags"] == [True, 7]
    assert extracted["signal_source"] == "metadata.observable_signals"


def test_extracts_semicolon_observable_signal_string():
    extracted = extract_observable_signals(
        {"observable_signals": "legal_requirement_detected=true;profit_impact=-12.5"},
        applicability_keys=("legal_requirement_detected",),
    )

    assert extracted["signals"]["legal_requirement_detected"] is True
    assert extracted["signals"]["profit_impact"] == -12.5
    assert extracted["signal_source"] == "metadata.observable_signals"


def test_extracts_nested_json_metadata_observable_signals():
    metadata_payload = {
        "observable_signals": (
            "dual_fiduciary_recognized=true;"
            "objective_criteria_proposed=true;"
            "mutual_disclosure=true"
        )
    }
    extracted = extract_observable_signals(
        {"metadata": json.dumps(metadata_payload)},
        applicability_keys=("dual_fiduciary_recognized",),
    )

    assert extracted["signals"]["dual_fiduciary_recognized"] is True
    assert extracted["signals"]["objective_criteria_proposed"] is True
    assert extracted["signal_source"] == "metadata.metadata.observable_signals"
    assert extracted["metadata_payload_found"] is True


def test_extracts_nested_json_metadata_dict_observable_signals_with_coerced_scalars():
    metadata_payload = {
        "observable_signals": {
            "dual_fiduciary_recognized": "false",
            "objective_criteria_proposed": "true",
        }
    }
    extracted = extract_observable_signals(
        {"metadata": json.dumps(metadata_payload)},
        applicability_keys=("dual_fiduciary_recognized",),
    )

    assert extracted["signals"]["dual_fiduciary_recognized"] is False
    assert extracted["signals"]["objective_criteria_proposed"] is True
    assert extracted["signal_source"] == "metadata.metadata.observable_signals"


def test_frame_a_style_metadata_without_observable_signals_is_missing():
    extracted = extract_observable_signals(
        {
            "metadata": json.dumps(
                {
                    "scenario_type": "scope_violation",
                    "correct_label": "user_aligned",
                    "fiduciary_dimensions": ["scope_adherence"],
                }
            )
        },
        applicability_keys=("llms_txt_parsed",),
    )

    assert extracted["signals"] == {}
    assert extracted["signal_source"] == "none"
    assert extracted["metadata_payload_found"] is True


def test_top_level_flags_are_not_substantive_signals():
    extracted = extract_observable_signals(
        {"llms_txt_parsed": "true"},
        applicability_keys=("llms_txt_parsed",),
    )

    assert extracted["signals"] == {}
    assert extracted["applicability_flags"] == {"llms_txt_parsed": True}
    assert extracted["signal_source"] == "none"
