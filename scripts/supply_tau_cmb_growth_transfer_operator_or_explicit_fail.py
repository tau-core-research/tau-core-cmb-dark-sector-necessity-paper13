#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FRONTIER_V06 = ROOT / "data/derived/tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_summary_v06.json"
GROWTH_COORDINATE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_growth_v01.csv"
GROWTH_KERNEL = ROOT / "data/derived/tau_cmb_growth_transfer_kernel_summary_v01.csv"
GROWTH_CLOSURE = ROOT / "data/derived/tau_cmb_growth_transfer_kernel_closure_summary_v01.csv"
DEFAULT_SUPPLY = ROOT / "physical_value_source_supplies/e_growth/growth_transfer_operator_explicit_fail_supply_v01.json"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_growth_transfer_operator_or_explicit_fail_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_growth_transfer_operator_or_explicit_fail_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_growth_transfer_operator_or_explicit_fail_supply_v01_"
    "growth_operator_explicit_fail_no_transfer_operator_no_score_no_likelihood_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_contains(path: Path, token: str) -> bool:
    return path.exists() and token in path.read_text(encoding="utf-8")


def input_chain_clean() -> bool:
    if not FRONTIER_V06.exists() or not GROWTH_COORDINATE.exists() or not GROWTH_KERNEL.exists() or not GROWTH_CLOSURE.exists():
        return False
    frontier = load_json(FRONTIER_V06)
    return (
        frontier.get("status") == "CMB_ENDPOINT_BLIND_PHYSICAL_VALUE_SOURCE_FRONTIER_RECOMPUTED_ACOUSTIC_EXPLICIT_FAILS_ACCEPTED"
        and frontier.get("next_minimal_unblock") == "tau_cmb_growth_transfer_operator_or_explicit_fail_supply_v01"
        and frontier.get("explicit_fail_accepted_rows") == 12
        and frontier.get("open_frontier_rows") == 4
        and frontier.get("physical_value_source_accepted_rows") == 0
        and text_contains(GROWTH_COORDINATE, "BLOCKED_OPERATOR_RULE_NOT_DERIVED")
        and text_contains(GROWTH_KERNEL, "GROWTH_TRANSFER_KERNEL_DECLARED_NOT_SPECIFIED")
        and text_contains(GROWTH_CLOSURE, "GROWTH_TRANSFER_KERNEL_PARTIAL_CLOSURE_SCORE_BLOCKED")
    )


def supply_payload() -> dict[str, Any]:
    return {
        "artifact_status": "GROWTH_TRANSFER_OPERATOR_EXPLICIT_FAIL_SUPPLIED_NO_ENDPOINT_BLIND_OPERATOR",
        "claim_boundary": CLAIM_BOUNDARY,
        "target_role": "growth",
        "coordinate_symbol": "e_growth",
        "coordinate_components_affected": ["operator_rule"],
        "formal_slots": ["Transfer_tau[X_tau_CMB](k,a)"],
        "supply_type": "explicit_fail_evidence",
        "numeric_value_supplied": False,
        "unit_or_convention": "not_applicable_explicit_fail",
        "source_strategy": "local_source_first_common_parent_later",
        "provenance": {
            "frontier_v06": rel(FRONTIER_V06),
            "growth_coordinate": rel(GROWTH_COORDINATE),
            "growth_kernel": rel(GROWTH_KERNEL),
            "growth_closure": rel(GROWTH_CLOSURE),
        },
        "replay": "make tau-cmb-endpoint-blind-physical-value-source-frontier-recompute-v06 && make tau-cmb-growth-transfer-operator-or-explicit-fail-supply",
        "endpoint_blind_attestation": True,
        "forbidden_input_attestation": True,
        "forbidden_inputs": [
            "CMB endpoint residuals",
            "ACT/Planck likelihood errors",
            "score outputs",
            "post-endpoint tuning fields",
            "dark-sector verdict labels",
        ],
        "required_missing_objects": [
            "endpoint-blind Tau CMB input state X_tau_CMB(k,a)",
            "initial condition map I_tau",
            "Tau evolution rule E_tau",
            "CMB-source output map M_CMB",
            "domain/codomain selection",
            "gauge, time-scale, and normalization conventions",
        ],
        "formal_required_shape": "Transfer_tau = M_CMB o E_tau o I_tau",
        "prior_explicit_fail_interactions": [
            "T_tau_CMB(k,a) explicit fail",
            "rho_tau_eff(a,k) explicit fail",
            "Phi_tau_eff(a,k) explicit fail",
            "endpoint_blind(A_tau) explicit fail",
        ],
        "physical_value_source_supplied": False,
        "explicit_fail_supplied": True,
        "physical_value_source_accepted": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "failure_statement": (
            "No endpoint-blind Tau-side CMB input state, evolution rule, transfer mapping, "
            "initial condition, normalization rule, and gauge/convention packet is accepted from which "
            "Transfer_tau[X_tau_CMB](k,a) can be derived."
        ),
        "nonclaims": [
            "This is not a numerical growth constraint.",
            "This is not a structure-growth data comparison.",
            "This is not a statement that Tau Core has no growth response.",
            "This is not an empirical validation or exclusion.",
            "This is not a dark-sector verdict.",
        ],
    }


