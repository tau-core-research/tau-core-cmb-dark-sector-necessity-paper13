#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_receipt_audit_v01.json"
ROUTER = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_router_summary_v01.json"
CONTENT_AUDIT = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_summary_v01.json"
DECISION_GATE = ROOT / "data/derived/cmb_tau_lensing_projection_operator_decision_gate_v01.json"
DEFAULT_REPORT = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_prescore_lock_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_endpoint_blind_operator_prescore_lock_v01.md"


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"status": "MISSING", "decision": "MISSING"}
    return json.loads(path.read_text())


def build_report() -> dict[str, Any]:
    receipt = read_json(RECEIPT)
    router = read_json(ROUTER)
    content = read_json(CONTENT_AUDIT)
    gate = read_json(DECISION_GATE)
    receipt_ready = receipt.get("status") == "OPERATOR_PACKET_RECEIPT_AUDIT_READY_FOR_CONTENT_AUDITS"
    router_ready = router.get("status") == "CONTENT_AUDIT_ROUTER_READY_NOT_SCORE"
    content_accepted = content.get("content_acceptance") is True
    gate_allows = gate.get("decision") == "ALLOW_PHYSICAL_SCORE_RETRY"
    lock_reasons = []
    if not receipt_ready:
        lock_reasons.append("endpoint_blind_operator_packet_receipt_not_ready")
    if not router_ready:
        lock_reasons.append("content_audit_router_not_ready")
    if not content_accepted:
        lock_reasons.append("operator_packet_content_audit_not_accepted")
    if not gate_allows:
        lock_reasons.append("projection_operator_decision_gate_does_not_allow_physical_score")
    locked = bool(lock_reasons)
    return {
        "report_id": "cmb_tau_lensing_endpoint_blind_operator_prescore_lock_v01",
        "claim_boundary": "endpoint_blind_operator_prescore_lock_only_no_physical_score_no_dark_sector_verdict",
        "status": "PHYSICAL_TAU_ROUTE_PRESCORE_LOCKED" if locked else "PHYSICAL_TAU_ROUTE_READY_FOR_SCORE_GUARD_NOT_SCORE",
        "lock_result": "pre_score_locked" if locked else "ready_for_score_guard",
        "score_attempt_allowed_for_physical_tau_route": not locked,
        "lock_reasons": lock_reasons,
        "receipt_audit": rel(RECEIPT),
        "receipt_status": receipt.get("status"),
        "receipt_decision": receipt.get("decision"),
        "content_audit_router": rel(ROUTER),
        "content_router_status": router.get("status"),
        "content_audit": rel(CONTENT_AUDIT),
        "content_audit_status": content.get("status"),
        "content_acceptance": content_accepted,
        "content_blocked_rows": content.get("blocked_rows", []),
        "content_partial_rows": content.get("partial_rows", []),
        "operator_decision_gate": rel(DECISION_GATE),
        "operator_gate_decision": gate.get("decision"),
        "next_minimal_unblock": "supply_endpoint_blind_operator_packet_submission"
        if not receipt_ready
        else content.get("next_minimal_unblock")
        or "complete_content_audits_and_rerun_operator_decision_gate",
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(report: dict[str, Any], path: Path) -> None:
    reasons = "\n".join(f"- `{item}`" for item in report["lock_reasons"]) or "- none"
    text = f"""# CMB Tau Lensing Endpoint-Blind Operator Prescore Lock v01

**Doc class:** physical Tau-route prescore lock
**Reader role:** Paper 13 Tau-grid implementer
**Status:** {report["status"]}
**Canonical parent:** `docs/cmb_tau_lensing_endpoint_blind_operator_packet_content_audit_router_v01.md`

## Claim Boundary

```text
{report["claim_boundary"]}
```

## Lock Result

```text
{report["lock_result"]}
score_attempt_allowed_for_physical_tau_route = {report["score_attempt_allowed_for_physical_tau_route"]}
```

## Lock Reasons

{reasons}

## Inputs

```text
receipt_status = {report["receipt_status"]}
receipt_decision = {report["receipt_decision"]}
content_router_status = {report["content_router_status"]}
content_audit_status = {report["content_audit_status"]}
operator_gate_decision = {report["operator_gate_decision"]}
```

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```

This lock is scoped to the endpoint-blind physical Tau-route. It does not claim
that other reduced diagnostic or synthetic smoke-test routes are physically
accepted.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build endpoint-blind operator prescore lock.")
    parser.add_argument("--write-report", nargs="?", const=str(DEFAULT_REPORT))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        path = Path(args.write_report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.write_doc:
        write_doc(report, Path(args.write_doc))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
