#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CERT_AUDIT = ROOT / "data/derived/tau_cmb_concrete_R_CMB_carrier_certificate_audit_v01.json"
ROLE_BUNDLE = ROOT / "data/derived/tau_cmb_readout_role_coordinate_bundle_closure_audit_v01.json"
DOMAIN_REQ = ROOT / "data/derived/tau_cmb_seed_readout_domain_certificate_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_carrier_domain_predicate_candidate_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_carrier_domain_predicate_candidate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_carrier_domain_predicate_candidate_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_carrier_domain_predicate_candidate_v01_candidate_only_"
    "carrier_not_certified_domain_not_certified_R_CMB_not_materialized_no_score_no_verdict"
)

FIELDS = [
    "predicate_row_id",
    "predicate_component",
    "formal_predicate",
    "candidate_rule",
    "required_evidence",
    "current_evidence",
    "predicate_status",
    "blocking_reason",
    "allows_carrier_certificate",
    "allows_domain_certificate",
    "allows_concrete_R_CMB",
    "allows_score_entry",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "predicate_component": "carrier_membership",
        "formal_predicate": "x in C_CMB^seed iff WellFormedRoleRepresentative_CMB(x)",
        "candidate_rule": "x must be representable over the audited CMB role-coordinate bundle with declared role typing and no endpoint-fitted coordinate",
        "required_evidence": "role-coordinate bundle closure audit plus role typing replay",
        "current_evidence": "bundle closure is audited but blocked not score-ready",
        "predicate_status": "CANDIDATE_DECLARED_NOT_CERTIFIED",
        "blocking_reason": "well-formed representative predicate is declared but not proved as a carrier certificate",
    },
    {
        "predicate_component": "domain_membership",
        "formal_predicate": "x in Dom(R_CMB) iff ParentSideCMBObject(x) and SupportOK(x) and NormalizationOK(x) and FirewallOK(x)",
        "candidate_rule": "domain objects may include seed, null seed, and later accepted source objects only after support, normalization, replay, and firewall evidence",
        "required_evidence": "support-domain rule, normalization replay, zero-control, evidence payload, endpoint firewall",
        "current_evidence": "domain certificate requirements exist but no accepted domain rule",
        "predicate_status": "CANDIDATE_DECLARED_DOMAIN_NOT_CERTIFIED",
        "blocking_reason": "support, normalization, payload acceptance, and firewall replay are not jointly certified",
    },
    {
        "predicate_component": "null_control_admissibility",
        "formal_predicate": "null_seed_tau_CMB in Dom(R_CMB) and R_CMB(null_seed_tau_CMB) = null_readout",
        "candidate_rule": "null seed is admissible only as a control object over the same domain convention and cannot be physical response evidence",
        "required_evidence": "zero-control audit, null coordinate audit, domain membership replay",
        "current_evidence": "zero-control and null coordinate are audited but blocked/not accepted",
        "predicate_status": "CANDIDATE_DECLARED_NULL_NOT_ACCEPTED",
        "blocking_reason": "null seed is not domain-certified and null readout is not materialized",
    },
    {
        "predicate_component": "source_object_admissibility",
        "formal_predicate": "source_tau_CMB in Dom(R_CMB) only if endpoint_blind_source_object(source_tau_CMB)",
        "candidate_rule": "rho_tau_eff, A_tau, Phi_tau_eff, and T_tau_CMB cannot enter the domain until derived endpoint-blind with replay",
        "required_evidence": "endpoint-blind source object packet and dimension/gauge replay",
        "current_evidence": "source objects remain role slots and are not accepted",
        "predicate_status": "CANDIDATE_DECLARED_SOURCE_OBJECTS_NOT_ACCEPTED",
        "blocking_reason": "no endpoint-blind source object derivation is accepted",
    },
    {
        "predicate_component": "forbidden_endpoint_dependency",
        "formal_predicate": "not UsesEndpointResidualsOrScores(x)",
        "candidate_rule": "domain and carrier predicates cannot depend on ACT/Planck residuals, likelihood deltas, score outputs, or post-endpoint tuning",
        "required_evidence": "endpoint firewall replay after concrete predicate/materialization values exist",
        "current_evidence": "firewall discipline is declared but cannot be replayed over absent values",
        "predicate_status": "FIREWALL_RULE_DECLARED_NOT_REPLAYED",
        "blocking_reason": "endpoint firewall must rerun after candidate values are populated",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "predicate_row_id": f"TCMBCDPC01_{index:03d}",
            "allows_carrier_certificate": "false",
            "allows_domain_certificate": "false",
            "allows_concrete_R_CMB": "false",
            "allows_score_entry": "false",
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
    cert = load_json(CERT_AUDIT) if CERT_AUDIT.exists() else {}
    bundle = load_json(ROLE_BUNDLE) if ROLE_BUNDLE.exists() else {}
    input_ok = (
        cert.get("status") == "CONCRETE_R_CMB_CARRIER_CERTIFICATE_REQUIREMENTS_AUDITED_BLOCKED"
        and cert.get("failed_rows") == 0
        and bundle.get("status") == "READOUT_ROLE_COORDINATE_BUNDLE_CLOSURE_AUDITED_BLOCKED_NOT_SCORE_READY"
        and DOMAIN_REQ.exists()
    )
    return {
        "report_id": "tau_cmb_carrier_domain_predicate_candidate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_certificate_audit": rel(CERT_AUDIT),
        "input_bundle_closure_audit": rel(ROLE_BUNDLE),
        "input_domain_requirements": rel(DOMAIN_REQ),
        "input_chain_clean": input_ok,
        "predicate_rows": len(rows),
        "candidate_rows": sum("CANDIDATE_DECLARED" in row["predicate_status"] for row in rows),
        "firewall_rows": sum("FIREWALL" in row["predicate_status"] for row in rows),
        "carrier_certificate_allowed": False,
        "domain_certificate_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CARRIER_DOMAIN_PREDICATE_CANDIDATE_DECLARED_NOT_CERTIFIED"
            if input_ok
            else "CARRIER_DOMAIN_PREDICATE_CANDIDATE_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_predicate_candidate_audit_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['predicate_component']}`: {row['predicate_status']} | `{row['formal_predicate']}`"
        for row in rows
    )
    text = f"""# Tau CMB Carrier Domain Predicate Candidate v01

**Doc class:** carrier/domain predicate candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares a candidate carrier/domain predicate for the CMB readout
route. It does not certify the carrier, certify `Dom(R_CMB)`, materialize
`R_CMB`, open score entry, or decide the dark-sector question.

## Predicate Rows

{row_text}

## Status

```text
{summary["status"]}
```

The candidate narrows what carrier/domain certification must mean, but all
certification permissions remain closed.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB carrier/domain predicate candidate.")
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
