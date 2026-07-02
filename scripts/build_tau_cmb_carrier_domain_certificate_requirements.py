#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PREDICATE_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_predicate_candidate_audit_v01.json"
SINGLE_PASS = ROOT / "data/derived/tau_cmb_single_pass_derivation_spine_summary_v01.json"
SEED_DOMAIN = ROOT / "data/derived/tau_cmb_seed_readout_domain_certificate_summary_v01.json"
ZERO_CONTROL = ROOT / "data/derived/tau_cmb_seed_zero_control_summary_v01.json"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_requirements_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_requirements_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_certificate_requirements_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_certificate_requirements_v01_requirements_only_"
    "carrier_not_certified_domain_not_certified_R_CMB_not_materialized_no_score_no_verdict"
)

FIELDS = [
    "requirement_row_id",
    "certificate_area",
    "formal_requirement",
    "acceptance_condition",
    "required_evidence",
    "current_evidence",
    "requirement_status",
    "blocking_reason",
    "allows_carrier_certificate",
    "allows_domain_certificate",
    "allows_concrete_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "certificate_area": "carrier_well_formedness",
        "formal_requirement": "CarrierOK(x) := WellFormedRoleRepresentative_CMB(x) and RoleTyped_CMB(x)",
        "acceptance_condition": "every admitted x has declared role typing over the audited six-role CMB basis and no endpoint-fitted coordinate",
        "required_evidence": "role-space basis audit, role-coordinate bundle closure audit, executable or proof-level CarrierOK checker",
        "current_evidence": "carrier predicate candidate is audit-visible but not proved",
        "requirement_status": "REQUIREMENT_DECLARED_CARRIER_NOT_CERTIFIED",
        "blocking_reason": "no accepted CarrierOK proof/checker exists",
    },
    {
        "certificate_area": "domain_membership_rule",
        "formal_requirement": "DomOK(x) := ParentSideCMBObject(x) and SupportOK(x) and NormalizationOK(x) and FirewallOK(x)",
        "acceptance_condition": "domain membership is accepted only after support, normalization, replay, payload, and endpoint-firewall evidence are jointly present",
        "required_evidence": "seed readout domain certificate, support-domain rule audit, normalization replay audit, payload acceptance, endpoint firewall replay",
        "current_evidence": "domain ingredients exist as candidates/audits but are not jointly certified",
        "requirement_status": "REQUIREMENT_DECLARED_DOMAIN_NOT_CERTIFIED",
        "blocking_reason": "no joint DomOK certificate exists",
    },
    {
        "certificate_area": "seed_admissibility",
        "formal_requirement": "seed_tau_CMB in Dom(R_CMB) only if SeedDescriptorOK and ActivationOK and QuotientSurvivalOK",
        "acceptance_condition": "seed object may enter the domain only after descriptor, activation, quotient/equivalence survival, and firewall checks pass",
        "required_evidence": "seed descriptor audit, activation rule audit, quotient survival test, equivalence proof obligation",
        "current_evidence": "seed chain is declared but not accepted as domain object",
        "requirement_status": "REQUIREMENT_DECLARED_SEED_NOT_ACCEPTED",
        "blocking_reason": "quotient survival and accepted activation are not proved",
    },
    {
        "certificate_area": "null_control_admissibility",
        "formal_requirement": "null_seed_tau_CMB in Dom(R_CMB) and R_CMB(null_seed_tau_CMB) = null_readout",
        "acceptance_condition": "null seed is accepted only as a control over the same domain convention and cannot count as physical source evidence",
        "required_evidence": "zero-control audit, null-coordinate audit, domain membership replay, no-response proof",
        "current_evidence": "null/control path is audited but not accepted as an in-domain materialized readout",
        "requirement_status": "REQUIREMENT_DECLARED_NULL_NOT_ACCEPTED",
        "blocking_reason": "null domain membership and null readout materialization are missing",
    },
    {
        "certificate_area": "source_object_admissibility",
        "formal_requirement": "source_tau_CMB in Dom(R_CMB) only if endpoint_blind_source_object(source_tau_CMB)",
        "acceptance_condition": "rho_tau_eff, A_tau, Phi_tau_eff, and T_tau_CMB can enter only as endpoint-blind derived source/readout objects with replay",
        "required_evidence": "endpoint-blind source object packet, dimension/gauge replay, known-limit check, post-population firewall",
        "current_evidence": "source quantities remain formula slots or candidates, not accepted objects",
        "requirement_status": "REQUIREMENT_DECLARED_SOURCE_OBJECTS_NOT_ACCEPTED",
        "blocking_reason": "no endpoint-blind source object derivation is accepted",
    },
    {
        "certificate_area": "quotient_and_equivalence_survival",
        "formal_requirement": "[x]_~ != [null] and R_CMB respects the declared equivalence relation",
        "acceptance_condition": "the admitted object survives null/gauge quotienting and equivalent representatives map to the same readout class",
        "required_evidence": "equivalence axiom proof obligation, quotient relation audit, non-null survival witness",
        "current_evidence": "quotient/equivalence objects are declared but survival is not proved",
        "requirement_status": "REQUIREMENT_DECLARED_QUOTIENT_SURVIVAL_NOT_PROVED",
        "blocking_reason": "no non-null survival certificate exists for domain objects",
    },
    {
        "certificate_area": "codomain_compatibility",
        "formal_requirement": "R_CMB(x) in V_CMB^roles with acoustic/density/lensing/growth/radiation/null typing",
        "acceptance_condition": "every readout value must land in the audited role-coordinate codomain with declared units, signs, and coordinate labels",
        "required_evidence": "role-coordinate bundle closure audit, role-specific numeric guards, dimension/sign replay",
        "current_evidence": "codomain roles are audited but not materialized by a concrete readout map",
        "requirement_status": "REQUIREMENT_DECLARED_CODOMAIN_PARTIAL",
        "blocking_reason": "role codomain is audit-visible but not yet a concrete output target",
    },
    {
        "certificate_area": "endpoint_firewall_replay",
        "formal_requirement": "not UsesEndpointResidualsOrScores(x, CarrierOK, DomOK)",
        "acceptance_condition": "carrier and domain certificates must be replayed after concrete values exist and before any Planck/ACT residual or score information is inspected",
        "required_evidence": "post-population endpoint firewall replay over carrier, domain, source, null, and codomain choices",
        "current_evidence": "firewall rule is declared but cannot be replayed over absent concrete values",
        "requirement_status": "REQUIREMENT_DECLARED_FIREWALL_NOT_REPLAYED",
        "blocking_reason": "endpoint firewall requires populated values",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "requirement_row_id": f"TCMBCDCREQ01_{index:03d}",
            "allows_carrier_certificate": "false",
            "allows_domain_certificate": "false",
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
    predicate = load_json(PREDICATE_AUDIT) if PREDICATE_AUDIT.exists() else {}
    single_pass = load_json(SINGLE_PASS) if SINGLE_PASS.exists() else {}
    seed_domain = load_json(SEED_DOMAIN) if SEED_DOMAIN.exists() else {}
    zero_control = load_json(ZERO_CONTROL) if ZERO_CONTROL.exists() else {}
    input_ok = (
        predicate.get("status") == "CARRIER_DOMAIN_PREDICATE_CANDIDATE_AUDITED_BLOCKED_NOT_SCORE_READY"
        and predicate.get("failed_rows") == 0
        and single_pass.get("status") == "SINGLE_PASS_DERIVATION_SPINE_DECLARED_ROUTE_BLOCKED_NOT_SCORE_READY"
        and single_pass.get("input_chain_consistent_with_blocked_route") is True
        and SEED_DOMAIN.exists()
        and ZERO_CONTROL.exists()
    )
    return {
        "report_id": "tau_cmb_carrier_domain_certificate_requirements_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_predicate_audit": rel(PREDICATE_AUDIT),
        "input_single_pass_spine": rel(SINGLE_PASS),
        "input_seed_domain_certificate": rel(SEED_DOMAIN),
        "input_zero_control": rel(ZERO_CONTROL),
        "input_chain_clean": input_ok,
        "input_seed_domain_status": seed_domain.get("status", "MISSING"),
        "input_zero_control_status": zero_control.get("status", "MISSING"),
        "requirement_rows": len(rows),
        "blocked_requirement_rows": len(rows),
        "carrier_certificate_allowed": False,
        "domain_certificate_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CERTIFICATE_REQUIREMENTS_DECLARED_BLOCKED"
            if input_ok
            else "CARRIER_DOMAIN_CERTIFICATE_REQUIREMENTS_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_certificate_requirements_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        (
            f"- `{row['certificate_area']}`: {row['requirement_status']} | "
            f"`{row['formal_requirement']}` | blocks: {row['blocking_reason']}"
        )
        for row in rows
    )
    text = f"""# Tau CMB Carrier Domain Certificate Requirements v01

**Doc class:** carrier/domain certificate requirements
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact turns the carrier/domain predicate candidate into a finite
certificate requirement set. It does not certify the carrier, certify
`Dom(R_CMB)`, materialize `R_CMB`, open score entry, compute a likelihood, or
decide the dark-sector question.

## Certificate Requirement Rows

{row_text}

## Status

```text
{summary["status"]}
```

The shortest path to a concrete `R_CMB` now requires discharging these
carrier/domain certificate requirements. All scoring and verdict permissions
remain closed.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB carrier/domain certificate requirements.")
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
