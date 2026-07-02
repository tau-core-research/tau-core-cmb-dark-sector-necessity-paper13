#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RULE_TABLE = ROOT / "data/derived/tau_cmb_seed_support_domain_rule_candidate_v01.csv"
PAYLOAD = ROOT / "payloads/seed_tau_payload_candidate_v01.csv"
PROVENANCE = ROOT / "payloads/seed_tau_payload_candidate_v01.provenance.json"
FIREWALL = ROOT / "payloads/seed_tau_payload_candidate_v01.firewall.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_seed_support_domain_rule_candidate_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_support_domain_rule_candidate_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_support_domain_rule_candidate_audit_v01_audit_only_"
    "support_not_certified_no_payload_acceptance_no_domain_certificate_no_readout_no_score_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def row(component: str, status: str, finding: str, passed: bool, blocking_reason: str) -> dict[str, Any]:
    return {
        "component": component,
        "audit_status": status,
        "finding": finding,
        "audit_passed": passed,
        "blocking_reason": blocking_reason,
    }


def build_report() -> dict[str, Any]:
    missing = [path for path in [RULE_TABLE, PAYLOAD, PROVENANCE, FIREWALL] if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "audit package incomplete"))
        return finalize(rows)

    rule_rows = read_csv(RULE_TABLE)
    payload_rows = read_csv(PAYLOAD)
    provenance = load_json(PROVENANCE)
    firewall = load_json(FIREWALL)
    payload = payload_rows[0] if payload_rows else {}

    expected_components = [
        "parent_domain_symbol",
        "support_coordinate_basis",
        "membership_rule",
        "forbidden_endpoint_dependence",
        "normalization_dependency",
        "zero_control_dependency",
    ]
    components = [item.get("rule_component") for item in rule_rows]
    rows.append(
        row(
            "rule_table_shape",
            "PASS_RULE_ROWS_PRESENT" if components == expected_components else "FAIL_RULE_ROW_SHAPE",
            f"components={components}",
            components == expected_components,
            "support rule audit requires the six declared candidate rows",
        )
    )

    parent_symbol_ok = any(
        item.get("formal_object") == "Tau_CMB_parent_domain := {morphology_readout_sector=CMB}"
        for item in rule_rows
    )
    rows.append(
        row(
            "parent_domain_symbol",
            "PASS_SYMBOL_DECLARED_AS_SECTOR_LABEL" if parent_symbol_ok else "FAIL_PARENT_DOMAIN_SYMBOL",
            "parent-domain symbol is declared as CMB morphology/readout sector label",
            parent_symbol_ok,
            "parent-domain symbol must remain sector-level and endpoint-blind",
        )
    )

    support_tuple_ok = (
        payload.get("tau_side_descriptor") == "M_tau^CMB as parent-side projection-conditioning morphology class"
        and payload.get("support_coordinate") == "parent Tau morphology / CMB readout sector"
        and payload.get("scale_label") == "CMB_readout_sector_scale_label_candidate_not_normalized"
    )
    rows.append(
        row(
            "support_tuple_well_formed_candidate",
            "PASS_TUPLE_FIELDS_PRESENT_NOT_NORMALIZED" if support_tuple_ok else "FAIL_SUPPORT_TUPLE_FIELDS",
            "payload provides morphology_class, readout_sector, and scale_label candidate fields",
            support_tuple_ok,
            "support tuple fields must exist before normalization replay can consume them",
        )
    )

    endpoint_blind_ok = (
        firewall.get("endpoint_inputs_used") == []
        and firewall.get("endpoint_blind_attestation") is True
        and provenance.get("score_entry_allowed") is False
    )
    rows.append(
        row(
            "endpoint_blindness_candidate",
            "PASS_ENDPOINT_BLIND_CANDIDATE_EVIDENCE" if endpoint_blind_ok else "FAIL_ENDPOINT_BLINDNESS",
            "firewall records endpoint_inputs_used=[] and provenance keeps score closed",
            endpoint_blind_ok,
            "support rule can reference candidate endpoint-blind evidence but cannot accept it",
        )
    )

    support_cert_block = payload.get("scale_label", "").endswith("_not_normalized")
    rows.append(
        row(
            "support_certification",
            "BLOCKED_SCALE_LABEL_NOT_NORMALIZED" if support_cert_block else "PASS_SUPPORT_CERTIFICATION",
            "scale label remains candidate_not_normalized",
            False,
            "support certification requires Tau-side normalization replay",
        )
    )

    membership_block = payload.get("allows_domain_certificate") == "false"
    rows.append(
        row(
            "domain_membership_promotion",
            "BLOCKED_DOMAIN_CERTIFICATE_PERMISSION_CLOSED" if membership_block else "FAIL_PERMISSION_OPEN",
            "payload explicitly keeps domain_certificate permission closed",
            False,
            "membership cannot promote to domain certificate before support and normalization audits pass",
        )
    )

    zero_block = "tau_cmb_seed_zero_control_v01" in {item.get("next_required_artifact") for item in rule_rows}
    rows.append(
        row(
            "zero_control_dependency",
            "BLOCKED_ZERO_CONTROL_NOT_DEFINED" if zero_block else "FAIL_ZERO_CONTROL_DEPENDENCY_MISSING",
            "support rule correctly requires later zero-control over the same convention",
            False,
            "null_seed / zero-control must be defined before quotient survival",
        )
    )

    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(item["audit_passed"]) for item in rows)
    blocked = sum(item["audit_status"].startswith("BLOCKED") for item in rows)
    failed = sum(item["audit_status"].startswith("FAIL") for item in rows)
    return {
        "report_id": "tau_cmb_seed_support_domain_rule_candidate_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_rule_table": rel(RULE_TABLE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "support_rule_candidate_audited": True,
        "support_certification_allowed": False,
        "payload_acceptance_allowed": False,
        "domain_certificate_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_SUPPORT_DOMAIN_RULE_CANDIDATE_AUDITED_BLOCKED_NOT_CERTIFIED",
        "next_minimal_unblock": "tau_cmb_seed_normalization_replay_candidate_v01",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{item['component']}`: {item['audit_status']} | {item['finding']}"
        for item in report["audit_rows"]
    )
    text = f"""# Tau CMB Seed Support Domain Rule Candidate Audit v01

**Doc class:** support-domain rule candidate audit
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether the support-domain rule candidate is well-formed and
endpoint-blind as a candidate. It does not certify support, accept the payload,
certify `seed_tau_CMB in Dom(R_CMB)`, evaluate readout survival, assign
`A_tau(a,k)`, enter scoring, or decide the dark-sector question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

The support-domain rule is now audited as a candidate, but certification is
blocked because the scale label is not normalized, domain-certificate
permission remains closed, and the zero-control object is not defined.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB seed support domain rule candidate.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), report)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
