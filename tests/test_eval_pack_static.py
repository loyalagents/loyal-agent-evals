from pathlib import Path

import yaml


EVAL_PACK_DIR = Path(__file__).resolve().parents[1] / "eval_packs"
TARGET_STAGES = {
    "fdl_frame_a_consumer.yaml": {"LLMS.txt Respect"},
    "fdl_frame_b_business.yaml": {"Compliance First", "Dual Fiduciary"},
}


def _load_pack(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_eval_pack_yaml_files_parse():
    for path in EVAL_PACK_DIR.glob("*.yaml"):
        data = _load_pack(path)
        assert isinstance(data, dict), f"{path.name} did not parse to a mapping"
        assert isinstance(data.get("pipeline"), list), f"{path.name} has no pipeline list"


def test_no_run_if_uses_metadata_get_calls():
    for path in EVAL_PACK_DIR.glob("*.yaml"):
        data = _load_pack(path)
        for stage in data.get("pipeline", []):
            run_if = stage.get("run_if")
            assert "metadata.get(" not in str(run_if or ""), (
                f"{path.name}:{stage.get('name')} uses metadata.get() in run_if"
            )


def test_specialized_stages_are_unconditional():
    for filename, stage_names in TARGET_STAGES.items():
        data = _load_pack(EVAL_PACK_DIR / filename)
        stages = {stage.get("name"): stage for stage in data.get("pipeline", [])}

        for stage_name in stage_names:
            assert stage_name in stages, f"{filename} is missing {stage_name}"
            assert "run_if" not in stages[stage_name], (
                f"{filename}:{stage_name} should self-gate in scorer code"
            )
