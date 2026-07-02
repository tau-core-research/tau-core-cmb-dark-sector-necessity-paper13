#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_candidate_audit_v01.json"
CANDIDATE_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_candidate_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_proof_checker_payload_packet_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_proof_checker_payload_packet_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_proof_checker_payload_packet_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_proof_checker_payload_packet_v01_payload_spec_only_"
    "no_checker_execution_no_certificate_pass_no_domain_acceptance_no_R_CMB_"
    "no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "payload_row_id",
    "certificate_area",
    "target_candidate_object",
    "payload_kind",
    "minimal_payload_spec",
    "checker_input_contract",
    "checker_output_contract",
    "required_replay",
    "current_payload_status",
    "blocking_reason",
    "payload_spec_declared",
    "checker_executed",
    "certificate_passed",
    "domain_object_accepted",
    "allows_concrete_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "certificate_area": "carrier_well_formedness",
        "target_candidate_object": "CarrierOK_candidate(x)",
        "payload_kind": "proof_or_executable_checker_spec",
        "minimal_payload_spec": "define CarrierOK checker inputs, role-basis membership test, role typing test, and endpoint-fitted-coordinate exclusion test",
        "checker_input_contract": "candidate x, audited role-space basis id, role-coordinate bundle id, provenance metadata",
        "checker_output_contract": "pass/fail plus failure code for WellFormedRoleRepresentative_CMB, RoleTyped_CMB, basis membership, endpoint-fit exclusion",
        "required_replay": "role-space basis replay and bundle-closure replay",
        "current_payload_status": "PAYLOAD_SPEC_DECLARED_NOT_EXECUTED",
        "blocking_reason": "no executable checker or proof transcript is supplied",
    },
    {
        "certificate_area": "domain_membership_rule",
        "target_candidate_object": "DomOK_candidate(x)",
        "payload_kind": "joint_domain_checker_spec",
        "minimal_payload_spec": "define DomOK checker as ParentSideCMBObject and SupportOK and NormalizationOK and PayloadOK and ReplayOK and FirewallOK",
        "checker_input_contract": "candidate x, support record, normalization record, payload record, replay trace, firewall trace",
        "checker_output_contract": "pass/fail plus component-level SupportOK, NormalizationOK, PayloadOK, ReplayOK, FirewallOK statuses",
        "required_replay": "support-domain, normalization, payload, replay, and firewall replay",
        "current_payload_status": "PAYLOAD_SPEC_DECLARED_NOT_EXECUTED",
        "blocking_reason": "joint domain checker is specified but not executed",
    },
    {
        "certificate_area": "seed_admissibility",
        "target_candidate_object": "SeedInDomain_candidate(seed_tau_CMB)",
        "payload_kind": "seed_admissibility_checker_spec",
        "minimal_payload_spec": "define seed checker requiring descriptor pass, activation pass, quotient survival, equivalence replay, and firewall pass",
        "checker_input_contract": "seed object, descriptor audit, activation audit, quotient survival object, equivalence replay, firewall metadata",
        "checker_output_contract": "pass/fail plus seed descriptor, activation, quotient survival, equivalence, and firewall substatuses",
        "required_replay": "seed descriptor replay, activation replay, quotient/equivalence replay, endpoint firewall replay",
        "current_payload_status": "PAYLOAD_SPEC_DECLARED_NOT_EXECUTED",
        "blocking_reason": "seed proof/checker payload is not populated with passing evidence",
    },
    {
        "certificate_area": "null_control_admissibility",
        "target_candidate_object": "NullControlInDomain_candidate(null_seed_tau_CMB)",
        "payload_kind": "null_control_checker_spec",
        "minimal_payload_spec": "define null-control checker requiring same-domain convention, null readout target, and no-response proof",
        "checker_input_contract": "null seed, zero-control record, null-coordinate record, domain convention id, null-readout materialization candidate",
        "checker_output_contract": "pass/fail plus same-domain, null-readout, and no-response substatuses",
        "required_replay": "zero-control replay, null-coordinate replay, domain replay",
        "current_payload_status": "PAYLOAD_SPEC_DECLARED_NOT_EXECUTED",
        "blocking_reason": "null readout is not materialized and no-response proof is absent",
    },
    {
        "certificate_area": "source_object_admissibility",
        "target_candidate_object": "SourceObjectInDomain_candidate(source_tau_CMB)",
        "payload_kind": "endpoint_blind_source_checker_spec",
        "minimal_payload_spec": "define source-object checker for endpoint-blind rho_tau_eff, A_tau, Phi_tau_eff, or T_tau_CMB derivation and replay",
        "checker_input_contract": "source object, derivation transcript, dimension/gauge replay, known-limit check, endpoint firewall trace",
        "checker_output_contract": "pass/fail plus endpoint-blind derivation, dimension/gauge, known-limit, and firewall substatuses",
        "required_replay": "source derivation replay, dimension/gauge replay, known-limit replay, post-population firewall",
        "current_payload_status": "PAYLOAD_SPEC_DECLARED_NOT_EXECUTED",
        "blocking_reason": "no endpoint-blind source object proof transcript is supplied",
    },
    {
        "certificate_area": "quotient_and_equivalence_survival",
        "target_candidate_object": "QuotientSurvival_candidate([x])",
        "payload_kind": "quotient_survival_checker_spec",
        "minimal_payload_spec": "define quotient checker requiring non-null survival and representative-independence under the declared equivalence relation",
        "checker_input_contract": "object x, null class, equivalence relation id, representative family, readout-class convention",
        "checker_output_contract": "pass/fail plus non-null survival and representative-independence substatuses",
        "required_replay": "equivalence axiom replay, quotient relation replay, non-null witness replay",
        "current_payload_status": "PAYLOAD_SPEC_DECLARED_NOT_EXECUTED",
        "blocking_reason": "non-null survival witness and representative-independence proof are absent",
    },
    {
        "certificate_area": "codomain_compatibility",
        "target_candidate_object": "CodomainOK_candidate(R_CMB(x))",
        "payload_kind": "codomain_output_checker_spec",
        "minimal_payload_spec": "define codomain checker for acoustic/density/lensing/growth/radiation/null role typing, units, signs, and numeric guards",
        "checker_input_contract": "future R_CMB output, role-coordinate basis, dimension/sign metadata, role-specific numeric guard records",
        "checker_output_contract": "pass/fail plus role typing, unit/sign, and numeric-guard substatuses",
        "required_replay": "role-coordinate bundle replay, dimension/sign replay, numeric guard replay",
        "current_payload_status": "PAYLOAD_SPEC_DECLARED_NOT_EXECUTED",
        "blocking_reason": "no concrete R_CMB output exists to check",
    },
    {
        "certificate_area": "endpoint_firewall_replay",
        "target_candidate_object": "EndpointBlindCarrierDomain_candidate",
        "payload_kind": "post_population_firewall_checker_spec",
        "minimal_payload_spec": "define endpoint firewall checker over populated carrier/domain/codomain choices before residuals, scores, or likelihood deltas are inspected",
        "checker_input_contract": "populated carrier/domain/codomain records, provenance log, endpoint data access log, score access log",
        "checker_output_contract": "pass/fail plus no-residual-use, no-score-use, no-likelihood-delta-use, and provenance-lock substatuses",
        "required_replay": "post-population endpoint firewall replay",
        "current_payload_status": "PAYLOAD_SPEC_DECLARED_NOT_EXECUTED",
        "blocking_reason": "firewall cannot execute before populated values exist",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "payload_row_id": f"TCMBCDPCP01_{index:03d}",
            "payload_spec_declared": "true",
            "checker_executed": "false",
            "certificate_passed": "false",
            "domain_object_accepted": "false",
            "allows_concrete_R_CMB": "false",
            "allows_score_entry": "false",
            "allows_likelihood": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(ROWS, start=1)
    ]


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    audit = load_json(CANDIDATE_AUDIT) if CANDIDATE_AUDIT.exists() else {}
    input_ok = (
        audit.get("status") == "CARRIER_DOMAIN_CERTIFICATE_CANDIDATE_AUDITED_UNPASSED_NOT_SCORE_READY"
        and audit.get("failed_rows") == 0
        and CANDIDATE_TABLE.exists()
    )
    return {
        "report_id": "tau_cmb_carrier_domain_proof_checker_payload_packet_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_candidate_audit": rel(CANDIDATE_AUDIT),
        "input_candidate_table": rel(CANDIDATE_TABLE),
        "input_chain_clean": input_ok,
        "payload_rows": len(rows),
        "payload_specs_declared": sum(row["payload_spec_declared"] == "true" for row in rows),
        "checkers_executed": sum(row["checker_executed"] == "true" for row in rows),
        "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] == "true" for row in rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_PROOF_CHECKER_PAYLOAD_PACKET_DECLARED_NOT_EXECUTED"
            if input_ok
            else "CARRIER_DOMAIN_PROOF_CHECKER_PAYLOAD_PACKET_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_proof_checker_payload_packet_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        (
            f"- `{row['certificate_area']}`: {row['current_payload_status']} | "
            f"`{row['target_candidate_object']}` | payload: {row['payload_kind']} | "
            f"blocks: {row['blocking_reason']}"
        )
        for row in rows
    )
    text = f"""# Tau CMB Carrier Domain Proof Checker Payload Packet v01

**Doc class:** carrier/domain proof/checker payload packet
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the minimal proof/checker payload specifications for the
named carrier/domain certificate candidates. It does not execute checkers, pass
certificates, accept domain objects, materialize `R_CMB`, open score entry,
compute a likelihood, or decide the dark-sector question.

## Payload Rows

{row_text}

## Status

```text
{summary["status"]}
```

The route now has explicit proof/checker input and output contracts, but all
execution, pass, and acceptance flags remain false.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB carrier/domain proof/checker payload packet.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    if args.write_table:
        write_table(table_path, rows)
    summary = build_summary(table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
