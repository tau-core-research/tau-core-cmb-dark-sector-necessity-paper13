#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHECKER_ACCEPTANCE_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_checker_execution_replay_acceptance_audit_v01.csv"
CHECKER_ACCEPTANCE_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_checker_execution_replay_acceptance_audit_summary_v01.json"
RULE_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_certificate_rule_execution_refresh_v01.csv"
TRACE_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_trace_acceptance_refresh_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_supply_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_supply_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_supply_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_supply_v01_"
    "certificate_level_checker_replay_candidate_supplied_semantic_certificate_only_"
    "no_domain_acceptance_no_physical_R_CMB_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "certificate_level_checker_replay_supply_row_id",
    "source_checker_execution_replay_acceptance_row_id",
    "certificate_area",
    "checker_name",
    "certificate_level_replay_artifact",
    "certificate_level_replay_hash_artifact",
    "certificate_level_replay_artifact_supplied",
    "hash_supplied",
    "hash_matches",
    "structural_checker_replay_present",
    "structural_checker_execution_succeeded",
    "all_traces_accepted",
    "certificate_rule_executable",
    "certificate_level_replay_body_present",
    "certificate_pass_candidate",
    "certificate_passed_after_supply",
    "domain_object_accepted",
    "allows_physical_R_CMB",
    "allows_score_entry",
    "allows_likelihood",
    "allows_dark_sector_verdict",
    "supply_status",
    "blocking_reason",
    "claim_boundary",
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_chain_clean() -> bool:
    if not CHECKER_ACCEPTANCE_SUMMARY.exists():
        return False
    summary = load_json(CHECKER_ACCEPTANCE_SUMMARY)
    return (
        summary.get("status") == "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CHECKER_EXECUTION_REPLAY_ACCEPTANCE_AUDITED_REJECTED_CERTIFICATE_LEVEL_REPLAY_REQUIRED"
        and summary.get("input_chain_clean") is True
        and summary.get("checker_execution_replay_acceptance_rows") == 7
        and summary.get("checker_replay_present_rows") == 7
        and summary.get("checker_execution_succeeded_rows") == 7
        and summary.get("certificate_passed_rows") == 0
        and summary.get("score_entry_allowed") is False
        and summary.get("likelihood_allowed") is False
        and summary.get("dark_sector_verdict_allowed") is False
    )


def traces_for(area: str, checker: str) -> list[dict[str, str]]:
    return [row for row in read_csv(TRACE_TABLE) if row["certificate_area"] == area and row["checker_name"] == checker]


def rule_for(area: str, checker: str) -> dict[str, str]:
    for row in read_csv(RULE_TABLE):
        if row["certificate_area"] == area and row["checker_name"] == checker:
            return row
    return {}


def replay_artifact_for(row: dict[str, str]) -> Path:
    return ROOT / "semantic_evidence_certificate_level_checker_replays" / row["certificate_area"] / f"{row['checker_name']}_certificate_level_replay_v01.json"


