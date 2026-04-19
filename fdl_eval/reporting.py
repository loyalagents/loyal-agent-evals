"""Stage-aware reporting for Loyal Agent eval reruns."""

from __future__ import annotations

import copy
import csv
import io
import json
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from fdl_eval.stage_identity import ensure_score_details


HEADLINE_STAGE_NAMES = ("Semantic Alignment", "Business Compliance Judge")


def sanitize_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Remove obvious secrets before writing run configuration."""

    sanitized = copy.deepcopy(config)

    def scrub(value: Any) -> Any:
        if isinstance(value, dict):
            for key in list(value.keys()):
                lowered = str(key).lower()
                if "api_key" in lowered or "secret" in lowered:
                    value[key] = "***REDACTED***"
                else:
                    value[key] = scrub(value[key])
        elif isinstance(value, list):
            value = [scrub(item) for item in value]
        return value

    return scrub(sanitized)


def _item_id(item: Any, item_index: int) -> str:
    return str(getattr(item, "id", None) or f"item_{item_index}")


def _numeric_score(score: Any) -> Optional[float]:
    if getattr(score, "numeric_score", None) is not None:
        return float(score.numeric_score)
    raw_score = getattr(score, "score", None)
    if isinstance(raw_score, (int, float)):
        return float(raw_score)
    return None


def _format_csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    return str(value)


def iter_score_rows(results: Any) -> Iterable[Dict[str, Any]]:
    """Yield one normalized row per scorer-stage result."""

    for item_index, item in enumerate(getattr(results, "items", []) or [], start=1):
        for score_index, score in enumerate(getattr(item, "scores", []) or [], start=1):
            details = ensure_score_details(score, score_index=score_index)
            yield {
                "item_id": _item_id(item, item_index),
                "item": item,
                "score": score,
                "score_index": score_index,
                "stage_id": details["stage_id"],
                "stage_name": details["stage_name"],
                "stage_index": int(details["stage_index"]),
                "scorer_name": getattr(score, "scorer_name", ""),
                "raw_score": getattr(score, "score", None),
                "numeric_score": _numeric_score(score),
                "passed": bool(getattr(score, "passed", False)),
                "applicable": bool(details["applicable"]),
                "status": str(details["status"]),
                "substantive": bool(details["substantive"]),
                "reasoning": getattr(score, "reasoning", None),
                "error": getattr(score, "error", None),
                "details": details,
            }


def _expected_stage_summaries(results: Any) -> List[Dict[str, Any]]:
    summaries: List[Dict[str, Any]] = []
    for stage in (getattr(results, "metadata", {}) or {}).get("stage_identity", []) or []:
        if not isinstance(stage, dict):
            continue
        summaries.append(
            {
                "stage_id": stage.get("stage_id"),
                "stage_name": stage.get("stage_name"),
                "stage_index": int(stage.get("stage_index") or 0),
                "scorer_name": stage.get("scorer_name"),
                "stage_level_outputs": 0,
                "applicable_outputs": 0,
                "not_applicable_outputs": 0,
                "substantive_outputs": 0,
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "numeric_scores": [],
            }
        )
    return [summary for summary in summaries if summary["stage_id"]]


def build_stage_summary(results: Any) -> List[Dict[str, Any]]:
    """Return stage-level metrics with explicitly labeled denominators."""

    by_stage: Dict[str, Dict[str, Any]] = {}
    order: List[str] = []

    for summary in _expected_stage_summaries(results):
        stage_id = summary["stage_id"]
        by_stage[stage_id] = summary
        order.append(stage_id)

    for row in iter_score_rows(results):
        stage_id = row["stage_id"]
        if stage_id not in by_stage:
            by_stage[stage_id] = {
                "stage_id": stage_id,
                "stage_name": row["stage_name"],
                "stage_index": row["stage_index"],
                "scorer_name": row["scorer_name"],
                "stage_level_outputs": 0,
                "applicable_outputs": 0,
                "not_applicable_outputs": 0,
                "substantive_outputs": 0,
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "numeric_scores": [],
            }
            order.append(stage_id)

        stats = by_stage[stage_id]
        stats["stage_level_outputs"] += 1
        if row["applicable"]:
            stats["applicable_outputs"] += 1
        else:
            stats["not_applicable_outputs"] += 1
        if row["substantive"]:
            stats["substantive_outputs"] += 1
        if row["error"]:
            stats["errors"] += 1
        elif row["applicable"] and row["substantive"] and row["passed"]:
            stats["passed"] += 1
        elif row["applicable"] and row["substantive"] and not row["passed"]:
            stats["failed"] += 1
        if row["numeric_score"] is not None and row["applicable"] and row["substantive"]:
            stats["numeric_scores"].append(row["numeric_score"])

    summaries: List[Dict[str, Any]] = []
    for stage_id in order:
        stats = by_stage[stage_id]
        denominator = stats["passed"] + stats["failed"] + stats["errors"]
        scores = stats.pop("numeric_scores")
        stats["accuracy"] = stats["passed"] / denominator if denominator else None
        stats["average_score"] = sum(scores) / len(scores) if scores else None
        summaries.append(stats)

    return summaries


def find_headline_stage_id(results: Any) -> Optional[str]:
    """Pick the final semantic/compliance judge as scenario-level headline."""

    for stage_name in HEADLINE_STAGE_NAMES:
        for summary in _expected_stage_summaries(results):
            if summary["stage_name"] == stage_name:
                return summary["stage_id"]

    stage_summaries = build_stage_summary(results)
    for stage_name in HEADLINE_STAGE_NAMES:
        for summary in stage_summaries:
            if summary["stage_name"] == stage_name:
                return summary["stage_id"]

    llm_judges = [
        summary
        for summary in stage_summaries
        if summary["scorer_name"] == "llm_judge" and summary["stage_name"] != "Signal Extractor"
    ]
    if llm_judges:
        return sorted(llm_judges, key=lambda item: item["stage_index"])[-1]["stage_id"]
    return None


def build_headline_summary(results: Any, headline_stage_id: Optional[str] = None) -> Dict[str, Any]:
    """Return deduplicated scenario-level metrics for the headline judge."""

    headline_stage_id = headline_stage_id or find_headline_stage_id(results)
    if not headline_stage_id:
        return {
            "headline_stage_id": None,
            "headline_stage_name": None,
            "scenario_level_items": 0,
            "substantive_denominator": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "not_applicable": 0,
            "missing_outputs": 0,
            "pass_rate": None,
            "average_score": None,
            "failures": [],
        }

    grouped: Dict[str, List[Dict[str, Any]]] = {}
    stage_name: Optional[str] = None
    for row in iter_score_rows(results):
        if row["stage_id"] == headline_stage_id:
            grouped.setdefault(row["item_id"], []).append(row)
            stage_name = row["stage_name"]

    if stage_name is None:
        for summary in _expected_stage_summaries(results):
            if summary["stage_id"] == headline_stage_id:
                stage_name = summary["stage_name"]
                break

    item_ids = [
        _item_id(item, item_index)
        for item_index, item in enumerate(getattr(results, "items", []) or [], start=1)
    ]
    passed = failed = errors = not_applicable = substantive_denominator = 0
    missing_outputs = 0
    numeric_scores: List[float] = []
    failures: List[Dict[str, Any]] = []

    for item_id in item_ids:
        rows = grouped.get(item_id, [])
        if not rows:
            errors += 1
            missing_outputs += 1
            failures.append(
                {
                    "id": item_id,
                    "score": None,
                    "reasoning": f"Missing headline-stage output for {headline_stage_id}.",
                }
            )
            continue

        substantive_rows = [
            row for row in rows if row["applicable"] and row["substantive"]
        ]
        if not substantive_rows:
            not_applicable += 1
            continue

        substantive_denominator += 1
        numeric_scores.extend(
            row["numeric_score"] for row in substantive_rows if row["numeric_score"] is not None
        )
        if any(row["error"] for row in substantive_rows):
            errors += 1
        elif any(not row["passed"] for row in substantive_rows):
            failed += 1
            first_failure = next(row for row in substantive_rows if not row["passed"])
            failures.append(
                {
                    "id": item_id,
                    "score": first_failure["raw_score"],
                    "reasoning": first_failure["reasoning"],
                }
            )
        else:
            passed += 1

    rate_denominator = passed + failed + errors
    return {
        "headline_stage_id": headline_stage_id,
        "headline_stage_name": stage_name,
        "scenario_level_items": len(item_ids),
        "substantive_denominator": substantive_denominator,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "not_applicable": not_applicable,
        "missing_outputs": missing_outputs,
        "pass_rate": passed / rate_denominator if rate_denominator else None,
        "average_score": sum(numeric_scores) / len(numeric_scores) if numeric_scores else None,
        "failures": failures,
    }


def headline_failure_items(results: Any, headline_stage_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return scenario-level headline failures deduplicated by item id."""

    return build_headline_summary(results, headline_stage_id)["failures"]


