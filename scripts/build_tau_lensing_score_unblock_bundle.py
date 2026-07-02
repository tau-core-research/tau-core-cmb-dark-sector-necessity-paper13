#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "scripts/decide_tau_lensing_score_readiness.py"
TODO = ROOT / "scripts/extract_tau_lensing_scoring_todo.py"
PACK = ROOT / "scripts/build_tau_lensing_route_evidence_pack.py"
FULFILLMENT = ROOT / "scripts/build_tau_lensing_scoring_input_fulfillment_packet.py"
DEFAULT_BUNDLE = ROOT / "data/derived/cmb_tau_lensing_score_unblock_bundle_v01.json"


def run_json(args: list[str]) -> dict[str, Any]:
    completed = subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def build_bundle() -> dict[str, Any]:
    readiness = run_json([sys.executable, str(READINESS), "--write-decision"])
    todo = run_json([sys.executable, str(TODO), "--write-todo"])
    pack = run_json([sys.executable, str(PACK), "--write-pack"])
    fulfillment = run_json([sys.executable, str(FULFILLMENT), "--write-packet"])
    return {
        "report_id": "tau_lensing_score_unblock_bundle_v01",
        "claim_boundary": "score_unblock_bundle_only_no_score_run_no_dark_sector_verdict",
        "readiness_decision": readiness.get("readiness_decision"),
        "blocking_layer": readiness.get("blocking_layer"),
        "act_environment_ready": readiness.get("act_environment_ready"),
        "selected_route_count": readiness.get("selected_route_count"),
        "projection_replay_written": readiness.get("projection_replay_written"),
        "preflight_ready": readiness.get("preflight_ready"),
        "pipeline_ready": readiness.get("pipeline_ready"),
        "todo_status": todo.get("todo_status"),
        "missing_files_by_route": todo.get("missing_files_by_route"),
        "route_options": pack.get("route_options"),
        "fulfillment_packet_id": fulfillment.get("report_id"),
        "fulfillment_current_blocker": fulfillment.get("current_blocker"),
        "fulfillment_route_packets": fulfillment.get("route_packets"),
        "forbidden_shortcuts": pack.get("forbidden_shortcuts"),
        "next_commands": [
            "make score-fulfillment",
            "make payload-checklist",
            "make staging-promote-direct-dry-run or make staging-promote-delta-dry-run or make staging-promote-failure-dry-run",
            "make staging-promote-direct or make staging-promote-delta or make staging-promote-failure after dry-run promotion is ready",
            "make route-pack",
            "make prepare-direct-hash or make prepare-delta-hash after the selected numeric grid exists",
            "make intake",
            "make evidence-check",
            "make route-submission-audit",
            "make materialize-replay",
            "make preflight",
            "make score-readiness",
            "make score-attempt-guard",
            "make score-report only if score-attempt-guard allows",
            "make score-output-audit",
        ],
        "score_run": False,
        "dark_sector_verdict": False,
        "next_required_action": readiness.get("next_required_action"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the compact Tau lensing score unblock bundle.")
    parser.add_argument(
        "--write-bundle",
        default=None,
        nargs="?",
        const=str(DEFAULT_BUNDLE),
        help=f"Optional JSON bundle path. Defaults to {DEFAULT_BUNDLE} when passed without a path.",
    )
    args = parser.parse_args()

    bundle = build_bundle()
    text = json.dumps(bundle, indent=2, sort_keys=True)
    if args.write_bundle:
        path = Path(args.write_bundle)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
