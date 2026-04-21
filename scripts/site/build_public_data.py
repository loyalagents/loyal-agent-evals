#!/usr/bin/env python3
"""Build public, leak-guarded data projections for the static website."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
RUN_ROOT = REPO_ROOT / "reports" / "final-rerun-20260419T065448Z"
DATA_DIR = REPO_ROOT / "assets" / "data"
HARD_LEAK_RE = re.compile(r"/Users/|Dropbox|file://|/tmp/\w")

FRAME_FILES = {
    "frame_a": RUN_ROOT / "frame_a" / "eval_results_20260418_235811.json",
    "frame_b": RUN_ROOT / "frame_b" / "eval_results_20260418_235858.json",
}

SCORER_DUTIES = {
    "conflict_immunity": "Loyalty",
    "ueta_compliance": "Confirmation / UETA",
    "llms_respect": "Obedience / ToS",
    "compliance_first": "Compliance first",
    "dual_fiduciary": "Dual fiduciary",
    "llm_judge": "Holistic alignment",
    "LLM Judge": "Holistic alignment",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def truncate(value: Any, limit: int = 520) -> str | None:
    if value is None:
        return None
    text = str(value).replace("\r\n", "\n").strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def hard_leak_guard(path: Path) -> None:
    text = path.read_text(errors="replace")
    hits = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if HARD_LEAK_RE.search(line):
            hits.append(f"{path.relative_to(REPO_ROOT)}:{line_no}: {line[:180]}")
    if hits:
        raise SystemExit("Hard-leak hits in generated data:\n  " + "\n  ".join(hits))


def projected_outputs(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    projected: list[dict[str, Any]] = []
    for out in manifest.get("outputs", []):
        baseline = out.get("baseline_compared")
        projected.append(
            {
                "frame": out.get("frame"),
                "eval_pack": out.get("eval_pack"),
                "artifact_type": out.get("artifact_type"),
                "artifact_role": out.get("artifact_role"),
                "baseline_compared_relpath": baseline,
                "sha256": out.get("sha256"),
            }
        )
    return projected


def project_score(score: dict[str, Any], item_id: str) -> dict[str, Any]:
    status = score.get("status") or score.get("details", {}).get("status")
    applicable = score.get("applicable")
    if applicable is None:
        applicable = score.get("details", {}).get("applicable", True)
    substantive = score.get("substantive")
    if substantive is None:
        substantive = score.get("details", {}).get("substantive", applicable)
    if applicable and status != "N/A" and score.get("score") is None:
        raise SystemExit(f"Null canonical score for applicable row: {item_id} / {score.get('stage_id')}")

    details = score.get("details") or {}
    return {
        "scorer_name": score.get("scorer_name"),
        "stage_id": score.get("stage_id"),
        "stage_name": score.get("stage_name"),
        "stage_index": score.get("stage_index"),
        "pipeline_stage": score.get("pipeline_stage"),
        "stage_scorer": score.get("stage_scorer"),
        "score": score.get("score"),
        "numeric_score": score.get("numeric_score"),
        "score_type": score.get("score_type"),
        "passed": score.get("passed"),
        "applicable": bool(applicable),
        "status": status,
        "substantive": bool(substantive),
        "reasoning": truncate(score.get("reasoning"), 360),
        "details": {
            "status": details.get("status", status),
            "applicable": details.get("applicable", applicable),
            "substantive": details.get("substantive", substantive),
        },
    }


def duty_for_score(score: dict[str, Any]) -> str:
    return (
        SCORER_DUTIES.get(str(score.get("stage_scorer")))
        or SCORER_DUTIES.get(str(score.get("scorer_name")))
        or SCORER_DUTIES.get(str(score.get("stage_name")))
        or "Other"
    )


def build_duty_rollup(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rollup: dict[str, dict[str, Any]] = {}
    for item in items:
        for score in item.get("scores", []):
            duty = duty_for_score(score)
            bucket = rollup.setdefault(
                duty,
                {"duty": duty, "passed": 0, "failed": 0, "not_applicable": 0, "applicable": 0, "total": 0},
            )
            bucket["total"] += 1
            if score.get("status") == "N/A" or not score.get("applicable", True):
                bucket["not_applicable"] += 1
            else:
                bucket["applicable"] += 1
                if score.get("status") == "PASS" or score.get("passed") is True:
                    bucket["passed"] += 1
                elif score.get("status") == "FAIL" or score.get("passed") is False:
                    bucket["failed"] += 1
    return sorted(rollup.values(), key=lambda row: row["duty"])


def project_frame(frame: str, path: Path) -> dict[str, Any]:
    data = read_json(path)
    items = []
    for item in data["items"]:
        items.append(
            {
                "id": item["id"],
                "input": truncate(item.get("input"), 520),
                "output": truncate(item.get("output"), 760),
                "scores": [project_score(score, item["id"]) for score in item.get("scores", [])],
            }
        )
    return {
        "frame": frame,
        "artifact_role": "public-projection",
        "source_artifact_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "headline_summary": data["headline_summary"],
        "stage_summary": data["stage_summary"],
        "duty_rollup": build_duty_rollup(items),
        "items": items,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    hard_leak_guard(path)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    manifest = read_json(RUN_ROOT / "manifest.json")

    site_data = {
        "manifest_version": manifest.get("manifest_version"),
        "artifact_role": "public-site-summary",
        "generated_utc": manifest.get("generated_utc"),
        "headline_results": manifest.get("headline_results"),
        "phase7_checks": manifest.get("phase7_checks"),
        "outputs": projected_outputs(manifest),
    }
    write_json(DATA_DIR / "site_data.v1.json", site_data)

    for frame, path in FRAME_FILES.items():
        write_json(DATA_DIR / f"{frame}.v1.json", project_frame(frame, path))

    print("Wrote public data projections:")
    for name in ("site_data.v1.json", "frame_a.v1.json", "frame_b.v1.json"):
        print(f"  assets/data/{name}")


if __name__ == "__main__":
    main()
