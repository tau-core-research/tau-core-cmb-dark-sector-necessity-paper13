#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

CONSTRAINT_FIELDS = [
    "constraint_id",
    "cmb_feature",
    "standard_lcdm_role",
    "tau_core_no_dark_requirement",
    "tau_core_response_requirement",
    "necessity_pressure",
    "current_protocol_status",
    "claim_boundary",
]

REQUIREMENT_FIELDS = [
    "requirement_id",
    "cmb_feature",
    "tau_core_module_needed",
    "minimum_deliverable",
    "blocks_no_dark_claim",
    "allows_dark_sector_verdict",
    "next_required_artifact",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "external_references_registered",
    "cmb_constraints_mapped",
    "requirements_written",
    "high_pressure_constraints",
    "no_dark_cmb_verdict_allowed",
    "tau_response_verdict_allowed",
    "overall_status",
    "next_required_artifact",
    "claim_boundary",
]

CLAIM_BOUNDARY = "paper13_cmb_constraint_map_only_no_likelihood_no_dark_sector_verdict"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def constraint_rows() -> list[dict[str, str]]:
    return [
        {
            "constraint_id": "CMB13_001",
            "cmb_feature": "acoustic_peak_phase_and_ratios",
            "standard_lcdm_role": "requires baryon photon plasma plus non-baryonic gravitational potential component",
            "tau_core_no_dark_requirement": "derive identical peak phase and relative heights without an effective non-baryonic source",
            "tau_core_response_requirement": "provide a Tau base-field response that sources early potentials while preserving photon-baryon acoustic physics",
            "necessity_pressure": "HIGH",
            "current_protocol_status": "MAPPED_NOT_SOLVED",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "CMB13_002",
            "cmb_feature": "matter_density_inference_omega_c_h2",
            "standard_lcdm_role": "Planck base-LCDM infers a tightly constrained cold-dark-matter density parameter",
            "tau_core_no_dark_requirement": "replace the inferred Omega_c h^2 role with a no-dark geometric/readout mechanism",
            "tau_core_response_requirement": "map Omega_c h^2 to an effective Tau response amplitude without claiming particle CDM",
            "necessity_pressure": "HIGH",
            "current_protocol_status": "MAPPED_NOT_SOLVED",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "CMB13_003",
            "cmb_feature": "cmb_lensing_power",
            "standard_lcdm_role": "late-time integrated matter distribution lenses the CMB",
            "tau_core_no_dark_requirement": "reproduce lensing amplitude and scale dependence without hidden effective mass",
            "tau_core_response_requirement": "derive an effective Tau source/readout contribution consistent with Planck and ACT lensing",
            "necessity_pressure": "HIGH",
            "current_protocol_status": "MAPPED_NOT_SOLVED",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "CMB13_004",
            "cmb_feature": "damping_tail_and_neff",
            "standard_lcdm_role": "constrains radiation content diffusion damping and recombination-era physics",
            "tau_core_no_dark_requirement": "avoid adding hidden radiation-like degrees of freedom outside allowed bounds",
            "tau_core_response_requirement": "prove Tau response does not overproduce relativistic effective degrees of freedom",
            "necessity_pressure": "MEDIUM",
            "current_protocol_status": "MAPPED_NOT_SOLVED",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "CMB13_005",
            "cmb_feature": "growth_seed_consistency",
            "standard_lcdm_role": "CMB initial conditions extrapolate to large-scale structure and lensing observables",
            "tau_core_no_dark_requirement": "connect Tau morphology/readout seeds to observed structure growth without post-hoc tuning",
            "tau_core_response_requirement": "provide perturbation-level transfer behavior for Tau base-field response",
            "necessity_pressure": "HIGH",
            "current_protocol_status": "MAPPED_NOT_SOLVED",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def requirement_rows(constraints: list[dict[str, str]]) -> list[dict[str, str]]:
    module_by_feature = {
        "acoustic_peak_phase_and_ratios": "tau_cmb_perturbation_source_model",
        "matter_density_inference_omega_c_h2": "tau_effective_density_mapping",
        "cmb_lensing_power": "tau_lensing_transfer_response",
        "damping_tail_and_neff": "tau_radiation_bound_audit",
        "growth_seed_consistency": "tau_growth_transfer_kernel",
    }
    rows: list[dict[str, str]] = []
    for index, row in enumerate(constraints, start=1):
        high_pressure = row["necessity_pressure"] == "HIGH"
        rows.append(
            {
                "requirement_id": f"TCMB13_{index:03d}",
                "cmb_feature": row["cmb_feature"],
                "tau_core_module_needed": module_by_feature[row["cmb_feature"]],
                "minimum_deliverable": "equation_level_mapping_plus_known_LCDM_limit_or_explicit_failure_mode",
                "blocks_no_dark_claim": str(high_pressure).lower(),
                "allows_dark_sector_verdict": "false",
                "next_required_artifact": "tau_cmb_effective_source_equation_v01",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(
    references: list[dict[str, str]],
    constraints: list[dict[str, str]],
    requirements: list[dict[str, str]],
) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "PAPER13_CMB_CONSTRAINT_MAP_V01",
            "external_references_registered": len(references),
            "cmb_constraints_mapped": len(constraints),
            "requirements_written": len(requirements),
            "high_pressure_constraints": sum(row["necessity_pressure"] == "HIGH" for row in constraints),
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_verdict_allowed": "false",
            "overall_status": "CMB_CONSTRAINTS_MAP_TO_TAU_RESPONSE_REQUIREMENTS_VERDICT_BLOCKED",
            "next_required_artifact": "tau_cmb_effective_source_equation_v01",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "cmb_constraint_map_v01.md").write_text(
        """# CMB Constraint Map v01

**Doc class:** CMB-facing Tau Core dark-sector necessity scaffold
**Reader role:** Paper 13 protocol reader
**Status:** constraint map only; no CMB likelihood and no verdict

This artifact maps CMB observables to Tau Core requirements. It does not
compute CMB spectra, fit Planck/ACT likelihoods, or decide whether Tau Core
requires a dark-sector response.

The current map identifies high-pressure CMB constraints where a completely
no-dark Tau Core cosmology is difficult to defend unless it can reproduce the
same acoustic, lensing, and growth roles without an effective non-baryonic
source.

## Outputs

```text
data/derived/cmb_constraint_map_v01.csv
data/derived/tau_core_dark_sector_requirement_map_v01.csv
data/derived/paper13_readiness_summary_v01.csv
```

## Claim Boundary

The artifact is a requirement map. It contains no CMB likelihood, no fitted
parameters, no Tau Core validation, and no dark-sector verdict.
""",
        encoding="utf-8",
    )


def main() -> None:
    references = read_csv(SOURCE / "cmb_external_reference_manifest_v01.csv")
    constraints = constraint_rows()
    requirements = requirement_rows(constraints)
    write_csv(DERIVED / "cmb_constraint_map_v01.csv", constraints, CONSTRAINT_FIELDS)
    write_csv(DERIVED / "tau_core_dark_sector_requirement_map_v01.csv", requirements, REQUIREMENT_FIELDS)
    write_csv(DERIVED / "paper13_readiness_summary_v01.csv", summary(references, constraints, requirements), SUMMARY_FIELDS)
    write_doc()
    print("PAPER13_CMB_CONSTRAINT_MAP_V01_BUILT")


if __name__ == "__main__":
    main()
