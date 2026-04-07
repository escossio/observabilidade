from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class TraceSample:
    run_id: str
    sample_id: str
    target: str
    target_slug: str
    mode: str
    dry_run: bool
    source_path: str
    hops: list[dict[str, Any]]
    report_path: str | None = None
    execution: dict[str, Any] | None = None
    map_metadata: dict[str, Any] | None = None
    batch_execution: dict[str, Any] | None = None


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _read_text(path: Path) -> str:
    return path.read_text(errors="ignore")


def _extract_target_from_report(report_path: Path) -> str | None:
    if not report_path.exists():
        return None
    first = report_path.read_text(errors="ignore").splitlines()[:3]
    for line in first:
        if line.startswith("# MTR Hop Map - "):
            return line.removeprefix("# MTR Hop Map - ").strip()
    return None


def _target_from_sample_dir(sample_dir: Path) -> str:
    execution = sample_dir / "execution.json"
    if execution.exists():
        data = _read_json(execution)
        target = data.get("target")
        if target:
            return str(target)
    map_metadata = sample_dir / "map_metadata.json"
    if map_metadata.exists():
        data = _read_json(map_metadata)
        target = data.get("target")
        if target:
            return str(target)
    report_target = _extract_target_from_report(sample_dir / "report.md")
    if report_target:
        return report_target
    return sample_dir.name


def _sample_paths(runs_root: Path) -> Iterable[Path]:
    for path in sorted(runs_root.rglob("mtr_normalized.json")):
        yield path


def _sample_metadata(sample_dir: Path) -> tuple[str, str, str, bool, dict[str, Any] | None, dict[str, Any] | None, dict[str, Any] | None]:
    run_id = sample_dir.name
    if sample_dir.parent.name == "targets":
        run_id = sample_dir.parent.parent.name

    execution_path = sample_dir / "execution.json"
    execution = _read_json(execution_path) if execution_path.exists() else None
    map_metadata_path = sample_dir / "map_metadata.json"
    map_metadata = _read_json(map_metadata_path) if map_metadata_path.exists() else None
    batch_execution_path = sample_dir.parent / "batch_execution.json"
    batch_execution = _read_json(batch_execution_path) if batch_execution_path.exists() else None

    target = _target_from_sample_dir(sample_dir)
    if execution and execution.get("target"):
        target = str(execution["target"])
    elif map_metadata and map_metadata.get("target"):
        target = str(map_metadata["target"])

    target_slug = sample_dir.name
    if execution and execution.get("target_slug"):
        target_slug = str(execution["target_slug"])
    elif map_metadata and map_metadata.get("target_slug"):
        target_slug = str(map_metadata["target_slug"])

    mode = "live"
    if execution and execution.get("mtr_source_kind"):
        mode = str(execution["mtr_source_kind"])
    elif map_metadata and map_metadata.get("mode"):
        mode = str(map_metadata["mode"])
    elif batch_execution and batch_execution.get("dry_run") is not None:
        mode = "live"

    dry_run = bool((execution or {}).get("dry_run", False) or (map_metadata or {}).get("dry_run", False) or bool(batch_execution and batch_execution.get("dry_run")))
    return run_id, target, target_slug, mode, dry_run, execution, map_metadata, batch_execution


def load_samples(runs_root: Path) -> list[TraceSample]:
    samples: list[TraceSample] = []
    for normalized_path in _sample_paths(runs_root):
        sample_dir = normalized_path.parent
        hops = _read_json(normalized_path)
        run_id, target, target_slug, mode, dry_run, execution, map_metadata, batch_execution = _sample_metadata(sample_dir)
        samples.append(
            TraceSample(
                run_id=run_id,
                sample_id=sample_dir.name,
                target=target,
                target_slug=target_slug,
                mode=mode,
                dry_run=dry_run,
                source_path=str(normalized_path),
                hops=hops,
                report_path=str(sample_dir / "report.md") if (sample_dir / "report.md").exists() else None,
                execution=execution,
                map_metadata=map_metadata,
                batch_execution=batch_execution,
            )
        )
    return samples
