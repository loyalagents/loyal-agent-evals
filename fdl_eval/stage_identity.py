"""Stage identity helpers for Lake Merritt scorer results.

Lake Merritt currently stores scorer results by scorer name only. The FDL
eval packs use two ``llm_judge`` stages per item, so this module annotates the
post-run results with the configured pipeline stage identity before export.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class StageIdentity:
    """Stable identity for one configured pipeline stage."""

    stage_index: int
    stage_id: str
    stage_name: str
    scorer_name: str


def slugify(value: str) -> str:
    """Return a stable ASCII slug for artifact keys."""

    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "stage"


def _canonical_scorer_name(value: str) -> str:
    """Normalize configured scorer IDs and Lake Merritt display names."""

    return slugify(str(value))


def _get_value(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _pack_pipeline(pack_data: Any) -> Iterable[Any]:
    if pack_data is None:
        return []
    if hasattr(pack_data, "model_dump"):
        pack_data = pack_data.model_dump(mode="json")
    return _get_value(pack_data, "pipeline", []) or []


def build_stage_identities(pack_data: Any) -> List[StageIdentity]:
    """Build ordered stage identities from an eval-pack dict or model."""

    identities: List[StageIdentity] = []
    seen: Dict[str, int] = {}

    for zero_index, stage in enumerate(_pack_pipeline(pack_data)):
        stage_index = zero_index + 1
        stage_name = str(_get_value(stage, "name", f"Stage {stage_index}"))
        scorer_name = str(_get_value(stage, "scorer", "unknown_scorer"))
        base_id = f"stage_{stage_index:02d}_{slugify(stage_name)}"
        count = seen.get(base_id, 0) + 1
        seen[base_id] = count
        stage_id = base_id if count == 1 else f"{base_id}_{count}"
        identities.append(
            StageIdentity(
                stage_index=stage_index,
                stage_id=stage_id,
                stage_name=stage_name,
                scorer_name=scorer_name,
            )
        )

    return identities


def _coerce_bool(value: Any, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "y"}:
            return True
        if normalized in {"false", "0", "no", "n"}:
            return False
    return default


def ensure_score_details(
    score: Any,
    identity: Optional[StageIdentity] = None,
    score_index: Optional[int] = None,
) -> Dict[str, Any]:
    """Ensure one scorer result has explicit stage and applicability fields."""

    details = dict(getattr(score, "details", None) or {})

    if identity is None:
        index = score_index or int(details.get("score_index", 1) or 1)
        scorer_name = str(
            details.get("stage_scorer")
            or getattr(score, "scorer_name", details.get("scorer_name", "scorer"))
        )
        identity = StageIdentity(
            stage_index=int(details.get("stage_index", index) or index),
            stage_id=str(details.get("stage_id", f"score_{index:02d}_{slugify(scorer_name)}")),
            stage_name=str(details.get("stage_name", scorer_name)),
            scorer_name=scorer_name,
        )

    raw_status = details.get("status")
    if raw_status is not None:
        status = str(raw_status)
    elif getattr(score, "error", None):
        status = "ERROR"
    elif bool(getattr(score, "passed", False)):
        status = "PASS"
    else:
        status = "FAIL"

    raw_applicable = details.get("applicable")
    applicable_default = status.upper() != "N/A"
    applicable = _coerce_bool(raw_applicable, default=applicable_default)
    if not applicable:
        status = "N/A"

    raw_substantive = details.get("substantive")
    substantive = _coerce_bool(
        raw_substantive,
        default=(applicable and status.upper() != "N/A"),
    )

    details.update(
        {
            "stage_id": identity.stage_id,
            "stage_name": identity.stage_name,
            "stage_index": identity.stage_index,
            "pipeline_stage": identity.stage_index,
            "stage_scorer": identity.scorer_name,
            "applicable": applicable,
            "status": status,
            "substantive": substantive,
        }
    )
    score.details = details
    return details


def annotate_results_with_stage_identity(results: Any, pack_data: Any) -> Any:
    """Annotate every scorer result with the eval-pack pipeline stage identity."""

    stages = build_stage_identities(pack_data)
    results.metadata.setdefault(
        "stage_identity",
        [
            {
                "stage_index": stage.stage_index,
                "stage_id": stage.stage_id,
                "stage_name": stage.stage_name,
                "scorer_name": stage.scorer_name,
            }
            for stage in stages
        ],
    )

    for item in getattr(results, "items", []) or []:
        stage_cursor = 0
        for score_index, score in enumerate(getattr(item, "scores", []) or [], start=1):
            matched: Optional[StageIdentity] = None
            scorer_name = str(getattr(score, "scorer_name", ""))
            canonical_scorer = _canonical_scorer_name(scorer_name)

            for stage_pos in range(stage_cursor, len(stages)):
                if _canonical_scorer_name(stages[stage_pos].scorer_name) == canonical_scorer:
                    matched = stages[stage_pos]
                    stage_cursor = stage_pos + 1
                    break

            if matched is None:
                matched = StageIdentity(
                    stage_index=score_index,
                    stage_id=f"unmapped_{score_index:02d}_{slugify(scorer_name)}",
                    stage_name=f"Unmapped {scorer_name}",
                    scorer_name=scorer_name,
                )

            ensure_score_details(score, matched, score_index=score_index)

    return results
