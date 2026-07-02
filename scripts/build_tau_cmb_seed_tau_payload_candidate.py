#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR = ROOT / "data/derived/tau_cmb_morphological_seed_descriptor_candidate_v01.csv"
DEFAULT_PAYLOAD = ROOT / "payloads/seed_tau_payload_candidate_v01.csv"
DEFAULT_PROVENANCE = ROOT / "payloads/seed_tau_payload_candidate_v01.provenance.json"
DEFAULT_REPLAY = ROOT / "payloads/seed_tau_payload_candidate_v01.replay.txt"
DEFAULT_HASHES = ROOT / "payloads/seed_tau_payload_candidate_v01.hashes.json"
DEFAULT_FIREWALL = ROOT / "payloads/seed_tau_payload_candidate_v01.firewall.json"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_seed_tau_payload_candidate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_tau_payload_candidate_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_tau_payload_candidate_v01_concrete_candidate_only_"
    "not_accepted_no_domain_certificate_no_readout_evaluation_no_survival_no_A_tau_value_no_score_no_verdict"
)

PAYLOAD_FIELDS = [
    "seed_id",
    "seed_component",
    "tau_side_descriptor",
    "support_coordinate",
    "scale_label",
    "normalization_convention",
    "dimension_role",
    "construction_source",
    "endpoint_exclusion_attestation",
    "null_limit_role",
    "notes",
    "allows_payload_acceptance",
    "allows_domain_certificate",
    "allows_score_entry",
    "claim_boundary",
]

