#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data/derived/cmb_tau_lensing_physical_projection_operator_packet_v01.csv"
SCAFFOLD = ROOT / "docs/cmb_tau_lensing_projection_operator_formula_spec_scaffold_v01.md"
ACCEPTANCE_MATRIX = ROOT / "docs/cmb_tau_lensing_projection_formula_spec_acceptance_matrix_v01.md"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_projection_operator_decision_gate_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_projection_operator_decision_gate_v01.md"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def build_report() -> dict[str, Any]:
    rows = read_rows(PACKET)
    by_id = {row.get("component_id", ""): row for row in rows}
    operator = by_id.get("projection_operator_rule", {})
    normalization = by_id.get("projection_normalization", {})
    replay = by_id.get("projection_replay", {})
    explicit_failure = "FAILURE" in str(operator.get("current_status", "")).upper()
    operator_supplied = (
        bool(str(operator.get("accepted_value", "")).strip())
        and "BLOCKED" not in str(operator.get("current_status", ""))
        and not explicit_failure
    )
    normalization_supplied = bool(str(normalization.get("accepted_value", "")).strip()) and "BLOCKED" not in str(
        normalization.get("current_status", "")
    )
    replay_supplied = bool(str(replay.get("accepted_value", "")).strip()) and "BLOCKED" not in str(
        replay.get("current_status", "")
    )
    can_physical_score = operator_supplied and not explicit_failure and normalization_supplied and replay_supplied
    decision = "ALLOW_PHYSICAL_SCORE_RETRY" if can_physical_score else "DO_NOT_SCORE_OPERATOR_CORE_OPEN"
    if explicit_failure:
        decision = "DO_NOT_SCORE_EXPLICIT_OPERATOR_FAILURE"
    return {
        "report_id": "cmb_tau_lensing_projection_operator_decision_gate_v01",
        "claim_boundary": "projection_operator_decision_gate_only_no_operator_no_score_no_dark_sector_verdict",
        "packet": rel(PACKET),
        "formula_spec_scaffold": rel(SCAFFOLD),
        "formula_spec_acceptance_matrix": rel(ACCEPTANCE_MATRIX),
        "decision": decision,
        "operator_core_status": {
            "projection_operator_rule_supplied": operator_supplied,
            "projection_operator_explicit_failure": explicit_failure,
            "projection_normalization_supplied": normalization_supplied,
            "projection_replay_supplied": replay_supplied,
        },
        "admissible_next_actions": [
            {
                "action": "SUPPLY_OPERATOR",
                "description": "provide endpoint-blind Projection_PP equation, kernel table, or transfer/projection integral with normalization and replay",
            },
            {
                "action": "FILL_FORMULA_SPEC_SCAFFOLD",
                "description": "populate every blocking row in the formula-spec acceptance matrix with endpoint-blind equation, kernel/measure, normalization, zero-limit, dimension/sign audit, replay, and post-population firewall evidence",
            },
            {
                "action": "DECLARE_EXPLICIT_FAILURE",
                "description": "record a non-score failure statement naming the missing operator, normalization, replay, and next theoretical blocker",
            },
            {
                "action": "RESUME_FROM_FAILURE",
                "description": "replace the explicit failure with an endpoint-blind operator packet, then rerun normalization, replay, firewall, and gate",
            },
        ],
        "blocked_shortcuts": [
            "do not use post-score alpha_star as Projection_PP normalization",
            "do not replay B_ACT @ grid as if it were physical Phi_lens_tau -> PP projection",
            "do not run physical score retry until operator, normalization, and replay are all accepted",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    status = report["operator_core_status"]
    actions = "\n".join(f"- `{row['action']}`: {row['description']}" for row in report["admissible_next_actions"])
    shortcuts = "\n".join(f"- {item}" for item in report["blocked_shortcuts"])
    text = f"""# CMB Tau Lensing Projection Operator Decision Gate v01

**Doc class:** projection-operator decision gate
**Reader role:** Paper 13 Tau-grid implementer
**Status:** physical score retry blocked until operator core closes
**Canonical parent:** `docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Decision

```text
{report["decision"]}
```

## Formula-Spec Acceptance Matrix

```text
{report["formula_spec_acceptance_matrix"]}
```

## Operator Core Status

```text
projection_operator_rule_supplied = {status["projection_operator_rule_supplied"]}
projection_operator_explicit_failure = {status["projection_operator_explicit_failure"]}
projection_normalization_supplied = {status["projection_normalization_supplied"]}
projection_replay_supplied = {status["projection_replay_supplied"]}
```

## Admissible Next Actions

{actions}

## Blocked Shortcuts

{shortcuts}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the projection-operator decision gate.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report()
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
