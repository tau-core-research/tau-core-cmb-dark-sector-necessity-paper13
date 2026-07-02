#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "data/derived/tau_cmb_concrete_R_CMB_candidate_gate_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_concrete_R_CMB_candidate_gate_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_concrete_R_CMB_candidate_gate_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_concrete_R_CMB_candidate_gate_audit_v01_audit_only_structural_candidate_shell_"
    "not_physical_R_CMB_no_codomain_pass_no_checker_execution_no_score_no_likelihood_no_verdict"
)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_row(component: str, status: str, finding: str, passed: bool, blocking_reason: str) -> dict[str, Any]:
    return {
        "component": component,
        "audit_status": status,
        "finding": finding,
        "audit_passed": passed,
        "blocking_reason": blocking_reason,
    }


def build_report() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    if not CANDIDATE.exists():
        rows.append(audit_row(rel(CANDIDATE), "FAIL_MISSING_ARTIFACT", "candidate gate is absent", False, "audit package incomplete"))
        return finalize(rows)

    candidate = load_json(CANDIDATE)
    source_ok = all(record.get("exists") and record.get("sha256") for record in candidate.get("source_records", []))
    rows.append(audit_row("source_records", "PASS_SOURCE_RECORDS_BOUND" if source_ok else "FAIL_SOURCE_RECORDS", "all source records exist and are hash-bound", source_ok, "candidate gate requires hash-bound source records"))

    signature_ok = (
        candidate.get("formal_readout_signature") == "R_CMB_candidate: Dom(R_CMB)_candidate -> C_CMB_role_candidate"
        and candidate.get("role_vector_slots")
        == ["e_acoustic", "e_density", "e_lensing", "e_growth", "e_radiation", "e_null"]
    )
    rows.append(audit_row("structural_signature", "PASS_STRUCTURAL_SIGNATURE" if signature_ok else "FAIL_STRUCTURAL_SIGNATURE", "formal readout signature and six role slots are declared", signature_ok, "candidate gate requires role-vector signature"))

    structural_ok = (
        candidate.get("status") == "CONCRETE_R_CMB_STRUCTURAL_CANDIDATE_GATE_DECLARED_NOT_PHYSICAL"
        and candidate.get("input_chain_clean") is True
        and candidate.get("structural_candidate_available_for_codomain_precheck") is True
    )
    rows.append(audit_row("candidate_gate_status", "PASS_STRUCTURAL_CANDIDATE_AVAILABLE" if structural_ok else "FAIL_STRUCTURAL_CANDIDATE_STATUS", "structural candidate shell is available for codomain precheck", structural_ok, "candidate gate must be clean before codomain precheck"))

    firewall_ok = (
        candidate.get("physical_R_CMB_materialized") is False
        and candidate.get("numeric_values_materialized") is False
        and candidate.get("carrier_certificate_passed") is False
        and candidate.get("domain_rule_accepted") is False
        and candidate.get("codomain_checker_passed") is False
        and candidate.get("checker_execution_allowed") is False
        and candidate.get("concrete_R_CMB_allowed") is False
        and candidate.get("score_entry_allowed") is False
        and candidate.get("likelihood_allowed") is False
        and candidate.get("dark_sector_verdict_allowed") is False
    )
    rows.append(audit_row("promotion_firewall", "PASS_CANDIDATE_FIREWALL_CLOSED" if firewall_ok else "FAIL_CANDIDATE_FIREWALL", "candidate shell does not open physical R_CMB, execution, score, likelihood, or verdict", firewall_ok, "candidate shell must not promote structural availability into physical readout"))

    rows.append(audit_row("physical_R_CMB", "BLOCKED_PHYSICAL_R_CMB_NOT_MATERIALIZED", "candidate shell has no physical/numeric readout values", False, "requires executable readout materialization rule and values"))
    rows.append(audit_row("carrier_domain_certification", "BLOCKED_CARRIER_DOMAIN_NOT_CERTIFIED", "carrier/domain certificate remains blocked", False, "requires accepted carrier predicate and domain rule"))
    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(r["audit_passed"]) for r in rows)
    blocked = sum(r["audit_status"].startswith("BLOCKED") for r in rows)
    failed = sum(r["audit_status"].startswith("FAIL") for r in rows)
    clean = failed == 0
    return {
        "report_id": "tau_cmb_concrete_R_CMB_candidate_gate_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_candidate": rel(CANDIDATE),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "structural_R_CMB_candidate_gate_audited": clean,
        "structural_candidate_available_for_codomain_precheck": clean,
        "physical_R_CMB_materialized": False,
        "codomain_checker_passed": False,
        "checker_execution_allowed": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CONCRETE_R_CMB_STRUCTURAL_CANDIDATE_GATE_AUDITED_NOT_PHYSICAL"
            if clean
            else "CONCRETE_R_CMB_STRUCTURAL_CANDIDATE_GATE_AUDIT_FAILED"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_checker_execution_packet_refresh_v02_with_structural_R_CMB_candidate",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    row_text = "\n".join(f"- `{r['component']}`: {r['audit_status']} | {r['finding']}" for r in report["audit_rows"])
    text = f"""# Tau CMB Concrete R_CMB Candidate Gate Audit v01

**Doc class:** concrete readout candidate gate audit
**Reader role:** Paper 13 / CMB readout route reviewer
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks the structural `R_CMB` candidate shell. It does not certify a
physical readout, pass codomain compatibility, execute checkers, open score
entry, compute a likelihood, or decide the dark-sector question.

## Audit Rows

{row_text}

## Status

```text
{report["status"]}
```

The structural candidate can be used to refresh the codomain precheck, but
physical materialization and carrier/domain certification remain blocked.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB concrete R_CMB structural candidate gate.")
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