FORBIDDEN_ENDPOINT_INPUTS = [
    "ACT residuals",
    "Planck residuals",
    "CMB role scores",
    "likelihood deltas",
    "peak residual shapes",
    "lensing residual directions",
    "score outputs",
    "post-endpoint tuning fields",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_descriptor_rows() -> list[dict[str, str]]:
    with DESCRIPTOR.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def descriptor(component: str, rows: list[dict[str, str]], field: str = "candidate_value") -> str:
    for row in rows:
        if row["descriptor_component"] == component:
            return row[field]
    raise KeyError(component)


def payload_row(rows: list[dict[str, str]]) -> dict[str, str]:
    return {
        "seed_id": descriptor("seed_identity", rows),
        "seed_component": "morphological_seed",
        "tau_side_descriptor": descriptor("intrinsic_morphology_basis", rows),
        "support_coordinate": descriptor("intrinsic_morphology_basis", rows, "support_domain"),
        "scale_label": "CMB_readout_sector_scale_label_candidate_not_normalized",
        "normalization_convention": "pending_tau_side_normalization_replay",
        "dimension_role": descriptor("intrinsic_morphology_basis", rows, "dimension_or_unit_status"),
        "construction_source": "; ".join(
            [
                descriptor("seed_identity", rows, "tau_core_anchor"),
                descriptor("readout_context", rows, "tau_core_anchor"),
                "data/derived/tau_cmb_morphological_seed_descriptor_candidate_v01.csv",
            ]
        ),
        "endpoint_exclusion_attestation": "endpoint_blind_candidate_no_CMB_endpoint_residuals_peak_shapes_scores_or_post_endpoint_tuning_used",
        "null_limit_role": "null_limit_required_not_defined",
        "notes": "candidate payload materialized from Tau-side descriptor rows only; not accepted",
        "allows_payload_acceptance": "false",
        "allows_domain_certificate": "false",
        "allows_score_entry": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_payload(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=PAYLOAD_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_provenance(payload_path: Path, descriptor_rows: list[dict[str, str]]) -> dict[str, Any]:
    source_files = sorted({row["tau_core_anchor"] for row in descriptor_rows} | {rel(DESCRIPTOR)})
    return {
        "artifact_id": "seed_tau_payload_candidate_v01.provenance",
        "payload": rel(payload_path),
        "claim_boundary": CLAIM_BOUNDARY,
        "construction_time_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "construction_rule": "copy only Tau-side descriptor fields from the morphological seed descriptor candidate; do not use CMB endpoint measurements",
        "source_files": source_files,
        "descriptor_rows_used": [row["seed_row_id"] for row in descriptor_rows],
        "payload_accepted": False,
        "domain_certificate_allowed": False,
        "score_entry_allowed": False,
    }


def write_replay(path: Path) -> None:
    text = """# seed_tau_payload_candidate_v01 replay

Rebuild command:

python3 scripts/build_tau_cmb_seed_tau_payload_candidate.py --write-all

Replay boundary:

- Reads only data/derived/tau_cmb_morphological_seed_descriptor_candidate_v01.csv.
- Does not read ACT/Planck residuals, endpoint score tables, likelihood deltas,
  peak residual shapes, or post-endpoint tuning artifacts.
- Produces a concrete candidate payload but does not accept it.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_firewall(payload_path: Path, provenance_path: Path, replay_path: Path) -> dict[str, Any]:
    return {
        "artifact_id": "seed_tau_payload_candidate_v01.firewall",
        "claim_boundary": CLAIM_BOUNDARY,
        "payload": rel(payload_path),
        "provenance": rel(provenance_path),
        "replay": rel(replay_path),
        "forbidden_endpoint_inputs": FORBIDDEN_ENDPOINT_INPUTS,
        "endpoint_inputs_used": [],
        "endpoint_blind_attestation": True,
        "firewall_passed_for_acceptance": False,
        "reason_not_passed": "candidate firewall attestation exists, but no independent audit has accepted it",
        "score_entry_allowed": False,
    }


def build_hashes(paths: list[Path]) -> dict[str, Any]:
    return {
        "artifact_id": "seed_tau_payload_candidate_v01.hashes",
        "claim_boundary": CLAIM_BOUNDARY,
        "hashes": {rel(path): sha256(path) for path in paths},
        "hash_manifest_accepted": False,
        "score_entry_allowed": False,
    }


def build_summary(payload_path: Path, provenance_path: Path, replay_path: Path, hashes_path: Path, firewall_path: Path) -> dict[str, Any]:
    return {
        "report_id": "tau_cmb_seed_tau_payload_candidate_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "payload": rel(payload_path),
        "provenance": rel(provenance_path),
        "replay": rel(replay_path),
        "hashes": rel(hashes_path),
        "firewall": rel(firewall_path),
        "payload_sha256": sha256(payload_path),
        "payload_values_populated": True,
        "payload_acceptance_allowed": False,
        "domain_certificate_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_TAU_PAYLOAD_CANDIDATE_MATERIALIZED_NOT_ACCEPTED",
        "next_minimal_unblock": "audit_seed_tau_payload_candidate_provenance_hashes_firewall_and_dimension_roles",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Seed Tau Payload Candidate v01

**Doc class:** endpoint-blind seed payload candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact materializes a concrete `seed_tau` candidate payload from the
Tau-side morphological seed descriptor candidate. It is not accepted, does not
certify `seed_tau_CMB in Dom(R_CMB)`, does not evaluate CMB readout survival,
does not assign `A_tau(a,k)`, and does not enter scoring.

## Produced Candidate Files

- payload: `{summary["payload"]}`
- provenance: `{summary["provenance"]}`
- replay: `{summary["replay"]}`
- hashes: `{summary["hashes"]}`
- firewall: `{summary["firewall"]}`

## Status

```text
{summary["status"]}
```

The payload is now concrete enough to audit, but all acceptance permissions
remain closed until provenance, hash binding, endpoint firewall, dimension
roles, support convention, and zero-control evidence pass separate audit.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB seed_tau payload candidate.")
    parser.add_argument("--write-all", action="store_true")
    parser.add_argument("--write-payload", nargs="?", const=str(DEFAULT_PAYLOAD))
    parser.add_argument("--write-provenance", nargs="?", const=str(DEFAULT_PROVENANCE))
    parser.add_argument("--write-replay", nargs="?", const=str(DEFAULT_REPLAY))
    parser.add_argument("--write-hashes", nargs="?", const=str(DEFAULT_HASHES))
    parser.add_argument("--write-firewall", nargs="?", const=str(DEFAULT_FIREWALL))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()

    if args.write_all:
        args.write_payload = args.write_payload or str(DEFAULT_PAYLOAD)
        args.write_provenance = args.write_provenance or str(DEFAULT_PROVENANCE)
        args.write_replay = args.write_replay or str(DEFAULT_REPLAY)
        args.write_hashes = args.write_hashes or str(DEFAULT_HASHES)
        args.write_firewall = args.write_firewall or str(DEFAULT_FIREWALL)
        args.write_summary = args.write_summary or str(DEFAULT_SUMMARY)
        args.write_doc = args.write_doc or str(DEFAULT_DOC)

    descriptor_rows = read_descriptor_rows()
    payload_path = Path(args.write_payload or DEFAULT_PAYLOAD)
    provenance_path = Path(args.write_provenance or DEFAULT_PROVENANCE)
    replay_path = Path(args.write_replay or DEFAULT_REPLAY)
    hashes_path = Path(args.write_hashes or DEFAULT_HASHES)
    firewall_path = Path(args.write_firewall or DEFAULT_FIREWALL)

    if args.write_payload:
        write_payload(payload_path, payload_row(descriptor_rows))
    if args.write_provenance:
        write_json(provenance_path, build_provenance(payload_path, descriptor_rows))
    if args.write_replay:
        write_replay(replay_path)
    if args.write_firewall:
        write_json(firewall_path, build_firewall(payload_path, provenance_path, replay_path))
    if args.write_hashes:
        hash_inputs = [payload_path, provenance_path, replay_path, firewall_path]
        write_json(hashes_path, build_hashes(hash_inputs))

    summary = build_summary(payload_path, provenance_path, replay_path, hashes_path, firewall_path)
    if args.write_summary:
        write_json(Path(args.write_summary), summary)
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
