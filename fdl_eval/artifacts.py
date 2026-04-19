"""Artifact path helpers for evaluation runs."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional


def resolve_output_dir(script_path: str, requested_output_dir: Optional[str] = None) -> Path:
    """Resolve and create the output directory for run artifacts."""

    if requested_output_dir:
        output_dir = Path(requested_output_dir).expanduser()
    else:
        output_dir = Path(script_path).resolve().parent / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def build_artifact_paths(output_dir: Path, timestamp: str) -> Dict[str, Path]:
    """Return the standard artifact paths for one eval run."""

    return {
        "json": output_dir / f"eval_results_{timestamp}.json",
        "csv": output_dir / f"eval_results_{timestamp}.csv",
        "markdown": output_dir / f"report_{timestamp}.md",
    }

