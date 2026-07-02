#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPLY_SUMMARY = ROOT / "data/derived/tau_cmb_growth_transfer_operator_or_explicit_fail_supply_summary_v01.json"
SUPPLY_ARTIFACT = ROOT / "physical_value_source_supplies/e_growth/growth_transfer_operator_explicit_fail_supply_v01.json"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_growth_transfer_operator_explicit_fail_acceptance_audit_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_growth_transfer_operator_explicit_fail_acceptance_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_growth_transfer_operator_explicit_fail_acceptance_audit_v01_"
    "explicit_fail_accepted_no_growth_operator_no_score_no_likelihood_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def input_chain_clean() -> bool:
    if not SUPPLY_SUMMARY.exists() or not SUPPLY_ARTIFACT.exists():
        return False
    summary = load_json(SUPPLY_SUMMARY)
    supply = load_json(SUPPLY_ARTIFACT)
    return (
        summary.get("status") == "CMB_GROWTH_TRANSFER_OPERATOR_EXPLICIT_FAIL_SUPPLIED_NO_SCORE"
        and summary.get("next_minimal_unblock") == "tau_cmb_growth_transfer_operator_explicit_fail_acceptance_audit_v01"
        and summary.get("affected_frontier_rows") == 1
        and summary.get("explicit_fail_supplied") is True
        and summary.get("numeric_value_supplied") is False
        and summary.get("physical_value_source_accepted") is False
        and summary.get("growth_score_allowed") is False
        and summary.get("supply_hash_matches") is True
        and supply.get("explicit_fail_supplied") is True
        and supply.get("physical_value_source_accepted") is False
        and supply.get("score_entry_allowed") is False
    )


def build_summary() -> dict[str, Any]:
    clean = input_chain_clean()
    return {
        "report_id": "tau_cmb_growth_transfer_operator_explicit_fail_acceptance_audit_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "input_supply_summary": rel(SUPPLY_SUMMARY),
        "input_supply_artifact": rel(SUPPLY_ARTIFACT),
        "input_chain_clean": clean,
        "target_role": "growth",
        "affected_frontier_rows": 1,
        "explicit_fail_accepted": clean,
        "numeric_growth_values_accepted": False,
        "physical_value_source_accepted": False,
        "physical_CMB_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_GROWTH_TRANSFER_OPERATOR_EXPLICIT_FAIL_ACCEPTED_PHYSICAL_SCORE_BLOCKED"
            if clean
            else "CMB_GROWTH_TRANSFER_OPERATOR_EXPLICIT_FAIL_ACCEPTANCE_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_v07",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Growth Transfer Operator Explicit Fail Acceptance Audit v01

**Doc class:** growth explicit fail acceptance audit
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Summary

```text
target_role={summary["target_role"]}
affected_frontier_rows={summary["affected_frontier_rows"]}
explicit_fail_accepted={summary["explicit_fail_accepted"]}
numeric_growth_values_accepted={summary["numeric_growth_values_accepted"]}
physical_value_source_accepted={summary["physical_value_source_accepted"]}
physical_CMB_score_allowed={summary["physical_CMB_score_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

The growth transfer operator row is closed only as an explicit non-score
failure. No transfer operator, growth score, structure-growth comparison,
likelihood, or dark-sector verdict is accepted.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit explicit fail acceptance for the Tau CMB growth transfer operator row.")
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    summary = build_summary()
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
