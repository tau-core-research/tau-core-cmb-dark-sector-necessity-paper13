#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "payloads/seed_tau_payload_candidate_v01.csv"
PROVENANCE = ROOT / "payloads/seed_tau_payload_candidate_v01.provenance.json"
REPLAY = ROOT / "payloads/seed_tau_payload_candidate_v01.replay.txt"
HASHES = ROOT / "payloads/seed_tau_payload_candidate_v01.hashes.json"
FIREWALL = ROOT / "payloads/seed_tau_payload_candidate_v01.firewall.json"
DEFAULT_REPORT = ROOT / "data/derived/tau_cmb_seed_tau_payload_candidate_audit_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_tau_payload_candidate_audit_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_tau_payload_candidate_audit_v01_audit_only_"
    "payload_not_accepted_no_domain_certificate_no_readout_no_survival_no_A_tau_value_no_score_no_verdict"
)

FORBIDDEN_TOKENS = [
    "ACT residual",
    "Planck residual",
    "CMB role score",
    "likelihood delta",
    "peak residual shape",
    "lensing residual direction",
    "score output",
    "post-endpoint tuning",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_payload_rows() -> list[dict[str, str]]:
    with PAYLOAD.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def token_hits(text: str) -> list[str]:
    lowered = text.lower()
    return [token for token in FORBIDDEN_TOKENS if token.lower() in lowered]


def row(component: str, status: str, finding: str, passed: bool, blocks: str) -> dict[str, Any]:
    return {
        "component": component,
        "audit_status": status,
        "finding": finding,
        "audit_passed": passed,
        "blocking_reason": blocks,
    }


def build_report() -> dict[str, Any]:
    missing = [path for path in [PAYLOAD, PROVENANCE, REPLAY, HASHES, FIREWALL] if not path.exists()]
    rows: list[dict[str, Any]] = []
    if missing:
        for path in missing:
            rows.append(row(rel(path), "FAIL_MISSING_ARTIFACT", "required artifact is absent", False, "candidate package incomplete"))
        return finalize(rows)

    payload_rows = load_payload_rows()
    provenance = load_json(PROVENANCE)
    hashes = load_json(HASHES)
    firewall = load_json(FIREWALL)

    rows.append(
        row(
            "payload_presence",
            "PASS_CANDIDATE_PRESENT",
            f"{len(payload_rows)} payload row(s) present",
            len(payload_rows) == 1,
            "payload must have exactly one candidate row",
        )
    )
    payload = payload_rows[0] if payload_rows else {}

    hash_findings: list[str] = []
    hash_pass = True
    for path in [PAYLOAD, PROVENANCE, REPLAY, FIREWALL]:
        expected = hashes.get("hashes", {}).get(rel(path))
        actual = sha256(path)
        ok = expected == actual
        hash_pass = hash_pass and ok
        hash_findings.append(f"{rel(path)} expected={expected} actual={actual} ok={ok}")
    rows.append(
        row(
            "hash_manifest",
            "PASS_HASHES_MATCH" if hash_pass else "FAIL_HASH_MISMATCH",
            "; ".join(hash_findings),
            hash_pass,
            "hash manifest must bind payload, provenance, replay, and firewall files",
        )
    )

    provenance_ok = (
        provenance.get("payload") == rel(PAYLOAD)
        and provenance.get("payload_accepted") is False
        and provenance.get("domain_certificate_allowed") is False
        and provenance.get("score_entry_allowed") is False
    )
    rows.append(
        row(
            "provenance_boundary",
            "PASS_PROVENANCE_BOUNDARY_CLOSED" if provenance_ok else "FAIL_PROVENANCE_BOUNDARY",
            "provenance links payload and keeps acceptance permissions closed",
            provenance_ok,
            "provenance must bind payload while forbidding acceptance and scoring",
        )
    )

    replay_text = REPLAY.read_text(encoding="utf-8")
    replay_ok = "build_tau_cmb_seed_tau_payload_candidate.py --write-all" in replay_text
    rows.append(
        row(
            "replay_presence",
            "PASS_REPLAY_DECLARED" if replay_ok else "FAIL_REPLAY_MISSING_COMMAND",
            "replay command declares deterministic candidate rebuild",
            replay_ok,
            "replay command must be explicit before later acceptance audit",
        )
    )

    combined_text = "\n".join(
        [
            PAYLOAD.read_text(encoding="utf-8"),
            PROVENANCE.read_text(encoding="utf-8"),
            REPLAY.read_text(encoding="utf-8"),
            FIREWALL.read_text(encoding="utf-8"),
        ]
    )
    hits = token_hits(combined_text)
    firewall_ok = (
        firewall.get("endpoint_inputs_used") == []
        and firewall.get("endpoint_blind_attestation") is True
        and firewall.get("firewall_passed_for_acceptance") is False
    )
    rows.append(
        row(
            "endpoint_firewall_candidate",
            "PASS_CANDIDATE_FIREWALL_ATTESTED_NOT_ACCEPTED" if firewall_ok else "FAIL_FIREWALL_ATTESTATION",
            f"endpoint_inputs_used={firewall.get('endpoint_inputs_used')}; textual_token_hits={hits}",
            firewall_ok,
            "candidate attestation can pass only as non-acceptance evidence",
        )
    )

    dimension_ok = payload.get("dimension_role") == "dimensionless_structure_class_pending_normalization"
    normalization_blocked = payload.get("normalization_convention") == "pending_tau_side_normalization_replay"
    rows.append(
        row(
            "dimension_and_normalization",
            "BLOCKED_NORMALIZATION_REPLAY_MISSING" if dimension_ok and normalization_blocked else "FAIL_DIMENSION_ROLE",
            "dimension role is declared, but normalization replay remains pending",
            False,
            "normalization replay is required before domain certificate or readout evaluation",
        )
    )

    support_ok = payload.get("support_coordinate") == "parent Tau morphology / CMB readout sector"
    rows.append(
        row(
            "support_convention",
            "BLOCKED_SUPPORT_COORDINATE_NOT_CONCRETE" if support_ok else "FAIL_SUPPORT_MISSING",
            "support is a sector label, not a concrete support coordinate system",
            False,
            "concrete support coordinates and parent-domain construction are required",
        )
    )

    null_blocked = payload.get("null_limit_role") == "null_limit_required_not_defined"
    rows.append(
        row(
            "null_limit_role",
            "BLOCKED_NULL_LIMIT_NOT_DEFINED" if null_blocked else "PASS_NULL_LIMIT_DECLARED",
            "null-limit role is explicitly required but not defined",
            False,
            "null_seed and null readout role are required before quotient survival",
        )
    )

    return finalize(rows)


def finalize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(bool(item["audit_passed"]) for item in rows)
    blocked = sum(item["audit_status"].startswith("BLOCKED") for item in rows)
    failed = sum(item["audit_status"].startswith("FAIL") for item in rows)
    return {
        "report_id": "tau_cmb_seed_tau_payload_candidate_audit_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "audited_payload": rel(PAYLOAD),
        "audit_rows": rows,
        "passed_rows": passed,
        "blocked_rows": blocked,
        "failed_rows": failed,
        "payload_acceptance_allowed": False,
        "domain_certificate_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_TAU_PAYLOAD_CANDIDATE_AUDITED_BLOCKED_NOT_ACCEPTED",
        "next_minimal_unblock": "define_seed_support_coordinates_normalization_replay_and_null_limit_role",
    }


def write_doc(path: Path, report: dict[str, Any]) -> None:
    rows = "\n".join(
        f"- `{item['component']}`: {item['audit_status']} | {item['finding']}"
        for item in report["audit_rows"]
    )
    text = f"""# Tau CMB Seed Tau Payload Candidate Audit v01

**Doc class:** endpoint-blind seed payload candidate audit
**Status:** {report["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This audit checks whether the materialized `seed_tau` payload candidate is
present, hash-bound, replayable, and endpoint-firewall clean as a candidate. It
does not accept the payload, certify the readout domain, evaluate quotient
survival, assign `A_tau(a,k)`, enter scoring, or decide the dark-sector
question.

## Audit Rows

{rows}

## Status

```text
{report["status"]}
```

Candidate-level evidence is now present, but acceptance remains blocked by
missing concrete support coordinates, Tau-side normalization replay, and
null-limit/zero-control definitions.

## Next Minimal Unblock

```text
{report["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Tau CMB seed_tau payload candidate.")
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
