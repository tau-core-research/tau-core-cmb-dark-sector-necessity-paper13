#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / "data/derived/tau_cmb_single_pass_derivation_spine_v01.csv"
DEFAULT_SUMMARY = ROOT / "data/derived/tau_cmb_single_pass_derivation_spine_summary_v01.json"
DEFAULT_DOC = ROOT / "docs/tau_cmb_single_pass_derivation_spine_v01.md"

INPUTS = {
    "cosmology_spine": ROOT / "data/derived/tau_cmb_cosmology_derivation_spine_summary_v01.json",
    "source_grounding": ROOT / "data/derived/tau_cmb_source_grounding_gate_summary_v01.json",
    "bundle_closure_audit": ROOT / "data/derived/tau_cmb_readout_role_coordinate_bundle_closure_audit_v01.json",
    "scoring_gap_matrix": ROOT / "data/derived/tau_cmb_scoring_input_gap_matrix_summary_v01.json",
    "carrier_certificate_audit": ROOT / "data/derived/tau_cmb_concrete_R_CMB_carrier_certificate_audit_v01.json",
    "carrier_domain_predicate_audit": ROOT / "data/derived/tau_cmb_carrier_domain_predicate_candidate_audit_v01.json",
}

CLAIM_BOUNDARY = (
    "tau_cmb_single_pass_derivation_spine_v01_route_spine_only_"
    "not_a_proof_no_concrete_R_CMB_no_score_no_likelihood_no_dark_sector_verdict"
)

FIELDS = [
    "step_id",
    "route_layer",
    "mathematical_object",
    "single_pass_statement",
    "claim_level",
    "current_status",
    "required_to_promote",
    "blocks_scoring_reason",
    "allows_score_entry",
    "allows_dark_sector_verdict",
    "claim_boundary",
]

