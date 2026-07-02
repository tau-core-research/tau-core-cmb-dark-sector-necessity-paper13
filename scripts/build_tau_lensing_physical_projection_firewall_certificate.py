#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "data/derived/cmb_tau_lensing_physical_projection_operator_packet_v01.csv"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_physical_projection_firewall_certificate_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_physical_projection_firewall_certificate_v01.md"

FORBIDDEN_MARKERS = [
    "ACT residual",
    "Planck residual",
    "reduced chi2",
    "score output",
    "post-score alpha",
    "alpha_star",
    "dark-sector verdict",
    "dark sector verdict",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def build_report(packet_path: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = [{"name": "packet_exists", "passes": packet_path.exists(), "detail": rel(packet_path)}]
    if not packet_path.exists():
        return finalize(checks, packet_path, [])
    rows = read_rows(packet_path)
    inspected_rows = [
        {
            "component_id": row.get("component_id", ""),
            "current_status": row.get("current_status", ""),
            "accepted_value": row.get("accepted_value", ""),
        }
        for row in rows
    ]
    inspected = json.dumps(inspected_rows, sort_keys=True)
    forbidden = [marker for marker in FORBIDDEN_MARKERS if marker.lower() in inspected.lower()]
    numeric_populated_rows = []
    for row in rows:
        value = str(row.get("accepted_value", "")).strip()
        if not value:
            continue
        if any(ch.isdigit() for ch in value) and row.get("component_id") not in {"projection_codomain"}:
            numeric_populated_rows.append(row.get("component_id"))
    checks.append({"name": "forbidden_endpoint_markers_absent", "passes": not forbidden, "detail": forbidden})
    checks.append(
        {
            "name": "no_endpoint_like_numeric_projection_values_populated",
            "passes": not numeric_populated_rows,
            "detail": numeric_populated_rows,
        }
    )
    return finalize(checks, packet_path, rows)


def finalize(checks: list[dict[str, Any]], packet_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    passed = all(check.get("passes") is True for check in checks)
    return {
        "report_id": "cmb_tau_lensing_physical_projection_firewall_certificate_v01",
        "claim_boundary": "projection_firewall_certificate_for_current_packet_only_no_operator_no_score_no_dark_sector_verdict",
        "packet": rel(packet_path),
        "firewall_certificate_status": (
            "PASS_FOR_CURRENT_SKELETON_ONLY" if passed else "BLOCKED_FORBIDDEN_ENDPOINT_CONTENT_FOUND"
        ),
        "checks": checks,
        "rows_inspected": len(rows),
        "certificate_scope": (
            "This certifies only the current physical projection operator packet contents. "
            "It must be rerun after any projection operator, normalization, or replay value is populated."
        ),
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    checks = "\n".join(f"- `{row['name']}`: {row['passes']}" for row in report["checks"])
    text = f"""# CMB Tau Lensing Physical Projection Firewall Certificate v01

**Doc class:** endpoint firewall certificate
**Reader role:** Paper 13 Tau-grid implementer
**Status:** current-packet firewall certificate only
**Canonical parent:** `docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Status

```text
{report["firewall_certificate_status"]}
```

This certificate covers only the current physical projection operator packet:

```text
{report["packet"]}
```

It must be rerun after any projection operator, normalization, or replay value
is populated.

## Checks

{checks}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build firewall certificate for the physical projection operator packet.")
    parser.add_argument("--packet", default=str(DEFAULT_PACKET))
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report(Path(args.packet).resolve())
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    if args.write_doc:
        write_doc(report, Path(args.write_doc))
    print(text)


if __name__ == "__main__":
    main()