def replay_payload(row: dict[str, str]) -> dict[str, Any]:
    traces = traces_for(row["certificate_area"], row["checker_name"])
    rule = rule_for(row["certificate_area"], row["checker_name"])
    all_traces_accepted = len(traces) > 0 and all(trace["trace_accepted"] == "true" for trace in traces)
    rule_executable = rule.get("certificate_rule_executable") == "true"
    structural_replay_ok = (
        row["checker_replay_present"] == "true"
        and row["checker_output_hash_matches"] == "true"
        and row["checker_execution_succeeded"] == "true"
    )
    pass_candidate = all_traces_accepted and rule_executable and structural_replay_ok
    return {
        "artifact_id": row["checker_execution_replay_acceptance_row_id"],
        "artifact_status": "CERTIFICATE_LEVEL_CHECKER_REPLAY_CANDIDATE_SUPPLIED_SEMANTIC_ONLY",
        "claim_boundary": CLAIM_BOUNDARY,
        "certificate_area": row["certificate_area"],
        "checker_name": row["checker_name"],
        "certificate_level_replay_body": {
            "scope": "semantic certificate-level checker replay only",
            "premises": {
                "all_semantic_traces_accepted": all_traces_accepted,
                "certificate_rule_executable": rule_executable,
                "structural_checker_replay_present": row["checker_replay_present"] == "true",
                "checker_output_hash_matches": row["checker_output_hash_matches"] == "true",
                "checker_execution_succeeded": row["checker_execution_succeeded"] == "true",
                "endpoint_blind": True,
            },
            "accepted_trace_rows": [
                {
                    "semantic_evidence_field": trace["semantic_evidence_field"],
                    "trace_acceptance_refresh_row_id": trace["trace_acceptance_refresh_row_id"],
                    "component_rows": trace["component_rows"],
                    "component_accepted_rows": trace["component_accepted_rows"],
                }
                for trace in traces
            ],
            "steps": [
                "Replay the accepted semantic evidence traces for the checker.",
                "Confirm that the checker-level certificate rule is executable from those traces.",
                "Bind the structural checker replay by hash and checker identity.",
                "Promote only the semantic certificate-level checker replay candidate; do not promote physical readout or score.",
            ],
            "conclusion": (
                "The checker has a semantic certificate-level replay candidate when accepted traces, executable rule, "
                "and structural checker replay are all present. This is not a physical R_CMB, likelihood, score, or verdict."
            ),
        },
        "certificate_pass_candidate": pass_candidate,
        "certificate_passed_after_supply": False,
        "domain_object_accepted": False,
        "physical_R_CMB_materialized": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "next_required_step": "audit certificate-level checker replay candidates for semantic certificate pass",
    }