ROWS = [
    {
        "route_layer": "seed_and_root_context",
        "mathematical_object": "m_tau^seed, CMB readout context",
        "single_pass_statement": "Start from a Tau morphological seed/readout context that is declared independently of endpoint residuals.",
        "claim_level": "CANDIDATE_CONTEXT",
        "current_status": "SEED_CONTEXT_DECLARED_NOT_ACCEPTED",
        "required_to_promote": "accepted seed descriptor, activation rule, quotient survival, and endpoint firewall",
        "blocks_scoring_reason": "seed is not yet an accepted source/domain object",
    },
    {
        "route_layer": "carrier",
        "mathematical_object": "C_CMB^seed",
        "single_pass_statement": "A CMB Tau object may enter the route only if it is a well-formed role-space representative.",
        "claim_level": "PREDICATE_CANDIDATE",
        "current_status": "CARRIER_PREDICATE_DECLARED_NOT_PROVED",
        "required_to_promote": "proof or executable checker for WellFormedRoleRepresentative_CMB",
        "blocks_scoring_reason": "carrier membership is not certified",
    },
    {
        "route_layer": "domain",
        "mathematical_object": "Dom(R_CMB)",
        "single_pass_statement": "Domain membership requires parent-side support, normalization, firewall, and replay evidence.",
        "claim_level": "PREDICATE_CANDIDATE",
        "current_status": "DOMAIN_RULE_DECLARED_NOT_CERTIFIED",
        "required_to_promote": "joint support-domain, normalization, evidence-payload, null-control, and firewall certificate",
        "blocks_scoring_reason": "readout input domain is not accepted",
    },
    {
        "route_layer": "concrete_readout",
        "mathematical_object": "R_CMB: Dom(R_CMB) -> V_CMB^roles",
        "single_pass_statement": "The concrete readout map must take certified Tau-side objects to the CMB role-coordinate codomain.",
        "claim_level": "REQUIRED_OBJECT_NOT_MATERIALIZED",
        "current_status": "CONCRETE_R_CMB_BLOCKED",
        "required_to_promote": "materialized map, codomain convention, dimension/gauge replay, and endpoint firewall rerun",
        "blocks_scoring_reason": "no concrete Tau-to-CMB readout exists",
    },
    {
        "route_layer": "effective_source",
        "mathematical_object": "rho_tau_eff(a,k) := A_tau(a,k) rho_ref(a)",
        "single_pass_statement": "A Tau-side effective source may fill the density role only if A_tau is derived endpoint-blind and dimensionless.",
        "claim_level": "CONDITIONAL_ROLE_FORMULA",
        "current_status": "SOURCE_OBJECT_NOT_ACCEPTED",
        "required_to_promote": "endpoint-blind A_tau/rho_tau_eff derivation plus normalization replay",
        "blocks_scoring_reason": "density source role is still a slot, not an accepted source",
    },
    {
        "route_layer": "potential_constraint",
        "mathematical_object": "k^2 Phi_tau_eff = 4 pi G a^2 rho_tau_eff Delta_tau",
        "single_pass_statement": "The effective potential slot is a role-matching target until Delta_tau and the Tau-side field equation are supplied.",
        "claim_level": "COMPARISON_SLOT_NOT_FIELD_EQUATION",
        "current_status": "PHI_TAU_EFF_NOT_DERIVED",
        "required_to_promote": "Tau-side perturbation equation, Delta_tau definition, known-limit and dimensional proof",
        "blocks_scoring_reason": "potential response is not derived from Tau dynamics",
    },
    {
        "route_layer": "transfer",
        "mathematical_object": "Phi_lens_tau = T_tau_CMB[Phi_tau_eff]",
        "single_pass_statement": "The lensing-era response requires an endpoint-blind transfer operator from the Tau potential slot.",
        "claim_level": "TRANSFER_OPERATOR_REQUIRED",
        "current_status": "T_TAU_CMB_NOT_MATERIALIZED",
        "required_to_promote": "analytic or executable T_tau_CMB with support, units, gauge convention, and zero-source behavior",
        "blocks_scoring_reason": "no transfer operator can populate a CMB grid",
    },
    {
        "route_layer": "projection",
        "mathematical_object": "tau_PP(L) = N_proj int K_tau_PP Phi_lens_tau dmu",
        "single_pass_statement": "The CMB observable grid requires a projection kernel, measure, support, and physical normalization.",
        "claim_level": "FORMULA_SCAFFOLD_NOT_ACCEPTED",
        "current_status": "KERNEL_MEASURE_NORMALIZATION_BLOCKED",
        "required_to_promote": "K_tau_PP, dmu, N_projection_physical, codomain units, and zero-source proof",
        "blocks_scoring_reason": "observable grid is not constructible",
    },
    {
        "route_layer": "role_bundle",
        "mathematical_object": "acoustic, density, lensing, growth, radiation, null roles",
        "single_pass_statement": "The six CMB readout roles must be populated consistently, including null controls and wrong-family guards.",
        "claim_level": "AUDITED_BUNDLE_BLOCKED",
        "current_status": "ROLE_BUNDLE_AUDITED_NOT_SCORE_READY",
        "required_to_promote": "cross-role consistency matrix, role-specific numeric guards, and quotient survival proof",
        "blocks_scoring_reason": "role coordinates are audited but not jointly materialized",
    },
    {
        "route_layer": "firewall_and_provenance",
        "mathematical_object": "endpoint-blind provenance path",
        "single_pass_statement": "Every source, map, kernel, and normalization must be frozen before Planck/ACT residuals or score deltas are inspected.",
        "claim_level": "PROTOCOL_REQUIREMENT",
        "current_status": "FIREWALL_DECLARED_NOT_REPLAYABLE_OVER_ABSENT_VALUES",
        "required_to_promote": "post-population endpoint firewall replay over concrete values",
        "blocks_scoring_reason": "cannot prove endpoint-blindness before route values exist",
    },
    {
        "route_layer": "scoring",
        "mathematical_object": "CMB role score / likelihood comparison",
        "single_pass_statement": "Only after the route is populated endpoint-blind may Paper 13 compare Tau and baseline dark-sector necessity roles.",
        "claim_level": "SCORING_GATE_CLOSED",
        "current_status": "NO_SCORE_ENTRY",
        "required_to_promote": "all upstream blockers closed plus fixed scoring rubric, covariance/readout convention, and stale-output guard",
        "blocks_scoring_reason": "score inputs are not fulfilled",
    },
    {
        "route_layer": "verdict",
        "mathematical_object": "dark-sector necessity decision",
        "single_pass_statement": "A dark-sector verdict is permitted only after a valid endpoint-blind score shows whether Tau response replaces, requires, or coexists with dark-sector roles.",
        "claim_level": "VERDICT_FORBIDDEN",
        "current_status": "NO_DARK_SECTOR_VERDICT",
        "required_to_promote": "accepted score outputs, controls, uncertainty accounting, and reviewer-safe decision rule",
        "blocks_scoring_reason": "verdict is downstream of a score that does not yet exist",
    },
]


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def table_rows() -> list[dict[str, str]]:
    return [
        {
            "step_id": f"TCMBSPDS01_{index:03d}",
            "allows_score_entry": "false",
            "allows_dark_sector_verdict": "false",
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


def build_summary(table_path: Path, rows: list[dict[str, str]]) -> dict[str, Any]:
    input_statuses = {
        name: (load_json(path).get("status") if path.exists() else "MISSING")
        for name, path in INPUTS.items()
    }
    required_present = all(path.exists() for path in INPUTS.values())
    expected_blocked_chain = (
        input_statuses["cosmology_spine"] == "DERIVATION_SPINE_DECLARED_PARTIAL_NOT_SCORE_ELIGIBLE"
        and input_statuses["source_grounding"] == "SOURCE_GROUNDING_GATE_DECLARED_BLOCKED"
        and input_statuses["bundle_closure_audit"] == "READOUT_ROLE_COORDINATE_BUNDLE_CLOSURE_AUDITED_BLOCKED_NOT_SCORE_READY"
        and input_statuses["scoring_gap_matrix"] == "SCORING_INPUT_GAP_MATRIX_DECLARED_ALL_ROWS_BLOCKED_NO_SCORE"
        and input_statuses["carrier_certificate_audit"] == "CONCRETE_R_CMB_CARRIER_CERTIFICATE_REQUIREMENTS_AUDITED_BLOCKED"
        and input_statuses["carrier_domain_predicate_audit"] == "CARRIER_DOMAIN_PREDICATE_CANDIDATE_AUDITED_BLOCKED_NOT_SCORE_READY"
    )
    return {
        "report_id": "tau_cmb_single_pass_derivation_spine_summary_v01",
        "claim_boundary": CLAIM_BOUNDARY,
        "table": rel(table_path),
        "input_statuses": input_statuses,
        "inputs_present": required_present,
        "input_chain_consistent_with_blocked_route": expected_blocked_chain,
        "route_steps": len(rows),
        "definition_or_candidate_steps": sum(
            row["claim_level"] in {"CANDIDATE_CONTEXT", "PREDICATE_CANDIDATE", "CONDITIONAL_ROLE_FORMULA"}
            for row in rows
        ),
        "required_object_steps": sum(
            row["claim_level"] in {"REQUIRED_OBJECT_NOT_MATERIALIZED", "TRANSFER_OPERATOR_REQUIRED"}
            for row in rows
        ),
        "scoring_or_verdict_steps_closed": 2,
        "score_entry_allowed": False,
        "likelihood_allowed": False,
        "dark_sector_verdict_allowed": False,
        "status": (
            "SINGLE_PASS_DERIVATION_SPINE_DECLARED_ROUTE_BLOCKED_NOT_SCORE_READY"
            if required_present and expected_blocked_chain
            else "SINGLE_PASS_DERIVATION_SPINE_BLOCKED_BY_INPUTS"
        ),
        "next_minimal_unblock": "tau_cmb_carrier_domain_certificate_requirements_v01",
    }


def write_doc(path: Path, rows: list[dict[str, str]], summary: dict[str, Any]) -> None:
    row_text = "\n".join(
        (
            f"- `{row['step_id']}` `{row['route_layer']}`: {row['claim_level']} / "
            f"{row['current_status']} | `{row['mathematical_object']}` | "
            f"promote by: {row['required_to_promote']}"
        )
        for row in rows
    )
    inputs = "\n".join(f"- `{name}`: {status}" for name, status in summary["input_statuses"].items())
    text = f"""# Tau CMB Single-Pass Derivation Spine v01

**Doc class:** single-pass derivation route spine
**Reader role:** Paper 13 / scoring-readiness reviewer
**Status:** {summary["status"]}
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
{CLAIM_BOUNDARY}
```

## Purpose

This artifact writes the whole Tau CMB route in one pass, from seed/domain to a
future dark-sector necessity decision. It is intentionally not a proof. Its job
is to prevent the work from becoming an endless sequence of local gates while
still preserving the boundary between definition, candidate, required object,
audit-visible blocker, score entry, and verdict.

## One-Pass Route

```text
Tau seed/root context
-> carrier C_CMB^seed
-> Dom(R_CMB)
-> concrete R_CMB
-> rho_tau_eff(a,k)
-> Phi_tau_eff(a,k)
-> T_tau_CMB
-> K_tau_PP dmu and N_projection_physical
-> six CMB role coordinates
-> endpoint firewall
-> score
-> dark-sector necessity decision
```

## Formula Spine

```text
rho_tau_eff(a,k) := A_tau(a,k) rho_ref(a)
k^2 Phi_tau_eff(a,k) = 4 pi G a^2 rho_tau_eff(a,k) Delta_tau(a,k)
Phi_lens_tau = T_tau_CMB[Phi_tau_eff]
tau_PP(L) = N_projection_physical int K_tau_PP(L; a,k) Phi_lens_tau(a,k) dmu(a,k)
```

These formulas are not yet promoted to physical Tau CMB equations. They are the
minimal route objects that must be populated endpoint-blind before scoring.

## Route Rows

{row_text}

## Input Chain

{inputs}

## Status

```text
{summary["status"]}
```

The route can be viewed in one pass, but the route is still blocked. No concrete
`R_CMB`, no score entry, no likelihood, and no dark-sector verdict are opened.

## Next Minimal Unblock

```text
{summary["next_minimal_unblock"]}
```
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Tau CMB single-pass derivation spine.")
    parser.add_argument("--write-table", nargs="?", const=str(DEFAULT_TABLE))
    parser.add_argument("--write-summary", nargs="?", const=str(DEFAULT_SUMMARY))
    parser.add_argument("--write-doc", nargs="?", const=str(DEFAULT_DOC))
    args = parser.parse_args()
    rows = table_rows()
    table_path = Path(args.write_table or DEFAULT_TABLE)
    if args.write_table:
        write_table(table_path, rows)
    summary = build_summary(table_path, rows)
    if args.write_summary:
        summary_path = Path(args.write_summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.write_doc:
        write_doc(Path(args.write_doc), rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
