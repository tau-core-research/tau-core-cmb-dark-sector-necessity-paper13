#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REFRESH_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_checker_execution_packet_refresh_audit_v01.json"
BUNDLE_AUDIT = ROOT / "data/derived/tau_cmb_readout_role_coordinate_bundle_closure_audit_v01.json"
CARRIER_CERT_AUDIT = ROOT / "data/derived/tau_cmb_concrete_R_CMB_carrier_certificate_audit_v01.json"
DEFAULT_CANDIDATE = ROOT / "data/derived/tau_cmb_concrete_R_CMB_candidate_gate_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_concrete_R_CMB_candidate_gate_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_concrete_R_CMB_candidate_gate_v01_structural_candidate_shell_only_"
    "not_physical_R_CMB_no_codomain_pass_no_checker_execution_no_score_no_likelihood_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_record(path: Path, role: str) -> dict[str, Any]:
    return {
        "path": rel(path),
        "role": role,
        "exists": path.exists(),
        "sha256": sha256(path) if path.exists() else None,
    }


def build_candidate() -> dict[str, Any]:
    refresh = load_json(REFRESH_AUDIT) if REFRESH_AUDIT.exists() else {}
    bundle = load_json(BUNDLE_AUDIT) if BUNDLE_AUDIT.exists() else {}
    carrier = load_json(CARRIER_CERT_AUDIT) if CARRIER_CERT_AUDIT.exists() else {}
    input_chain_clean = (
        refresh.get("status")
        == "CARRIER_DOMAIN_CHECKER_EXECUTION_PACKET_REFRESH_AUDITED_PARTIAL_EXECUTION_READY_NOT_ATTEMPTED"
        and refresh.get("failed_rows") == 0
        and bundle.get("status") == "READOUT_ROLE_COORDINATE_BUNDLE_CLOSURE_AUDITED_BLOCKED_NOT_SCORE_READY"
        and bundle.get("failed_rows") == 0
        and carrier.get("status") == "CONCRETE_R_CMB_CARRIER_CERTIFICATE_REQUIREMENTS_AUDITED_BLOCKED"
        and carrier.get("failed_rows") == 0
    )
    role_vector_slots = [
        "e_acoustic",
        "e_density",
        "e_lensing",
        "e_growth",
        "e_radiation",
        "e_null",
    ]
    candidate = {
        "candidate_id": "tau_cmb_concrete_R_CMB_candidate_gate_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_class": "structural_R_CMB_candidate_shell",
        "input_chain_clean": input_chain_clean,
        "formal_readout_signature": "R_CMB_candidate: Dom(R_CMB)_candidate -> C_CMB_role_candidate",
        "role_vector_slots": role_vector_slots,
        "structural_candidate_available_for_codomain_precheck": input_chain_clean,
        "physical_R_CMB_materialized": False,
        "numeric_values_materialized": False,
        "carrier_certificate_passed": False,
        "domain_rule_accepted": False,
        "codomain_checker_passed": False,
        "checker_execution_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "source_records": [
            source_record(REFRESH_AUDIT, "checker_execution_refresh_audit"),
            source_record(BUNDLE_AUDIT, "role_coordinate_bundle_closure_audit"),
            source_record(CARRIER_CERT_AUDIT, "carrier_certificate_requirement_audit"),
        ],
        "candidate_gate_rows": [
            {
                "component": "readout_signature",
                "status": "PASS_STRUCTURAL_SIGNATURE_DECLARED" if input_chain_clean else "BLOCKED_INPUT_CHAIN",
                "finding": "formal R_CMB candidate signature is declared without numeric values",
            },
            {
                "component": "role_vector_slots",
                "status": "PASS_ROLE_VECTOR_SLOTS_ENUMERATED",
                "finding": ", ".join(role_vector_slots),
            },
            {
                "component": "carrier_domain_certification",
                "status": "BLOCKED_CARRIER_DOMAIN_NOT_CERTIFIED",
                "finding": "carrier/domain certificate requirements remain blocked",
            },
            {
                "component": "physical_materialization",
                "status": "BLOCKED_PHYSICAL_R_CMB_NOT_MATERIALIZED",
                "finding": "candidate shell has no physical/numeric readout values",
            },
            {
                "component": "promotion_firewall",
                "status": "PASS_NO_SCORE_OR_VERDICT_OPENED",
                "finding": "score, likelihood, and dark-sector verdict remain closed",
            },
        ],
        "status": (
            "CONCRETE_R_CMB_STRUCTURAL_CANDIDATE_GATE_DECLARED_NOT_PHYSICAL"
            if input_chain_clean
            else "CONCRETE_R_CMB_STRUCTURAL_CANDIDATE_GATE_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "tau_cmb_concrete_R_CMB_candidate_gate_audit_v01",
    }
    return candidate


def write_doc(path: Path, candidate: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['component']}`: {row['status']} | {row['finding']}"
        for row in candidate["candidate_gate_rows"]
    )
    text = f"""# Tau CMB Concrete R_CMB Candidate Gate v01

**Doc class:** concrete readout candidate gate
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {candidate["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares a structural `R_CMB` candidate shell for codomain
prechecking. It is not a physical or numerical CMB readout. It does not certify
the carrier/domain, pass the codomain checker, execute checkers, materialize
physical `R_CMB`, open score entry, compute a likelihood, or decide the
dark-sector question.

## Candidate Rows

{row_text}

## Status

```text
{candidate["status"]}
```

The gate gives the codomain route a structural readout target, while preserving
the physical materialization and carrier/domain certification blockers.

## Next Minimal Unblock

```text
{candidate["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB concrete R_CMB structural candidate gate.")
    parser.add_argument("--write-candidate", nargs="?", const=str(DEFAULT_CANDIDATE))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    candidate = build_candidate()
    if args.write_candidate:
        path = Path(args.write_candidate)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), candidate)
    print(json.dumps(candidate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