def results_to_csv(results: Any) -> str:
    """Convert results to a wide CSV with stage-aware scorer columns."""

    items = getattr(results, "items", []) or []
    if not items:
        return ""

    metadata_keys = sorted(
        {
            key
            for item in items
            for key in (getattr(item, "metadata", None) or {}).keys()
        }
    )
    stage_summaries = build_stage_summary(results)
    stage_ids = [summary["stage_id"] for summary in stage_summaries]

    fieldnames = ["id", "input", "output", "expected_output"]
    fieldnames.extend(f"metadata_{key}" for key in metadata_keys)
    for stage_id in stage_ids:
        fieldnames.extend(
            [
                f"{stage_id}__stage_name",
                f"{stage_id}__scorer_name",
                f"{stage_id}__score",
                f"{stage_id}__numeric_score",
                f"{stage_id}__passed",
                f"{stage_id}__status",
                f"{stage_id}__applicable",
                f"{stage_id}__substantive",
                f"{stage_id}__reasoning",
                f"{stage_id}__error",
            ]
        )

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for item_index, item in enumerate(items, start=1):
        row: Dict[str, Any] = {
            "id": _item_id(item, item_index),
            "input": getattr(item, "input", ""),
            "output": getattr(item, "output", "") or "",
            "expected_output": getattr(item, "expected_output", "") or "",
        }
        metadata = getattr(item, "metadata", None) or {}
        for key in metadata_keys:
            row[f"metadata_{key}"] = metadata.get(key, "")

        for score_index, score in enumerate(getattr(item, "scores", []) or [], start=1):
            details = ensure_score_details(score, score_index=score_index)
            stage_id = details["stage_id"]
            row[f"{stage_id}__stage_name"] = details["stage_name"]
            row[f"{stage_id}__scorer_name"] = getattr(score, "scorer_name", "")
            row[f"{stage_id}__score"] = getattr(score, "score", None)
            row[f"{stage_id}__numeric_score"] = _numeric_score(score)
            row[f"{stage_id}__passed"] = bool(getattr(score, "passed", False))
            row[f"{stage_id}__status"] = details["status"]
            row[f"{stage_id}__applicable"] = bool(details["applicable"])
            row[f"{stage_id}__substantive"] = bool(details["substantive"])
            row[f"{stage_id}__reasoning"] = getattr(score, "reasoning", "") or ""
            row[f"{stage_id}__error"] = getattr(score, "error", "") or ""

        writer.writerow({key: _format_csv_value(row.get(key)) for key in fieldnames})

    return output.getvalue()


