#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "data/derived/cmb_tau_lensing_payload_replacement_packet_v01.json"

ROUTE = "delta_PP_tau_against_named_fiducial_PP"
FILES = {
    "tau_lensing_response_delta_pp_v01.csv": "numeric_delta_grid",
    "tau_lensing_response_fiducial_pp_reference_v01.json": "fiducial_reference",
    "tau_lensing_response_grid_route_declaration_v01.md": "route_declaration",
    "tau_lensing_response_grid_provenance_v01.json": "route_provenance",
}


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(filename: str, role: str) -> dict[str, Any]:
    active = ROOT / "payloads" / filename
    staging = ROOT / "payload_staging" / ROUTE / filename
    return {
        "role": role,
        "active_payload": rel(active),
        "active_exists": active.exists(),
        "active_sha256": sha256_file(active),
        "replacement_staging": rel(staging),
        "replacement_exists": staging.exists(),
        "replacement_sha256": sha256_file(staging),
        "changed": sha256_file(active) != sha256_file(staging),
    }


def build_packet() -> dict[str, Any]:
    records = [file_record(filename, role) for filename, role in FILES.items()]
    ready = all(record["replacement_exists"] for record in records)
    return {
        "report_id": "cmb_tau_lensing_payload_replacement_packet_v01",
        "claim_boundary": "payload_replacement_packet_only_no_score_no_dark_sector_verdict",
        "selected_route": ROUTE,
        "replacement_ready": ready,
        "replacement_type": "control_or_prior_payload_to_protocol_verified_route_b_candidate",
        "important_boundary": (
            "The replacement promotes a protocol-verified endpoint-blind Route B candidate. "
            "It is not empirical validation of the Tau response and not a dark-sector verdict."
        ),
        "file_records": records,
        "archive_policy": "archive_existing_payload_files_before_replacement_copy",
        "promotion_command": "python3 scripts/promote_tau_lensing_staging_payload.py --route delta_PP_tau_against_named_fiducial_PP --allow-replace --write-report",
        "post_promotion_commands": [
            "make prepare-delta-hash",
            "make intake",
            "make evidence-check",
            "make route-submission-audit",
            "make materialize-replay",
            "make preflight",
            "make score-attempt-guard",
        ],
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
        "created_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "next_required_action": (
            "run_explicit_allow_replace_promotion"
            if ready
            else "repair_missing_staging_replacement_files"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build payload replacement packet for Tau lensing route.")
    parser.add_argument("--write-packet", nargs="?", const=str(DEFAULT_PACKET))
    args = parser.parse_args()
    packet = build_packet()
    text = json.dumps(packet, indent=2, sort_keys=True)
    if args.write_packet:
        path = Path(args.write_packet)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