def supply_rows(write_artifacts: bool) -> list[dict[str, str]]:
    if not input_chain_clean():
        raise SystemExit("checker execution replay acceptance summary is not clean")
    rows: list[dict[str, str]] = []
    for source in read_csv(CHECKER_ACCEPTANCE_TABLE):
        index = len(rows) + 1
        artifact = replay_artifact_for(source)
        hash_artifact = artifact.with_suffix(".hashes.json")
        if write_artifacts:
            write_json(artifact, replay_payload(source))
            write_json(
                hash_artifact,
                {
                    "target": rel(artifact),
                    "sha256": sha256(artifact),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "certificate_pass_candidate": True,
                    "certificate_passed_after_supply": False,
                    "score_entry_allowed": False,
                    "likelihood_allowed": False,
                    "dark_sector_verdict_allowed": False,
                },
            )
        supplied = artifact.exists()
        hash_supplied = hash_artifact.exists()
        hash_matches = supplied and hash_supplied and load_json(hash_artifact).get("sha256") == sha256(artifact)
        payload = load_json(artifact) if supplied else {}
        body_present = bool(payload.get("certificate_level_replay_body"))
        traces = traces_for(source["certificate_area"], source["checker_name"])
        rule = rule_for(source["certificate_area"], source["checker_name"])
        all_traces_accepted = len(traces) > 0 and all(trace["trace_accepted"] == "true" for trace in traces)
        rule_executable = rule.get("certificate_rule_executable") == "true"
        pass_candidate = payload.get("certificate_pass_candidate") is True
        rows.append(
            {
                "certificate_level_checker_replay_supply_row_id": f"TCMBCDSEMCERTREPLAY01_{index:03d}",
                "source_checker_execution_replay_acceptance_row_id": source["checker_execution_replay_acceptance_row_id"],
                "certificate_area": source["certificate_area"],
                "checker_name": source["checker_name"],
                "certificate_level_replay_artifact": rel(artifact),
                "certificate_level_replay_hash_artifact": rel(hash_artifact),
                "certificate_level_replay_artifact_supplied": str(supplied).lower(),
                "hash_supplied": str(hash_supplied).lower(),
                "hash_matches": str(hash_matches).lower(),
                "structural_checker_replay_present": source["checker_replay_present"],
                "structural_checker_execution_succeeded": source["checker_execution_succeeded"],
                "all_traces_accepted": str(all_traces_accepted).lower(),
                "certificate_rule_executable": str(rule_executable).lower(),
                "certificate_level_replay_body_present": str(body_present).lower(),
                "certificate_pass_candidate": str(pass_candidate).lower(),
                "certificate_passed_after_supply": "false",
                "domain_object_accepted": "false",
                "allows_physical_R_CMB": "false",
                "allows_score_entry": "false",
                "allows_likelihood": "false",
                "allows_dark_sector_verdict": "false",
                "supply_status": (
                    "CERTIFICATE_LEVEL_CHECKER_REPLAY_CANDIDATE_SUPPLIED_NOT_AUDITED"
                    if supplied and hash_matches and body_present and pass_candidate
                    else "CERTIFICATE_LEVEL_CHECKER_REPLAY_SUPPLY_BLOCKED"
                ),
                "blocking_reason": (
                    "certificate-level replay candidate supplied; semantic certificate-pass audit remains downstream"
                    if supplied and hash_matches and body_present and pass_candidate
                    else "requires supplied replay artifact, matching hash, accepted traces, executable rule, and structural checker replay"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "report_id": "tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_supply_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_checker_execution_replay_acceptance_table": rel(CHECKER_ACCEPTANCE_TABLE),
        "input_checker_execution_replay_acceptance_summary": rel(CHECKER_ACCEPTANCE_SUMMARY),
        "input_chain_clean": input_chain_clean(),
        "certificate_level_checker_replay_supply_rows": len(rows),
        "certificate_level_replay_artifact_supplied_rows": sum(row["certificate_level_replay_artifact_supplied"] == "true" for row in rows),
        "hash_matched_rows": sum(row["hash_matches"] == "true" for row in rows),
        "all_traces_accepted_rows": sum(row["all_traces_accepted"] == "true" for row in rows),
        "certificate_rule_executable_rows": sum(row["certificate_rule_executable"] == "true" for row in rows),
        "certificate_level_replay_body_present_rows": sum(row["certificate_level_replay_body_present"] == "true" for row in rows),
        "certificate_pass_candidate_rows": sum(row["certificate_pass_candidate"] == "true" for row in rows),
        "certificate_passed_after_supply_rows": 0,
        "accepted_domain_objects": 0,
        "physical_R_CMB_materialized": False,
        "concrete_R_CMB_allowed": False,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CERTIFICATE_LEVEL_CHECKER_REPLAY_CANDIDATES_SUPPLIED"
            if input_chain_clean()
            and len(rows) == 7
            and all(row["certificate_pass_candidate"] == "true" for row in rows)
            else "CMB_CERTIFICATE_SEMANTIC_EVIDENCE_CERTIFICATE_LEVEL_CHECKER_REPLAY_SUPPLY_BLOCKED"
        ),
        "next_minimal_unblock": "tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_acceptance_audit_v01",
    }


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    text = f"""# Tau CMB Certificate Semantic Evidence Certificate-Level Checker Replay Supply v01

**Doc class:** semantic evidence certificate-level checker replay supply
**Reader role:** Paper 13 / CMB scoring route implementer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This step supplies certificate-level checker replay candidates for seven checker
rules using accepted semantic traces, executable checker rules, and hash-bound
structural checker replay. It does not accept domain objects, materialize
physical R_CMB, run scoring, evaluate likelihoods, or decide the dark-sector
question.

## Summary

```text
certificate_level_checker_replay_supply_rows={summary["certificate_level_checker_replay_supply_rows"]}
certificate_level_replay_artifact_supplied_rows={summary["certificate_level_replay_artifact_supplied_rows"]}
hash_matched_rows={summary["hash_matched_rows"]}
all_traces_accepted_rows={summary["all_traces_accepted_rows"]}
certificate_rule_executable_rows={summary["certificate_rule_executable_rows"]}
certificate_level_replay_body_present_rows={summary["certificate_level_replay_body_present_rows"]}
certificate_pass_candidate_rows={summary["certificate_pass_candidate_rows"]}
certificate_passed_after_supply_rows={summary["certificate_passed_after_supply_rows"]}
score_entry_allowed={summary["score_entry_allowed"]}
likelihood_allowed={summary["likelihood_allowed"]}
dark_sector_verdict_allowed={summary["dark_sector_verdict_allowed"]}
```

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Supply Tau CMB certificate-level checker replay candidates.")
    parser.add_argument("--write-artifacts", action="store_true")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = supply_rows(write_artifacts=args.write_artifacts)
    table_path = Path(args.write_table) if args.write_table else DEFAULT_TABLE
    summary = build_summary(table_path, rows)
    if args.write_table:
        write_table(table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
