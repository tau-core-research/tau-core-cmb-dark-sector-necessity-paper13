#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRIDGE_SUMMARY = ROOT / "data/derived/tau_cmb_endpoint_blind_lensing_bridge_candidates_audit_summary_v01.json"
PROJECTION_OPERATOR_FAILURE_DOC = ROOT / "docs/cmb_tau_lensing_projection_operator_explicit_failure_v01.md"
PROJECTION_OPERATOR_AUDIT = ROOT / "data/derived/cmb_tau_lensing_physical_projection_operator_packet_audit_v01.json"
DEFAULT_SUPPLY = ROOT / "physical_value_source_supplies/e_lensing/transfer_kernel_explicit_fail_supply_v01.json"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_lensing_transfer_kernel_explicit_fail_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_lensing_transfer_kernel_explicit_fail_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_lensing_transfer_kernel_explicit_fail_supply_v01_"
    "row_specific_explicit_fail_no_operator_no_score_no_likelihood_no_verdict"
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


def input_chain_clean() -> bool:
    if not BRIDGE_SUMMARY.exists() or not PROJECTION_OPERATOR_FAILURE_DOC.exists() or not PROJECTION_OPERATOR_AUDIT.exists():
        return False
    summary = load_json(BRIDGE_SUMMARY)
    audit = load_json(PROJECTION_OPERATOR_AUDIT)
    return (
        summary.get("status") == "CMB_ENDPOINT_BLIND_LENSING_BRIDGE_CANDIDATES_AUDITED_NO_AUTOMATIC_SOURCE_ACCEPTANCE"
        and summary.get("next_minimal_unblock") == "tau_cmb_lensing_transfer_kernel_row_specific_explicit_fail_supply_v01"
        and summary.get("bridge_candidate_rows") == 2
        and summary.get("automatic_bridge_acceptance_rows") == 0
        and summary.get("explicit_fail_supply_allowed_rows") == 1
        and summary.get("physical_value_source_accepted_rows") == 0
        and audit.get("decision") == "DO_NOT_SCORE_EXPLICIT_OPERATOR_FAILURE"
        and audit.get("explicit_operator_failure_declared") is True
        and audit.get("projection_operator_packet_accepted") is False
        and audit.get("score_run") is False
    )


def supply_payload() -> dict[str, Any]:
    return {
        "artifact_status": "ROW_SPECIFIC_EXPLICIT_FAIL_SUPPLIED_NO_TRANSFER_KERNEL_OPERATOR",
        "claim_boundary": CLAIM_BOUNDARY,
        "target_role": "lensing",
        "coordinate_symbol": "e_lensing",
        "coordinate_component": "transfer_kernel",
        "formal_slot": "T_tau_CMB(k,a)",
        "supply_type": "explicit_fail_evidence",
        "numeric_value_supplied": False,
        "unit_or_convention": "not_applicable_explicit_fail",
        "provenance": {
            "projection_operator_failure_doc": rel(PROJECTION_OPERATOR_FAILURE_DOC),
            "projection_operator_audit": rel(PROJECTION_OPERATOR_AUDIT),
        },
        "replay": "make tau-cmb-endpoint-blind-lensing-bridge-candidates-audit && make tau-cmb-lensing-transfer-kernel-explicit-fail-supply",
        "endpoint_blind_attestation": True,
        "forbidden_input_attestation": True,
        "forbidden_inputs": [
            "CMB endpoint residuals",
            "ACT/Planck likelihood errors",
            "score outputs",
            "post-endpoint tuning fields",
            "dark-sector verdict labels",
        ],
        "physical_value_source_supplied": False,
        "explicit_fail_supplied": True,
        "physical_value_source_accepted": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "failure_statement": "No lawful endpoint-blind T_tau_CMB(k,a) transfer kernel is supplied for the CMB lensing transfer-kernel row; the row is supplied only as explicit non-score failure evidence.",
    }


def build_summary(supply_path: Path) -> dict[str, Any]:
    hash_path = supply_path.with_suffix(".hashes.json")
    hash_matches = supply_path.exists() and hash_path.exists() and load_json(hash_path).get("sha256") == sha256(supply_path)
    return {
        "report_id": "tau_cmb_lensing_transfer_kernel_explicit_fail_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "supply_artifact": rel(supply_path),
        "supply_hash_artifact": rel(hash_path),
        "input_bridge_candidates_audit_summary": rel(BRIDGE_SUMMARY),
        "input_projection_operator_failure_doc": rel(PROJECTION_OPERATOR_FAILURE_DOC),
        "input_projection_operator_audit": rel(PROJECTION_OPERATOR_AUDIT),
        "input_chain_clean": input_chain_clean(),
        "target_role": "lensing",
        "coordinate_symbol": "e_lensing",
        "coordinate_component": "transfer_kernel",
        "formal_slot": "T_tau_CMB(k,a)",
        "explicit_fail_supplied": True,
        "numeric_value_supplied": False,
        "physical_value_source_accepted": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "supply_hash_matches": hash_matches,
        "status": (
            "CMB_LENSING_TRANSFER_KERNEL_ROW_SPECIFIC_EXPLICIT_FAIL_SUPPLIED_NO_SCORE"
            if input_chain_clean() and hash_matches
            else "CMB_LENSING_TRANSFER_KERNEL_EXPLICIT_FAIL_SUPPLY_NONCANONICAL_RESULT"
        ),
        "next_minimal_unblock": "tau_cmb_lensing_transfer_kernel_explicit_fail_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Lensing Transfer Kernel Explicit Fail Supply v01

**Doc class:** row-specific explicit fail supply
**Reader role:** Paper 13 / CMB scoring route reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Summary

```text
coordinate_component={summary["coordinate_component"]}
formal_slot={summary["formal_slot"]}
explicit_fail_supplied={summary["explicit_fail_supplied"]}
numeric_value_supplied={summary["numeric_value_supplied"]}
physical_value_source_accepted={summary["physical_value_source_accepted"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

This is not a transfer-kernel value source. It supplies row-specific explicit
fail evidence stating that no lawful endpoint-blind `T_tau_CMB(k,a)` operator is
currently supplied.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Supply row-specific explicit fail evidence for Tau CMB lensing transfer kernel.")
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
