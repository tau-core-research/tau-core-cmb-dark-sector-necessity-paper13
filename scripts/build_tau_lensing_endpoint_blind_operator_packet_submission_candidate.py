#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUBMISSION = ROOT / "payloads/cmb_tau_lensing_endpoint_blind_operator_packet_submission_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/cmb_tau_lensing_endpoint_blind_operator_packet_submission_candidate_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/cmb_tau_lensing_endpoint_blind_operator_packet_submission_candidate_v01.md"


FIELDNAMES = [
    "packet_slot",
    "supplied_object",
    "evidence_artifact",
    "provenance_hash",
    "endpoint_blind_attestation",
    "dimension_status",
    "zero_source_status",
    "replay_status",
    "firewall_status",
    "notes",
]


ROWS = [
    {
        "packet_slot": "source_domain",
        "supplied_object": "CANDIDATE_NOT_ACCEPTED: Phi_tau_eff(a,k) source domain and lensing interface; not yet Phi_lens_tau(a,k) operator domain",
        "evidence_artifact": "payloads/tau_lensing_phi_source_lensing_interface_v01.md",
        "endpoint_blind_attestation": "candidate source/interface artifact states forbidden ACT/Planck residual shortcut and no score use",
        "dimension_status": "PARTIAL_SOURCE_INTERFACE_ONLY",
        "zero_source_status": "NOT_APPLICABLE_TO_SOURCE_DOMAIN_ONLY",
        "replay_status": "BLOCKED_NO_FULL_OPERATOR_REPLAY",
        "firewall_status": "PARTIAL_PAYLOAD_ATTESTATION_ONLY",
        "notes": "usable as source-domain candidate for content audit, not accepted physical projection source",
    },
    {
        "packet_slot": "projection_equation",
        "supplied_object": "CANDIDATE_NOT_ACCEPTED: Route B L-space equation delta_PP_tau(L)=normalization*parent_tau_source_value(L), not full a,k projection integral",
        "evidence_artifact": "payloads/tau_lensing_response_grid_provenance_v01.json",
        "endpoint_blind_attestation": "provenance states no endpoint fit, no residual tuning, no score tuning, and no verdict tuning",
        "dimension_status": "PARTIAL_L_SPACE_CANDIDATE_ONLY",
        "zero_source_status": "CANDIDATE_ZERO_LIMIT_STATED_FOR_LINEAR_PARENT_SOURCE",
        "replay_status": "GRID_REPLAY_ARTIFACT_EXISTS_FOR_L_SPACE_CANDIDATE",
        "firewall_status": "PARTIAL_PROVENANCE_ATTESTATION_ONLY",
        "notes": "does not supply Projection_PP[Phi_lens_tau](L) kernel from a,k support",
    },
    {
        "packet_slot": "kernel_measure",
        "supplied_object": "BLOCKED: no K_tau_PP(L; a,k)dmu(a,k) supplied; only L-space Route B materialization provenance exists",
        "evidence_artifact": "docs/cmb_tau_lensing_projection_kernel_measure_spec_scaffold_v01.md",
        "endpoint_blind_attestation": "kernel/measure scaffold forbids endpoint-selected support, L mapping, units, or score-shaped kernel",
        "dimension_status": "BLOCKED_NO_KERNEL_MEASURE",
        "zero_source_status": "BLOCKED_DEPENDS_ON_KERNEL_MEASURE",
        "replay_status": "BLOCKED_NO_AK_TO_L_KERNEL_REPLAY",
        "firewall_status": "BLOCKED_UNTIL_KERNEL_POPULATED",
        "notes": "intentional blocker row; keeps candidate from becoming accepted operator packet",
    },
    {
        "packet_slot": "normalization",
        "supplied_object": "BLOCKED: N_projection_physical not supplied; post-score alpha_star forbidden",
        "evidence_artifact": "docs/cmb_tau_lensing_projection_normalization_spec_scaffold_v01.md",
        "endpoint_blind_attestation": "normalization spec forbids post-score alpha_star, ACT/Planck residual minimization, reduced chi2 tuning, and verdict preference",
        "dimension_status": "BLOCKED_NO_N_PROJECTION_PHYSICAL",
        "zero_source_status": "BLOCKED_DEPENDS_ON_FINITE_NORMALIZATION",
        "replay_status": "BLOCKED_NO_ACCEPTED_NORMALIZATION_REPLAY",
        "firewall_status": "BLOCKED_UNTIL_NORMALIZATION_POPULATED",
        "notes": "candidate cannot be score eligible until a finite endpoint-blind normalization is supplied",
    },
    {
        "packet_slot": "output_replay",
        "supplied_object": "CANDIDATE_NOT_ACCEPTED: 3000-row delta_PP_tau grid replay exists for Route B L-space candidate",
        "evidence_artifact": "payloads/tau_lensing_pp_grid_projection_replay_v01.json",
        "endpoint_blind_attestation": "replay artifact records score_computed=false and no dark-sector verdict",
        "dimension_status": "PARTIAL_GRID_SHAPE_FINITE_ONLY",
        "zero_source_status": "PARTIAL_DEPENDS_ON_ROUTE_B_LINEAR_SOURCE_STATEMENT",
        "replay_status": "CANDIDATE_REPLAY_EXISTS_NOT_PHYSICAL_OPERATOR_ACCEPTANCE",
        "firewall_status": "BLOCKED_NEEDS_POST_POPULATION_FIREWALL",
        "notes": "adapter replay B_ACT @ grid is not the physical Phi_lens_tau-to-PP operator",
    },
    {
        "packet_slot": "zero_source_limit",
        "supplied_object": "CANDIDATE_NOT_ACCEPTED: Route B provenance states parent_tau_source_value -> 0 implies delta_PP_tau -> 0 under linear adapter",
        "evidence_artifact": "payloads/tau_lensing_response_grid_provenance_v01.json",
        "endpoint_blind_attestation": "known-limit statement is source-side and not inferred from scored residuals",
        "dimension_status": "PARTIAL_L_SPACE_ROUTE_ONLY",
        "zero_source_status": "PARTIAL_CANDIDATE_NOT_FULL_OPERATOR_PROOF",
        "replay_status": "BLOCKED_NO_ACCEPTED_ZERO_SOURCE_REPLAY",
        "firewall_status": "PARTIAL_PROVENANCE_ATTESTATION_ONLY",
        "notes": "does not discharge zero-source limit for missing K_tau_PP and N_projection_physical",
    },
    {
        "packet_slot": "dimension_sign_audit",
        "supplied_object": "BLOCKED: dimension/sign audit schema exists but is not filled for a full projection operator",
        "evidence_artifact": "docs/cmb_tau_lensing_projection_dimension_sign_audit_scaffold_v01.md",
        "endpoint_blind_attestation": "audit scaffold requires units/signs before materialization and forbids post-score inference",
        "dimension_status": "AUDIT_SCHEMA_DECLARED_NOT_FILLED",
        "zero_source_status": "BLOCKED_DEPENDS_ON_OPERATOR_AUDIT",
        "replay_status": "BLOCKED_DEPENDS_ON_REPLAY_AUDIT",
        "firewall_status": "BLOCKED_DEPENDS_ON_POST_POPULATION_FIREWALL",
        "notes": "intentional blocker row",
    },
    {
        "packet_slot": "post_population_firewall",
        "supplied_object": "BLOCKED: post-population firewall spec exists but cannot pass until operator, kernel, normalization, and output grid values are populated",
        "evidence_artifact": "docs/cmb_tau_lensing_projection_post_population_firewall_spec_scaffold_v01.md",
        "endpoint_blind_attestation": "firewall spec requires proof after values are populated that no endpoint residual, score, or verdict preference shaped them",
        "dimension_status": "NOT_APPLICABLE_FIREWALL_ROW",
        "zero_source_status": "NOT_APPLICABLE_FIREWALL_ROW",
        "replay_status": "BLOCKED_UNTIL_VALUES_POPULATED",
        "firewall_status": "POST_POPULATION_FIREWALL_SPEC_DECLARED_NOT_RUN",
        "notes": "intentional blocker row",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def sha256_rel(path_text: str) -> str:
    path = ROOT / path_text
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows_with_hashes() -> list[dict[str, str]]:
    rows = []
    for row in ROWS:
        item = dict(row)
        item["provenance_hash"] = sha256_rel(item["evidence_artifact"])
        rows.append(item)
    return rows


def write_submission(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def build_summary(path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    blocked_rows = [
        row["packet_slot"]
        for row in rows
        if "BLOCKED" in row["supplied_object"] or "BLOCKED" in row["dimension_status"] or "BLOCKED" in row["firewall_status"]
    ]
    candidate_rows = [row["packet_slot"] for row in rows if "CANDIDATE_NOT_ACCEPTED" in row["supplied_object"]]
    return {
        "report_id": "cmb_tau_lensing_endpoint_blind_operator_packet_submission_candidate_summary_v01",
        "claim_boundary": "endpoint_blind_operator_packet_submission_candidate_only_no_operator_acceptance_no_physical_score_no_dark_sector_verdict",
        "submission": rel(path),
        "status": "SUBMISSION_CANDIDATE_SUPPLIED_FOR_AUDIT_NOT_ACCEPTED",
        "rows": len(rows),
        "candidate_rows": candidate_rows,
        "blocked_rows": sorted(set(blocked_rows)),
        "acceptance": False,
        "score_run": False,
        "physical_tau_score_run": False,
        "dark_sector_verdict": False,
    }


def write_doc(summary: dict[str, Any], path: Path) -> None:
    candidates = "\n".join(f"- `{item}`" for item in summary["candidate_rows"]) or "- none"
    blockers = "\n".join(f"- `{item}`" for item in summary["blocked_rows"]) or "- none"
    text = f"""# CMB Tau Lensing Endpoint-Blind Operator Packet Submission Candidate v01

**Doc class:** endpoint-blind operator packet submission candidate
**Reader role:** Paper 13 Tau-grid implementer
**Status:** supplied for audit; not accepted; not score eligible
**Canonical parent:** `docs/cmb_tau_lensing_endpoint_blind_operator_packet_submission_template_v01.md`

## Claim Boundary

```text
{summary["claim_boundary"]}
```

## Submission Path

```text
{summary["submission"]}
```

## Candidate Rows

{candidates}

## Blocking Rows

{blockers}

## Interpretation

This candidate packages existing endpoint-blind-looking artifacts so the receipt
and content-audit path can run. It intentionally preserves blockers for the
missing full `K_tau_PP(L; a,k)dmu(a,k)` projection kernel, physical projection
normalization, dimension/sign audit, and post-population firewall. It does not
accept the physical Tau-route and does not allow scoring.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build endpoint-blind operator packet submission candidate.")
    parser.add_argument("--write-submission", nargs="?", const=str(DEFAULT_SUBMISSION))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = rows_with_hashes()
    submission_path = Path(args.write_submission or DEFAULT_SUBMISSION)
    if args.write_submission:
        write_submission(submission_path, rows)
    summary = build_summary(submission_path, rows)
    if args.write_summary:
        path = Path(args.write_summary)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    if args.write_doc:
        write_doc(summary, Path(args.write_doc))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
