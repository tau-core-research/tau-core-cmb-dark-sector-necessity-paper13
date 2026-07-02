#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = (
    "tau_cmb_phi_tau_parent_input_certificate_candidate_v01_candidate_certificates_only_"
    "no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"
)

FIELDS = [
    "candidate_row_id",
    "certificate_component",
    "target_payload_component",
    "candidate_status",
    "evidence_source",
    "candidate_certificate_content",
    "dimension_certificate_status",
    "replay_certificate_status",
    "firewall_certificate_status",
    "acceptance_blocker",
    "scorecard_effect",
    "certificate_candidate_declared",
    "dimension_certificate_supplied",
    "replay_certificate_supplied",
    "firewall_certificate_supplied",
    "certificate_passed",
    "payload_accepted",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "candidate_rows_declared",
    "manifest_rows",
    "candidate_certificate_rows",
    "blocked_rows",
    "dimension_certificates_supplied",
    "replay_certificates_supplied",
    "firewall_certificates_supplied",
    "certificate_passed_rows",
    "accepted_rows",
    "hard_failures_triggered",
    "certificate_candidate_satisfied",
    "scores_computed",
    "cmb_likelihood_available",
    "no_dark_blockers",
    "no_dark_cmb_verdict_allowed",
    "tau_response_claim_allowed",
    "dark_sector_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def candidate_rows() -> list[dict[str, str]]:
    rows = [
        {
            "certificate_component": "certificate_candidate_manifest_identity",
            "target_payload_component": "all_parent_payload_rows",
            "candidate_status": "MANIFEST_CERTIFICATE_CANDIDATE_DECLARED_UNACCEPTED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01",
            "candidate_certificate_content": "declares the candidate certificate inventory for all parent-input payload rows",
            "dimension_certificate_status": "candidate inventory declared but no dimension certificate supplied",
            "replay_certificate_status": "candidate inventory declared but no executable replay supplied",
            "firewall_certificate_status": "candidate inventory declared but no payload firewall certificate supplied",
            "acceptance_blocker": "candidate package is only declared; no certificate can pass",
            "scorecard_effect": "keeps all scoring inputs blocked until candidate certificates are audited",
        },
        {
            "certificate_component": "base_field_dimension_replay_certificate_candidate",
            "target_payload_component": "base_field_state_payload_candidate",
            "candidate_status": "CANDIDATE_CERTIFICATE_DECLARED_UNPASSED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01",
            "candidate_certificate_content": "candidate proof obligation for B_tau dimensions, units, replay, and endpoint-firewall cleanliness",
            "dimension_certificate_status": "candidate declared; no dimensional proof supplied",
            "replay_certificate_status": "candidate declared; no endpoint-blind replay supplied",
            "firewall_certificate_status": "candidate declared; no endpoint-firewall proof supplied",
            "acceptance_blocker": "base-field parent input cannot be accepted before audit and pass",
            "scorecard_effect": "blocks density-amplitude and potential-source scoring inputs",
        },
        {
            "certificate_component": "seed_dimension_replay_certificate_candidate",
            "target_payload_component": "morphological_seed_payload_candidate",
            "candidate_status": "CANDIDATE_CERTIFICATE_DECLARED_UNPASSED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01",
            "candidate_certificate_content": "candidate proof obligation for seed_tau scale, normalization, replay, and endpoint-firewall cleanliness",
            "dimension_certificate_status": "candidate declared; no scale or normalization proof supplied",
            "replay_certificate_status": "candidate declared; no seed replay supplied",
            "firewall_certificate_status": "candidate declared; no endpoint-firewall proof supplied",
            "acceptance_blocker": "seed parent input cannot be accepted before audit and pass",
            "scorecard_effect": "blocks source-activation and readout-compatibility scoring inputs",
        },
        {
            "certificate_component": "operator_dimension_replay_certificate_candidate",
            "target_payload_component": "response_operator_payload_candidate",
            "candidate_status": "CANDIDATE_CERTIFICATE_DECLARED_UNPASSED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01",
            "candidate_certificate_content": "candidate proof obligation for R_tau dimensional mapping, replay, and endpoint-firewall cleanliness",
            "dimension_certificate_status": "candidate declared; no operator dimensional-map proof supplied",
            "replay_certificate_status": "candidate declared; no operator replay supplied",
            "firewall_certificate_status": "candidate declared; no endpoint-firewall proof supplied",
            "acceptance_blocker": "response-operator parent input cannot be accepted before audit and pass",
            "scorecard_effect": "blocks Phi_tau_eff derivation and transfer-kernel scoring inputs",
        },
        {
            "certificate_component": "gauge_normalization_replay_certificate_candidate",
            "target_payload_component": "gauge_normalization_payload_candidate",
            "candidate_status": "CANDIDATE_CERTIFICATE_DECLARED_UNPASSED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01",
            "candidate_certificate_content": "candidate proof obligation for gauge, sign, unit, and normalization lock before endpoint comparison",
            "dimension_certificate_status": "candidate declared; no gauge/unit/normalization proof supplied",
            "replay_certificate_status": "candidate declared; no metadata-lock replay supplied",
            "firewall_certificate_status": "candidate declared; no post-endpoint-normalization firewall proof supplied",
            "acceptance_blocker": "normalization metadata cannot be accepted before audit and pass",
            "scorecard_effect": "blocks shared acoustic, lensing, and growth source comparisons",
        },
        {
            "certificate_component": "payload_firewall_certificate_candidate",
            "target_payload_component": "endpoint_firewall_payload_candidate",
            "candidate_status": "BLOCKED_FIREWALL_CERTIFICATE_UNPASSED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01",
            "candidate_certificate_content": "candidate payload-level firewall certificate for all parent-input rows",
            "dimension_certificate_status": "depends on physical-row dimension certificates that are not supplied",
            "replay_certificate_status": "depends on replay trace that is not supplied",
            "firewall_certificate_status": "candidate declared but firewall certificate is unpassed",
            "acceptance_blocker": "payload-level firewall certificate is not passed",
            "scorecard_effect": "blocks accepting any parent-input payload row",
        },
        {
            "certificate_component": "executable_replay_certificate_candidate",
            "target_payload_component": "provenance_replay_payload_candidate",
            "candidate_status": "BLOCKED_REPLAY_CERTIFICATE_UNPASSED",
            "evidence_source": "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01",
            "candidate_certificate_content": "candidate executable replay certificate for the parent-input candidate package",
            "dimension_certificate_status": "depends on physical-row dimension certificates that are not supplied",
            "replay_certificate_status": "candidate declared but executable replay certificate is unpassed",
            "firewall_certificate_status": "depends on payload firewall trace that is not supplied",
            "acceptance_blocker": "executable replay certificate is not passed",
            "scorecard_effect": "blocks transition from parent-input candidate package into scoring acceptance",
        },
    ]
    return [
        {
            "candidate_row_id": f"TCMBPTPICC01_{index:03d}",
            "certificate_candidate_declared": "true",
            "dimension_certificate_supplied": "false",
            "replay_certificate_supplied": "false",
            "firewall_certificate_supplied": "false",
            "certificate_passed": "false",
            "payload_accepted": "false",
            "hard_failure_triggered": "false",
            "blocks_no_dark_claim": "true",
            "allows_tau_response_claim": "false",
            "allows_dark_sector_verdict": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            **row,
        }
        for index, row in enumerate(rows, start=1)
    ]


def summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_CANDIDATE_V01",
            "candidate_rows_declared": len(rows),
            "manifest_rows": sum(row["candidate_status"].startswith("MANIFEST") for row in rows),
            "candidate_certificate_rows": sum(row["candidate_status"].startswith("CANDIDATE") for row in rows),
            "blocked_rows": sum(row["candidate_status"].startswith("BLOCKED") for row in rows),
            "dimension_certificates_supplied": sum(row["dimension_certificate_supplied"] == "true" for row in rows),
            "replay_certificates_supplied": sum(row["replay_certificate_supplied"] == "true" for row in rows),
            "firewall_certificates_supplied": sum(row["firewall_certificate_supplied"] == "true" for row in rows),
            "certificate_passed_rows": sum(row["certificate_passed"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "certificate_candidate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CERTIFICATE_CANDIDATE_DECLARED_UNPASSED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_certificate_audit_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_certificate_candidate_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Certificate Candidate v01

**Doc class:** parent-input certificate-candidate package
**Status:** certificate candidates declared but unpassed; no certificate pass, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_certificate_candidate.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_certificate_candidate_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_certificate_candidate_summary_v01.csv
```

This artifact declares certificate candidates for the parent-side base-field,
morphological seed, response operator, gauge/normalization metadata,
payload-firewall, and executable-replay rows. It does not pass any certificate
and accepts no parent-side Tau input.

The certificate candidate is not satisfied:

```text
certificate_candidate_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_certificate_audit_v01
```

## Claim Boundary

This artifact declares certificate candidates only. It supplies no dimension,
replay, or firewall certificate, provides no payload-level firewall pass,
accepts no parent-side Tau inputs, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = candidate_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_certificate_candidate_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_certificate_candidate_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_CANDIDATE_V01_BUILT")


if __name__ == "__main__":
    main()
