#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
NORMALIZATION_AUDIT = ROOT / "data/derived/tau_cmb_seed_normalization_replay_candidate_audit_v01.json"
SUPPORT_RULE = ROOT / "data/derived/tau_cmb_seed_support_domain_rule_candidate_v01.csv"
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_seed_zero_control_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_seed_zero_control_summary_v01.json"
DEFAULT_REPLAY = ROOT / "payloads/seed_tau_zero_control_v01.replay.txt"
DEFAULT_DOC = ROOT / "docs/tau_cmb_seed_zero_control_v01.md"

CLAIM_BOUNDARY = (
    "tau_cmb_seed_zero_control_v01_control_candidate_only_"
    "zero_control_not_accepted_no_physical_response_no_domain_certificate_no_readout_no_score_no_verdict"
)

FIELDS = [
    "zero_row_id",
    "component",
    "formal_object",
    "candidate_rule",
    "dependency",
    "status",
    "blocking_reason",
    "next_required_artifact",
    "allows_zero_control_acceptance",
    "allows_physical_response_claim",
    "allows_domain_certificate",
    "allows_readout_evaluation",
    "allows_score_entry",
    "claim_boundary",
]

ROWS = [
    {
        "component": "null_seed_definition",
        "formal_object": "null_seed_tau_CMB := (null_morphology_control, CMB_readout_sector, canonical_scale_v01)",
        "candidate_rule": "define null_seed over the same support and canonical scale convention as seed_tau_CMB",
        "dependency": "support-domain rule candidate and normalization replay candidate audit",
        "status": "NULL_SEED_DECLARED_NOT_ACCEPTED",
        "blocking_reason": "null seed is control evidence only and has not passed zero-control audit",
        "next_required_artifact": "tau_cmb_seed_zero_control_audit_v01",
    },
    {
        "component": "same_domain_convention",
        "formal_object": "null_seed in Tau_CMB_parent_domain",
        "candidate_rule": "null_seed uses the same readout_sector and canonical scale convention as the seed candidate",
        "dependency": "Tau_CMB_parent_domain support rule",
        "status": "DOMAIN_CONTROL_DECLARED_NOT_CERTIFIED",
        "blocking_reason": "support certification and domain certificate remain closed",
        "next_required_artifact": "tau_cmb_seed_zero_control_audit_v01",
    },
    {
        "component": "inactive_activation",
        "formal_object": "Act_tau_CMB[null_seed](a,k) := 0 or inactive",
        "candidate_rule": "null_seed cannot create A_tau_candidate by construction",
        "dependency": "morphological seed activation rule candidate zero-seed limit",
        "status": "INACTIVE_ACTIVATION_DECLARED_NOT_PROVED",
        "blocking_reason": "activation map is still a skeleton and no physical A_tau is accepted",
        "next_required_artifact": "tau_cmb_seed_zero_control_audit_v01",
    },
    {
        "component": "null_readout_role",
        "formal_object": "R_CMB(null_seed) := null_readout",
        "candidate_rule": "null_seed readout is a control baseline, not a fitted CMB residual response",
        "dependency": "seed readout-interface candidate",
        "status": "NULL_READOUT_DECLARED_NOT_EVALUATED",
        "blocking_reason": "R_CMB is not concrete and no readout evaluation is allowed",
        "next_required_artifact": "tau_cmb_seed_zero_control_audit_v01",
    },
    {
        "component": "forbidden_promotion",
        "formal_object": "null_seed != physical Tau response",
        "candidate_rule": "zero-control cannot be promoted as evidence for a physical Tau source or dark-sector verdict",
        "dependency": "claim-boundary firewall",
        "status": "PROMOTION_FORBIDDEN_DECLARED",
        "blocking_reason": "control is deliberately non-physical and non-scoring",
        "next_required_artifact": "tau_cmb_seed_zero_control_audit_v01",
    },
    {
        "component": "quotient_survival_dependency",
        "formal_object": "Null_R(seed_tau_CMB) iff R_CMB(seed_tau_CMB) ~ R_CMB(null_seed)",
        "candidate_rule": "zero-control provides the null side for later quotient survival, not the survival proof itself",
        "dependency": "morphological seed quotient survival test",
        "status": "QUOTIENT_NULL_SIDE_DECLARED_NOT_PROVED",
        "blocking_reason": "quotient equivalence relation and concrete R_CMB are still missing",
        "next_required_artifact": "tau_cmb_seed_zero_control_audit_v01",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "zero_row_id": f"TCMBSZC01_{index:03d}",
            "allows_zero_control_acceptance": "false",
            "allows_physical_response_claim": "false",
            "allows_domain_certificate": "false",
            "allows_readout_evaluation": "false",
            "allows_score_entry": "false",
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


def write_replay(path: Path) -> None:
    text = """# seed_tau zero-control candidate replay v01

Control tuple:

null_seed_tau_CMB = (
  morphology_class = null_morphology_control,
  readout_sector = CMB_readout_sector,
  scale_label = CMB_readout_sector_scale_label_canonical_v01
)

Control rule:

Act_tau_CMB[null_seed_tau_CMB](a,k) := 0 or inactive.
R_CMB(null_seed_tau_CMB) := null_readout.

Boundary:

This is a control object only. It is not a physical Tau response, not a dark
sector source, not a CMB fit, and not a score input.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_summary(table_path: Path, replay_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    normalization_audit_status = None
    if NORMALIZATION_AUDIT.exists():
        normalization_audit_status = json.loads(NORMALIZATION_AUDIT.read_text(encoding="utf-8")).get("status")
    return {
        "report_id": "tau_cmb_seed_zero_control_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "replay": rel(replay_path),
        "zero_rows": len(rows),
        "normalization_audit_status": normalization_audit_status,
        "zero_control_declared": True,
        "zero_control_acceptance_allowed": False,
        "physical_response_claim_allowed": False,
        "domain_certificate_allowed": False,
        "readout_evaluation_allowed": False,
        "score_entry_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": "SEED_ZERO_CONTROL_DECLARED_NOT_ACCEPTED",
        "next_minimal_unblock": "tau_cmb_seed_zero_control_audit_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        f"- `{row['zero_row_id']}` `{row['component']}`: {row['status']} | `{row['formal_object']}`"
        for row in rows
    )
    text = f"""# Tau CMB Seed Zero Control v01

**Doc class:** zero-control candidate
**Status:** {summary["status"]}

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact declares the null-seed / zero-control side required by the CMB
seed route. It does not accept zero-control, claim a physical Tau response,
certify domain membership, evaluate readout, enter scoring, or decide the
dark-sector question.

## Control Replay

```text
{summary["replay"]}
```

## Rows

{row_text}

## Status

```text
{summary["status"]}
```

The zero-control is now declared as a candidate control object over the same
support and canonical scale convention. It remains unaccepted until an audit
checks same-domain convention, inactive activation, null-readout role, and
forbidden promotion.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB seed zero-control candidate.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-replay", nargs="?", const=str(DEFAULT_REPLAY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    replay_path = Path(args.write_replay or DEFAULT_REPLAY)
    if args.write_table:
        write_table(table_path, rows)
    if args.write_replay:
        write_replay(replay_path)
    summary = build_summary(table_path, replay_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