def _score_to_json(score: Any, score_index: int) -> Dict[str, Any]:
    details = ensure_score_details(score, score_index=score_index)
    if hasattr(score, "model_dump"):
        score_data = score.model_dump(mode="json")
    else:
        score_data = dict(score)
    score_data.update(
        {
            "stage_id": details["stage_id"],
            "stage_name": details["stage_name"],
            "stage_index": details["stage_index"],
            "pipeline_stage": details["pipeline_stage"],
            "stage_scorer": details["stage_scorer"],
            "applicable": bool(details["applicable"]),
            "status": details["status"],
            "substantive": bool(details["substantive"]),
        }
    )
    score_data["details"] = details
    return score_data


def results_to_json(results: Any) -> str:
    """Convert results to JSON while preserving every stage-scoped score."""

    items: List[Dict[str, Any]] = []
    for item_index, item in enumerate(getattr(results, "items", []) or [], start=1):
        item_data = {
            "id": _item_id(item, item_index),
            "input": getattr(item, "input", ""),
            "output": getattr(item, "output", None),
            "expected_output": getattr(item, "expected_output", None),
            "metadata": getattr(item, "metadata", None) or {},
            "scores": [
                _score_to_json(score, score_index)
                for score_index, score in enumerate(getattr(item, "scores", []) or [], start=1)
            ],
        }
        items.append(item_data)

    payload = {
        "items": items,
        "config": sanitize_config(getattr(results, "config", {}) or {}),
        "summary_stats": getattr(results, "summary_stats", {}) or {},
        "metadata": getattr(results, "metadata", {}) or {},
        "headline_summary": build_headline_summary(results),
        "stage_summary": build_stage_summary(results),
    }
    return json.dumps(payload, indent=2)