def build_summary(supply_path: Path) -> dict[str, Any]:
    hash_path = supply_path.with_suffix(".hashes.json")
    hash_matches = supply_path.exists() and hash_path.exists() and load_json(hash_path).get("sha256") == sha256(supply_path)
    return {
        "report_id": "tau_cmb_growth_transfer_operator_or_explicit_fail_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "supply_artifact": rel(supply_path),
        "supply_hash_artifact": rel(hash_path),
        "input_frontier_recompute_v06": rel(FRONTIER_V06),
        "input_growth_coordinate": rel(GROWTH_COORDINATE),
        "input_growth_kernel": rel(GROWTH_KERNEL),
        "input_growth_closure": rel(GROWTH_CLOSURE),
        "input_chain_clean": input_chain_clean(),
        "target_role": "growth",
        "affected_frontier_rows": 1,
        "explicit_fail_supplied": True,
        "numeric_value_supplied": False,
        "physical_value_source_accepted": False,
        "growth_score_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "supply_hash_matches": hash_matches,
        "status": (
            "CMB_GROWTH_TRANSFER_OPERATOR_EXPLICIT_FAIL_SUPPLIED_NO_SCORE"
            if input_chain_clean() and hash_matches
            else "CMB_GROWTH_TRANSFER_OPERATOR_EXPLICIT_FAIL_SUPPLY_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_growth_transfer_operator_explicit_fail_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Growth Transfer Operator or Explicit Fail Supply v01

**Doc class:** growth operator explicit fail supply
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
explicit_fail_supplied={summary["explicit_fail_supplied"]}
numeric_value_supplied={summary["numeric_value_supplied"]}
physical_value_source_accepted={summary["physical_value_source_accepted"]}
growth_score_allowed={summary["growth_score_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

This follows the local-source-first, common-parent-later strategy. It does not
deny a future common Tau parent; it only records that the current frontier does
not supply the local growth transfer operator required before scoring.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Supply explicit fail evidence for the Tau CMB growth transfer operator row.")
    parser.add_argument("--write-artifact", nargs="?", const=str(DEFAULT_SUPPLY))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    supply_path = Path(args.write_artifact) if args.write_artifact else DEFAULT_SUPPLY
    if args.write_artifact:
        write_json(supply_path, supply_payload())
        write_json(
            supply_path.with_suffix(".hashes.json"),
            {
                "target": rel(supply_path),
                "sha256": sha256(supply_path),
                "claim_boundary": CLAIM_BOUNDARY,
                "explicit_fail_supplied": True,
                "physical_value_source_accepted": False,
                "score_entry_allowed": False,
            },
        )
    summary = build_summary(supply_path)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
