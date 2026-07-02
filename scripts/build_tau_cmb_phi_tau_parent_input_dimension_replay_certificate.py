#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CLAIM_BOUNDARY = "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01_certificate_requirements_only_no_certificate_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict"

FIELDS = [
    "certificate_row_id",
    "certificate_component",
    "target_payload_component",
    "certificate_status",
    "evidence_source",
    "dimension_certificate_requirement",
    "replay_certificate_requirement",
    "firewall_certificate_requirement",
    "remaining_blocker",
    "scorecard_effect",
    "dimension_certificate_supplied",
    "replay_certificate_supplied",
    "firewall_certificate_supplied",
    "certificate_satisfied",
    "payload_accepted",
    "hard_failure_triggered",
    "blocks_no_dark_claim",
    "allows_tau_response_claim",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "certificate_rows_declared",
    "declared_rows",
    "requirement_rows",
    "blocked_rows",
    "dimension_certificates_supplied",
    "replay_certificates_supplied",
    "firewall_certificates_supplied",
    "satisfied_rows",
    "accepted_rows",
    "hard_failures_triggered",
    "dimension_replay_certificate_satisfied",
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


def certificate_rows() -> list[dict[str, str]]:
    rows = [
        {
            "certificate_component": "certificate_manifest_identity",
            "target_payload_component": "all_parent_payload_rows",
            "certificate_status": "DECLARED_CERTIFICATE_REQUIREMENTS_MANIFEST",
            "evidence_source": "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01",
            "dimension_certificate_requirement": "manifest must list all physical rows requiring dimension or unit checks",
            "replay_certificate_requirement": "manifest must identify the executable replay entry point",
            "firewall_certificate_requirement": "manifest must identify the payload-level firewall certificate",
            "remaining_blocker": "no certificate package is supplied",
            "scorecard_effect": "creates the acceptance contract for parent payload certification",
        },
        {
            "certificate_component": "base_field_dimension_replay_certificate",
            "target_payload_component": "base_field_state_payload_candidate",
            "certificate_status": "REQUIREMENT_DECLARED_CERTIFICATE_MISSING",
            "evidence_source": "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01",
            "dimension_certificate_requirement": "prove dimensional/unit status for B_tau before source construction",
            "replay_certificate_requirement": "replay must rebuild the base-field candidate without endpoint tables",
            "firewall_certificate_requirement": "certificate must prove no acoustic/lensing/score/likelihood-derived fields enter B_tau",
            "remaining_blocker": "dimension certificate, replay, and firewall certificate are missing",
            "scorecard_effect": "keeps density and potential amplitude scoring blocked",
        },
        {
            "certificate_component": "seed_dimension_replay_certificate",
            "target_payload_component": "morphological_seed_payload_candidate",
            "certificate_status": "REQUIREMENT_DECLARED_CERTIFICATE_MISSING",
            "evidence_source": "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01",
            "dimension_certificate_requirement": "prove scale/normalization status for seed_tau before readout comparison",
            "replay_certificate_requirement": "replay must rebuild the seed candidate without endpoint residual shapes",
            "firewall_certificate_requirement": "certificate must prove no CMB peak-shape or residual-derived fields enter seed_tau",
            "remaining_blocker": "scale certificate, replay, and firewall certificate are missing",
            "scorecard_effect": "keeps source activation interpretation blocked",
        },
        {
            "certificate_component": "operator_dimension_replay_certificate",
            "target_payload_component": "response_operator_payload_candidate",
            "certificate_status": "REQUIREMENT_DECLARED_CERTIFICATE_MISSING",
            "evidence_source": "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01",
            "dimension_certificate_requirement": "prove the response-operator dimensional map preserves parent payload dimensions",
            "replay_certificate_requirement": "replay must rebuild operator inputs without score outputs",
            "firewall_certificate_requirement": "certificate must prove no role-score or residual-tuning fields enter R_tau",
            "remaining_blocker": "operator dimensional map certificate, replay, and firewall certificate are missing",
            "scorecard_effect": "keeps Phi_tau_eff derivation blocked",
        },
        {
            "certificate_component": "gauge_normalization_replay_certificate",
            "target_payload_component": "gauge_normalization_payload_candidate",
            "certificate_status": "REQUIREMENT_DECLARED_CERTIFICATE_MISSING",
            "evidence_source": "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01",
            "dimension_certificate_requirement": "prove gauge/sign/unit/normalization lock before endpoint comparison",
            "replay_certificate_requirement": "replay must show metadata lock precedes endpoint evaluation",
            "firewall_certificate_requirement": "certificate must prove no post-endpoint normalization choice enters metadata",
            "remaining_blocker": "metadata lock certificate, replay, and firewall certificate are missing",
            "scorecard_effect": "keeps shared acoustic/lensing source comparison blocked",
        },
        {
            "certificate_component": "payload_firewall_certificate",
            "target_payload_component": "endpoint_firewall_payload_candidate",
            "certificate_status": "BLOCKED_PAYLOAD_FIREWALL_CERTIFICATE_MISSING",
            "evidence_source": "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01",
            "dimension_certificate_requirement": "must reference physical-row dimension certificates",
            "replay_certificate_requirement": "must be reproducible from the replay package",
            "firewall_certificate_requirement": "must certify every payload row against score/residual/likelihood-derived inputs",
            "remaining_blocker": "payload-level firewall certificate is missing",
            "scorecard_effect": "blocks accepting any parent payload input",
        },
        {
            "certificate_component": "executable_replay_certificate",
            "target_payload_component": "provenance_replay_payload_candidate",
            "certificate_status": "BLOCKED_EXECUTABLE_REPLAY_CERTIFICATE_MISSING",
            "evidence_source": "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01",
            "dimension_certificate_requirement": "must replay or reference all physical-row dimension checks",
            "replay_certificate_requirement": "must execute without reading score outputs, residual tables, or likelihood errors",
            "firewall_certificate_requirement": "must provide the input trace used by the firewall certificate",
            "remaining_blocker": "executable replay certificate is missing",
            "scorecard_effect": "blocks transition into scoring input acceptance",
        },
    ]
    return [
        {
            "certificate_row_id": f"TCMBPTPIDRC01_{index:03d}",
            "dimension_certificate_supplied": "false",
            "replay_certificate_supplied": "false",
            "firewall_certificate_supplied": "false",
            "certificate_satisfied": "false",
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
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_DIMENSION_REPLAY_CERTIFICATE_V01",
            "certificate_rows_declared": len(rows),
            "declared_rows": sum(row["certificate_status"].startswith("DECLARED") for row in rows),
            "requirement_rows": sum(row["certificate_status"].startswith("REQUIREMENT") for row in rows),
            "blocked_rows": sum(row["certificate_status"].startswith("BLOCKED") for row in rows),
            "dimension_certificates_supplied": sum(row["dimension_certificate_supplied"] == "true" for row in rows),
            "replay_certificates_supplied": sum(row["replay_certificate_supplied"] == "true" for row in rows),
            "firewall_certificates_supplied": sum(row["firewall_certificate_supplied"] == "true" for row in rows),
            "satisfied_rows": sum(row["certificate_satisfied"] == "true" for row in rows),
            "accepted_rows": sum(row["payload_accepted"] == "true" for row in rows),
            "hard_failures_triggered": sum(row["hard_failure_triggered"] == "true" for row in rows),
            "dimension_replay_certificate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": sum(row["blocks_no_dark_claim"] == "true" for row in rows),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_DIMENSION_REPLAY_CERTIFICATE_DECLARED_UNSUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_certificate_candidate_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01.md").write_text(
        """# Tau CMB Phi Tau Parent Input Dimension Replay Certificate v01

**Doc class:** dimension/replay/firewall certificate requirements
**Status:** certificate requirements declared but unsupplied; no certificate, no payload pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_dimension_replay_certificate.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_dimension_replay_certificate_summary_v01.csv
```

This artifact declares the certificate requirements needed after the
payload-firewall audit: dimension or unit certificates, executable replay
certificates, and payload-level firewall certificates.
It supplies no certificate package and accepts no parent-side Tau input.

The dimension/replay certificate is not satisfied:

```text
dimension_replay_certificate_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_certificate_candidate_v01
```

## Claim Boundary

This artifact declares certificate requirements only. It supplies no dimension,
replay, or firewall certificate, provides no payload-level firewall pass,
accepts no parent-side Tau inputs, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = certificate_rows()
    write_csv(DERIVED / "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01.csv", rows, FIELDS)
    write_csv(
        DERIVED / "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_summary_v01.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER13_TAU_CMB_PHI_TAU_PARENT_INPUT_DIMENSION_REPLAY_CERTIFICATE_V01_BUILT")


if __name__ == "__main__":
    main()
