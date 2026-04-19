# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Stanford Loyal Agents Initiative / Civics.com

from __future__ import annotations

import json
import math
from typing import Any, Dict, Iterable, Mapping, Optional

from core.data_models import ScorerResult


def parse_signal_string(raw: str) -> Dict[str, Any]:
    """Parse semicolon-delimited key=value signal strings or JSON objects."""
    text = raw.strip()
    if not text:
        return {}

    if text.startswith("{") and text.endswith("}"):
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, dict):
            return _coerce_signal_mapping(parsed)

    signals: Dict[str, Any] = {}
    for pair in text.split(";"):
        if "=" not in pair:
            continue
        key, value = pair.split("=", 1)
        signals[key.strip()] = _coerce_scalar(value.strip())
    return signals


def extract_observable_signals(
    metadata: Optional[Mapping[str, Any]],
    applicability_keys: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    """Extract real observable signals without fabricating them from CSV flags."""
    md = dict(metadata or {})
    nested = _coerce_json_object(md.get("metadata"))

    direct = _coerce_signal_payload(md.get("observable_signals"))
    if direct:
        source = "metadata.observable_signals"
        signals = direct
    else:
        nested_signals = _coerce_signal_payload(nested.get("observable_signals") if nested else None)
        if nested_signals:
            source = "metadata.metadata.observable_signals"
            signals = nested_signals
        else:
            source = "none"
            signals = {}

    flags: Dict[str, Any] = {}
    for key in applicability_keys or ():
        if key in md:
            flags[key] = _coerce_scalar(md[key])
        elif nested and key in nested:
            flags[key] = _coerce_scalar(nested[key])

    return {
        "signals": signals,
        "signal_source": source,
        "applicability_flags": flags,
        "metadata_payload_found": bool(nested),
    }


def signal_details(extracted: Mapping[str, Any], applicable: bool) -> Dict[str, Any]:
    status = "APPLICABLE" if applicable else "N/A"
    return {
        "applicable": applicable,
        "status": status,
        "substantive": applicable,
        "signal_source": extracted.get("signal_source", "none"),
        "applicability_flags": dict(extracted.get("applicability_flags") or {}),
    }


def inapplicable_result(
    scorer_name: str,
    reasoning: str,
    extracted: Mapping[str, Any],
    extra_details: Optional[Mapping[str, Any]] = None,
) -> ScorerResult:
    details = signal_details(extracted, applicable=False)
    if extra_details:
        details.update(dict(extra_details))
    return ScorerResult(
        scorer_name=scorer_name,
        score=1.0,
        passed=True,
        reasoning=reasoning,
        details=details,
    )


def outcome_details(
    extracted: Mapping[str, Any],
    passed: bool,
    extra_details: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    details = signal_details(extracted, applicable=True)
    details["status"] = "PASS" if passed else "FAIL"
    if extra_details:
        details.update(dict(extra_details))
    return details


def _coerce_signal_payload(value: Any) -> Dict[str, Any]:
    if _missing(value):
        return {}
    if isinstance(value, dict):
        return _coerce_signal_mapping(value)
    if isinstance(value, str):
        return parse_signal_string(value)
    return {}


def _coerce_signal_mapping(value: Mapping[str, Any]) -> Dict[str, Any]:
    return {str(key): _coerce_signal_value(signal_value) for key, signal_value in value.items()}


def _coerce_signal_value(value: Any) -> Any:
    if isinstance(value, dict):
        return _coerce_signal_mapping(value)
    if isinstance(value, list):
        return [_coerce_signal_value(item) for item in value]
    return _coerce_scalar(value)


def _coerce_json_object(value: Any) -> Dict[str, Any]:
    if _missing(value):
        return {}
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return {}
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _coerce_scalar(value: Any) -> Any:
    if _missing(value):
        return None
    if isinstance(value, str):
        text = value.strip()
        lowered = text.lower()
        if lowered in {"true", "false"}:
            return lowered == "true"
        if lowered in {"none", "null", "nan", ""}:
            return None
        try:
            return int(text)
        except ValueError:
            pass
        try:
            return float(text)
        except ValueError:
            return text
    return value


def _missing(value: Any) -> bool:
    if value is None:
        return True
    try:
        return bool(math.isnan(value))
    except (TypeError, ValueError):
        return False
    return False
