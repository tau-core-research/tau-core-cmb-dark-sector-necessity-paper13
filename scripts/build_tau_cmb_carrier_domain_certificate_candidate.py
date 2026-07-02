#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQ_AUDIT = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_requirements_audit_v01.json"
REQ_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_requirements_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_candidate_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_certificate_candidate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_certificate_candidate_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_certificate_candidate_v01_candidate_only_"
    "certificates_declared_unpassed_domain_unaccepted_R_CMB_not_materialized_"
    "no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "candidate_row_id",
    "certificate_area",
    "candidate_certificate_object",
    "candidate_certificate_content",
    "required_payload",
    "current_payload",
    "candidate_status",
    "acceptance_blocker",
    "certificate_candidate_declared",
    "carrier_certificate_passed",
    "domain_certificate_passed",
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
        "candidate_certificate_object": "CarrierOK_candidate(x)",
        "candidate_certificate_content": "CarrierOK_candidate(x) checks WellFormedRoleRepresentative_CMB(x), RoleTyped_CMB(x), role-basis membership, and absence of endpoint-fitted coordinates.",
        "required_payload": "executable or proof-level carrier checker plus role-space basis and bundle replay",
        "current_payload": "formal checker shape declared; no proof or executable checker payload supplied",
        "candidate_status": "CANDIDATE_DECLARED_CARRIER_CERTIFICATE_UNPASSED",
        "acceptance_blocker": "CarrierOK_candidate is not proved or executable",
    },
    {
        "certificate_area": "domain_membership_rule",
        "candidate_certificate_object": "DomOK_candidate(x)",
        "candidate_certificate_content": "DomOK_candidate(x) conjoins ParentSideCMBObject, SupportOK, NormalizationOK, PayloadOK, ReplayOK, and FirewallOK.",
        "required_payload": "joint domain checker with support, normalization, payload, replay, and firewall evidence",
        "current_payload": "domain conjunction declared; joint checker/evidence payload absent",
        "candidate_status": "CANDIDATE_DECLARED_DOMAIN_CERTIFICATE_UNPASSED",
        "acceptance_blocker": "DomOK_candidate has no joint pass certificate",
    },
    {
        "certificate_area": "seed_admissibility",
        "candidate_certificate_object": "SeedInDomain_candidate(seed_tau_CMB)",
        "candidate_certificate_content": "Seed may enter Dom(R_CMB) only if descriptor, activation, quotient survival, and firewall predicates pass.",
        "required_payload": "seed descriptor pass, activation pass, quotient survival witness, equivalence replay, endpoint firewall",
        "current_payload": "seed route declared but quotient survival and activation acceptance are absent",
        "candidate_status": "CANDIDATE_DECLARED_SEED_ADMISSIBILITY_UNPASSED",
        "acceptance_blocker": "seed is not accepted as an in-domain object",
    },
    {
        "certificate_area": "null_control_admissibility",
        "candidate_certificate_object": "NullControlInDomain_candidate(null_seed_tau_CMB)",
        "candidate_certificate_content": "Null seed may enter only as a control object and must map to a null readout under the same domain convention.",
        "required_payload": "zero-control pass, null-coordinate pass, null readout materialization, no-response proof",
        "current_payload": "zero-control route exists but null domain membership and null readout materialization are absent",
        "candidate_status": "CANDIDATE_DECLARED_NULL_CONTROL_UNPASSED",
        "acceptance_blocker": "null control is not accepted as materialized in-domain control",
    },
    {
        "certificate_area": "source_object_admissibility",
        "candidate_certificate_object": "SourceObjectInDomain_candidate(source_tau_CMB)",
        "candidate_certificate_content": "Tau source objects may enter only if endpoint-blind source derivation and replay are supplied for rho_tau_eff, A_tau, Phi_tau_eff, or T_tau_CMB.",
        "required_payload": "endpoint-blind source object packet, dimension/gauge replay, known-limit check, post-population firewall",
        "current_payload": "source objects remain formula/readout slots and are not accepted",
        "candidate_status": "CANDIDATE_DECLARED_SOURCE_OBJECT_UNPASSED",
        "acceptance_blocker": "no endpoint-blind source object certificate exists",
    },
    {
        "certificate_area": "quotient_and_equivalence_survival",
        "candidate_certificate_object": "QuotientSurvival_candidate([x])",
        "candidate_certificate_content": "Admitted objects must survive the null/gauge quotient and equivalent representatives must map to the same readout class.",
        "required_payload": "equivalence axiom proof, quotient relation audit pass, non-null survival witness, representative-independence check",
        "current_payload": "quotient/equivalence route is declared but no non-null survival certificate is supplied",
        "candidate_status": "CANDIDATE_DECLARED_QUOTIENT_SURVIVAL_UNPASSED",
        "acceptance_blocker": "non-null survival and representative independence are not proved",
    },
    {
        "certificate_area": "codomain_compatibility",
        "candidate_certificate_object": "CodomainOK_candidate(R_CMB(x))",
        "candidate_certificate_content": "Every future readout value must land in the audited acoustic/density/lensing/growth/radiation/null role codomain with declared units and signs.",
        "required_payload": "role-coordinate output typing, dimension/sign replay, role-specific numeric guards",
        "current_payload": "codomain basis is audit-visible but no concrete readout output exists",
        "candidate_status": "CANDIDATE_DECLARED_CODOMAIN_OUTPUT_UNPASSED",
        "acceptance_blocker": "no concrete R_CMB output can be checked yet",
    },
    {
        "certificate_area": "endpoint_firewall_replay",
        "candidate_certificate_object": "EndpointBlindCarrierDomain_candidate",
        "candidate_certificate_content": "CarrierOK, DomOK, admissibility, quotient, and codomain choices must be replayed before endpoint residuals, scores, or likelihood deltas are inspected.",
        "required_payload": "post-population endpoint firewall replay over populated carrier/domain/codomain values",
        "current_payload": "firewall condition is declared but cannot be replayed over absent values",
        "candidate_status": "CANDIDATE_DECLARED_FIREWALL_UNPASSED",
        "acceptance_blocker": "endpoint firewall requires populated values and replay trace",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "candidate_row_id": f"TCMBCDCC01_{index:03d}",
            "certificate_candidate_declared": "true",
            "carrier_certificate_passed": "false",
            "domain_certificate_passed": "false",
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
    audit = load_json(REQ_AUDIT) if REQ_AUDIT.exists() else {}
    input_ok = (
        audit.get("status") == "CARRIER_DOMAIN_CERTIFICATE_REQUIREMENTS_AUDITED_BLOCKED_NOT_SCORE_READY"
        and audit.get("failed_rows") == 0
        and REQ_TABLE.exists()
    )
    return {
        "report_id": "tau_cmb_carrier_domain_certificate_candidate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_requirements_audit": rel(REQ_AUDIT),
        "input_requirements_table": rel(REQ_TABLE),
        "input_chain_clean": input_ok,
        "candidate_rows": len(rows),
        "declared_candidate_rows": sum(row["certificate_candidate_declared"] == "true" for row in rows),
        "carrier_certificate_passed_rows": sum(row["carrier_certificate_passed"] == "true" for row in rows),
        "domain_certificate_passed_rows": sum(row["domain_certificate_passed"] == "true" for row in rows),
        "accepted_domain_objects": sum(row["domain_object_accepted"] == "true" for row in rows),
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_CERTIFICATE_CANDIDATE_DECLARED_UNPASSED"
            if input_ok
            else "CARRIER_DOMAIN_CERTIFICATE_CANDIDATE_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "audit_tau_cmb_carrier_domain_certificate_candidate_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        (
            f"- `{row['certificate_area']}`: {row['candidate_status']} | "
            f"`{row['candidate_certificate_object']}` | blocks: {row['acceptance_blocker']}"
        )
        for row in rows
    )
    text = f"""# Tau CMB Carrier Domain Certificate Candidate v01

**Doc class:** carrier/domain certificate candidate
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares candidate certificate objects for `CarrierOK`,
`DomOK`, seed/null/source admissibility, quotient survival, codomain
compatibility, and endpoint-firewall replay. It does not pass the certificates,
accept domain objects, materialize `R_CMB`, open score entry, compute a
likelihood, or decide the dark-sector question.

## Candidate Certificate Rows

{row_text}

## Status

```text
{summary["status"]}
```

The route now has concrete candidate certificate names and payload slots, but
all pass/acceptance flags remain false.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB carrier/domain certificate candidate.")
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