def _format_metric(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def generate_summary_report(results: Any) -> str:
    """Generate a Markdown report with scenario and stage metrics separated."""

    items = getattr(results, "items", []) or []
    if not items:
        return "# Evaluation Summary Report\n\nNo evaluation results to summarize."

    headline = build_headline_summary(results)
    stage_summary = build_stage_summary(results)
    lines: List[str] = []

    lines.append("# Evaluation Summary Report")
    lines.append("")
    lines.append(f"Generated UTC: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    lines.append("## Overview")
    lines.append("")
    lines.append(f"- Total scenarios evaluated: {len(items)}")
    lines.append(f"- Total scorer-stage outputs: {sum(stage['stage_level_outputs'] for stage in stage_summary)}")
    lines.append("")

    lines.append("## Scenario-Level Headline")
    lines.append("")
    lines.append(
        f"- Headline stage: {headline['headline_stage_name'] or 'N/A'} "
        f"({headline['headline_stage_id'] or 'N/A'})"
    )
    lines.append(f"- Scenarios scored: {headline['scenario_level_items']}")
    lines.append(
        f"- Substantive denominator: {headline['substantive_denominator']} "
        "(scenario-level; excludes N/A rows)"
    )
    lines.append(f"- Passed: {headline['passed']}")
    lines.append(f"- Failed: {headline['failed']}")
    lines.append(f"- Errors: {headline['errors']}")
    lines.append(f"- N/A: {headline['not_applicable']}")
    lines.append(f"- Missing headline outputs: {headline['missing_outputs']}")
    lines.append(f"- Pass rate: {_format_metric(headline['pass_rate'])}")
    lines.append(f"- Average score: {_format_metric(headline['average_score'])}")
    lines.append("")

    lines.append("## Stage-Level Metrics")
    lines.append("")
    lines.append("Stage-level denominators count scorer-stage outputs, not scenarios.")
    lines.append("")
    lines.append(
        "| Stage | Scorer | Stage-level outputs | Applicable | N/A | Passed | Failed | Errors | Average score |"
    )
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for stage in stage_summary:
        display_stage = dict(stage)
        display_stage["average_score"] = _format_metric(stage["average_score"])
        lines.append(
            "| {stage_name} | {scorer_name} | {stage_level_outputs} | "
            "{applicable_outputs} | {not_applicable_outputs} | {passed} | {failed} | "
            "{errors} | {average_score} |".format(**display_stage)
        )
    lines.append("")

    lines.append("## Headline Failures")
    lines.append("")
    failures = headline["failures"]
    if not failures:
        lines.append("No scenario-level headline failures detected.")
    else:
        lines.append("Scenario-level failures are deduplicated by scenario ID.")
        for failure in failures[:10]:
            reason = failure.get("reasoning") or ""
            reason = reason[:160] + ("..." if len(reason) > 160 else "")
            lines.append(f"- {failure['id']}: score={failure.get('score')} {reason}")
        if len(failures) > 10:
            lines.append(f"- ... and {len(failures) - 10} more failures")
    lines.append("")

    lines.append("## Configuration")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(sanitize_config(getattr(results, "config", {}) or {}), indent=2))
    lines.append("```")
    lines.append("")

    return "\n".join(lines)
