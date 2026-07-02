#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_external_reference_manifest() -> None:
    rows = read_csv(ROOT / "data/source_manifest/cmb_external_reference_manifest_v01.csv")
    require(len(rows) == 3, "expected three external CMB references")
    require({row["citation_key"] for row in rows} == {"planck2018parameters", "actdr6lensing", "actdr6extended"}, "reference keys mismatch")
    require(all(row["claim_boundary"] == "external_reference_only_no_tau_core_validation" for row in rows), "external refs cannot validate Tau Core")


def validate_decision_ladder() -> None:
    rows = read_csv(ROOT / "data/source_manifest/tau_core_cmb_decision_ladder_v01.csv")
    require([row["decision_id"] for row in rows] == ["TC0", "TC1", "TC2"], "decision ladder order mismatch")
    forbidden = " ".join(row["forbidden_interpretation"] for row in rows).lower()
    require("galaxy-rotation fit alone" in forbidden, "ladder must forbid galaxy-only CMB conclusion")
    require("tau field detected" in forbidden, "ladder must forbid detection overclaim")
    require(all(row["claim_boundary"] == "no_verdict_without_cmb_likelihood" for row in rows), "decision ladder must block verdicts")


def validate_cmb_constraint_map() -> None:
    constraints = read_csv(ROOT / "data/derived/cmb_constraint_map_v01.csv")
    requirements = read_csv(ROOT / "data/derived/tau_core_dark_sector_requirement_map_v01.csv")
    summary = read_csv(ROOT / "data/derived/paper13_readiness_summary_v01.csv")
    require(len(constraints) == 5, "expected five mapped CMB constraints")
    require(len(requirements) == 5, "expected five Tau Core requirements")
    require(sum(row["necessity_pressure"] == "HIGH" for row in constraints) == 4, "expected four high-pressure constraints")
    require(all(row["current_protocol_status"] == "MAPPED_NOT_SOLVED" for row in constraints), "constraints must remain unsolved")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in requirements), "requirements cannot allow verdicts")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in requirements) == 4, "expected four no-dark blockers")
    require(len(summary) == 1, "summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "PAPER13_CMB_CONSTRAINT_MAP_V01", "summary id mismatch")
    require(row["external_references_registered"] == "3", "reference count mismatch")
    require(row["cmb_constraints_mapped"] == "5", "constraint count mismatch")
    require(row["requirements_written"] == "5", "requirement count mismatch")
    require(row["high_pressure_constraints"] == "4", "high-pressure count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_verdict_allowed"] == "false", "Tau response verdict must be blocked")
    require(row["next_required_artifact"] == "tau_cmb_effective_source_equation_v01", "next artifact mismatch")


def validate_tau_cmb_effective_source_equation_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_effective_source_equation_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_effective_source_equation_summary_v01.csv")
    require(len(rows) == 8, "expected eight effective-source target components")
    require(
        [row["target_component"] for row in rows]
        == [
            "base_carrier",
            "disturbance_seed",
            "response_operator",
            "effective_density",
            "effective_potential",
            "transfer_response",
            "radiation_guard",
            "known_limit_gate",
        ],
        "effective-source component order mismatch",
    )
    require({row["current_status"] for row in rows} == {"DECLARED_NOT_FILLED"}, "v01 rows must remain unfilled")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "v01 cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "v01 cannot allow verdicts")
    require(len(summary) == 1, "effective-source summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_EFFECTIVE_SOURCE_EQUATION_V01", "effective-source summary id mismatch")
    require(row["components_declared"] == "8", "component count mismatch")
    require(row["lcdm_role_checks_declared"] == "8", "LCDM role check count mismatch")
    require(row["dimension_roles_declared"] == "8", "dimension role count mismatch")
    require(row["source_equation_filled"] == "false", "source equation must remain unfilled")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "EFFECTIVE_SOURCE_EQUATION_TARGET_DECLARED_NOT_FILLED",
        "effective-source status mismatch",
    )
    require(row["next_required_artifact"] == "tau_cmb_known_limit_and_dimension_audit_v01", "effective-source next artifact mismatch")


def validate_tau_cmb_known_limit_and_dimension_audit_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_known_limit_and_dimension_audit_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_known_limit_and_dimension_audit_summary_v01.csv")
    require(len(rows) == 8, "known-limit audit must cover eight components")
    require({row["formula_available"] for row in rows} == {"false"}, "no formulas can be available in v01 audit")
    require(
        {row["dimensional_consistency_proved"] for row in rows} == {"false"},
        "v01 audit cannot prove dimensional consistency",
    )
    require(
        all("DECLARED" in row["dimension_slot_status"] for row in rows),
        "v01 audit must only declare dimension slots",
    )
    require(
        all("NOT_MATCHED" in row["lcdm_role_check_status"] or "NOT_PROVED" in row["lcdm_role_check_status"] or "NOT_EVALUATED" in row["lcdm_role_check_status"] or "NOT_RUN" in row["lcdm_role_check_status"] for row in rows),
        "v01 audit cannot match LCDM roles",
    )
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "known-limit audit cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "known-limit audit cannot allow verdicts")
    require(len(summary) == 1, "known-limit audit summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_KNOWN_LIMIT_AND_DIMENSION_AUDIT_V01", "known-limit audit summary id mismatch")
    require(row["audited_components"] == "8", "known-limit audit component count mismatch")
    require(row["dimension_slots_declared"] == "8", "dimension slot count mismatch")
    require(row["formula_available_components"] == "0", "formula count must be zero")
    require(row["dimensional_consistency_proved_components"] == "0", "dimensional proof count must be zero")
    require(row["lcdm_roles_matched"] == "0", "LCDM match count must be zero")
    require(row["lcdm_roles_unmatched"] == "8", "LCDM unmatched count mismatch")
    require(row["no_dark_blockers"] == "7", "known-limit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "KNOWN_LIMIT_DIMENSION_SLOTS_DECLARED_FORMULA_AND_LCDM_MATCH_BLOCKED",
        "known-limit audit status mismatch",
    )
    require(row["next_required_artifact"] == "tau_cmb_minimal_source_term_candidate_v01", "known-limit audit next artifact mismatch")


def validate_tau_cmb_minimal_source_term_candidate_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_minimal_source_term_candidate_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_minimal_source_term_candidate_summary_v01.csv")
    require(len(rows) == 6, "minimal source-term candidate must have six rows")
    require(
        [row["source_term_component"] for row in rows]
        == [
            "carrier_to_response_state",
            "effective_density_source",
            "effective_potential_poisson_slot",
            "transfer_kernel_slot",
            "radiation_guard_slot",
            "known_limit_branch",
        ],
        "minimal source-term candidate order mismatch",
    )
    require(
        {row["current_status"] for row in rows} == {"CANDIDATE_SKELETON_DECLARED_NOT_VALIDATED"},
        "minimal source-term candidate cannot be validated in v01",
    )
    require(
        sum(row["dimensional_precheck_status"].startswith("CONDITIONALLY_PRECHECKABLE") for row in rows) == 3,
        "expected three conditionally precheckable skeletons",
    )
    require({row["lcdm_role_match_status"] for row in rows} == {"LCDM_ROLE_DECLARED_NOT_MATCHED"}, "v01 cannot match LCDM roles")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "minimal candidate cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "minimal candidate cannot allow verdicts")
    require(len(summary) == 1, "minimal source-term candidate summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_MINIMAL_SOURCE_TERM_CANDIDATE_V01", "minimal candidate summary id mismatch")
    require(row["candidate_components_declared"] == "6", "minimal candidate row count mismatch")
    require(row["formula_skeletons_declared"] == "6", "formula skeleton count mismatch")
    require(row["dimensionally_precheckable_skeletons"] == "3", "precheckable skeleton count mismatch")
    require(row["dimensional_consistency_proved_components"] == "0", "dimensional proof count must be zero")
    require(row["lcdm_role_matches_claimed"] == "0", "LCDM matches must be zero")
    require(row["no_dark_blockers"] == "5", "minimal candidate no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "MINIMAL_SOURCE_TERM_CANDIDATE_DECLARED_NOT_VALIDATED",
        "minimal candidate status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_source_term_dimensional_precheck_v01",
        "minimal candidate next artifact mismatch",
    )


def validate_tau_cmb_source_term_dimensional_precheck_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_source_term_dimensional_precheck_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_source_term_dimensional_precheck_summary_v01.csv")
    require(len(rows) == 6, "source-term dimensional precheck must have six rows")
    require(
        sum(row["precheck_result"].startswith("CONDITIONAL_PASS") for row in rows) == 3,
        "expected three conditional dimensional passes",
    )
    require(
        sum(row["precheck_result"].startswith("BLOCKED") for row in rows) == 3,
        "expected three blocked dimensional rows",
    )
    require(sum(row["blocks_scoring"] == "true" for row in rows) == 3, "expected three scoring blockers")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "precheck cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "precheck cannot allow verdicts")
    require(len(summary) == 1, "source-term dimensional precheck summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_SOURCE_TERM_DIMENSIONAL_PRECHECK_V01",
        "source-term dimensional precheck summary id mismatch",
    )
    require(row["prechecked_components"] == "6", "precheck component count mismatch")
    require(row["conditional_dimension_passes"] == "3", "conditional pass count mismatch")
    require(row["blocked_dimension_rows"] == "3", "blocked dimension row count mismatch")
    require(row["full_dimensional_proofs"] == "0", "full dimensional proof count must be zero")
    require(row["scoring_blockers"] == "3", "scoring blocker count mismatch")
    require(row["no_dark_blockers"] == "5", "precheck no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "SOURCE_TERM_DIMENSIONAL_PRECHECK_PARTIAL_CONDITIONAL_SCORING_BLOCKED",
        "source-term dimensional precheck status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_lcdm_role_scoring_rubric_v01",
        "source-term dimensional precheck next artifact mismatch",
    )


def validate_tau_cmb_lcdm_role_scoring_rubric_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_lcdm_role_scoring_rubric_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_lcdm_role_scoring_rubric_summary_v01.csv")
    require(len(rows) == 6, "LCDM role scoring rubric must have six rows")
    require(
        [row["cmb_role"] for row in rows]
        == [
            "acoustic_peak_phase_and_height",
            "omega_c_h2_density_inference",
            "cmb_lensing_potential",
            "damping_tail_and_radiation_guard",
            "growth_seed_and_transfer_consistency",
            "known_limit_or_explicit_failure",
        ],
        "LCDM role scoring rubric order mismatch",
    )
    require(all(row["score_0_condition"] for row in rows), "every rubric row needs a score-0 condition")
    require(all(row["score_1_condition"] for row in rows), "every rubric row needs a score-1 condition")
    require(all(row["score_2_condition"] for row in rows), "every rubric row needs a score-2 condition")
    require(all(row["hard_failure_condition"] for row in rows), "every rubric row needs a hard-failure condition")
    require({row["currently_scoreable"] for row in rows} == {"false"}, "v01 rubric cannot mark rows scoreable")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "rubric cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "rubric cannot allow verdicts")
    require(len(summary) == 1, "LCDM role scoring rubric summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_LCDM_ROLE_SCORING_RUBRIC_V01", "rubric summary id mismatch")
    require(row["rubric_rows_declared"] == "6", "rubric row count mismatch")
    require(row["score_levels_declared_per_row"] == "3", "score level count mismatch")
    require(row["currently_scoreable_rows"] == "0", "v01 scoreable rows must be zero")
    require(row["hard_failure_rules_declared"] == "6", "hard-failure rule count mismatch")
    require(row["no_dark_blockers"] == "5", "rubric no-dark blocker count mismatch")
    require(row["scores_computed"] == "false", "v01 cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "LCDM_ROLE_SCORING_RUBRIC_DECLARED_NO_SCORES_COMPUTED",
        "rubric status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_role_scorecard_template_v01",
        "rubric next artifact mismatch",
    )


def validate_tau_cmb_role_scorecard_template_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_role_scorecard_template_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_role_scorecard_template_summary_v01.csv")
    require(len(rows) == 6, "role scorecard template must have six rows")
    require({row["score_status"] for row in rows} == {"NOT_COMPUTED_INPUT_BLOCKED"}, "all scorecard rows must be blocked")
    require({row["assigned_score"] for row in rows} == {"NA"}, "v01 scorecard cannot assign scores")
    require({row["score_evidence_pointer"] for row in rows} == {"NA"}, "v01 scorecard cannot point to score evidence")
    require(all(row["minimum_unblock_artifact"] for row in rows), "every row needs an unblock artifact")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "v01 scorecard cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "scorecard template cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "scorecard template cannot allow verdicts")
    require(len(summary) == 1, "role scorecard template summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_ROLE_SCORECARD_TEMPLATE_V01", "scorecard summary id mismatch")
    require(row["scorecard_rows_declared"] == "6", "scorecard row count mismatch")
    require(row["scores_computed"] == "0", "scores computed must be zero")
    require(row["not_computed_rows"] == "6", "not-computed row count mismatch")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["blocked_rows"] == "6", "blocked row count mismatch")
    require(row["no_dark_blockers"] == "5", "scorecard no-dark blocker count mismatch")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "ROLE_SCORECARD_TEMPLATE_DECLARED_ALL_SCORES_BLOCKED",
        "scorecard template status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_score_input_unblock_plan_v01",
        "scorecard template next artifact mismatch",
    )


def validate_tau_cmb_score_input_unblock_plan_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_score_input_unblock_plan_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_score_input_unblock_plan_summary_v01.csv")
    require(len(rows) == 6, "score input unblock plan must have six rows")
    require([row["priority_rank"] for row in rows] == ["1", "2", "3", "4", "5", "6"], "priority ranks mismatch")
    require(
        [row["minimum_unblock_artifact"] for row in rows]
        == [
            "tau_cmb_known_limit_failure_map_v01",
            "tau_cmb_density_amplitude_derivation_v01",
            "tau_cmb_acoustic_role_reduced_benchmark_v01",
            "tau_cmb_lensing_transfer_benchmark_v01",
            "tau_cmb_growth_transfer_kernel_v01",
            "tau_cmb_radiation_guard_bound_check_v01",
        ],
        "unblock artifact priority order mismatch",
    )
    require(all(row["unblock_goal"] for row in rows), "every unblock row needs a goal")
    require(all(row["why_this_priority"] for row in rows), "every unblock row needs priority rationale")
    require(sum(row["can_unlock_score_without_likelihood"] == "true" for row in rows) == 5, "expected five reduced-score unlocks")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "unblock plan cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "unblock plan cannot allow verdicts")
    require(len(summary) == 1, "score input unblock plan summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_SCORE_INPUT_UNBLOCK_PLAN_V01", "unblock plan summary id mismatch")
    require(row["unblock_rows_declared"] == "6", "unblock row count mismatch")
    require(row["ranked_rows"] == "6", "ranked row count mismatch")
    require(row["immediate_next_artifact"] == "tau_cmb_known_limit_failure_map_v01", "immediate next artifact mismatch")
    require(row["likelihood_required_for_verdict"] == "true", "likelihood must be required for verdict")
    require(row["scores_computed"] == "false", "unblock plan cannot compute scores")
    require(row["no_dark_blockers"] == "5", "unblock no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "SCORE_INPUT_UNBLOCK_PLAN_DECLARED_NO_SCORES_COMPUTED",
        "unblock plan status mismatch",
    )
    require(row["next_required_artifact"] == "tau_cmb_known_limit_failure_map_v01", "unblock next artifact mismatch")


def validate_tau_cmb_known_limit_failure_map_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_known_limit_failure_map_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_known_limit_failure_map_summary_v01.csv")
    require(len(rows) == 6, "known-limit failure map must have six rows")
    require(
        {row["allowed_decision_states"] for row in rows} == {"REPRODUCE;APPROXIMATE;FAIL;UNRESOLVED"},
        "known-limit map decision states mismatch",
    )
    require(
        {row["current_decision_state"] for row in rows} == {"UNRESOLVED_INPUT_MISSING"},
        "v01 known-limit map cannot resolve roles",
    )
    require(all(row["minimum_evidence_for_reproduce"] for row in rows), "each row needs reproduce evidence criteria")
    require(all(row["minimum_evidence_for_approximate"] for row in rows), "each row needs approximate evidence criteria")
    require(all(row["minimum_evidence_for_fail"] for row in rows), "each row needs fail evidence criteria")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "known-limit map cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "known-limit map cannot allow verdicts")
    require(len(summary) == 1, "known-limit failure map summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_KNOWN_LIMIT_FAILURE_MAP_V01", "known-limit map summary id mismatch")
    require(row["known_limit_rows_declared"] == "6", "known-limit row count mismatch")
    require(row["allowed_decision_states_per_row"] == "4", "decision state count mismatch")
    require(row["resolved_rows"] == "0", "resolved rows must be zero")
    require(row["unresolved_rows"] == "6", "unresolved row count mismatch")
    require(row["failures_declared"] == "0", "failures declared must be zero")
    require(row["reproductions_declared"] == "0", "reproductions declared must be zero")
    require(row["approximations_declared"] == "0", "approximations declared must be zero")
    require(row["no_dark_blockers"] == "5", "known-limit no-dark blocker count mismatch")
    require(row["scores_computed"] == "false", "known-limit map cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "KNOWN_LIMIT_FAILURE_MAP_DECLARED_ALL_ROLES_UNRESOLVED",
        "known-limit map status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_density_amplitude_derivation_v01",
        "known-limit map next artifact mismatch",
    )


def validate_tau_cmb_density_amplitude_derivation_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_density_amplitude_derivation_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_density_amplitude_derivation_summary_v01.csv")
    require(len(rows) == 5, "density amplitude derivation must have five rows")
    require(
        [row["derivation_component"] for row in rows]
        == [
            "reference_density_normalization",
            "tau_effective_density_slot",
            "dimensionless_amplitude_definition",
            "endpoint_blindness_gate",
            "omega_c_h2_comparison_gate",
        ],
        "density amplitude derivation component order mismatch",
    )
    require(
        sum(row["dimension_status"].startswith("CONDITIONAL_DIMENSION_PASS") for row in rows) == 1,
        "expected one conditional dimension pass",
    )
    require(
        all("NOT_SUPPLIED" in row["endpoint_blindness_status"] or "NOT_PROVED" in row["endpoint_blindness_status"] or "NOT_TAU_DERIVED" in row["endpoint_blindness_status"] or "WAITING" in row["endpoint_blindness_status"] for row in rows),
        "v01 cannot contain an endpoint-blind derivation",
    )
    require(all("MATCHED" not in row["omega_c_h2_role_status"] for row in rows), "v01 cannot match Omega_c h^2")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five density no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "density derivation cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "density derivation cannot allow verdicts")
    require(len(summary) == 1, "density amplitude derivation summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_DENSITY_AMPLITUDE_DERIVATION_V01", "density summary id mismatch")
    require(row["density_rows_declared"] == "5", "density row count mismatch")
    require(row["conditional_dimension_passes"] == "1", "conditional dimension pass count mismatch")
    require(row["endpoint_blind_derivations_available"] == "0", "endpoint-blind derivations must be zero")
    require(row["omega_c_h2_role_matches"] == "0", "Omega_c h^2 matches must be zero")
    require(row["scores_computed"] == "false", "density derivation cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "5", "density no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "DENSITY_AMPLITUDE_DEFINITION_DECLARED_DERIVATION_AND_MATCH_BLOCKED",
        "density status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_acoustic_role_reduced_benchmark_v01",
        "density next artifact mismatch",
    )


def validate_tau_cmb_acoustic_role_reduced_benchmark_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_acoustic_role_reduced_benchmark_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_acoustic_role_reduced_benchmark_summary_v01.csv")
    require(len(rows) == 6, "acoustic reduced benchmark must have six rows")
    require(
        [row["benchmark_component"] for row in rows]
        == [
            "potential_source_presence",
            "acoustic_phase_support",
            "relative_peak_height_support",
            "baryon_loading_compatibility",
            "scale_horizon_convention",
            "explicit_failure_branch",
        ],
        "acoustic benchmark component order mismatch",
    )
    require({row["current_status"] for row in rows} == {"DECLARED_NOT_EVALUATED"}, "v01 acoustic benchmark cannot evaluate rows")
    require(all(row["reduced_benchmark_condition"] for row in rows), "every acoustic row needs a reduced benchmark condition")
    require(all(row["required_input"] for row in rows), "every acoustic row needs a required input")
    require(all(row["hard_failure_if"] for row in rows), "every acoustic row needs a hard-failure condition")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6, "expected six acoustic no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "acoustic benchmark cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "acoustic benchmark cannot allow verdicts")
    require(len(summary) == 1, "acoustic benchmark summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_ACOUSTIC_ROLE_REDUCED_BENCHMARK_V01", "acoustic summary id mismatch")
    require(row["benchmark_rows_declared"] == "6", "acoustic row count mismatch")
    require(row["evaluated_rows"] == "0", "acoustic evaluated rows must be zero")
    require(row["hard_failures_triggered"] == "0", "acoustic hard failures must be zero")
    require(row["scores_computed"] == "false", "acoustic benchmark cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "6", "acoustic no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "ACOUSTIC_REDUCED_BENCHMARK_DECLARED_NOT_EVALUATED",
        "acoustic status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_lensing_transfer_benchmark_v01",
        "acoustic next artifact mismatch",
    )


def validate_tau_cmb_lensing_transfer_benchmark_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_lensing_transfer_benchmark_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_lensing_transfer_benchmark_summary_v01.csv")
    require(len(rows) == 6, "lensing transfer benchmark must have six rows")
    require(
        [row["benchmark_component"] for row in rows]
        == [
            "lensing_potential_source_presence",
            "transfer_kernel_presence",
            "projection_geometry_convention",
            "amplitude_shape_support",
            "cross_readout_consistency",
            "explicit_failure_branch",
        ],
        "lensing benchmark component order mismatch",
    )
    require({row["current_status"] for row in rows} == {"DECLARED_NOT_EVALUATED"}, "v01 lensing benchmark cannot evaluate rows")
    require(all(row["reduced_benchmark_condition"] for row in rows), "every lensing row needs a reduced benchmark condition")
    require(all(row["required_input"] for row in rows), "every lensing row needs a required input")
    require(all(row["hard_failure_if"] for row in rows), "every lensing row needs a hard-failure condition")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6, "expected six lensing no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "lensing benchmark cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "lensing benchmark cannot allow verdicts")
    require(len(summary) == 1, "lensing benchmark summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_LENSING_TRANSFER_BENCHMARK_V01", "lensing summary id mismatch")
    require(row["benchmark_rows_declared"] == "6", "lensing row count mismatch")
    require(row["evaluated_rows"] == "0", "lensing evaluated rows must be zero")
    require(row["hard_failures_triggered"] == "0", "lensing hard failures must be zero")
    require(row["scores_computed"] == "false", "lensing benchmark cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "6", "lensing no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "LENSING_TRANSFER_BENCHMARK_DECLARED_NOT_EVALUATED",
        "lensing status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_growth_transfer_kernel_v01",
        "lensing next artifact mismatch",
    )


def validate_tau_cmb_growth_transfer_kernel_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_growth_transfer_kernel_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_growth_transfer_kernel_summary_v01.csv")
    require(len(rows) == 6, "growth transfer kernel must have six rows")
    require(
        [row["kernel_component"] for row in rows]
        == [
            "domain_specification",
            "codomain_specification",
            "time_scale_convention",
            "operator_rule",
            "cross_role_consistency",
            "explicit_failure_branch",
        ],
        "growth transfer kernel component order mismatch",
    )
    require({row["current_status"] for row in rows} == {"DECLARED_NOT_SPECIFIED"}, "v01 growth kernel cannot specify rows")
    require(all(row["required_specification"] for row in rows), "every growth kernel row needs a required specification")
    require(all(row["dimension_or_normalization_status"] for row in rows), "every growth kernel row needs dimension/normalization status")
    require(all(row["hard_failure_if"] for row in rows), "every growth kernel row needs a hard-failure condition")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6, "expected six growth no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "growth kernel cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "growth kernel cannot allow verdicts")
    require(len(summary) == 1, "growth transfer kernel summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_GROWTH_TRANSFER_KERNEL_V01", "growth kernel summary id mismatch")
    require(row["kernel_rows_declared"] == "6", "growth kernel row count mismatch")
    require(row["specified_rows"] == "0", "growth kernel specified rows must be zero")
    require(row["dimension_or_normalization_rows_declared"] == "6", "growth kernel dimension row count mismatch")
    require(row["hard_failures_triggered"] == "0", "growth hard failures must be zero")
    require(row["scores_computed"] == "false", "growth kernel cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "6", "growth no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(row["overall_status"] == "GROWTH_TRANSFER_KERNEL_DECLARED_NOT_SPECIFIED", "growth kernel status mismatch")
    require(
        row["next_required_artifact"] == "tau_cmb_radiation_guard_bound_check_v01",
        "growth kernel next artifact mismatch",
    )


def validate_tau_cmb_radiation_guard_bound_check_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_radiation_guard_bound_check_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_radiation_guard_bound_check_summary_v01.csv")
    require(len(rows) == 5, "radiation guard bound check must have five rows")
    require(
        [row["guard_component"] for row in rows]
        == [
            "tau_radiation_like_contribution",
            "external_bound_convention",
            "damping_tail_guard",
            "cross_role_consistency",
            "explicit_failure_branch",
        ],
        "radiation guard component order mismatch",
    )
    require({row["current_status"] for row in rows} == {"DECLARED_NOT_EVALUATED"}, "v01 radiation guard cannot evaluate rows")
    require(all(row["required_check"] for row in rows), "every radiation guard row needs a required check")
    require(all(row["dimension_status"] for row in rows), "every radiation guard row needs dimension status")
    require(all(row["hard_failure_if"] for row in rows), "every radiation guard row needs a hard-failure condition")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 0, "radiation guard is not a direct no-dark blocker in v01")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "radiation guard cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "radiation guard cannot allow verdicts")
    require(len(summary) == 1, "radiation guard summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_RADIATION_GUARD_BOUND_CHECK_V01", "radiation guard summary id mismatch")
    require(row["guard_rows_declared"] == "5", "radiation guard row count mismatch")
    require(row["evaluated_rows"] == "0", "radiation guard evaluated rows must be zero")
    require(row["dimensionless_rows_declared"] == "3", "radiation guard dimensionless row count mismatch")
    require(row["hard_failures_triggered"] == "0", "radiation guard hard failures must be zero")
    require(row["scores_computed"] == "false", "radiation guard cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "0", "radiation guard no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "RADIATION_GUARD_BOUND_CHECK_DECLARED_NOT_EVALUATED",
        "radiation guard status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_scorecard_readiness_audit_v01",
        "radiation guard next artifact mismatch",
    )


def validate_tau_cmb_scorecard_readiness_audit_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_scorecard_readiness_audit_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_scorecard_readiness_audit_summary_v01.csv")
    require(len(rows) == 6, "scorecard readiness audit must have six rows")
    require(
        [row["cmb_role"] for row in rows]
        == [
            "acoustic_peak_phase_and_height",
            "omega_c_h2_density_inference",
            "cmb_lensing_potential",
            "damping_tail_and_radiation_guard",
            "growth_seed_and_transfer_consistency",
            "known_limit_or_explicit_failure",
        ],
        "scorecard readiness audit role order mismatch",
    )
    require({row["can_compute_score"] for row in rows} == {"false"}, "v01 readiness audit cannot allow score computation")
    require(all(row["score_readiness_status"].startswith("NOT_READY") for row in rows), "all readiness rows must be not-ready")
    require(all(row["minimum_missing_input"] for row in rows), "every readiness row needs a missing input")
    require(len({row["input_artifact_checked"] for row in rows}) == 6, "readiness audit must check six input artifacts")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five direct no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "readiness audit cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "readiness audit cannot allow verdicts")
    require(len(summary) == 1, "scorecard readiness audit summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_SCORECARD_READINESS_AUDIT_V01", "readiness summary id mismatch")
    require(row["readiness_rows_declared"] == "6", "readiness row count mismatch")
    require(row["input_artifacts_checked"] == "6", "checked artifact count mismatch")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["score_blocked_rows"] == "6", "score-blocked row count mismatch")
    require(row["direct_no_dark_blockers"] == "5", "direct no-dark blocker count mismatch")
    require(row["scores_computed"] == "false", "readiness audit cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(row["overall_status"] == "SCORECARD_NOT_READY_ALL_ROWS_BLOCKED", "readiness status mismatch")
    require(
        row["next_required_artifact"] == "tau_cmb_scorecard_blocker_closure_plan_v01",
        "readiness next artifact mismatch",
    )


def validate_tau_cmb_scorecard_blocker_closure_plan_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_scorecard_blocker_closure_plan_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_scorecard_blocker_closure_plan_summary_v01.csv")
    require(len(rows) == 6, "scorecard blocker closure plan must have six rows")
    require([row["priority_rank"] for row in rows] == ["1", "2", "3", "4", "5", "6"], "closure priority ranks mismatch")
    require(
        [row["next_artifact_to_build"] for row in rows]
        == [
            "tau_cmb_density_amplitude_closure_v01",
            "tau_cmb_acoustic_reduced_evaluation_v01",
            "tau_cmb_lensing_transfer_reduced_evaluation_v01",
            "tau_cmb_growth_transfer_kernel_closure_v01",
            "tau_cmb_radiation_guard_evaluation_v01",
            "tau_cmb_known_limit_decision_update_v01",
        ],
        "closure artifact order mismatch",
    )
    require(all(row["closure_action"] for row in rows), "every closure row needs an action")
    require(all(row["closure_criterion"] for row in rows), "every closure row needs a criterion")
    require(all(row["stop_rule"] for row in rows), "every closure row needs a stop rule")
    require({row["can_compute_score_after_closure"] for row in rows} == {"true"}, "every closure should unlock a score attempt")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five direct no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "closure plan cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "closure plan cannot allow verdicts")
    require(len(summary) == 1, "scorecard closure plan summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_SCORECARD_BLOCKER_CLOSURE_PLAN_V01", "closure summary id mismatch")
    require(row["closure_rows_declared"] == "6", "closure row count mismatch")
    require(row["ranked_rows"] == "6", "ranked closure row count mismatch")
    require(row["immediate_next_artifact"] == "tau_cmb_density_amplitude_closure_v01", "closure immediate next artifact mismatch")
    require(row["closures_completed"] == "0", "closures completed must be zero")
    require(row["scores_computed"] == "false", "closure plan cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "5", "closure no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "BLOCKER_CLOSURE_PLAN_DECLARED_NO_CLOSURES_COMPLETED",
        "closure plan status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_density_amplitude_closure_v01",
        "closure next artifact mismatch",
    )


def validate_tau_cmb_density_amplitude_closure_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_density_amplitude_closure_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_density_amplitude_closure_summary_v01.csv")
    require(len(rows) == 5, "density amplitude closure must have five rows")
    require(
        [row["closure_check"] for row in rows]
        == [
            "density_ratio_dimension_check",
            "tau_effective_density_formula",
            "endpoint_blind_amplitude_derivation",
            "omega_c_h2_role_comparison",
            "density_stop_rule",
        ],
        "density closure check order mismatch",
    )
    require(sum(row["closure_result"].startswith("CLOSED") for row in rows) == 1, "expected one closed density row")
    require(sum(row["closure_result"].startswith("BLOCKED") for row in rows) == 3, "expected three blocked density rows")
    require(sum(row["closure_result"].startswith("PARTIAL_CLOSURE") for row in rows) == 1, "expected one partial closure row")
    require({row["can_compute_density_score"] for row in rows} == {"false"}, "density score must remain blocked")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "density closure cannot trigger hard failure in v01")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five density closure no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "density closure cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "density closure cannot allow verdicts")
    require(len(summary) == 1, "density closure summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_DENSITY_AMPLITUDE_CLOSURE_V01", "density closure summary id mismatch")
    require(row["closure_rows_declared"] == "5", "density closure row count mismatch")
    require(row["closed_rows"] == "1", "density closed row count mismatch")
    require(row["partial_closure_rows"] == "1", "density partial closure count mismatch")
    require(row["blocked_rows"] == "3", "density blocked row count mismatch")
    require(row["hard_failures_triggered"] == "0", "density hard failures must be zero")
    require(row["can_compute_density_score"] == "false", "density score must remain blocked")
    require(row["scores_computed"] == "false", "density closure cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "5", "density closure no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "DENSITY_AMPLITUDE_PARTIAL_CLOSURE_SCORE_BLOCKED",
        "density closure status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_acoustic_reduced_evaluation_v01",
        "density closure next artifact mismatch",
    )


def validate_tau_cmb_acoustic_reduced_evaluation_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_acoustic_reduced_evaluation_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_acoustic_reduced_evaluation_summary_v01.csv")
    require(len(rows) == 6, "acoustic reduced evaluation must have six rows")
    require(
        [row["benchmark_component"] for row in rows]
        == [
            "potential_source_presence",
            "acoustic_phase_support",
            "relative_peak_height_support",
            "baryon_loading_compatibility",
            "scale_horizon_convention",
            "explicit_failure_branch",
        ],
        "acoustic evaluation component order mismatch",
    )
    require(sum(row["evaluation_result"].startswith("CLOSED") for row in rows) == 1, "expected one closed acoustic guard")
    require(sum(row["evaluation_result"].startswith("BLOCKED") for row in rows) == 4, "expected four blocked acoustic rows")
    require(
        sum(row["evaluation_result"].startswith("PARTIAL_EVALUATION") for row in rows) == 1,
        "expected one partial acoustic evaluation row",
    )
    require({row["can_compute_acoustic_score"] for row in rows} == {"false"}, "acoustic score must remain blocked")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "acoustic evaluation cannot trigger hard failure in v01")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6, "expected six acoustic no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "acoustic evaluation cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "acoustic evaluation cannot allow verdicts")
    require(len(summary) == 1, "acoustic evaluation summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_ACOUSTIC_REDUCED_EVALUATION_V01", "acoustic evaluation summary id mismatch")
    require(row["evaluation_rows_declared"] == "6", "acoustic evaluation row count mismatch")
    require(row["closed_rows"] == "1", "acoustic closed row count mismatch")
    require(row["partial_evaluation_rows"] == "1", "acoustic partial row count mismatch")
    require(row["blocked_rows"] == "4", "acoustic blocked row count mismatch")
    require(row["hard_failures_triggered"] == "0", "acoustic hard failures must be zero")
    require(row["can_compute_acoustic_score"] == "false", "acoustic score must remain blocked")
    require(row["scores_computed"] == "false", "acoustic evaluation cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "6", "acoustic evaluation no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "ACOUSTIC_REDUCED_EVALUATION_PARTIAL_SCORE_BLOCKED",
        "acoustic evaluation status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_lensing_transfer_reduced_evaluation_v01",
        "acoustic evaluation next artifact mismatch",
    )


def validate_tau_cmb_lensing_transfer_reduced_evaluation_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_lensing_transfer_reduced_evaluation_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_lensing_transfer_reduced_evaluation_summary_v01.csv")
    require(len(rows) == 6, "lensing reduced evaluation must have six rows")
    require(
        [row["benchmark_component"] for row in rows]
        == [
            "lensing_potential_source_presence",
            "transfer_kernel_presence",
            "projection_geometry_convention",
            "amplitude_shape_support",
            "cross_readout_consistency",
            "explicit_failure_branch",
        ],
        "lensing evaluation component order mismatch",
    )
    require(sum(row["evaluation_result"].startswith("CLOSED") for row in rows) == 1, "expected one closed lensing guard")
    require(sum(row["evaluation_result"].startswith("BLOCKED") for row in rows) == 4, "expected four blocked lensing rows")
    require(
        sum(row["evaluation_result"].startswith("PARTIAL_EVALUATION") for row in rows) == 1,
        "expected one partial lensing evaluation row",
    )
    require({row["can_compute_lensing_score"] for row in rows} == {"false"}, "lensing score must remain blocked")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "lensing evaluation cannot trigger hard failure in v01")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6, "expected six lensing no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "lensing evaluation cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "lensing evaluation cannot allow verdicts")
    require(len(summary) == 1, "lensing evaluation summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_LENSING_TRANSFER_REDUCED_EVALUATION_V01", "lensing evaluation summary id mismatch")
    require(row["evaluation_rows_declared"] == "6", "lensing evaluation row count mismatch")
    require(row["closed_rows"] == "1", "lensing closed row count mismatch")
    require(row["partial_evaluation_rows"] == "1", "lensing partial row count mismatch")
    require(row["blocked_rows"] == "4", "lensing blocked row count mismatch")
    require(row["hard_failures_triggered"] == "0", "lensing hard failures must be zero")
    require(row["can_compute_lensing_score"] == "false", "lensing score must remain blocked")
    require(row["scores_computed"] == "false", "lensing evaluation cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "6", "lensing evaluation no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "LENSING_TRANSFER_REDUCED_EVALUATION_PARTIAL_SCORE_BLOCKED",
        "lensing evaluation status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_growth_transfer_kernel_closure_v01",
        "lensing evaluation next artifact mismatch",
    )


def validate_tau_cmb_growth_transfer_kernel_closure_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_growth_transfer_kernel_closure_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_growth_transfer_kernel_closure_summary_v01.csv")
    require(len(rows) == 6, "growth transfer kernel closure must have six rows")
    require(
        [row["kernel_component"] for row in rows]
        == [
            "domain_specification",
            "codomain_specification",
            "time_scale_convention",
            "operator_rule",
            "cross_role_consistency",
            "explicit_failure_branch",
        ],
        "growth closure component order mismatch",
    )
    require(sum(row["closure_result"].startswith("CLOSED") for row in rows) == 1, "expected one closed growth guard")
    require(sum(row["closure_result"].startswith("PARTIAL_CLOSURE") for row in rows) == 3, "expected three partial growth closure rows")
    require(sum(row["closure_result"].startswith("BLOCKED") for row in rows) == 2, "expected two blocked growth rows")
    require({row["can_compute_growth_score"] for row in rows} == {"false"}, "growth score must remain blocked")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "growth closure cannot trigger hard failure in v01")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6, "expected six growth no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "growth closure cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "growth closure cannot allow verdicts")
    require(len(summary) == 1, "growth closure summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_GROWTH_TRANSFER_KERNEL_CLOSURE_V01", "growth closure summary id mismatch")
    require(row["closure_rows_declared"] == "6", "growth closure row count mismatch")
    require(row["closed_rows"] == "1", "growth closed row count mismatch")
    require(row["partial_closure_rows"] == "3", "growth partial closure count mismatch")
    require(row["blocked_rows"] == "2", "growth blocked row count mismatch")
    require(row["hard_failures_triggered"] == "0", "growth hard failures must be zero")
    require(row["can_compute_growth_score"] == "false", "growth score must remain blocked")
    require(row["scores_computed"] == "false", "growth closure cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "6", "growth closure no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "GROWTH_TRANSFER_KERNEL_PARTIAL_CLOSURE_SCORE_BLOCKED",
        "growth closure status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_radiation_guard_evaluation_v01",
        "growth closure next artifact mismatch",
    )


def validate_tau_cmb_radiation_guard_evaluation_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_radiation_guard_evaluation_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_radiation_guard_evaluation_summary_v01.csv")
    require(len(rows) == 5, "radiation guard evaluation must have five rows")
    require(
        [row["guard_component"] for row in rows]
        == [
            "tau_radiation_like_contribution",
            "external_bound_convention",
            "damping_tail_guard",
            "cross_role_consistency",
            "explicit_failure_branch",
        ],
        "radiation guard evaluation component order mismatch",
    )
    require(sum(row["evaluation_result"].startswith("CLOSED") for row in rows) == 1, "expected one closed radiation guard")
    require(sum(row["evaluation_result"].startswith("PARTIAL_EVALUATION") for row in rows) == 1, "expected one partial radiation row")
    require(sum(row["evaluation_result"].startswith("BLOCKED") for row in rows) == 3, "expected three blocked radiation rows")
    require({row["can_compute_radiation_score"] for row in rows} == {"false"}, "radiation score must remain blocked")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "radiation guard cannot trigger hard failure in v01")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 0, "radiation guard is not a direct no-dark blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "radiation evaluation cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "radiation evaluation cannot allow verdicts")
    require(len(summary) == 1, "radiation evaluation summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_RADIATION_GUARD_EVALUATION_V01", "radiation evaluation summary id mismatch")
    require(row["evaluation_rows_declared"] == "5", "radiation evaluation row count mismatch")
    require(row["closed_rows"] == "1", "radiation closed row count mismatch")
    require(row["partial_evaluation_rows"] == "1", "radiation partial row count mismatch")
    require(row["blocked_rows"] == "3", "radiation blocked row count mismatch")
    require(row["hard_failures_triggered"] == "0", "radiation hard failures must be zero")
    require(row["can_compute_radiation_score"] == "false", "radiation score must remain blocked")
    require(row["scores_computed"] == "false", "radiation evaluation cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "0", "radiation evaluation no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "RADIATION_GUARD_EVALUATION_PARTIAL_SCORE_BLOCKED",
        "radiation evaluation status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_known_limit_decision_update_v01",
        "radiation evaluation next artifact mismatch",
    )


def validate_tau_cmb_known_limit_decision_update_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_known_limit_decision_update_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_known_limit_decision_update_summary_v01.csv")
    require(len(rows) == 6, "known-limit decision update must have six rows")
    require(
        [row["cmb_role"] for row in rows]
        == [
            "acoustic_peak_phase_and_height",
            "omega_c_h2_density_inference",
            "cmb_lensing_potential",
            "damping_tail_and_radiation_guard",
            "growth_seed_and_transfer_consistency",
            "known_limit_or_explicit_failure",
        ],
        "decision update role order mismatch",
    )
    require({row["prior_decision_state"] for row in rows} == {"UNRESOLVED_INPUT_MISSING"}, "prior decision state mismatch")
    require(
        {row["updated_decision_state"] for row in rows} == {"UNRESOLVED_EVIDENCE_INSUFFICIENT"},
        "v01 decision update cannot resolve roles",
    )
    require({row["score_ready"] for row in rows} == {"false"}, "decision update cannot make rows score-ready")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "decision update cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "decision update cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "decision update cannot allow verdicts")
    require(len(summary) == 1, "decision update summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_KNOWN_LIMIT_DECISION_UPDATE_V01", "decision update summary id mismatch")
    require(row["decision_rows_declared"] == "6", "decision update row count mismatch")
    require(row["resolved_rows"] == "0", "resolved rows must be zero")
    require(row["unresolved_rows"] == "6", "unresolved rows must be six")
    require(row["failures_declared"] == "0", "failures declared must be zero")
    require(row["reproductions_declared"] == "0", "reproductions declared must be zero")
    require(row["approximations_declared"] == "0", "approximations declared must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "decision update cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "5", "decision update no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "KNOWN_LIMIT_DECISION_UPDATE_ALL_ROLES_UNRESOLVED_SCORE_BLOCKED",
        "decision update status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_scorecard_prescore_blocker_summary_v01",
        "decision update next artifact mismatch",
    )


def validate_tau_cmb_scorecard_prescore_blocker_summary_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_scorecard_prescore_blocker_summary_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_scorecard_prescore_blocker_summary_summary_v01.csv")
    require(len(rows) == 6, "prescore blocker summary must have six rows")
    require(
        [row["cmb_role"] for row in rows]
        == [
            "acoustic_peak_phase_and_height",
            "omega_c_h2_density_inference",
            "cmb_lensing_potential",
            "damping_tail_and_radiation_guard",
            "growth_seed_and_transfer_consistency",
            "known_limit_or_explicit_failure",
        ],
        "prescore blocker role order mismatch",
    )
    require(
        {row["decision_state"] for row in rows} == {"UNRESOLVED_EVIDENCE_INSUFFICIENT"},
        "prescore blocker decisions must remain unresolved",
    )
    require(
        {row["score_gate_status"] for row in rows} == {"SCORE_BLOCKED_UNRESOLVED_EVIDENCE"},
        "prescore blocker gate status mismatch",
    )
    require({row["score_ready"] for row in rows} == {"false"}, "prescore blocker cannot mark rows score-ready")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "prescore blocker cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "prescore blocker cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "prescore blocker cannot allow verdicts")
    require(len(summary) == 1, "prescore blocker summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_SCORECARD_PRESCORE_BLOCKER_SUMMARY_V01", "prescore summary id mismatch")
    require(row["blocker_rows_declared"] == "6", "prescore blocker row count mismatch")
    require(row["score_ready_rows"] == "0", "prescore score-ready rows must be zero")
    require(row["score_blocked_rows"] == "6", "prescore blocked rows must be six")
    require(row["unresolved_rows"] == "6", "prescore unresolved rows must be six")
    require(row["hard_failures_triggered"] == "0", "prescore hard failures must be zero")
    require(row["scores_computed"] == "false", "prescore summary cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "5", "prescore no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PRESCORE_BLOCKERS_SUMMARIZED_ALL_SCORE_ROWS_BLOCKED",
        "prescore blocker status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_minimal_scoring_input_contract_v01",
        "prescore blocker next artifact mismatch",
    )


def validate_tau_cmb_minimal_scoring_input_contract_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_minimal_scoring_input_contract_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_minimal_scoring_input_contract_summary_v01.csv")
    require(len(rows) == 6, "minimal scoring input contract must have six rows")
    require(
        [row["cmb_role"] for row in rows]
        == [
            "acoustic_peak_phase_and_height",
            "omega_c_h2_density_inference",
            "cmb_lensing_potential",
            "damping_tail_and_radiation_guard",
            "growth_seed_and_transfer_consistency",
            "known_limit_or_explicit_failure",
        ],
        "minimal scoring contract role order mismatch",
    )
    require(
        {row["current_contract_status"] for row in rows} == {"UNSATISFIED_INPUT_MISSING"},
        "minimal scoring inputs must remain unsatisfied in v01",
    )
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "score entry must remain blocked")
    require(all(row["required_scoring_input"] for row in rows), "each contract row needs a required scoring input")
    require(all(row["contract_requirement"] for row in rows), "each contract row needs a requirement")
    require(all(row["missing_condition"] for row in rows), "each contract row needs a missing condition")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "minimal contract cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "minimal contract cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "minimal contract cannot allow verdicts")
    require(len(summary) == 1, "minimal contract summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_MINIMAL_SCORING_INPUT_CONTRACT_V01", "minimal contract summary id mismatch")
    require(row["contract_rows_declared"] == "6", "minimal contract row count mismatch")
    require(row["satisfied_rows"] == "0", "minimal contract satisfied rows must be zero")
    require(row["unsatisfied_rows"] == "6", "minimal contract unsatisfied rows must be six")
    require(row["score_entry_allowed_rows"] == "0", "minimal contract score entry rows must be zero")
    require(row["hard_failures_triggered"] == "0", "minimal contract hard failures must be zero")
    require(row["scores_computed"] == "false", "minimal contract cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "5", "minimal contract no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "MINIMAL_SCORING_INPUT_CONTRACT_DECLARED_ALL_INPUTS_UNSATISFIED",
        "minimal contract status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_scoring_execution_gate_v01",
        "minimal contract next artifact mismatch",
    )


def validate_tau_cmb_scoring_execution_gate_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_scoring_execution_gate_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_scoring_execution_gate_summary_v01.csv")
    require(len(rows) == 6, "scoring execution gate must have six rows")
    require(
        [row["cmb_role"] for row in rows]
        == [
            "acoustic_peak_phase_and_height",
            "omega_c_h2_density_inference",
            "cmb_lensing_potential",
            "damping_tail_and_radiation_guard",
            "growth_seed_and_transfer_consistency",
            "known_limit_or_explicit_failure",
        ],
        "scoring gate role order mismatch",
    )
    require({row["contract_status"] for row in rows} == {"UNSATISFIED_INPUT_MISSING"}, "gate contracts must be unsatisfied")
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "score entry must remain blocked")
    require({row["execution_gate_decision"] for row in rows} == {"SCORING_BLOCKED"}, "scoring gate must block every row")
    require({row["score_computed"] for row in rows} == {"false"}, "scoring gate cannot compute scores")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "scoring gate cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five no-dark blockers")
    require(all(row["blocking_reason"] for row in rows), "each scoring gate row needs a blocking reason")
    require(all(row["required_before_run"] for row in rows), "each scoring gate row needs a run requirement")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "scoring gate cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "scoring gate cannot allow verdicts")
    require(len(summary) == 1, "scoring gate summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_SCORING_EXECUTION_GATE_V01", "scoring gate summary id mismatch")
    require(row["gate_rows_declared"] == "6", "scoring gate row count mismatch")
    require(row["run_allowed_rows"] == "0", "run allowed rows must be zero")
    require(row["run_blocked_rows"] == "6", "run blocked rows must be six")
    require(row["score_computed_rows"] == "0", "score computed rows must be zero")
    require(row["hard_failures_triggered"] == "0", "scoring gate hard failures must be zero")
    require(row["scores_computed"] == "false", "scoring gate cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "5", "scoring gate no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "SCORING_EXECUTION_GATE_BLOCKED_ALL_ROWS",
        "scoring gate status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_scoring_input_fulfillment_plan_v01",
        "scoring gate next artifact mismatch",
    )


def validate_tau_cmb_scoring_input_fulfillment_plan_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_scoring_input_fulfillment_plan_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_scoring_input_fulfillment_plan_summary_v01.csv")
    require(len(rows) == 6, "scoring input fulfillment plan must have six rows")
    require([row["priority_rank"] for row in rows] == ["1", "2", "3", "4", "5", "6"], "fulfillment ranks mismatch")
    require(
        [row["cmb_role"] for row in rows]
        == [
            "acoustic_peak_phase_and_height",
            "omega_c_h2_density_inference",
            "growth_seed_and_transfer_consistency",
            "cmb_lensing_potential",
            "damping_tail_and_radiation_guard",
            "known_limit_or_explicit_failure",
        ],
        "fulfillment role order mismatch",
    )
    require({row["blocked_gate_decision"] for row in rows} == {"SCORING_BLOCKED"}, "fulfillment plan must start from blocked gates")
    require({row["completed_in_v01"] for row in rows} == {"false"}, "fulfillment plan cannot complete inputs in v01")
    require(
        {row["score_entry_allowed_after_completion"] for row in rows} == {"true"},
        "each fulfillment row should state score entry can be retried after completion",
    )
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "fulfillment plan cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five no-dark blockers")
    require(all(row["fulfillment_action"] for row in rows), "each fulfillment row needs an action")
    require(all(row["acceptance_criterion"] for row in rows), "each fulfillment row needs an acceptance criterion")
    require(all(row["required_artifact_to_build"] for row in rows), "each fulfillment row needs a required artifact")
    require(all(row["stop_rule"] for row in rows), "each fulfillment row needs a stop rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "fulfillment plan cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "fulfillment plan cannot allow verdicts")
    require(len(summary) == 1, "fulfillment plan summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_SCORING_INPUT_FULFILLMENT_PLAN_V01", "fulfillment summary id mismatch")
    require(row["fulfillment_rows_declared"] == "6", "fulfillment row count mismatch")
    require(row["ranked_rows"] == "6", "ranked row count mismatch")
    require(row["completed_rows"] == "0", "completed rows must be zero")
    require(row["pending_rows"] == "6", "pending rows must be six")
    require(row["hard_failures_triggered"] == "0", "fulfillment hard failures must be zero")
    require(row["score_entry_allowed_rows"] == "0", "no score entry should be allowed before completion")
    require(row["scores_computed"] == "false", "fulfillment plan cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "5", "fulfillment no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "SCORING_INPUT_FULFILLMENT_PLAN_DECLARED_NO_INPUTS_COMPLETED",
        "fulfillment status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_effective_potential_source_handoff_v01",
        "fulfillment next artifact mismatch",
    )


def validate_tau_cmb_planck_pr3_peak_source_freeze_packet_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_source_freeze_packet_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_source_freeze_packet_summary_v01.csv")
    require(len(rows) == 4, "Planck PR3 source-freeze packet must have four rows")
    require(
        [row["artifact_id"] for row in rows]
        == [
            "PLANCK_PR3_PEAKSRC_001",
            "PLANCK_PR3_PEAKSRC_002",
            "PLANCK_PR3_PEAKSRC_003",
            "PLANCK_PR3_PEAKSRC_004",
        ],
        "Planck PR3 artifact ids mismatch",
    )
    require(
        {row["official_url"].startswith("https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/cosmoparams/") for row in rows}
        == {True},
        "Planck PR3 URLs must use the official IRSA ancillary cosmoparams path",
    )
    require({row["download_status"] for row in rows} == {"NOT_DOWNLOADED_BY_REPRO_PACKAGE"}, "raw downloads are not allowed")
    require({row["raw_artifact_hash"] for row in rows} == {"NOT_COMPUTED"}, "raw hashes must remain pending")
    require({row["extraction_status"] for row in rows} == {"DECLARED_NOT_EXECUTED"}, "extraction must remain pending")
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "score entry must remain blocked")
    require({row["allows_tau_response_claim"] for row in rows} == {"false"}, "Tau response claims must remain blocked")
    require({row["allows_dark_sector_verdict"] for row in rows} == {"false"}, "dark-sector verdicts must remain blocked")
    require(len(summary) == 1, "Planck PR3 source-freeze summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PLANCK_PR3_PEAK_SOURCE_FREEZE_PACKET_V01", "Planck PR3 summary id mismatch")
    require(row["artifact_rows_declared"] == "4", "Planck PR3 artifact row count mismatch")
    require(row["artifact_urls_selected"] == "4", "Planck PR3 artifact URL count mismatch")
    require(row["local_hashes_computed"] == "0", "Planck PR3 hashes must not be computed")
    require(row["extraction_rules_declared"] == "2", "Planck PR3 extraction rule count mismatch")
    require(row["extraction_rules_executed"] == "0", "Planck PR3 extraction cannot be executed")
    require(row["score_ready"] == "false", "Planck PR3 packet cannot be score-ready")
    require(row["score_entry_allowed_rows"] == "0", "Planck PR3 packet cannot allow score rows")
    require(row["scores_computed"] == "false", "Planck PR3 packet cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "Planck PR3 packet cannot provide likelihood")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must remain blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "PLANCK_PR3_ARTIFACT_URLS_SELECTED_EXTRACTION_FREEZE_PENDING",
        "Planck PR3 source-freeze status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_planck_pr3_peak_extraction_rule_v01",
        "Planck PR3 next artifact mismatch",
    )


def validate_tau_cmb_planck_pr3_peak_extraction_rule_v01() -> None:
    receipts = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_source_receipt_v01.csv")
    peaks = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_observable_table_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_extraction_rule_summary_v01.csv")
    require(len(receipts) == 4, "Planck PR3 receipt must have four rows")
    require(len(peaks) == 36, "Planck PR3 peak observable table must have 36 rows")
    require({row["download_status"] for row in receipts} == {"DOWNLOADED_TO_GITIGNORED_EXTERNAL_CACHE"}, "Planck PR3 receipt download status mismatch")
    require(all(len(row["sha256"]) == 64 for row in receipts), "Planck PR3 receipt hashes must be SHA256 hex strings")
    require(sum(row["spectrum"] == "TT" for row in peaks) == 10, "TT peak count mismatch")
    require(sum(row["spectrum"] == "TE" for row in peaks) == 13, "TE extremum count mismatch")
    require(sum(row["spectrum"] == "EE" for row in peaks) == 13, "EE peak count mismatch")
    require({row["score_entry_allowed"] for row in peaks} == {"false"}, "Planck PR3 extracted peaks cannot allow scoring")
    require({row["allows_tau_response_claim"] for row in peaks} == {"false"}, "Planck PR3 extracted peaks cannot allow Tau response claims")
    require({row["allows_dark_sector_verdict"] for row in peaks} == {"false"}, "Planck PR3 extracted peaks cannot allow dark-sector verdicts")
    require(peaks[0]["peak_id"] == "TT_PEAK_01", "first extracted peak id mismatch")
    require(peaks[0]["ell_center"] == "225.164945", "first TT peak ell mismatch")
    require(len(summary) == 1, "Planck PR3 extraction summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PLANCK_PR3_PEAK_EXTRACTION_RULE_V01", "Planck PR3 extraction summary id mismatch")
    require(row["source_artifacts_declared"] == "4", "Planck PR3 source declaration count mismatch")
    require(row["source_artifacts_downloaded"] == "4", "Planck PR3 download count mismatch")
    require(row["source_hashes_computed"] == "4", "Planck PR3 hash count mismatch")
    require(row["spectra_peak_extracted"] == "3", "Planck PR3 extracted spectra count mismatch")
    require(row["peak_rows_extracted"] == "36", "Planck PR3 extracted peak row count mismatch")
    require(row["tt_peak_rows"] == "10", "Planck PR3 TT peak count mismatch")
    require(row["te_extremum_rows"] == "13", "Planck PR3 TE extremum count mismatch")
    require(row["ee_peak_rows"] == "13", "Planck PR3 EE peak count mismatch")
    require(row["minimum_theory_reference_downloaded"] == "true", "Planck PR3 minimum theory reference must be downloaded")
    require(row["parser_rule_frozen"] == "true", "Planck PR3 parser rule must be frozen")
    require(row["observable_table_materialized"] == "true", "Planck PR3 observable table must be materialized")
    require(row["score_ready"] == "false", "Planck PR3 extraction cannot be score-ready")
    require(row["scores_computed"] == "false", "Planck PR3 extraction cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "Planck PR3 extraction cannot provide likelihood")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must remain blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "PLANCK_PR3_PEAK_OBSERVABLE_TABLE_MATERIALIZED_SCORING_STILL_BLOCKED",
        "Planck PR3 extraction status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_planck_pr3_peak_scoring_input_candidate_v01",
        "Planck PR3 extraction next artifact mismatch",
    )


def validate_tau_cmb_planck_pr3_peak_scoring_input_candidate_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_scoring_input_candidate_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_scoring_input_candidate_summary_v01.csv")
    require(len(rows) == 36, "Planck PR3 peak scoring input candidate must have 36 rows")
    require({row["cmb_role"] for row in rows} == {"acoustic_peak_phase_and_height"}, "candidate role mismatch")
    require({row["observable_family"] for row in rows} == {"planck_pr3_binned_peak_observable"}, "candidate observable family mismatch")
    require(sum(row["spectrum"] == "TT" for row in rows) == 10, "candidate TT row count mismatch")
    require(sum(row["spectrum"] == "TE" for row in rows) == 13, "candidate TE row count mismatch")
    require(sum(row["spectrum"] == "EE" for row in rows) == 13, "candidate EE row count mismatch")
    require({row["observed_side_ready"] for row in rows} == {"true"}, "observed side must be ready")
    require({row["tau_prediction_required"] for row in rows} == {"true"}, "Tau prediction must be required")
    require({row["tau_prediction_supplied"] for row in rows} == {"false"}, "Tau prediction must be missing")
    require({row["null_response_supplied"] for row in rows} == {"false"}, "null response must be missing")
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "score entry must remain blocked")
    require({row["score_blocker"] for row in rows} == {"TAU_PREDICTION_OR_NULL_RESPONSE_NOT_SUPPLIED"}, "candidate blocker mismatch")
    require({row["allows_tau_response_claim"] for row in rows} == {"false"}, "candidate cannot allow Tau response claims")
    require({row["allows_dark_sector_verdict"] for row in rows} == {"false"}, "candidate cannot allow dark-sector verdicts")
    require(rows[0]["candidate_id"] == "TCMBP3PSC01_001", "first candidate id mismatch")
    require(rows[0]["source_peak_id"] == "TT_PEAK_01", "first candidate source peak mismatch")
    require(rows[0]["ell_center"] == "225.164945", "first candidate ell mismatch")
    require(len(summary) == 1, "Planck PR3 peak scoring input candidate summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PLANCK_PR3_PEAK_SCORING_INPUT_CANDIDATE_V01", "candidate summary id mismatch")
    require(row["candidate_rows_declared"] == "36", "candidate row count mismatch")
    require(row["observed_side_ready_rows"] == "36", "observed ready count mismatch")
    require(row["comparison_rule_declared_rows"] == "36", "comparison rule count mismatch")
    require(row["tau_prediction_required_rows"] == "36", "Tau prediction required count mismatch")
    require(row["tau_prediction_supplied_rows"] == "0", "Tau prediction supplied count must be zero")
    require(row["null_response_supplied_rows"] == "0", "null response supplied count must be zero")
    require(row["score_ready_rows"] == "0", "candidate score-ready rows must be zero")
    require(row["observed_side_fulfillment_score"] == "1.000000", "observed side protocol score mismatch")
    require(row["scores_computed"] == "false", "candidate cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "candidate cannot provide likelihood")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must remain blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "OBSERVED_PEAK_SCORING_INPUT_CANDIDATE_READY_TAU_PREDICTION_MISSING_SCORE_BLOCKED",
        "candidate status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01",
        "candidate next artifact mismatch",
    )


def validate_tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_summary_v01.csv")
    require(len(rows) == 36, "Tau-side response audit must have 36 rows")
    require({row["tau_prediction_status"] for row in rows} == {"NOT_SUPPLIED"}, "Tau prediction must be absent")
    require({row["null_response_status"] for row in rows} == {"NOT_SUPPLIED"}, "null response must be absent")
    require(
        {row["admissible_response_status"] for row in rows} == {"NO_ADMISSIBLE_TAU_RESPONSE_OR_NULL_RESPONSE"},
        "admissible response status mismatch",
    )
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "Tau-side audit cannot allow score entry")
    require(
        {row["score_blocker"] for row in rows} == {"TAU_SIDE_PREDICTION_AND_NULL_RESPONSE_BOTH_MISSING"},
        "Tau-side audit score blocker mismatch",
    )
    require({row["hard_failure_triggered"] for row in rows} == {"false"}, "Tau-side audit cannot trigger hard failures")
    require({row["allows_tau_response_claim"] for row in rows} == {"false"}, "Tau-side audit cannot allow Tau response claims")
    require({row["allows_dark_sector_verdict"] for row in rows} == {"false"}, "Tau-side audit cannot allow verdicts")
    require(len(summary) == 1, "Tau-side response audit summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PLANCK_PR3_PEAK_TAU_PREDICTION_OR_NULL_RESPONSE_V01", "Tau-side audit summary id mismatch")
    require(row["response_rows_declared"] == "36", "Tau-side audit row count mismatch")
    require(row["observed_candidate_rows_checked"] == "36", "Tau-side observed candidate count mismatch")
    require(row["tau_prediction_required_rows"] == "36", "Tau prediction required count mismatch")
    require(row["tau_prediction_supplied_rows"] == "0", "Tau prediction supplied count must be zero")
    require(row["null_response_supplied_rows"] == "0", "null response supplied count must be zero")
    require(row["admissible_response_rows"] == "0", "admissible response count must be zero")
    require(row["score_ready_rows"] == "0", "Tau-side audit score-ready rows must be zero")
    require(row["explicit_missing_response_rows"] == "36", "explicit missing response count mismatch")
    require(row["hard_failures_triggered"] == "0", "Tau-side audit hard failures must be zero")
    require(row["scores_computed"] == "false", "Tau-side audit cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "Tau-side audit cannot provide likelihood")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must remain blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "TAU_SIDE_PEAK_RESPONSE_AUDITED_NO_PREDICTION_OR_NULL_RESPONSE_SCORE_BLOCKED",
        "Tau-side audit status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_planck_pr3_peak_score_attempt_guard_v01",
        "Tau-side audit next artifact mismatch",
    )


def validate_tau_cmb_planck_pr3_peak_score_attempt_guard_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_score_attempt_guard_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_score_attempt_guard_summary_v01.csv")
    require(len(rows) == 3, "score attempt guard must have three rows")
    require(sum(row["guard_decision"] == "GUARD_PASSED" for row in rows) == 1, "score guard pass count mismatch")
    require(sum(row["guard_decision"] == "SCORE_ATTEMPT_BLOCKED" for row in rows) == 2, "score guard block count mismatch")
    require({row["hard_failure_triggered"] for row in rows} == {"false"}, "score guard cannot trigger hard failures")
    require({row["allows_tau_response_claim"] for row in rows} == {"false"}, "score guard cannot allow Tau response claims")
    require({row["allows_dark_sector_verdict"] for row in rows} == {"false"}, "score guard cannot allow verdicts")
    require(len(summary) == 1, "score attempt guard summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PLANCK_PR3_PEAK_SCORE_ATTEMPT_GUARD_V01", "score guard summary id mismatch")
    require(row["guard_rows_declared"] == "3", "score guard row count mismatch")
    require(row["guard_pass_rows"] == "1", "score guard pass summary mismatch")
    require(row["guard_block_rows"] == "2", "score guard block summary mismatch")
    require(row["observed_side_ready"] == "true", "observed side must be ready")
    require(row["tau_side_response_ready"] == "false", "Tau-side response must be missing")
    require(row["score_attempt_allowed"] == "false", "score attempt must remain blocked")
    require(row["scores_computed"] == "false", "score guard cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "score guard cannot provide likelihood")
    require(row["hard_failures_triggered"] == "0", "score guard hard failures must be zero")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must remain blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "PLANCK_PR3_PEAK_SCORE_ATTEMPT_BLOCKED_TAU_SIDE_RESPONSE_MISSING",
        "score guard status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01",
        "score guard next artifact mismatch",
    )


def validate_tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_materialization_summary_v01.csv")
    require(len(rows) == 36, "Tau prediction materialization spec must have 36 rows")
    require(
        {row["tau_prediction_value_status"] for row in rows} == {"MISSING"},
        "Tau prediction values must remain missing in the spec",
    )
    require(
        {row["tau_prediction_ell_status"] for row in rows} == {"MISSING"},
        "Tau prediction peak positions must remain missing in the spec",
    )
    require(
        {row["tau_prediction_amplitude_status"] for row in rows} == {"MISSING"},
        "Tau prediction amplitudes must remain missing in the spec",
    )
    require(
        {row["tau_prediction_source_artifact_status"] for row in rows} == {"MISSING"},
        "Tau prediction source artifacts must remain missing in the spec",
    )
    require(
        {row["materialization_acceptance_status"] for row in rows}
        == {"BLOCKED_TAU_PREDICTION_PAYLOAD_NOT_MATERIALIZED"},
        "Tau prediction materialization acceptance status mismatch",
    )
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "materialization spec cannot allow score entry")
    require(
        {row["score_blocker"] for row in rows} == {"ENDPOINT_BLIND_TAU_PEAK_PREDICTION_PAYLOAD_MISSING"},
        "materialization score blocker mismatch",
    )
    require({row["allows_tau_response_claim"] for row in rows} == {"false"}, "materialization spec cannot allow Tau response claims")
    require({row["allows_dark_sector_verdict"] for row in rows} == {"false"}, "materialization spec cannot allow verdicts")
    require(len(summary) == 1, "Tau prediction materialization summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PLANCK_PR3_PEAK_TAU_PREDICTION_MATERIALIZATION_V01",
        "Tau prediction materialization summary id mismatch",
    )
    require(row["materialization_rows_declared"] == "36", "materialization row count mismatch")
    require(row["observed_candidate_rows_checked"] == "36", "observed candidate count mismatch")
    require(row["required_tau_payload_rows"] == "36", "required Tau payload count mismatch")
    require(row["tau_prediction_value_rows"] == "0", "Tau prediction values must be zero")
    require(row["tau_prediction_ell_rows"] == "0", "Tau prediction ell rows must be zero")
    require(row["tau_prediction_amplitude_rows"] == "0", "Tau prediction amplitude rows must be zero")
    require(row["tau_prediction_source_artifact_rows"] == "0", "Tau prediction source artifact rows must be zero")
    require(row["endpoint_blind_attestation_rows"] == "0", "endpoint-blind attestation rows must be zero")
    require(row["convention_lock_rows"] == "0", "convention lock rows must be zero")
    require(row["uncertainty_model_rows"] == "0", "uncertainty model rows must be zero")
    require(row["accepted_materialization_rows"] == "0", "accepted materialization rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["missing_prediction_rows"] == "36", "missing prediction row count mismatch")
    require(row["scores_computed"] == "false", "materialization spec cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "materialization spec cannot provide likelihood")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "TAU_PEAK_PREDICTION_MATERIALIZATION_SPEC_READY_PAYLOAD_MISSING_SCORE_BLOCKED",
        "Tau prediction materialization status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01",
        "Tau prediction materialization next artifact mismatch",
    )


def validate_tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_summary_v01.csv")
    require(len(rows) == 36, "Tau prediction payload supply must have 36 rows")
    require(
        {row["supply_mode"] for row in rows}
        == {"EXPLICIT_EMPTY_SUPPLY_NO_ENDPOINT_BLIND_TAU_ACOUSTIC_PREDICTION_AVAILABLE"},
        "payload supply mode mismatch",
    )
    require({row["endpoint_blind_derivation_trace_status"] for row in rows} == {"MISSING"}, "derivation trace must be missing")
    require({row["predicted_ell_center"] for row in rows} == {"NA"}, "predicted ell must be absent")
    require({row["predicted_observable_value"] for row in rows} == {"NA"}, "predicted values must be absent")
    require({row["prediction_uncertainty"] for row in rows} == {"NA"}, "prediction uncertainty must be absent")
    require({row["endpoint_blind_attestation_status"] for row in rows} == {"MISSING"}, "endpoint-blind attestation must be missing")
    require({row["null_response_control_status"] for row in rows} == {"NOT_SUPPLIED"}, "null-response control must be absent")
    require(
        {row["payload_acceptance_decision"] for row in rows}
        == {"REJECTED_NO_TAU_PREDICTION_OR_NULL_RESPONSE_PAYLOAD"},
        "payload acceptance decision mismatch",
    )
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "payload supply cannot allow score entry")
    require(
        {row["score_blocker"] for row in rows} == {"TAU_PEAK_PAYLOAD_SUPPLY_EXPLICITLY_EMPTY"},
        "payload supply score blocker mismatch",
    )
    require({row["hard_failure_triggered"] for row in rows} == {"false"}, "payload supply cannot trigger hard failures")
    require({row["allows_tau_response_claim"] for row in rows} == {"false"}, "payload supply cannot allow Tau response claims")
    require({row["allows_dark_sector_verdict"] for row in rows} == {"false"}, "payload supply cannot allow verdicts")
    require(len(summary) == 1, "Tau prediction payload supply summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PLANCK_PR3_PEAK_TAU_PREDICTION_PAYLOAD_SUPPLY_V01",
        "payload supply summary id mismatch",
    )
    require(row["payload_supply_rows_declared"] == "36", "payload supply row count mismatch")
    require(row["materialization_rows_checked"] == "36", "materialization row count mismatch")
    require(row["explicit_empty_supply_rows"] == "36", "explicit empty supply count mismatch")
    require(row["tau_prediction_payload_rows"] == "0", "Tau prediction payload count must be zero")
    require(row["null_response_control_rows"] == "0", "null-response control count must be zero")
    require(row["endpoint_blind_attestation_rows"] == "0", "endpoint-blind attestation count must be zero")
    require(row["convention_lock_rows"] == "0", "convention lock count must be zero")
    require(row["comparison_rule_rows"] == "0", "comparison rule count must be zero")
    require(row["accepted_payload_rows"] == "0", "accepted payload count must be zero")
    require(row["rejected_payload_rows"] == "36", "rejected payload count mismatch")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["scores_computed"] == "false", "payload supply cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "payload supply cannot provide likelihood")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "TAU_PEAK_PREDICTION_PAYLOAD_SUPPLY_EXPLICIT_EMPTY_SCORE_BLOCKED",
        "payload supply status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_acoustic_tau_prediction_source_derivation_v01",
        "payload supply next artifact mismatch",
    )


def validate_tau_cmb_acoustic_tau_prediction_source_derivation_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_acoustic_tau_prediction_source_derivation_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_acoustic_tau_prediction_source_derivation_summary_v01.csv")
    require(len(rows) == 8, "acoustic Tau prediction source derivation spine must have eight rows")
    require(
        any(row["symbolic_object"] == "S_tau_ac(k,a)" and row["derivation_status"] == "FORMAL_DEFINITION_ONLY_NOT_DERIVED" for row in rows),
        "formal acoustic source target row missing",
    )
    require(
        {row["score_entry_allowed"] for row in rows} == {"false"},
        "source derivation spine cannot allow score entry",
    )
    require(
        {row["allows_tau_response_claim"] for row in rows} == {"false"},
        "source derivation spine cannot allow Tau response claims",
    )
    require(
        {row["allows_dark_sector_verdict"] for row in rows} == {"false"},
        "source derivation spine cannot allow verdicts",
    )
    require(
        sum(row["derivation_status"].startswith("BLOCKED") for row in rows) == 6,
        "source derivation missing dependency count mismatch",
    )
    require(
        any(row["derivation_status"] == "FIREWALL_CLOSED" for row in rows),
        "score firewall row missing",
    )
    require(len(summary) == 1, "source derivation summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_ACOUSTIC_TAU_PREDICTION_SOURCE_DERIVATION_V01",
        "source derivation summary id mismatch",
    )
    require(row["derivation_rows_declared"] == "8", "source derivation row count mismatch")
    require(row["formal_definition_rows"] == "1", "formal definition count mismatch")
    require(row["dependency_rows"] == "5", "dependency row count mismatch")
    require(row["missing_dependency_rows"] == "6", "missing dependency row count mismatch")
    require(row["derived_source_rows"] == "0", "derived source rows must be zero")
    require(row["executable_prediction_rows"] == "0", "executable prediction rows must be zero")
    require(row["accepted_planck_payload_rows"] == "0", "accepted Planck payload rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "source derivation spine cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "source derivation spine cannot provide likelihood")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"]
        == "ACOUSTIC_TAU_PREDICTION_SOURCE_DERIVATION_SPINE_DECLARED_SOURCE_NOT_DERIVED_SCORE_BLOCKED",
        "source derivation status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_acoustic_source_operator_payload_v01",
        "source derivation next artifact mismatch",
    )


def validate_tau_cmb_acoustic_source_operator_payload_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_acoustic_source_operator_payload_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_acoustic_source_operator_payload_summary_v01.csv")
    require(len(rows) == 8, "acoustic source operator payload contract must have eight rows")
    require(
        [row["operator_component"] for row in rows]
        == [
            "domain_and_basis_lock",
            "effective_potential_input",
            "amplitude_input",
            "oscillator_kernel_rule",
            "baryon_loading_coupling",
            "projection_rule_to_peak_payload",
            "uncertainty_and_null_policy",
            "score_firewall",
        ],
        "operator payload component order mismatch",
    )
    require(
        sum(row["payload_status"] == "REQUIRED_NOT_SUPPLIED" for row in rows) == 7,
        "operator payload must have seven unsupplied required rows",
    )
    require(
        {row["score_entry_allowed"] for row in rows} == {"false"},
        "operator payload contract cannot allow score entry",
    )
    require(
        {row["allows_tau_response_claim"] for row in rows} == {"false"},
        "operator payload contract cannot allow Tau response claims",
    )
    require(
        {row["allows_dark_sector_verdict"] for row in rows} == {"false"},
        "operator payload contract cannot allow verdicts",
    )
    require(len(summary) == 1, "operator payload summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_V01", "operator payload summary id mismatch")
    require(row["operator_rows_declared"] == "8", "operator payload row count mismatch")
    require(row["required_operator_payload_rows"] == "7", "required operator payload count mismatch")
    require(row["payload_supplied_rows"] == "0", "payload supplied rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["payload_rejected_rows"] == "7", "payload rejected rows mismatch")
    require(row["endpoint_blind_pass_rows"] == "1", "endpoint-blind pass rows must contain only firewall row")
    require(row["dimension_convention_pass_rows"] == "1", "dimension/convention pass rows must contain only firewall row")
    require(row["derived_source_rows"] == "0", "derived source rows must be zero")
    require(row["executable_prediction_rows"] == "0", "executable prediction rows must be zero")
    require(row["accepted_planck_payload_rows"] == "0", "accepted Planck payload rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "operator payload contract cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "operator payload contract cannot provide likelihood")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_CONTRACT_DECLARED_PAYLOAD_NOT_SUPPLIED_SCORE_BLOCKED",
        "operator payload status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_acoustic_source_operator_payload_supply_v01",
        "operator payload next artifact mismatch",
    )


def validate_tau_cmb_acoustic_source_operator_payload_supply_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_acoustic_source_operator_payload_supply_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_acoustic_source_operator_payload_supply_summary_v01.csv")
    require(len(rows) == 8, "acoustic source operator payload supply must have eight rows")
    require(
        [row["operator_component"] for row in rows]
        == [
            "domain_and_basis_lock",
            "effective_potential_input",
            "amplitude_input",
            "oscillator_kernel_rule",
            "baryon_loading_coupling",
            "projection_rule_to_peak_payload",
            "uncertainty_and_null_policy",
            "score_firewall",
        ],
        "operator payload supply component order mismatch",
    )
    require(
        sum(row["supply_mode"] == "EXPLICIT_EMPTY_OPERATOR_PAYLOAD_SUPPLY" for row in rows) == 7,
        "operator payload supply must explicitly mark seven empty rows",
    )
    require(
        sum(row["acceptance_decision"] == "REJECTED_OPERATOR_PAYLOAD_SUPPLY_EMPTY" for row in rows) == 7,
        "operator payload supply must reject seven empty rows",
    )
    require(
        sum(row["supply_mode"] == "FIREWALL_PRESERVED" for row in rows) == 1,
        "operator payload supply must preserve one firewall row",
    )
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "operator payload supply cannot allow score entry")
    require(
        {row["allows_tau_response_claim"] for row in rows} == {"false"},
        "operator payload supply cannot allow Tau response claims",
    )
    require(
        {row["allows_dark_sector_verdict"] for row in rows} == {"false"},
        "operator payload supply cannot allow verdicts",
    )
    require(len(summary) == 1, "operator payload supply summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_SUPPLY_V01", "operator payload supply summary id mismatch")
    require(row["supply_rows_declared"] == "8", "operator payload supply row count mismatch")
    require(row["required_operator_payload_rows_checked"] == "7", "operator payload supply required count mismatch")
    require(row["operator_payload_supplied_rows"] == "0", "operator payload supplied rows must be zero")
    require(row["operator_payload_accepted_rows"] == "0", "operator payload accepted rows must be zero")
    require(row["operator_payload_rejected_rows"] == "7", "operator payload rejected rows mismatch")
    require(row["firewall_preserved_rows"] == "1", "operator payload firewall row mismatch")
    require(row["derived_source_rows"] == "0", "derived source rows must be zero")
    require(row["executable_prediction_rows"] == "0", "executable prediction rows must be zero")
    require(row["accepted_planck_payload_rows"] == "0", "accepted Planck payload rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "operator payload supply cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "operator payload supply cannot provide likelihood")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_SUPPLY_EXPLICIT_EMPTY_SCORE_BLOCKED",
        "operator payload supply status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_acoustic_minimal_operator_model_attempt_v01",
        "operator payload supply next artifact mismatch",
    )


def validate_tau_cmb_acoustic_minimal_operator_model_attempt_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_acoustic_minimal_operator_model_attempt_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_acoustic_minimal_operator_model_attempt_summary_v01.csv")
    require(len(rows) == 8, "acoustic minimal operator model attempt must have eight rows")
    require(
        [row["operator_component"] for row in rows]
        == [
            "domain_and_basis_lock",
            "effective_potential_input",
            "amplitude_input",
            "oscillator_kernel_rule",
            "baryon_loading_coupling",
            "projection_rule_to_peak_payload",
            "uncertainty_and_null_policy",
            "score_firewall",
        ],
        "minimal operator model component order mismatch",
    )
    require(
        sum(row["attempt_status"] == "FORMULA_SCAFFOLD_DECLARED_NOT_EXECUTABLE" for row in rows) == 3,
        "minimal operator model must declare three non-executable formula scaffolds",
    )
    require(
        sum(row["attempt_status"] == "DEPENDENCY_BLOCKED" for row in rows) == 3,
        "minimal operator model must keep three dependency-blocked rows",
    )
    require(
        sum(row["attempt_status"] == "CANDIDATE_RULE_DECLARED_NOT_ACCEPTED" for row in rows) == 1,
        "minimal operator model must keep the domain rule unaccepted",
    )
    require(
        sum(row["attempt_status"] == "FIREWALL_PRESERVED" for row in rows) == 1,
        "minimal operator model must preserve one firewall row",
    )
    require(
        {row["acceptance_decision"] for row in rows} == {"REJECTED_OPERATOR_MODEL_ROW_NOT_EXECUTABLE"},
        "minimal operator model cannot accept any row",
    )
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "minimal operator model cannot allow score entry")
    require(
        {row["allows_tau_response_claim"] for row in rows} == {"false"},
        "minimal operator model cannot allow Tau response claims",
    )
    require(
        {row["allows_dark_sector_verdict"] for row in rows} == {"false"},
        "minimal operator model cannot allow verdicts",
    )
    require(len(summary) == 1, "minimal operator model summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_ACOUSTIC_MINIMAL_OPERATOR_MODEL_ATTEMPT_V01", "minimal operator model summary id mismatch")
    require(row["model_rows_declared"] == "8", "minimal operator model row count mismatch")
    require(row["candidate_rule_rows_declared"] == "4", "minimal operator model candidate rule count mismatch")
    require(row["dependency_blocked_rows"] == "3", "minimal operator model dependency blocker count mismatch")
    require(row["dimensionally_closed_rows"] == "0", "minimal operator model cannot close dimensions")
    require(row["known_limit_closed_rows"] == "0", "minimal operator model cannot close known limits")
    require(row["operator_model_accepted_rows"] == "0", "minimal operator model cannot accept operator rows")
    require(row["derived_source_rows"] == "0", "derived source rows must be zero")
    require(row["executable_prediction_rows"] == "0", "executable prediction rows must be zero")
    require(row["accepted_planck_payload_rows"] == "0", "accepted Planck payload rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "minimal operator model cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "minimal operator model cannot provide likelihood")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "ACOUSTIC_MINIMAL_OPERATOR_MODEL_ATTEMPT_DECLARED_NOT_EXECUTABLE_SCORE_BLOCKED",
        "minimal operator model status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_acoustic_operator_dependency_unblock_plan_v01",
        "minimal operator model next artifact mismatch",
    )


def validate_tau_cmb_acoustic_operator_dependency_unblock_plan_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_acoustic_operator_dependency_unblock_plan_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_acoustic_operator_dependency_unblock_plan_summary_v01.csv")
    require(len(rows) == 8, "acoustic operator dependency unblock plan must have eight rows")
    require(
        [row["operator_component"] for row in rows]
        == [
            "domain_and_basis_lock",
            "effective_potential_input",
            "amplitude_input",
            "oscillator_kernel_rule",
            "baryon_loading_coupling",
            "projection_rule_to_peak_payload",
            "uncertainty_and_null_policy",
            "score_firewall",
        ],
        "acoustic operator dependency unblock component order mismatch",
    )
    require([row["priority_order"] for row in rows] == [str(i) for i in range(1, 9)], "unblock priorities must be ordered")
    require({row["unblock_status"] for row in rows} == {"DECLARED_NOT_COMPLETED"}, "unblock rows cannot be completed in v01")
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "unblock plan cannot allow score entry")
    require(
        {row["allows_tau_response_claim"] for row in rows} == {"false"},
        "unblock plan cannot allow Tau response claims",
    )
    require(
        {row["allows_dark_sector_verdict"] for row in rows} == {"false"},
        "unblock plan cannot allow verdicts",
    )
    require(
        rows[0]["required_unblock_artifact"] == "tau_cmb_acoustic_domain_basis_lock_acceptance_v01",
        "first unblock artifact must be domain/basis lock acceptance",
    )
    require(len(summary) == 1, "acoustic operator dependency unblock summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_ACOUSTIC_OPERATOR_DEPENDENCY_UNBLOCK_PLAN_V01", "unblock plan summary id mismatch")
    require(row["unblock_rows_declared"] == "8", "unblock plan row count mismatch")
    require(row["critical_unblock_rows"] == "7", "critical unblock count mismatch")
    require(row["completed_unblock_rows"] == "0", "completed unblock rows must be zero")
    require(row["pending_unblock_rows"] == "8", "pending unblock rows mismatch")
    require(row["operator_model_accepted_rows"] == "0", "operator model accepted rows must be zero")
    require(row["derived_source_rows"] == "0", "derived source rows must be zero")
    require(row["executable_prediction_rows"] == "0", "executable prediction rows must be zero")
    require(row["accepted_planck_payload_rows"] == "0", "accepted Planck payload rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "unblock plan cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "unblock plan cannot provide likelihood")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "ACOUSTIC_OPERATOR_DEPENDENCY_UNBLOCK_PLAN_DECLARED_SCORE_BLOCKED",
        "unblock plan status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_acoustic_domain_basis_lock_acceptance_v01",
        "unblock plan next artifact mismatch",
    )


def validate_tau_cmb_acoustic_domain_basis_lock_acceptance_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_acoustic_domain_basis_lock_acceptance_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_acoustic_domain_basis_lock_acceptance_summary_v01.csv")
    require(len(rows) == 7, "acoustic domain basis lock acceptance must have seven rows")
    require(
        [row["basis_component"] for row in rows]
        == [
            "wavenumber_domain",
            "scale_readout_domain",
            "recombination_readout_slice",
            "angular_peak_coordinate",
            "integration_measure_placeholder",
            "spectrum_role_basis",
            "comparison_boundary",
        ],
        "domain basis lock component order mismatch",
    )
    require(
        {row["acceptance_decision"] for row in rows} == {"ACCEPTED_DOMAIN_BASIS_LOCK_ROW"},
        "all domain basis lock rows must be accepted",
    )
    require(
        {row["endpoint_blind_status"] for row in rows} == {"PASS_NO_ENDPOINT_RESIDUALS_READ"},
        "domain basis lock must be endpoint-blind",
    )
    require(
        {row["dimension_convention_status"] for row in rows} == {"LOCKED_CONVENTION_ONLY"},
        "domain basis lock must remain convention-only",
    )
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "domain basis lock cannot allow score entry")
    require(
        {row["allows_tau_response_claim"] for row in rows} == {"false"},
        "domain basis lock cannot allow Tau response claims",
    )
    require(
        {row["allows_dark_sector_verdict"] for row in rows} == {"false"},
        "domain basis lock cannot allow verdicts",
    )
    require(len(summary) == 1, "domain basis lock summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_ACOUSTIC_DOMAIN_BASIS_LOCK_ACCEPTANCE_V01", "domain basis lock summary id mismatch")
    require(row["lock_rows_declared"] == "7", "domain basis lock row count mismatch")
    require(row["lock_rows_accepted"] == "7", "domain basis lock accepted count mismatch")
    require(row["endpoint_blind_pass_rows"] == "7", "domain basis endpoint-blind pass count mismatch")
    require(row["dimension_convention_locked_rows"] == "7", "domain basis convention count mismatch")
    require(row["domain_basis_lock_accepted"] == "true", "domain basis lock must be accepted")
    require(row["operator_model_accepted_rows"] == "1", "domain basis lock should accept one operator model row")
    require(row["derived_source_rows"] == "0", "derived source rows must be zero")
    require(row["executable_prediction_rows"] == "0", "executable prediction rows must be zero")
    require(row["accepted_planck_payload_rows"] == "0", "accepted Planck payload rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "domain basis lock cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "domain basis lock cannot provide likelihood")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "ACOUSTIC_DOMAIN_BASIS_LOCK_ACCEPTED_SCORE_BLOCKED",
        "domain basis lock status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01",
        "domain basis lock next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_eff_acoustic_input_acceptance_summary_v01.csv")
    require(len(rows) == 6, "Phi_tau_eff acoustic input acceptance must have six rows")
    require(
        [row["input_component"] for row in rows]
        == [
            "source_slot_identity",
            "endpoint_blind_provenance",
            "normalization_convention",
            "timing_sign_convention",
            "baryon_photon_coupling_role",
            "score_firewall",
        ],
        "Phi_tau_eff acoustic input component order mismatch",
    )
    require(
        sum(row["acceptance_status"].startswith("ACCEPTED") for row in rows) == 1,
        "only Phi_tau_eff source-slot identity can be accepted",
    )
    require(
        sum(row["acceptance_status"].startswith("BLOCKED") for row in rows) == 3,
        "Phi_tau_eff acoustic input must have three blocked rows",
    )
    require(
        sum(row["acceptance_status"].startswith("PARTIAL") for row in rows) == 1,
        "Phi_tau_eff acoustic input must have one partial row",
    )
    require(
        sum(row["acceptance_status"] == "FIREWALL_PRESERVED" for row in rows) == 1,
        "Phi_tau_eff acoustic input must preserve one firewall row",
    )
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "Phi_tau_eff input cannot allow score entry")
    require(
        {row["allows_tau_response_claim"] for row in rows} == {"false"},
        "Phi_tau_eff input cannot allow Tau response claims",
    )
    require(
        {row["allows_dark_sector_verdict"] for row in rows} == {"false"},
        "Phi_tau_eff input cannot allow verdicts",
    )
    require(len(summary) == 1, "Phi_tau_eff acoustic input summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_EFF_ACOUSTIC_INPUT_ACCEPTANCE_V01", "Phi_tau_eff input summary id mismatch")
    require(row["acceptance_rows_declared"] == "6", "Phi_tau_eff input row count mismatch")
    require(row["accepted_rows"] == "1", "Phi_tau_eff accepted rows mismatch")
    require(row["blocked_rows"] == "3", "Phi_tau_eff blocked rows mismatch")
    require(row["partial_rows"] == "1", "Phi_tau_eff partial rows mismatch")
    require(row["phi_tau_eff_source_slot_accepted"] == "true", "Phi_tau_eff source slot must be accepted")
    require(row["phi_tau_eff_acoustic_input_accepted"] == "false", "full Phi_tau_eff acoustic input cannot be accepted")
    require(row["operator_model_accepted_rows"] == "1", "only domain/basis operator row remains accepted")
    require(row["derived_source_rows"] == "0", "derived source rows must be zero")
    require(row["executable_prediction_rows"] == "0", "executable prediction rows must be zero")
    require(row["accepted_planck_payload_rows"] == "0", "accepted Planck payload rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "Phi_tau_eff input cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "Phi_tau_eff input cannot provide likelihood")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "PHI_TAU_EFF_ACOUSTIC_INPUT_IDENTITY_ACCEPTED_INPUT_BLOCKED_SCORE_BLOCKED",
        "Phi_tau_eff acoustic input status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01",
        "Phi_tau_eff acoustic input next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_summary_v01.csv"
    )
    require(len(rows) == 6, "Phi_tau_eff endpoint-blind provenance acceptance must have six rows")
    require(
        [row["provenance_component"] for row in rows]
        == [
            "endpoint_exclusion_rule",
            "parent_input_manifest",
            "parent_side_content",
            "derivation_rule",
            "audit_replay_package",
            "failure_branch",
        ],
        "Phi_tau_eff endpoint-blind provenance component order mismatch",
    )
    require(
        sum(row["acceptance_status"].startswith("ACCEPTED_POLICY") for row in rows) == 1,
        "only the endpoint-exclusion policy can be accepted",
    )
    require(
        sum(row["acceptance_status"].startswith("BLOCKED") for row in rows) == 4,
        "Phi_tau_eff endpoint-blind provenance must have four blocked rows",
    )
    require(
        sum(row["acceptance_status"].startswith("PARTIAL") for row in rows) == 1,
        "Phi_tau_eff endpoint-blind provenance must have one partial row",
    )
    require(
        {row["score_entry_allowed"] for row in rows} == {"false"},
        "Phi_tau_eff endpoint-blind provenance cannot allow score entry",
    )
    require(
        {row["allows_tau_response_claim"] for row in rows} == {"false"},
        "Phi_tau_eff endpoint-blind provenance cannot allow Tau response claims",
    )
    require(
        {row["allows_dark_sector_verdict"] for row in rows} == {"false"},
        "Phi_tau_eff endpoint-blind provenance cannot allow verdicts",
    )
    require(len(summary) == 1, "Phi_tau_eff endpoint-blind provenance summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_EFF_ENDPOINT_BLIND_PROVENANCE_ACCEPTANCE_V01",
        "Phi_tau_eff endpoint-blind provenance summary id mismatch",
    )
    require(row["provenance_acceptance_rows_declared"] == "6", "Phi_tau_eff provenance row count mismatch")
    require(row["accepted_policy_rows"] == "1", "Phi_tau_eff accepted policy rows mismatch")
    require(row["blocked_rows"] == "4", "Phi_tau_eff provenance blocked rows mismatch")
    require(row["partial_rows"] == "1", "Phi_tau_eff provenance partial rows mismatch")
    require(row["endpoint_exclusion_rule_accepted"] == "true", "endpoint-exclusion policy must be accepted")
    require(row["parent_input_manifest_supplied"] == "false", "parent input manifest must remain unsupplied")
    require(row["derivation_rule_supplied"] == "false", "derivation rule must remain unsupplied")
    require(row["replay_package_supplied"] == "false", "replay package must remain unsupplied")
    require(
        row["endpoint_blind_provenance_accepted"] == "false",
        "endpoint-blind provenance must remain unaccepted",
    )
    require(row["phi_tau_eff_acoustic_input_accepted"] == "false", "Phi_tau_eff acoustic input must remain blocked")
    require(row["operator_model_accepted_rows"] == "1", "only domain/basis operator row remains accepted")
    require(row["derived_source_rows"] == "0", "derived source rows must be zero")
    require(row["executable_prediction_rows"] == "0", "executable prediction rows must be zero")
    require(row["accepted_planck_payload_rows"] == "0", "accepted Planck payload rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "Phi_tau_eff provenance cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "Phi_tau_eff provenance cannot provide likelihood")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_EFF_ENDPOINT_BLIND_PROVENANCE_POLICY_ACCEPTED_PROVENANCE_BLOCKED_SCORE_BLOCKED",
        "Phi_tau_eff endpoint-blind provenance status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01",
        "Phi_tau_eff endpoint-blind provenance next artifact mismatch",
    )


def validate_tau_cmb_effective_potential_source_handoff_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_effective_potential_source_handoff_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_effective_potential_source_handoff_summary_v01.csv")
    require(len(rows) == 6, "effective potential source handoff must have six rows")
    require(
        [row["handoff_component"] for row in rows]
        == [
            "source_slot_identity",
            "endpoint_blind_provenance",
            "normalization_convention",
            "timing_sign_convention",
            "baryon_photon_coupling_role",
            "lensing_projection_handoff",
        ],
        "effective potential handoff component order mismatch",
    )
    require(sum(row["handoff_status"].startswith("DECLARED") for row in rows) == 1, "expected one declared handoff row")
    require(sum(row["handoff_status"].startswith("PARTIAL") for row in rows) == 1, "expected one partial handoff row")
    require(sum(row["handoff_status"].startswith("BLOCKED") for row in rows) == 4, "expected four blocked handoff rows")
    require({row["source_handoff_completed"] for row in rows} == {"false"}, "source handoff must remain incomplete")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "handoff cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6, "expected six handoff no-dark blockers")
    require(all(row["handoff_requirement"] for row in rows), "each handoff row needs a requirement")
    require(all(row["remaining_blocker"] for row in rows), "each handoff row needs a remaining blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "handoff cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "handoff cannot allow verdicts")
    require(len(summary) == 1, "handoff summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_EFFECTIVE_POTENTIAL_SOURCE_HANDOFF_V01", "handoff summary id mismatch")
    require(row["handoff_rows_declared"] == "6", "handoff row count mismatch")
    require(row["declared_rows"] == "1", "handoff declared row count mismatch")
    require(row["partial_rows"] == "1", "handoff partial row count mismatch")
    require(row["blocked_rows"] == "4", "handoff blocked row count mismatch")
    require(row["completed_rows"] == "0", "handoff completed rows must be zero")
    require(row["hard_failures_triggered"] == "0", "handoff hard failures must be zero")
    require(row["source_handoff_completed"] == "false", "source handoff must be incomplete")
    require(row["scores_computed"] == "false", "handoff cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "6", "handoff no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "EFFECTIVE_POTENTIAL_SOURCE_HANDOFF_DECLARED_BUT_BLOCKED",
        "handoff status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01",
        "handoff next artifact mismatch",
    )


def validate_tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_endpoint_blind_phi_tau_derivation_contract_summary_v01.csv")
    require(len(rows) == 6, "endpoint-blind Phi Tau contract must have six rows")
    require(
        [row["contract_component"] for row in rows]
        == [
            "parent_side_input_provenance",
            "endpoint_exclusion_rule",
            "derivation_rule_required",
            "normalization_lock",
            "audit_replay_package",
            "failure_branch",
        ],
        "endpoint-blind contract component order mismatch",
    )
    require(sum(row["contract_status"].startswith("DECLARED") for row in rows) == 1, "expected one declared contract row")
    require(sum(row["contract_status"].startswith("PARTIAL") for row in rows) == 2, "expected two partial contract rows")
    require(sum(row["contract_status"].startswith("BLOCKED") for row in rows) == 3, "expected three blocked contract rows")
    require({row["endpoint_blind_contract_satisfied"] for row in rows} == {"false"}, "contract must remain unsatisfied")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "contract cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6, "expected six contract no-dark blockers")
    require(all(row["contract_requirement"] for row in rows), "each contract row needs a requirement")
    require(all(row["endpoint_exclusion_rule"] for row in rows), "each contract row needs an endpoint exclusion rule")
    require(all(row["remaining_blocker"] for row in rows), "each contract row needs a remaining blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "contract cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "contract cannot allow verdicts")
    require(len(summary) == 1, "endpoint-blind contract summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_ENDPOINT_BLIND_PHI_TAU_DERIVATION_CONTRACT_V01", "contract summary id mismatch")
    require(row["contract_rows_declared"] == "6", "contract row count mismatch")
    require(row["declared_rows"] == "1", "contract declared row count mismatch")
    require(row["partial_rows"] == "2", "contract partial row count mismatch")
    require(row["blocked_rows"] == "3", "contract blocked row count mismatch")
    require(row["satisfied_rows"] == "0", "contract satisfied rows must be zero")
    require(row["hard_failures_triggered"] == "0", "contract hard failures must be zero")
    require(row["endpoint_blind_contract_satisfied"] == "false", "endpoint-blind contract must be unsatisfied")
    require(row["scores_computed"] == "false", "contract cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "6", "contract no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "ENDPOINT_BLIND_PHI_TAU_DERIVATION_CONTRACT_DECLARED_UNSATISFIED",
        "contract status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_provenance_v01",
        "contract next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_provenance_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_provenance_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_provenance_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input provenance must have seven rows")
    require(
        [row["parent_input_component"] for row in rows]
        == [
            "parent_input_manifest_identity",
            "tau_base_field_state",
            "morphological_seed_descriptor",
            "response_operator_inputs",
            "gauge_normalization_metadata",
            "endpoint_firewall_audit",
            "provenance_replay_status",
        ],
        "Phi Tau parent-input provenance component order mismatch",
    )
    require(sum(row["provenance_status"].startswith("DECLARED") for row in rows) == 1, "expected one declared provenance row")
    require(sum(row["provenance_status"].startswith("PARTIAL") for row in rows) == 2, "expected two partial provenance rows")
    require(sum(row["provenance_status"].startswith("BLOCKED") for row in rows) == 4, "expected four blocked provenance rows")
    require({row["parent_input_supplied"] for row in rows} == {"false"}, "parent inputs must remain unsupplied")
    require({row["provenance_satisfied"] for row in rows} == {"false"}, "provenance must remain unsatisfied")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "provenance cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven provenance no-dark blockers")
    require(all(row["required_parent_side_content"] for row in rows), "each provenance row needs required parent-side content")
    require(all(row["endpoint_firewall_rule"] for row in rows), "each provenance row needs an endpoint firewall rule")
    require(all(row["remaining_blocker"] for row in rows), "each provenance row needs a remaining blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "provenance cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "provenance cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input provenance summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_PROVENANCE_V01", "provenance summary id mismatch")
    require(row["provenance_rows_declared"] == "7", "provenance row count mismatch")
    require(row["declared_rows"] == "1", "provenance declared row count mismatch")
    require(row["partial_rows"] == "2", "provenance partial row count mismatch")
    require(row["blocked_rows"] == "4", "provenance blocked row count mismatch")
    require(row["supplied_rows"] == "0", "provenance supplied rows must be zero")
    require(row["satisfied_rows"] == "0", "provenance satisfied rows must be zero")
    require(row["hard_failures_triggered"] == "0", "provenance hard failures must be zero")
    require(row["parent_input_provenance_satisfied"] == "false", "parent-input provenance must be unsatisfied")
    require(row["scores_computed"] == "false", "provenance cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "provenance no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_PROVENANCE_DECLARED_UNSATISFIED",
        "provenance status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
        "provenance next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_candidate_manifest_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input candidate manifest must have seven rows")
    require(
        [row["candidate_component"] for row in rows]
        == [
            "candidate_manifest_identity",
            "base_field_state_candidate",
            "morphological_seed_candidate",
            "response_operator_candidate",
            "gauge_normalization_candidate",
            "endpoint_firewall_candidate",
            "provenance_replay_candidate",
        ],
        "Phi Tau parent-input candidate manifest component order mismatch",
    )
    require(sum(row["candidate_status"].startswith("DECLARED") for row in rows) == 1, "expected one declared candidate row")
    require(sum(row["candidate_status"].startswith("CANDIDATE") for row in rows) == 3, "expected three candidate rows")
    require(sum(row["candidate_status"].startswith("PARTIAL") for row in rows) == 2, "expected two partial candidate rows")
    require(sum(row["candidate_status"].startswith("BLOCKED") for row in rows) == 1, "expected one blocked candidate row")
    require({row["candidate_declared"] for row in rows} == {"true"}, "all candidate rows must be declared")
    require({row["candidate_accepted"] for row in rows} == {"false"}, "candidate inputs must remain unaccepted")
    require({row["manifest_satisfied"] for row in rows} == {"false"}, "candidate manifest must remain unsatisfied")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "candidate manifest cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven candidate no-dark blockers")
    require(all(row["candidate_parent_side_role"] for row in rows), "each candidate row needs a parent-side role")
    require(all(row["endpoint_exclusion_rule"] for row in rows), "each candidate row needs an endpoint exclusion rule")
    require(all(row["acceptance_requirement"] for row in rows), "each candidate row needs an acceptance requirement")
    require(all(row["remaining_blocker"] for row in rows), "each candidate row needs a remaining blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "candidate manifest cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "candidate manifest cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input candidate manifest summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_V01", "candidate manifest summary id mismatch")
    require(row["manifest_rows_declared"] == "7", "candidate manifest row count mismatch")
    require(row["declared_rows"] == "1", "candidate manifest declared row count mismatch")
    require(row["candidate_rows"] == "3", "candidate manifest candidate row count mismatch")
    require(row["partial_rows"] == "2", "candidate manifest partial row count mismatch")
    require(row["blocked_rows"] == "1", "candidate manifest blocked row count mismatch")
    require(row["accepted_rows"] == "0", "candidate manifest accepted rows must be zero")
    require(row["satisfied_rows"] == "0", "candidate manifest satisfied rows must be zero")
    require(row["hard_failures_triggered"] == "0", "candidate manifest hard failures must be zero")
    require(row["candidate_manifest_satisfied"] == "false", "candidate manifest must be unsatisfied")
    require(row["scores_computed"] == "false", "candidate manifest cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "candidate manifest no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_DECLARED_UNACCEPTED",
        "candidate manifest status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01",
        "candidate manifest next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau parent-input candidate manifest acceptance must have seven rows")
    require(
        [row["candidate_component"] for row in rows]
        == [
            "candidate_manifest_identity",
            "base_field_state_candidate",
            "morphological_seed_candidate",
            "response_operator_candidate",
            "gauge_normalization_candidate",
            "endpoint_firewall_candidate",
            "provenance_replay_candidate",
        ],
        "Phi Tau parent-input candidate manifest acceptance component order mismatch",
    )
    require(
        sum(row["acceptance_status"].startswith("ACCEPTED_IDENTITY") for row in rows) == 1,
        "candidate manifest acceptance must accept one identity row only",
    )
    require(
        sum(row["acceptance_status"].startswith("BLOCKED") for row in rows) == 4,
        "candidate manifest acceptance must have four blocked rows",
    )
    require(
        sum(row["acceptance_status"].startswith("PARTIAL") for row in rows) == 2,
        "candidate manifest acceptance must have two partial rows",
    )
    require({row["accepted_as_parent_input"] for row in rows} == {"false"}, "no parent inputs can be accepted")
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "candidate acceptance cannot allow score entry")
    require(
        {row["allows_tau_response_claim"] for row in rows} == {"false"},
        "candidate acceptance cannot allow Tau response claims",
    )
    require(
        {row["allows_dark_sector_verdict"] for row in rows} == {"false"},
        "candidate acceptance cannot allow verdicts",
    )
    require(len(summary) == 1, "Phi Tau parent-input candidate manifest acceptance summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_ACCEPTANCE_V01",
        "candidate manifest acceptance summary id mismatch",
    )
    require(row["candidate_acceptance_rows_declared"] == "7", "candidate manifest acceptance row count mismatch")
    require(row["accepted_identity_rows"] == "1", "candidate manifest accepted identity rows mismatch")
    require(row["accepted_parent_input_rows"] == "0", "candidate manifest accepted parent inputs must be zero")
    require(row["blocked_rows"] == "4", "candidate manifest acceptance blocked rows mismatch")
    require(row["partial_rows"] == "2", "candidate manifest acceptance partial rows mismatch")
    require(row["candidate_packet_identity_accepted"] == "true", "candidate packet identity must be accepted")
    require(row["base_field_state_accepted"] == "false", "base-field state must remain unaccepted")
    require(row["morphological_seed_accepted"] == "false", "morphological seed must remain unaccepted")
    require(row["response_operator_accepted"] == "false", "response operator must remain unaccepted")
    require(row["gauge_normalization_locked"] == "false", "gauge normalization must remain unlocked")
    require(row["endpoint_firewall_executed"] == "false", "endpoint firewall must remain unexecuted")
    require(row["provenance_replay_supplied"] == "false", "provenance replay must remain unsupplied")
    require(
        row["candidate_manifest_acceptance_satisfied"] == "false",
        "candidate manifest acceptance must remain unsatisfied",
    )
    require(row["endpoint_blind_provenance_accepted"] == "false", "endpoint-blind provenance must remain blocked")
    require(row["phi_tau_eff_acoustic_input_accepted"] == "false", "Phi_tau_eff acoustic input must remain blocked")
    require(row["operator_model_accepted_rows"] == "1", "only domain/basis operator row remains accepted")
    require(row["derived_source_rows"] == "0", "derived source rows must be zero")
    require(row["executable_prediction_rows"] == "0", "executable prediction rows must be zero")
    require(row["accepted_planck_payload_rows"] == "0", "accepted Planck payload rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "candidate acceptance cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "candidate acceptance cannot provide likelihood")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_IDENTITY_ACCEPTED_INPUTS_BLOCKED_SCORE_BLOCKED",
        "candidate manifest acceptance status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_firewall_audit_v01",
        "candidate manifest acceptance next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_firewall_audit_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_firewall_audit_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_firewall_audit_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input firewall audit must have seven rows")
    require(
        [row["audited_candidate_component"] for row in rows]
        == [
            "candidate_manifest_identity",
            "base_field_state_candidate",
            "morphological_seed_candidate",
            "response_operator_candidate",
            "gauge_normalization_candidate",
            "endpoint_firewall_candidate",
            "provenance_replay_candidate",
        ],
        "Phi Tau parent-input firewall audit component order mismatch",
    )
    require(sum(row["audit_status"].startswith("DECLARED") for row in rows) == 1, "expected one declared audit row")
    require(sum(row["audit_status"].startswith("PARTIAL") for row in rows) == 1, "expected one partial audit row")
    require(sum(row["audit_status"].startswith("BLOCKED") for row in rows) == 5, "expected five blocked audit rows")
    require({row["observed_endpoint_dependency"] for row in rows} == {"false"}, "no endpoint dependency can be observed without payload")
    require({row["endpoint_firewall_passed"] for row in rows} == {"false"}, "firewall cannot pass without payload")
    require({row["candidate_accepted"] for row in rows} == {"false"}, "candidate inputs must remain unaccepted")
    require({row["audit_satisfied"] for row in rows} == {"false"}, "firewall audit must remain unsatisfied")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "firewall audit cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven firewall no-dark blockers")
    require(all(row["audit_rule"] for row in rows), "each firewall row needs an audit rule")
    require(all(row["audit_evidence"] for row in rows), "each firewall row needs audit evidence")
    require(all(row["remaining_blocker"] for row in rows), "each firewall row needs a remaining blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "firewall audit cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "firewall audit cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input firewall audit summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_FIREWALL_AUDIT_V01", "firewall audit summary id mismatch")
    require(row["audit_rows_declared"] == "7", "firewall audit row count mismatch")
    require(row["declared_rows"] == "1", "firewall audit declared row count mismatch")
    require(row["partial_rows"] == "1", "firewall audit partial row count mismatch")
    require(row["blocked_rows"] == "5", "firewall audit blocked row count mismatch")
    require(row["passed_rows"] == "0", "firewall audit passed rows must be zero")
    require(row["accepted_rows"] == "0", "firewall audit accepted rows must be zero")
    require(row["satisfied_rows"] == "0", "firewall audit satisfied rows must be zero")
    require(row["endpoint_dependencies_detected"] == "0", "firewall audit endpoint dependency count mismatch")
    require(row["hard_failures_triggered"] == "0", "firewall audit hard failures must be zero")
    require(row["endpoint_firewall_audit_satisfied"] == "false", "firewall audit must be unsatisfied")
    require(row["scores_computed"] == "false", "firewall audit cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "firewall audit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_FIREWALL_AUDIT_DECLARED_BLOCKED_BY_MISSING_PAYLOAD",
        "firewall audit status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_payload_stub_v01",
        "firewall audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_payload_stub_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_payload_stub_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_payload_stub_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input payload stub must have seven rows")
    require(
        [row["payload_component"] for row in rows]
        == [
            "payload_manifest_identity",
            "base_field_state_payload_stub",
            "morphological_seed_payload_stub",
            "response_operator_payload_stub",
            "gauge_normalization_payload_stub",
            "endpoint_firewall_payload_stub",
            "provenance_replay_payload_stub",
        ],
        "Phi Tau parent-input payload stub component order mismatch",
    )
    require(sum(row["payload_status"].startswith("DECLARED") for row in rows) == 1, "expected one declared payload row")
    require(sum(row["payload_status"].startswith("STUB") for row in rows) == 4, "expected four payload stub rows")
    require(sum(row["payload_status"].startswith("PARTIAL") for row in rows) == 1, "expected one partial payload row")
    require(sum(row["payload_status"].startswith("BLOCKED") for row in rows) == 1, "expected one blocked payload row")
    require({row["payload_stub_declared"] for row in rows} == {"true"}, "payload stubs must be declared")
    require({row["concrete_payload_supplied"] for row in rows} == {"false"}, "concrete payload values must remain absent")
    require({row["endpoint_firewall_executable"] for row in rows} == {"false"}, "firewall cannot be executable without concrete payload")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload stubs cannot be accepted")
    require({row["payload_satisfied"] for row in rows} == {"false"}, "payload stub must remain unsatisfied")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "payload stub cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven payload no-dark blockers")
    require(all(row["stub_content"] for row in rows), "each payload row needs stub content")
    require(all(row["endpoint_exclusion_metadata"] for row in rows), "each payload row needs endpoint exclusion metadata")
    require(all(row["payload_limitation"] for row in rows), "each payload row needs a limitation")
    require(all(row["remaining_blocker"] for row in rows), "each payload row needs a remaining blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "payload stub cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "payload stub cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input payload stub summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_PAYLOAD_STUB_V01", "payload stub summary id mismatch")
    require(row["payload_rows_declared"] == "7", "payload stub row count mismatch")
    require(row["declared_rows"] == "1", "payload stub declared row count mismatch")
    require(row["stub_rows"] == "4", "payload stub row count mismatch")
    require(row["partial_rows"] == "1", "payload stub partial row count mismatch")
    require(row["blocked_rows"] == "1", "payload stub blocked row count mismatch")
    require(row["concrete_payload_rows"] == "0", "concrete payload rows must be zero")
    require(row["firewall_executable_rows"] == "0", "firewall executable rows must be zero")
    require(row["accepted_rows"] == "0", "payload stub accepted rows must be zero")
    require(row["satisfied_rows"] == "0", "payload stub satisfied rows must be zero")
    require(row["hard_failures_triggered"] == "0", "payload stub hard failures must be zero")
    require(row["payload_stub_satisfied"] == "false", "payload stub must be unsatisfied")
    require(row["scores_computed"] == "false", "payload stub cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "payload stub no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_PAYLOAD_STUB_DECLARED_NO_CONCRETE_VALUES",
        "payload stub status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_firewall_execution_v01",
        "payload stub next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_firewall_execution_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_firewall_execution_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_firewall_execution_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input firewall execution must have seven rows")
    require(
        [row["inspected_payload_component"] for row in rows]
        == [
            "payload_manifest_identity",
            "base_field_state_payload_stub",
            "morphological_seed_payload_stub",
            "response_operator_payload_stub",
            "gauge_normalization_payload_stub",
            "endpoint_firewall_payload_stub",
            "provenance_replay_payload_stub",
        ],
        "Phi Tau parent-input firewall execution component order mismatch",
    )
    require(sum(row["schema_firewall_executed"] == "true" for row in rows) == 6, "expected six schema-executed rows")
    require(sum(row["schema_firewall_passed"] == "true" for row in rows) == 6, "expected six schema-passed rows")
    require(sum(row["execution_status"].startswith("BLOCKED") for row in rows) == 1, "expected one blocked execution row")
    require({row["forbidden_endpoint_fields_present"] for row in rows} == {"false"}, "forbidden endpoint fields must remain absent")
    require({row["concrete_payload_supplied"] for row in rows} == {"false"}, "concrete payload values must remain absent")
    require({row["payload_firewall_passed"] for row in rows} == {"false"}, "payload firewall cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "firewall execution cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven firewall-execution no-dark blockers")
    require(all(row["forbidden_endpoint_fields_checked"] for row in rows), "each execution row needs checked fields")
    require(all(row["execution_evidence"] for row in rows), "each execution row needs evidence")
    require(all(row["remaining_blocker"] for row in rows), "each execution row needs a remaining blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "firewall execution cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "firewall execution cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input firewall execution summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_FIREWALL_EXECUTION_V01", "firewall execution summary id mismatch")
    require(row["execution_rows_declared"] == "7", "firewall execution row count mismatch")
    require(row["schema_executed_rows"] == "6", "firewall execution schema-executed row count mismatch")
    require(row["schema_passed_rows"] == "6", "firewall execution schema-passed row count mismatch")
    require(row["payload_passed_rows"] == "0", "payload-passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["blocked_rows"] == "1", "firewall execution blocked row count mismatch")
    require(row["forbidden_endpoint_fields_detected"] == "0", "forbidden endpoint field count mismatch")
    require(row["concrete_payload_rows"] == "0", "concrete payload rows must be zero")
    require(row["hard_failures_triggered"] == "0", "firewall execution hard failures must be zero")
    require(row["schema_firewall_execution_satisfied"] == "true", "schema firewall execution should be satisfied")
    require(row["payload_firewall_satisfied"] == "false", "payload firewall must remain unsatisfied")
    require(row["scores_computed"] == "false", "firewall execution cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "firewall execution no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_FIREWALL_EXECUTION_SCHEMA_PASS_PAYLOAD_BLOCKED",
        "firewall execution status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01",
        "firewall execution next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_requirements_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input concrete payload requirements must have seven rows")
    require(
        [row["payload_component"] for row in rows]
        == [
            "requirements_manifest_identity",
            "base_field_state_payload",
            "morphological_seed_payload",
            "response_operator_payload",
            "gauge_normalization_payload",
            "endpoint_firewall_payload",
            "provenance_replay_payload",
        ],
        "Phi Tau parent-input concrete payload requirements component order mismatch",
    )
    require(sum(row["requirement_status"].startswith("DECLARED") for row in rows) == 1, "expected one declared requirement row")
    require(sum(row["requirement_status"].startswith("REQUIREMENT") for row in rows) == 5, "expected five concrete requirement rows")
    require(sum(row["requirement_status"].startswith("BLOCKED") for row in rows) == 1, "expected one blocked replay requirement row")
    require({row["concrete_payload_supplied"] for row in rows} == {"false"}, "concrete payload values must remain absent")
    require({row["requirement_satisfied"] for row in rows} == {"false"}, "requirements must remain unsatisfied")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "requirements cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven concrete-payload no-dark blockers")
    require(all(row["required_payload_type"] for row in rows), "each row needs a required payload type")
    require(all(row["required_parent_side_content"] for row in rows), "each row needs required parent-side content")
    require(all(row["dimensional_or_units_requirement"] for row in rows), "each row needs a dimensional or units requirement")
    require(all(row["endpoint_blind_evidence_required"] for row in rows), "each row needs endpoint-blind evidence")
    require(all(row["replay_requirement"] for row in rows), "each row needs replay requirement")
    require(all(row["acceptance_criterion"] for row in rows), "each row needs an acceptance criterion")
    require(all(row["remaining_blocker"] for row in rows), "each row needs a remaining blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "requirements cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "requirements cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input concrete payload requirements summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_REQUIREMENTS_V01",
        "concrete payload requirements summary id mismatch",
    )
    require(row["requirement_rows_declared"] == "7", "concrete payload requirements row count mismatch")
    require(row["declared_rows"] == "1", "concrete payload requirements declared row count mismatch")
    require(row["requirement_rows"] == "5", "concrete payload requirements requirement row count mismatch")
    require(row["blocked_rows"] == "1", "concrete payload requirements blocked row count mismatch")
    require(row["concrete_payload_rows"] == "0", "concrete payload rows must be zero")
    require(row["satisfied_rows"] == "0", "satisfied rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["concrete_payload_requirements_satisfied"] == "false", "requirements must be unsatisfied")
    require(row["scores_computed"] == "false", "requirements cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "concrete payload no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_REQUIREMENTS_DECLARED_UNSATISFIED",
        "concrete payload requirements status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01",
        "concrete payload requirements next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_candidate_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input concrete payload candidate must have seven rows")
    require(
        [row["payload_component"] for row in rows]
        == [
            "candidate_payload_manifest_identity",
            "base_field_state_payload_candidate",
            "morphological_seed_payload_candidate",
            "response_operator_payload_candidate",
            "gauge_normalization_payload_candidate",
            "endpoint_firewall_payload_candidate",
            "provenance_replay_payload_candidate",
        ],
        "Phi Tau parent-input concrete payload candidate component order mismatch",
    )
    require(sum(row["candidate_status"].startswith("MANIFEST") for row in rows) == 1, "expected one manifest candidate row")
    require(sum(row["candidate_status"].startswith("CANDIDATE") for row in rows) == 4, "expected four candidate payload rows")
    require(sum(row["candidate_status"].startswith("BLOCKED") for row in rows) == 2, "expected two blocked payload rows")
    require({row["candidate_payload_declared"] for row in rows} == {"true"}, "all candidate payload rows must be declared")
    require(sum(row["concrete_payload_supplied"] == "true" for row in rows) == 5, "expected five concrete candidate payload rows")
    require({row["dimension_check_passed"] for row in rows} == {"false"}, "dimension checks must not pass")
    require({row["endpoint_firewall_passed"] for row in rows} == {"false"}, "payload firewall must not pass")
    require({row["replay_available"] for row in rows} == {"false"}, "replay must remain unavailable")
    require({row["payload_accepted"] for row in rows} == {"false"}, "candidate payload cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "candidate payload cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven candidate-payload no-dark blockers")
    require(all(row["candidate_payload_content"] for row in rows), "each candidate row needs payload content")
    require(all(row["dimension_or_units_status"] for row in rows), "each candidate row needs dimension/unit status")
    require(all(row["endpoint_blind_status"] for row in rows), "each candidate row needs endpoint-blind status")
    require(all(row["replay_status"] for row in rows), "each candidate row needs replay status")
    require(all(row["acceptance_blocker"] for row in rows), "each candidate row needs acceptance blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "candidate payload cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "candidate payload cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input concrete payload candidate summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_CANDIDATE_V01",
        "concrete payload candidate summary id mismatch",
    )
    require(row["candidate_rows_declared"] == "7", "candidate payload row count mismatch")
    require(row["manifest_rows"] == "1", "candidate payload manifest row count mismatch")
    require(row["candidate_payload_rows"] == "4", "candidate payload row count mismatch")
    require(row["blocked_rows"] == "2", "candidate payload blocked row count mismatch")
    require(row["concrete_payload_rows"] == "5", "concrete candidate payload row count mismatch")
    require(row["dimension_passed_rows"] == "0", "dimension passed rows must be zero")
    require(row["firewall_passed_rows"] == "0", "firewall passed rows must be zero")
    require(row["replay_available_rows"] == "0", "replay available rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["concrete_payload_candidate_satisfied"] == "false", "candidate payload must be unsatisfied")
    require(row["scores_computed"] == "false", "candidate payload cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "candidate payload no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_CANDIDATE_DECLARED_UNACCEPTED",
        "concrete payload candidate status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01",
        "concrete payload candidate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_payload_firewall_audit_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input payload firewall audit must have seven rows")
    require(
        [row["audited_payload_component"] for row in rows]
        == [
            "candidate_payload_manifest_identity",
            "base_field_state_payload_candidate",
            "morphological_seed_payload_candidate",
            "response_operator_payload_candidate",
            "gauge_normalization_payload_candidate",
            "endpoint_firewall_payload_candidate",
            "provenance_replay_payload_candidate",
        ],
        "Phi Tau parent-input payload firewall audit component order mismatch",
    )
    require(sum(row["payload_firewall_audited"] == "true" for row in rows) == 7, "all payload rows must be audited")
    require({row["endpoint_fields_detected"] for row in rows} == {"false"}, "endpoint-derived fields must not be detected")
    require(sum(row["audit_status"].startswith("BLOCKED") for row in rows) == 2, "expected two blocked payload-firewall rows")
    require({row["payload_firewall_passed"] for row in rows} == {"false"}, "payload firewall cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "payload firewall audit cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven payload-firewall no-dark blockers")
    require(all(row["endpoint_fields_checked"] for row in rows), "each audit row needs checked endpoint fields")
    require(all(row["dimension_check_status"] for row in rows), "each audit row needs dimension status")
    require(all(row["firewall_certificate_status"] == "certificate_missing" for row in rows), "certificate must remain missing")
    require(all(row["replay_status"] == "replay_missing" for row in rows), "replay must remain missing")
    require(all(row["payload_firewall_result"].startswith("BLOCKED") for row in rows), "all audit rows must remain blocked")
    require(all(row["audit_evidence"] for row in rows), "each audit row needs evidence")
    require(all(row["remaining_blocker"] for row in rows), "each audit row needs a remaining blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "payload audit cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "payload audit cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input payload firewall audit summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_PAYLOAD_FIREWALL_AUDIT_V01", "payload firewall audit summary id mismatch")
    require(row["audit_rows_declared"] == "7", "payload firewall audit row count mismatch")
    require(row["audited_rows"] == "7", "payload firewall audited row count mismatch")
    require(row["endpoint_clean_rows"] == "7", "payload firewall endpoint-clean row count mismatch")
    require(row["dimension_passed_rows"] == "0", "dimension passed rows must be zero")
    require(row["certificate_supplied_rows"] == "0", "certificate supplied rows must be zero")
    require(row["replay_available_rows"] == "0", "replay available rows must be zero")
    require(row["payload_passed_rows"] == "0", "payload passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["blocked_rows"] == "2", "payload firewall blocked row count mismatch")
    require(row["endpoint_fields_detected"] == "0", "endpoint field detected count must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["payload_firewall_audit_satisfied"] == "false", "payload firewall audit must be unsatisfied")
    require(row["scores_computed"] == "false", "payload firewall audit cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "payload firewall no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_PAYLOAD_FIREWALL_AUDIT_ENDPOINT_CLEAN_BUT_BLOCKED",
        "payload firewall audit status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_source_content_closure_decision_v01",
        "payload firewall audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_source_content_closure_decision_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_source_content_closure_decision_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_source_content_closure_decision_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent source-content closure decision must have seven rows")
    require(
        [row["source_content_component"] for row in rows]
        == [
            "candidate_payload_manifest_identity",
            "base_field_state_payload_candidate",
            "morphological_seed_payload_candidate",
            "response_operator_payload_candidate",
            "gauge_normalization_payload_candidate",
            "endpoint_firewall_payload_candidate",
            "provenance_replay_payload_candidate",
        ],
        "Phi Tau parent source-content closure component order mismatch",
    )
    require(sum(row["candidate_content_present"] == "true" for row in rows) == 5, "expected five candidate content rows")
    require({row["endpoint_clean"] for row in rows} == {"true"}, "all closure rows must be endpoint clean")
    require({row["dimension_or_lock_passed"] for row in rows} == {"false"}, "no dimension or lock row can pass")
    require({row["payload_firewall_passed"] for row in rows} == {"false"}, "payload firewall cannot pass")
    require({row["replay_available"] for row in rows} == {"false"}, "replay must remain unavailable")
    require({row["accepted_as_parent_input"] for row in rows} == {"false"}, "no parent input can be accepted")
    require(sum(row["closure_decision"].startswith("BLOCKED") for row in rows) == 5, "expected five blocked closure rows")
    require(sum(row["closure_decision"].startswith("PARTIAL") for row in rows) == 2, "expected two partial closure rows")
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "closure decision cannot allow score entry")
    require(
        {row["allows_tau_response_claim"] for row in rows} == {"false"},
        "closure decision cannot allow Tau response claims",
    )
    require(
        {row["allows_dark_sector_verdict"] for row in rows} == {"false"},
        "closure decision cannot allow verdicts",
    )
    require(len(summary) == 1, "Phi Tau parent source-content closure summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_SOURCE_CONTENT_CLOSURE_DECISION_V01",
        "source-content closure summary id mismatch",
    )
    require(row["source_content_rows_declared"] == "7", "source-content closure row count mismatch")
    require(row["candidate_content_rows"] == "5", "candidate content row count mismatch")
    require(row["endpoint_clean_rows"] == "7", "endpoint clean row count mismatch")
    require(row["dimension_or_lock_passed_rows"] == "0", "dimension/lock passed rows must be zero")
    require(row["payload_firewall_passed_rows"] == "0", "payload firewall passed rows must be zero")
    require(row["replay_available_rows"] == "0", "replay available rows must be zero")
    require(row["accepted_parent_input_rows"] == "0", "accepted parent input rows must be zero")
    require(row["closed_rows"] == "0", "closed rows must be zero")
    require(row["blocked_rows"] == "5", "blocked closure row count mismatch")
    require(row["partial_rows"] == "2", "partial closure row count mismatch")
    require(row["phi_tau_parent_source_content_closed"] == "false", "parent source content must remain unclosed")
    require(row["endpoint_blind_provenance_accepted"] == "false", "endpoint-blind provenance must remain blocked")
    require(row["phi_tau_eff_source_derivation_allowed"] == "false", "Phi_tau_eff derivation must remain disallowed")
    require(row["phi_tau_eff_acoustic_input_accepted"] == "false", "Phi_tau_eff acoustic input must remain blocked")
    require(row["operator_model_accepted_rows"] == "1", "only domain/basis operator row remains accepted")
    require(row["derived_source_rows"] == "0", "derived source rows must be zero")
    require(row["executable_prediction_rows"] == "0", "executable prediction rows must be zero")
    require(row["accepted_planck_payload_rows"] == "0", "accepted Planck payload rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "closure decision cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_SOURCE_CONTENT_ENDPOINT_CLEAN_BUT_UNCLOSED_SCORE_BLOCKED",
        "source-content closure status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01",
        "source-content closure next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_dimension_replay_certificate_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input dimension replay certificate must have seven rows")
    require(
        [row["certificate_component"] for row in rows]
        == [
            "certificate_manifest_identity",
            "base_field_dimension_replay_certificate",
            "seed_dimension_replay_certificate",
            "operator_dimension_replay_certificate",
            "gauge_normalization_replay_certificate",
            "payload_firewall_certificate",
            "executable_replay_certificate",
        ],
        "Phi Tau parent-input dimension replay certificate component order mismatch",
    )
    require(sum(row["certificate_status"].startswith("DECLARED") for row in rows) == 1, "expected one declared certificate row")
    require(sum(row["certificate_status"].startswith("REQUIREMENT") for row in rows) == 4, "expected four certificate requirement rows")
    require(sum(row["certificate_status"].startswith("BLOCKED") for row in rows) == 2, "expected two blocked certificate rows")
    require({row["dimension_certificate_supplied"] for row in rows} == {"false"}, "dimension certificates must remain absent")
    require({row["replay_certificate_supplied"] for row in rows} == {"false"}, "replay certificates must remain absent")
    require({row["firewall_certificate_supplied"] for row in rows} == {"false"}, "firewall certificates must remain absent")
    require({row["certificate_satisfied"] for row in rows} == {"false"}, "certificates must remain unsatisfied")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "certificate requirements cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven certificate no-dark blockers")
    require(all(row["dimension_certificate_requirement"] for row in rows), "each row needs dimension certificate requirement")
    require(all(row["replay_certificate_requirement"] for row in rows), "each row needs replay certificate requirement")
    require(all(row["firewall_certificate_requirement"] for row in rows), "each row needs firewall certificate requirement")
    require(all(row["remaining_blocker"] for row in rows), "each row needs a remaining blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "certificate requirements cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "certificate requirements cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input dimension replay certificate summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_DIMENSION_REPLAY_CERTIFICATE_V01", "certificate summary id mismatch")
    require(row["certificate_rows_declared"] == "7", "certificate row count mismatch")
    require(row["declared_rows"] == "1", "certificate declared row count mismatch")
    require(row["requirement_rows"] == "4", "certificate requirement row count mismatch")
    require(row["blocked_rows"] == "2", "certificate blocked row count mismatch")
    require(row["dimension_certificates_supplied"] == "0", "dimension certificate count must be zero")
    require(row["replay_certificates_supplied"] == "0", "replay certificate count must be zero")
    require(row["firewall_certificates_supplied"] == "0", "firewall certificate count must be zero")
    require(row["satisfied_rows"] == "0", "satisfied rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["dimension_replay_certificate_satisfied"] == "false", "dimension replay certificate must be unsatisfied")
    require(row["scores_computed"] == "false", "certificate requirements cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "certificate no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_DIMENSION_REPLAY_CERTIFICATE_DECLARED_UNSUPPLIED",
        "certificate status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_certificate_candidate_v01",
        "certificate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_certificate_candidate_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_candidate_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_candidate_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input certificate candidate must have seven rows")
    require(
        [row["certificate_component"] for row in rows]
        == [
            "certificate_candidate_manifest_identity",
            "base_field_dimension_replay_certificate_candidate",
            "seed_dimension_replay_certificate_candidate",
            "operator_dimension_replay_certificate_candidate",
            "gauge_normalization_replay_certificate_candidate",
            "payload_firewall_certificate_candidate",
            "executable_replay_certificate_candidate",
        ],
        "Phi Tau parent-input certificate candidate component order mismatch",
    )
    require(sum(row["candidate_status"].startswith("MANIFEST") for row in rows) == 1, "expected one candidate manifest row")
    require(sum(row["candidate_status"].startswith("CANDIDATE") for row in rows) == 4, "expected four candidate certificate rows")
    require(sum(row["candidate_status"].startswith("BLOCKED") for row in rows) == 2, "expected two blocked certificate candidate rows")
    require({row["certificate_candidate_declared"] for row in rows} == {"true"}, "candidate certificates must be declared")
    require({row["dimension_certificate_supplied"] for row in rows} == {"false"}, "dimension certificates must remain absent")
    require({row["replay_certificate_supplied"] for row in rows} == {"false"}, "replay certificates must remain absent")
    require({row["firewall_certificate_supplied"] for row in rows} == {"false"}, "firewall certificates must remain absent")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate candidates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "certificate candidates cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven certificate candidate no-dark blockers")
    require(all(row["candidate_certificate_content"] for row in rows), "each row needs candidate certificate content")
    require(all(row["dimension_certificate_status"] for row in rows), "each row needs dimension certificate status")
    require(all(row["replay_certificate_status"] for row in rows), "each row needs replay certificate status")
    require(all(row["firewall_certificate_status"] for row in rows), "each row needs firewall certificate status")
    require(all(row["acceptance_blocker"] for row in rows), "each row needs an acceptance blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "certificate candidates cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "certificate candidates cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input certificate candidate summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_CANDIDATE_V01", "certificate candidate summary id mismatch")
    require(row["candidate_rows_declared"] == "7", "certificate candidate row count mismatch")
    require(row["manifest_rows"] == "1", "certificate candidate manifest row count mismatch")
    require(row["candidate_certificate_rows"] == "4", "certificate candidate row count mismatch")
    require(row["blocked_rows"] == "2", "certificate candidate blocked row count mismatch")
    require(row["dimension_certificates_supplied"] == "0", "dimension certificate count must be zero")
    require(row["replay_certificates_supplied"] == "0", "replay certificate count must be zero")
    require(row["firewall_certificates_supplied"] == "0", "firewall certificate count must be zero")
    require(row["certificate_passed_rows"] == "0", "passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["certificate_candidate_satisfied"] == "false", "certificate candidate must be unsatisfied")
    require(row["scores_computed"] == "false", "certificate candidate cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "certificate candidate no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_CERTIFICATE_CANDIDATE_DECLARED_UNPASSED",
        "certificate candidate status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_certificate_audit_v01",
        "certificate candidate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_certificate_audit_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_audit_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_audit_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input certificate audit must have seven rows")
    require(
        [row["certificate_component"] for row in rows]
        == [
            "certificate_candidate_manifest_identity",
            "base_field_dimension_replay_certificate_candidate",
            "seed_dimension_replay_certificate_candidate",
            "operator_dimension_replay_certificate_candidate",
            "gauge_normalization_replay_certificate_candidate",
            "payload_firewall_certificate_candidate",
            "executable_replay_certificate_candidate",
        ],
        "Phi Tau parent-input certificate audit component order mismatch",
    )
    require({row["audit_status"] for row in rows} == {"AUDIT_FAIL_MISSING_CERTIFICATE_EVIDENCE"}, "audit must fail without evidence")
    require({row["candidate_audited"] for row in rows} == {"true"}, "all candidates must be audited")
    require({row["certificate_evidence_supplied"] for row in rows} == {"false"}, "certificate evidence must remain absent")
    require({row["dimension_audit_passed"] for row in rows} == {"false"}, "dimension audits cannot pass")
    require({row["replay_audit_passed"] for row in rows} == {"false"}, "replay audits cannot pass")
    require({row["firewall_audit_passed"] for row in rows} == {"false"}, "firewall audits cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "certificate audit cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven certificate audit no-dark blockers")
    require(all(row["audit_finding"] for row in rows), "each row needs an audit finding")
    require(all(row["missing_evidence"] for row in rows), "each row needs missing evidence")
    require(
        all(row["acceptance_decision"] == "reject_for_scoring_input_acceptance" for row in rows),
        "each row must reject scoring acceptance",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "certificate audit cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "certificate audit cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input certificate audit summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_AUDIT_V01", "certificate audit summary id mismatch")
    require(row["audit_rows_declared"] == "7", "certificate audit row count mismatch")
    require(row["audited_rows"] == "7", "audited row count mismatch")
    require(row["audit_passed_rows"] == "0", "audit passed rows must be zero")
    require(row["audit_failed_rows"] == "7", "audit failed rows must be seven")
    require(row["certificate_evidence_supplied_rows"] == "0", "certificate evidence supplied rows must be zero")
    require(row["dimension_audit_passed_rows"] == "0", "dimension audit passed rows must be zero")
    require(row["replay_audit_passed_rows"] == "0", "replay audit passed rows must be zero")
    require(row["firewall_audit_passed_rows"] == "0", "firewall audit passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["certificate_audit_satisfied"] == "false", "certificate audit must be unsatisfied")
    require(row["scores_computed"] == "false", "certificate audit cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "certificate audit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_CERTIFICATE_AUDIT_FAILED_MISSING_EVIDENCE",
        "certificate audit status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_certificate_closure_decision_v01",
        "certificate audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_certificate_closure_decision_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_certificate_closure_decision_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_certificate_closure_decision_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent certificate closure decision must have seven rows")
    require(
        [row["certificate_component"] for row in rows]
        == [
            "certificate_candidate_manifest_identity",
            "base_field_dimension_replay_certificate_candidate",
            "seed_dimension_replay_certificate_candidate",
            "operator_dimension_replay_certificate_candidate",
            "gauge_normalization_replay_certificate_candidate",
            "payload_firewall_certificate_candidate",
            "executable_replay_certificate_candidate",
        ],
        "Phi Tau parent certificate closure component order mismatch",
    )
    require({row["requirement_declared"] for row in rows} == {"true"}, "all certificate requirements must be declared")
    require({row["candidate_declared"] for row in rows} == {"true"}, "all certificate candidates must be declared")
    require({row["candidate_audited"] for row in rows} == {"true"}, "all certificate candidates must be audited")
    require({row["certificate_evidence_supplied"] for row in rows} == {"false"}, "certificate evidence must remain absent")
    require({row["dimension_passed"] for row in rows} == {"false"}, "dimension checks cannot pass")
    require({row["replay_passed"] for row in rows} == {"false"}, "replay checks cannot pass")
    require({row["firewall_passed"] for row in rows} == {"false"}, "firewall checks cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["closure_decision"] for row in rows} == {"BLOCKED_CERTIFICATE_NOT_CLOSED"}, "certificates must be blocked")
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "certificate closure cannot allow score entry")
    require(
        {row["allows_tau_response_claim"] for row in rows} == {"false"},
        "certificate closure cannot allow Tau response claims",
    )
    require(
        {row["allows_dark_sector_verdict"] for row in rows} == {"false"},
        "certificate closure cannot allow verdicts",
    )
    require(len(summary) == 1, "Phi Tau parent certificate closure summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_CERTIFICATE_CLOSURE_DECISION_V01",
        "certificate closure summary id mismatch",
    )
    require(row["certificate_closure_rows_declared"] == "7", "certificate closure row count mismatch")
    require(row["requirements_declared_rows"] == "7", "requirements declared row count mismatch")
    require(row["candidate_declared_rows"] == "7", "candidate declared row count mismatch")
    require(row["candidate_audited_rows"] == "7", "candidate audited row count mismatch")
    require(row["certificate_evidence_supplied_rows"] == "0", "certificate evidence supplied rows must be zero")
    require(row["dimension_passed_rows"] == "0", "dimension passed rows must be zero")
    require(row["replay_passed_rows"] == "0", "replay passed rows must be zero")
    require(row["firewall_passed_rows"] == "0", "firewall passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["closed_rows"] == "0", "closed rows must be zero")
    require(row["blocked_rows"] == "7", "blocked rows must be seven")
    require(row["phi_tau_parent_certificates_closed"] == "false", "parent certificates must remain unclosed")
    require(row["phi_tau_parent_source_content_closed"] == "false", "parent source content must remain unclosed")
    require(row["endpoint_blind_provenance_accepted"] == "false", "endpoint-blind provenance must remain blocked")
    require(row["phi_tau_eff_source_derivation_allowed"] == "false", "Phi_tau_eff derivation must remain disallowed")
    require(row["phi_tau_eff_acoustic_input_accepted"] == "false", "Phi_tau_eff acoustic input must remain blocked")
    require(row["operator_model_accepted_rows"] == "1", "only domain/basis operator row remains accepted")
    require(row["derived_source_rows"] == "0", "derived source rows must be zero")
    require(row["executable_prediction_rows"] == "0", "executable prediction rows must be zero")
    require(row["accepted_planck_payload_rows"] == "0", "accepted Planck payload rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "certificate closure cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must remain blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must remain blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_CERTIFICATES_DECLARED_AND_AUDITED_BUT_UNCLOSED_SCORE_BLOCKED",
        "certificate closure status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01",
        "certificate closure next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_request_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input certificate evidence request must have seven rows")
    require(
        [row["certificate_component"] for row in rows]
        == [
            "certificate_candidate_manifest_identity",
            "base_field_dimension_replay_certificate_candidate",
            "seed_dimension_replay_certificate_candidate",
            "operator_dimension_replay_certificate_candidate",
            "gauge_normalization_replay_certificate_candidate",
            "payload_firewall_certificate_candidate",
            "executable_replay_certificate_candidate",
        ],
        "Phi Tau parent-input certificate evidence request component order mismatch",
    )
    require({row["request_status"] for row in rows} == {"EVIDENCE_REQUESTED_NOT_SUPPLIED"}, "evidence requests must remain unsupplied")
    require({row["evidence_requested"] for row in rows} == {"true"}, "all rows must request evidence")
    require({row["evidence_supplied"] for row in rows} == {"false"}, "evidence must remain absent")
    require({row["dimension_evidence_supplied"] for row in rows} == {"false"}, "dimension evidence must remain absent")
    require({row["replay_evidence_supplied"] for row in rows} == {"false"}, "replay evidence must remain absent")
    require({row["firewall_evidence_supplied"] for row in rows} == {"false"}, "firewall evidence must remain absent")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "evidence request cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven evidence request no-dark blockers")
    require(all(row["required_evidence_bundle"] for row in rows), "each row needs a required evidence bundle")
    require(all(row["dimension_evidence_request"] for row in rows), "each row needs a dimension evidence request")
    require(all(row["replay_evidence_request"] for row in rows), "each row needs a replay evidence request")
    require(all(row["firewall_evidence_request"] for row in rows), "each row needs a firewall evidence request")
    require(all(row["acceptance_criterion"] for row in rows), "each row needs an acceptance criterion")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "evidence request cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "evidence request cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input certificate evidence request summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_REQUEST_V01", "evidence request summary id mismatch")
    require(row["request_rows_declared"] == "7", "evidence request row count mismatch")
    require(row["evidence_requested_rows"] == "7", "evidence requested row count mismatch")
    require(row["evidence_supplied_rows"] == "0", "evidence supplied rows must be zero")
    require(row["dimension_evidence_supplied_rows"] == "0", "dimension evidence supplied rows must be zero")
    require(row["replay_evidence_supplied_rows"] == "0", "replay evidence supplied rows must be zero")
    require(row["firewall_evidence_supplied_rows"] == "0", "firewall evidence supplied rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["certificate_evidence_request_satisfied"] == "false", "certificate evidence request must be unsatisfied")
    require(row["scores_computed"] == "false", "evidence request cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "evidence request no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_REQUESTED_NOT_SUPPLIED",
        "evidence request status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01",
        "evidence request next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input certificate evidence package candidate must have seven rows")
    require(
        [row["certificate_component"] for row in rows]
        == [
            "certificate_candidate_manifest_identity",
            "base_field_dimension_replay_certificate_candidate",
            "seed_dimension_replay_certificate_candidate",
            "operator_dimension_replay_certificate_candidate",
            "gauge_normalization_replay_certificate_candidate",
            "payload_firewall_certificate_candidate",
            "executable_replay_certificate_candidate",
        ],
        "Phi Tau parent-input certificate evidence package candidate component order mismatch",
    )
    require(
        {row["package_candidate_status"] for row in rows} == {"EVIDENCE_PACKAGE_CANDIDATE_DECLARED_UNPOPULATED"},
        "evidence package candidates must remain unpopulated",
    )
    require({row["package_candidate_declared"] for row in rows} == {"true"}, "package candidates must be declared")
    require({row["dimension_evidence_slot_declared"] for row in rows} == {"true"}, "dimension evidence slots must be declared")
    require({row["replay_evidence_slot_declared"] for row in rows} == {"true"}, "replay evidence slots must be declared")
    require({row["firewall_evidence_slot_declared"] for row in rows} == {"true"}, "firewall evidence slots must be declared")
    require({row["evidence_payload_supplied"] for row in rows} == {"false"}, "evidence payloads must remain absent")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "package candidate cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven package candidate no-dark blockers")
    require(all(row["package_candidate_content"] for row in rows), "each row needs package candidate content")
    require(all(row["required_dimension_evidence_slot"] for row in rows), "each row needs a dimension evidence slot")
    require(all(row["required_replay_evidence_slot"] for row in rows), "each row needs a replay evidence slot")
    require(all(row["required_firewall_evidence_slot"] for row in rows), "each row needs a firewall evidence slot")
    require(all(row["package_acceptance_gate"] for row in rows), "each row needs a package acceptance gate")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "package candidate cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "package candidate cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input evidence package candidate summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_CANDIDATE_V01",
        "package candidate summary id mismatch",
    )
    require(row["package_rows_declared"] == "7", "package candidate row count mismatch")
    require(row["package_candidate_rows"] == "7", "package candidate declared row count mismatch")
    require(row["dimension_slots_declared"] == "7", "dimension slot count mismatch")
    require(row["replay_slots_declared"] == "7", "replay slot count mismatch")
    require(row["firewall_slots_declared"] == "7", "firewall slot count mismatch")
    require(row["evidence_payload_supplied_rows"] == "0", "evidence payload supplied rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["certificate_evidence_package_candidate_satisfied"] == "false",
        "certificate evidence package candidate must be unsatisfied",
    )
    require(row["scores_computed"] == "false", "package candidate cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "package candidate no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_CANDIDATE_DECLARED_UNPOPULATED",
        "package candidate status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01",
        "package candidate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent-input certificate evidence package audit must have seven rows")
    require(
        [row["certificate_component"] for row in rows]
        == [
            "certificate_candidate_manifest_identity",
            "base_field_dimension_replay_certificate_candidate",
            "seed_dimension_replay_certificate_candidate",
            "operator_dimension_replay_certificate_candidate",
            "gauge_normalization_replay_certificate_candidate",
            "payload_firewall_certificate_candidate",
            "executable_replay_certificate_candidate",
        ],
        "Phi Tau parent-input certificate evidence package audit component order mismatch",
    )
    require(
        {row["package_audit_status"] for row in rows} == {"PACKAGE_AUDIT_FAIL_UNPOPULATED_EVIDENCE_PAYLOAD"},
        "package audit must fail for unpopulated evidence payloads",
    )
    require({row["package_candidate_audited"] for row in rows} == {"true"}, "all package candidates must be audited")
    require({row["evidence_payload_supplied"] for row in rows} == {"false"}, "evidence payloads must remain absent")
    require({row["dimension_payload_supplied"] for row in rows} == {"false"}, "dimension payloads must remain absent")
    require({row["replay_payload_supplied"] for row in rows} == {"false"}, "replay payloads must remain absent")
    require({row["firewall_payload_supplied"] for row in rows} == {"false"}, "firewall payloads must remain absent")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "package audit cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven package audit no-dark blockers")
    require(all(row["audit_finding"] for row in rows), "each row needs an audit finding")
    require(all(row["missing_payload"] for row in rows), "each row needs missing payload")
    require(
        all(row["package_acceptance_decision"] == "reject_package_for_scoring_input_acceptance" for row in rows),
        "each row must reject package scoring acceptance",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "package audit cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "package audit cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input evidence package audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_AUDIT_V01",
        "package audit summary id mismatch",
    )
    require(row["audit_rows_declared"] == "7", "package audit row count mismatch")
    require(row["package_candidate_audited_rows"] == "7", "package candidate audited row count mismatch")
    require(row["package_audit_passed_rows"] == "0", "package audit passed rows must be zero")
    require(row["package_audit_failed_rows"] == "7", "package audit failed rows must be seven")
    require(row["evidence_payload_supplied_rows"] == "0", "evidence payload supplied rows must be zero")
    require(row["dimension_payload_supplied_rows"] == "0", "dimension payload supplied rows must be zero")
    require(row["replay_payload_supplied_rows"] == "0", "replay payload supplied rows must be zero")
    require(row["firewall_payload_supplied_rows"] == "0", "firewall payload supplied rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["certificate_evidence_package_audit_satisfied"] == "false", "certificate evidence package audit must be unsatisfied")
    require(row["scores_computed"] == "false", "package audit cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "package audit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_AUDIT_FAILED_UNPOPULATED",
        "package audit status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01",
        "package audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_package_closure_decision_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent evidence-package closure decision must have seven rows")
    require(
        [row["evidence_component"] for row in rows]
        == [
            "certificate_candidate_manifest_identity",
            "base_field_dimension_replay_certificate_candidate",
            "seed_dimension_replay_certificate_candidate",
            "operator_dimension_replay_certificate_candidate",
            "gauge_normalization_replay_certificate_candidate",
            "payload_firewall_certificate_candidate",
            "executable_replay_certificate_candidate",
        ],
        "Phi Tau parent evidence-package closure component order mismatch",
    )
    require({row["evidence_requested"] for row in rows} == {"true"}, "all evidence rows must be requested")
    require({row["package_candidate_declared"] for row in rows} == {"true"}, "all package candidates must be declared")
    require({row["package_audited"] for row in rows} == {"true"}, "all packages must be audited")
    require({row["evidence_payload_supplied"] for row in rows} == {"false"}, "evidence payloads must remain absent")
    require({row["dimension_evidence_supplied"] for row in rows} == {"false"}, "dimension evidence must remain absent")
    require({row["replay_evidence_supplied"] for row in rows} == {"false"}, "replay evidence must remain absent")
    require({row["firewall_evidence_supplied"] for row in rows} == {"false"}, "firewall evidence must remain absent")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require(
        {row["closure_decision"] for row in rows} == {"BLOCKED_EVIDENCE_PACKAGE_NOT_CLOSED"},
        "evidence package closure must remain blocked",
    )
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "score entry must remain blocked")
    require(all(row["remaining_blocker"] for row in rows), "each closure row needs a remaining blocker")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "closure cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "closure cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent evidence-package closure summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PACKAGE_CLOSURE_DECISION_V01",
        "evidence-package closure summary id mismatch",
    )
    require(row["evidence_closure_rows_declared"] == "7", "evidence closure row count mismatch")
    require(row["evidence_requested_rows"] == "7", "evidence requested row count mismatch")
    require(row["package_candidate_declared_rows"] == "7", "package candidate declared row count mismatch")
    require(row["package_audited_rows"] == "7", "package audited row count mismatch")
    require(row["evidence_payload_supplied_rows"] == "0", "evidence payload supplied rows must be zero")
    require(row["dimension_evidence_supplied_rows"] == "0", "dimension evidence supplied rows must be zero")
    require(row["replay_evidence_supplied_rows"] == "0", "replay evidence supplied rows must be zero")
    require(row["firewall_evidence_supplied_rows"] == "0", "firewall evidence supplied rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["closed_rows"] == "0", "closed rows must be zero")
    require(row["blocked_rows"] == "7", "blocked rows must be seven")
    require(row["phi_tau_parent_evidence_package_closed"] == "false", "evidence package must remain unclosed")
    require(row["phi_tau_parent_certificates_closed"] == "false", "certificates must remain unclosed")
    require(row["phi_tau_parent_source_content_closed"] == "false", "source content must remain unclosed")
    require(row["endpoint_blind_provenance_accepted"] == "false", "endpoint-blind provenance must remain unaccepted")
    require(row["phi_tau_eff_source_derivation_allowed"] == "false", "Phi_tau_eff derivation must remain blocked")
    require(row["phi_tau_eff_acoustic_input_accepted"] == "false", "Phi_tau_eff acoustic input must remain blocked")
    require(row["operator_model_accepted_rows"] == "1", "operator model accepted row count mismatch")
    require(row["derived_source_rows"] == "0", "derived source rows must be zero")
    require(row["executable_prediction_rows"] == "0", "executable prediction rows must be zero")
    require(row["accepted_planck_payload_rows"] == "0", "accepted Planck payload rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "closure cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "closure cannot provide a CMB likelihood")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_EVIDENCE_PACKAGE_DECLARED_AND_AUDITED_BUT_UNCLOSED_SCORE_BLOCKED",
        "evidence-package closure status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01",
        "evidence-package closure next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_summary_v01.csv")
    require(len(rows) == 5, "Phi Tau parent-input scoring acceptance precheck must have five rows")
    require(
        [row["acceptance_component"] for row in rows]
        == [
            "evidence_package_acceptance",
            "certificate_acceptance",
            "payload_acceptance",
            "phi_tau_eff_derivation_acceptance",
            "cmb_scoring_acceptance",
        ],
        "Phi Tau parent-input scoring acceptance component order mismatch",
    )
    require({row["precheck_status"] for row in rows} == {"SCORING_ACCEPTANCE_PRECHECK_BLOCKED"}, "precheck rows must be blocked")
    require({row["precheck_executed"] for row in rows} == {"true"}, "precheck rows must be executed")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["phi_tau_eff_derivable"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derivable")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring inputs cannot be accepted")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood must remain unavailable")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "precheck cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five precheck no-dark blockers")
    require(all(row["blocking_condition"] for row in rows), "each row needs a blocking condition")
    require(all(row["required_unblock_condition"] for row in rows), "each row needs a required unblock condition")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "precheck cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "precheck cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input scoring acceptance precheck summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_PRECHECK_V01", "precheck summary id mismatch")
    require(row["precheck_rows_declared"] == "5", "precheck row count mismatch")
    require(row["precheck_executed_rows"] == "5", "precheck executed row count mismatch")
    require(row["blocked_rows"] == "5", "blocked row count mismatch")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["phi_tau_eff_derivable_rows"] == "0", "Phi_tau_eff derivable rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["scores_computed"] == "false", "precheck cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["scoring_acceptance_precheck_satisfied"] == "false", "scoring acceptance precheck must be unsatisfied")
    require(row["no_dark_blockers"] == "5", "precheck no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(row["overall_status"] == "PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_PRECHECK_BLOCKED", "precheck status mismatch")
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01",
        "precheck next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_summary_v01.csv")
    require(len(rows) == 5, "Phi Tau parent-input scoring acceptance unblock plan must have five rows")
    require(
        [row["acceptance_component"] for row in rows]
        == [
            "evidence_package_acceptance",
            "certificate_acceptance",
            "payload_acceptance",
            "phi_tau_eff_derivation_acceptance",
            "cmb_scoring_acceptance",
        ],
        "Phi Tau parent-input scoring acceptance unblock component order mismatch",
    )
    require([row["rank"] for row in rows] == ["1", "2", "3", "4", "5"], "unblock plan rank order mismatch")
    require({row["plan_declared"] for row in rows} == {"true"}, "all unblock plan rows must be declared")
    require({row["unblock_completed"] for row in rows} == {"false"}, "unblock steps must remain open")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["phi_tau_eff_derivable"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derivable")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring inputs cannot be accepted")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood must remain unavailable")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "unblock plan cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5, "expected five unblock plan no-dark blockers")
    require(all(row["unblock_target_artifact"] for row in rows), "each row needs an unblock target artifact")
    require(all(row["unblock_action"] for row in rows), "each row needs an unblock action")
    require(all(row["completion_criterion"] for row in rows), "each row needs a completion criterion")
    require(all(row["stop_rule"] for row in rows), "each row needs a stop rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "unblock plan cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "unblock plan cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau parent-input scoring acceptance unblock plan summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_UNBLOCK_PLAN_V01", "unblock plan summary id mismatch")
    require(row["plan_rows_declared"] == "5", "unblock plan row count mismatch")
    require(row["plan_declared_rows"] == "5", "unblock plan declared row count mismatch")
    require(row["unblock_completed_rows"] == "0", "unblock completed rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["phi_tau_eff_derivable_rows"] == "0", "Phi_tau_eff derivable rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["scores_computed"] == "false", "unblock plan cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["scoring_acceptance_unblock_plan_satisfied"] == "false", "scoring acceptance unblock plan must be unsatisfied")
    require(row["no_dark_blockers"] == "5", "unblock plan no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_OPEN",
        "unblock plan status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01",
        "unblock plan next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau populated evidence package candidate must have seven rows")
    require(
        {row["populated_candidate_status"] for row in rows} == {"POPULATED_EVIDENCE_PACKAGE_CANDIDATE_DECLARED_NOT_SUPPLIED"},
        "populated evidence package candidate must remain not supplied",
    )
    require({row["populated_candidate_declared"] for row in rows} == {"true"}, "populated candidates must be declared")
    require({row["payload_record_declared"] for row in rows} == {"true"}, "payload records must be declared")
    require({row["evidence_payload_supplied"] for row in rows} == {"false"}, "evidence payloads must remain absent")
    require({row["dimension_payload_supplied"] for row in rows} == {"false"}, "dimension payloads must remain absent")
    require({row["replay_payload_supplied"] for row in rows} == {"false"}, "replay payloads must remain absent")
    require({row["firewall_payload_supplied"] for row in rows} == {"false"}, "firewall payloads must remain absent")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring inputs cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "populated candidate cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven populated candidate no-dark blockers")
    require(all(row["required_payload_record"] for row in rows), "each row needs a required payload record")
    require(all(row["payload_population_rule"] for row in rows), "each row needs a payload population rule")
    require(all(row["endpoint_blindness_rule"] for row in rows), "each row needs an endpoint-blindness rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "populated candidate cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "populated candidate cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau populated evidence package candidate summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_CANDIDATE_V01",
        "populated candidate summary id mismatch",
    )
    require(row["candidate_rows_declared"] == "7", "populated candidate row count mismatch")
    require(row["populated_candidate_declared_rows"] == "7", "populated candidate declared row count mismatch")
    require(row["payload_record_declared_rows"] == "7", "payload record declared count mismatch")
    require(row["evidence_payload_supplied_rows"] == "0", "evidence payload supplied rows must be zero")
    require(row["dimension_payload_supplied_rows"] == "0", "dimension payload supplied rows must be zero")
    require(row["replay_payload_supplied_rows"] == "0", "replay payload supplied rows must be zero")
    require(row["firewall_payload_supplied_rows"] == "0", "firewall payload supplied rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["populated_evidence_package_candidate_satisfied"] == "false", "populated candidate must be unsatisfied")
    require(row["scores_computed"] == "false", "populated candidate cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "populated candidate no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_CANDIDATE_DECLARED_NOT_SUPPLIED",
        "populated candidate status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01",
        "populated candidate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau populated evidence package audit must have seven rows")
    require(
        {row["populated_audit_status"] for row in rows} == {"POPULATED_EVIDENCE_PACKAGE_AUDIT_FAIL_PAYLOAD_NOT_SUPPLIED"},
        "populated evidence package audit must fail without payloads",
    )
    require({row["populated_candidate_audited"] for row in rows} == {"true"}, "populated candidates must be audited")
    require({row["payload_record_declared"] for row in rows} == {"true"}, "payload records must be declared")
    require({row["evidence_payload_supplied"] for row in rows} == {"false"}, "evidence payloads must remain absent")
    require({row["dimension_payload_supplied"] for row in rows} == {"false"}, "dimension payloads must remain absent")
    require({row["replay_payload_supplied"] for row in rows} == {"false"}, "replay payloads must remain absent")
    require({row["firewall_payload_supplied"] for row in rows} == {"false"}, "firewall payloads must remain absent")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring inputs cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "populated audit cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven populated audit no-dark blockers")
    require(all(row["audit_finding"] for row in rows), "each row needs an audit finding")
    require(all(row["missing_payload_record"] for row in rows), "each row needs a missing payload record")
    require(all(row["payload_population_audit_result"] == "fail_payload_not_supplied" for row in rows), "payload audit must fail")
    require(
        all(row["package_acceptance_decision"] == "reject_populated_package_for_scoring_input_acceptance" for row in rows),
        "each row must reject populated package scoring acceptance",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "populated audit cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "populated audit cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau populated evidence package audit summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_AUDIT_V01", "populated audit summary id mismatch")
    require(row["audit_rows_declared"] == "7", "populated audit row count mismatch")
    require(row["populated_candidate_audited_rows"] == "7", "populated audited row count mismatch")
    require(row["payload_record_declared_rows"] == "7", "payload record declared count mismatch")
    require(row["populated_audit_passed_rows"] == "0", "populated audit passed rows must be zero")
    require(row["populated_audit_failed_rows"] == "7", "populated audit failed rows must be seven")
    require(row["evidence_payload_supplied_rows"] == "0", "evidence payload supplied rows must be zero")
    require(row["dimension_payload_supplied_rows"] == "0", "dimension payload supplied rows must be zero")
    require(row["replay_payload_supplied_rows"] == "0", "replay payload supplied rows must be zero")
    require(row["firewall_payload_supplied_rows"] == "0", "firewall payload supplied rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["populated_evidence_package_audit_satisfied"] == "false", "populated audit must be unsatisfied")
    require(row["scores_computed"] == "false", "populated audit cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "populated audit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_AUDIT_FAILED_PAYLOAD_NOT_SUPPLIED",
        "populated audit status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01",
        "populated audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_evidence_payload_acquisition_v01() -> None:
    candidate_rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01.csv")
    candidate_summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_summary_v01.csv")
    audit_rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01.csv")
    audit_summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_summary_v01.csv")
    require(len(candidate_rows) == 7, "Phi Tau evidence payload acquisition candidate must have seven rows")
    require(len(audit_rows) == 7, "Phi Tau evidence payload acquisition audit must have seven rows")
    require({row["source_artifact_present"] for row in candidate_rows} == {"true"}, "all candidate source artifacts must be present")
    require({row["hash_bound"] for row in candidate_rows} == {"true"}, "all candidate sources must be hash-bound")
    require({row["endpoint_blind_candidate"] for row in candidate_rows} == {"true"}, "all candidates must be endpoint-blind")
    require({row["semantic_replay_candidate"] for row in candidate_rows} == {"true"}, "all candidates must be semantic replays")
    require({row["candidate_payload_supplied"] for row in candidate_rows} == {"true"}, "all candidate payload rows must be supplied")
    require({row["certificate_passed"] for row in candidate_rows} == {"false"}, "candidate acquisition cannot pass certificates")
    require({row["parent_payload_accepted"] for row in candidate_rows} == {"false"}, "candidate acquisition cannot accept parent payloads")
    require({row["score_entry_allowed"] for row in candidate_rows} == {"false"}, "candidate acquisition cannot allow score entry")
    require({row["candidate_payload_audit_passed"] for row in audit_rows} == {"true"}, "candidate payload audit must pass for candidates")
    require(
        {row["parent_acceptance_decision"] for row in audit_rows} == {"reject_for_parent_acceptance_until_certificate_pass"},
        "audit must reject parent acceptance until certificate pass",
    )
    require({row["certificate_passed"] for row in audit_rows} == {"false"}, "audit cannot pass certificates")
    require({row["parent_payload_accepted"] for row in audit_rows} == {"false"}, "audit cannot accept parent payloads")
    require({row["score_entry_allowed"] for row in audit_rows} == {"false"}, "audit cannot allow score entry")
    require(len(candidate_summary) == 1, "Phi Tau evidence payload acquisition candidate summary must have one row")
    row = candidate_summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PAYLOAD_ACQUISITION_CANDIDATE_V01", "candidate summary id mismatch")
    require(row["payload_candidate_rows_declared"] == "7", "candidate row count mismatch")
    require(row["source_artifact_present_rows"] == "7", "candidate source artifact count mismatch")
    require(row["hash_bound_rows"] == "7", "candidate hash-bound count mismatch")
    require(row["endpoint_blind_candidate_rows"] == "7", "candidate endpoint-blind count mismatch")
    require(row["semantic_replay_candidate_rows"] == "7", "candidate semantic replay count mismatch")
    require(row["candidate_payload_supplied_rows"] == "7", "candidate payload supplied count mismatch")
    require(row["dimension_payload_supplied_rows"] == "4", "candidate dimension payload count mismatch")
    require(row["replay_payload_supplied_rows"] == "6", "candidate replay payload count mismatch")
    require(row["firewall_payload_supplied_rows"] == "3", "candidate firewall payload count mismatch")
    require(row["certificate_pass_candidate_rows"] == "7", "certificate pass candidate count mismatch")
    require(row["certificate_passed_rows"] == "0", "candidate cannot pass certificates")
    require(row["parent_payload_accepted_rows"] == "0", "candidate cannot accept parent payloads")
    require(row["score_ready_rows"] == "0", "candidate cannot be score-ready")
    require(row["scores_computed"] == "false", "candidate cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "candidate cannot provide CMB likelihood")
    require(row["tau_response_claim_allowed"] == "false", "candidate cannot allow Tau response claim")
    require(row["dark_sector_verdict_allowed"] == "false", "candidate cannot allow dark-sector verdict")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_EVIDENCE_PAYLOAD_CANDIDATES_ACQUIRED_NOT_ACCEPTED",
        "candidate overall status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01",
        "candidate next artifact mismatch",
    )
    require(len(audit_summary) == 1, "Phi Tau evidence payload acquisition audit summary must have one row")
    row = audit_summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PAYLOAD_ACQUISITION_AUDIT_V01", "audit summary id mismatch")
    require(row["audit_rows_declared"] == "7", "audit row count mismatch")
    require(row["source_artifact_present_rows"] == "7", "audit source artifact count mismatch")
    require(row["hash_bound_rows"] == "7", "audit hash-bound count mismatch")
    require(row["endpoint_blind_candidate_rows"] == "7", "audit endpoint-blind count mismatch")
    require(row["semantic_replay_candidate_rows"] == "7", "audit semantic replay count mismatch")
    require(row["candidate_payload_supplied_rows"] == "7", "audit candidate payload count mismatch")
    require(row["candidate_payload_audit_passed_rows"] == "7", "audit pass count mismatch")
    require(row["certificate_passed_rows"] == "0", "audit cannot pass certificates")
    require(row["parent_payload_accepted_rows"] == "0", "audit cannot accept parent payloads")
    require(row["score_ready_rows"] == "0", "audit cannot be score-ready")
    require(row["scores_computed"] == "false", "audit cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "audit cannot provide CMB likelihood")
    require(row["tau_response_claim_allowed"] == "false", "audit cannot allow Tau response claim")
    require(row["dark_sector_verdict_allowed"] == "false", "audit cannot allow dark-sector verdict")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_EVIDENCE_PAYLOAD_CANDIDATES_AUDITED_PRESENT_BUT_NOT_ACCEPTED",
        "audit overall status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01",
        "audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau evidence payload intake bridge decision must have seven rows")
    require(
        {row["bridge_status"] for row in rows} == {"CANDIDATE_PAYLOAD_ACQUIRED_REPACKAGING_REQUIRED"},
        "bridge must require canonical repackaging",
    )
    require({row["candidate_payload_audit_passed"] for row in rows} == {"true"}, "candidate payload audit must pass")
    require({row["canonical_submission_packet_present"] for row in rows} == {"false"}, "canonical submission packets must be absent")
    require({row["receipt_binding_present"] for row in rows} == {"false"}, "receipt bindings must be absent")
    require({row["dimension_receipt_ready"] for row in rows} == {"false"}, "dimension receipts must be absent")
    require({row["replay_receipt_ready"] for row in rows} == {"false"}, "replay receipts must be absent")
    require({row["firewall_receipt_ready"] for row in rows} == {"false"}, "firewall receipts must be absent")
    require({row["canonical_repackaging_required"] for row in rows} == {"true"}, "canonical repackaging must be required")
    require({row["intake_bridge_passed"] for row in rows} == {"false"}, "intake bridge cannot pass yet")
    require({row["parent_payload_accepted"] for row in rows} == {"false"}, "bridge cannot accept parent payloads")
    require({row["certificate_passed"] for row in rows} == {"false"}, "bridge cannot pass certificates")
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "bridge cannot allow score entry")
    require(
        {row["bridge_decision"] for row in rows} == {"ROUTE_TO_CANONICAL_PAYLOAD_PACKET_AND_RECEIPT_BINDING"},
        "bridge decision mismatch",
    )
    require(len(summary) == 1, "Phi Tau evidence payload intake bridge decision summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PAYLOAD_INTAKE_BRIDGE_DECISION_V01",
        "bridge summary id mismatch",
    )
    require(row["bridge_rows_declared"] == "7", "bridge row count mismatch")
    require(row["candidate_payload_audit_passed_rows"] == "7", "bridge candidate pass count mismatch")
    require(row["canonical_submission_packet_present_rows"] == "0", "canonical packet count must be zero")
    require(row["receipt_binding_present_rows"] == "0", "receipt binding count must be zero")
    require(row["dimension_receipt_ready_rows"] == "0", "dimension receipt count must be zero")
    require(row["replay_receipt_ready_rows"] == "0", "replay receipt count must be zero")
    require(row["firewall_receipt_ready_rows"] == "0", "firewall receipt count must be zero")
    require(row["canonical_repackaging_required_rows"] == "7", "canonical repackaging required count mismatch")
    require(row["intake_bridge_passed_rows"] == "0", "intake bridge passed rows must be zero")
    require(row["parent_payload_accepted_rows"] == "0", "parent payload accepted rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "bridge cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "bridge cannot provide CMB likelihood")
    require(row["tau_response_claim_allowed"] == "false", "bridge cannot allow Tau response claim")
    require(row["dark_sector_verdict_allowed"] == "false", "bridge cannot allow dark-sector verdict")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_EVIDENCE_PAYLOAD_CANDIDATE_ACQUIRED_CANONICAL_REPACKAGING_REQUIRED",
        "bridge overall status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_canonical_payload_packet_v01",
        "bridge next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_canonical_payload_packet_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_canonical_payload_packet_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_canonical_payload_packet_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau parent canonical payload packet must have seven rows")
    require({row["canonical_packet_present"] for row in rows} == {"true"}, "canonical packet rows must be present")
    require({row["receipt_binding_present"] for row in rows} == {"true"}, "receipt bindings must be present")
    require(sum(row["dimension_binding_present"] == "true" for row in rows) == 4, "dimension binding count mismatch")
    require(sum(row["replay_binding_present"] == "true" for row in rows) == 6, "replay binding count mismatch")
    require(sum(row["firewall_binding_present"] == "true" for row in rows) == 3, "firewall binding count mismatch")
    require({row["canonical_repackaging_completed"] for row in rows} == {"true"}, "canonical repackaging must be completed")
    require({row["binding_triads_complete"] for row in rows} == {"false"}, "binding triads must remain incomplete")
    require({row["parent_acceptance_ready"] for row in rows} == {"false"}, "packet cannot be parent-acceptance ready")
    require({row["parent_payload_accepted"] for row in rows} == {"false"}, "packet cannot accept parent payloads")
    require({row["certificate_passed"] for row in rows} == {"false"}, "packet cannot pass certificates")
    require({row["score_entry_allowed"] for row in rows} == {"false"}, "packet cannot allow score entry")
    require(len(summary) == 1, "Phi Tau parent canonical payload packet summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_CANONICAL_PAYLOAD_PACKET_V01", "canonical packet summary id mismatch")
    require(row["packet_rows_declared"] == "7", "canonical packet row count mismatch")
    require(row["canonical_packet_present_rows"] == "7", "canonical packet present count mismatch")
    require(row["receipt_binding_present_rows"] == "7", "receipt binding count mismatch")
    require(row["dimension_binding_present_rows"] == "4", "dimension binding summary mismatch")
    require(row["replay_binding_present_rows"] == "6", "replay binding summary mismatch")
    require(row["firewall_binding_present_rows"] == "3", "firewall binding summary mismatch")
    require(row["canonical_repackaging_completed_rows"] == "7", "canonical repackaging count mismatch")
    require(row["binding_triads_complete_rows"] == "0", "binding triads complete rows must be zero")
    require(row["parent_acceptance_ready_rows"] == "0", "parent acceptance ready rows must be zero")
    require(row["parent_payload_accepted_rows"] == "0", "parent payload accepted rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["score_ready_rows"] == "0", "score-ready rows must be zero")
    require(row["scores_computed"] == "false", "canonical packet cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "canonical packet cannot provide CMB likelihood")
    require(row["tau_response_claim_allowed"] == "false", "canonical packet cannot allow Tau response claim")
    require(row["dark_sector_verdict_allowed"] == "false", "canonical packet cannot allow dark-sector verdict")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_CANONICAL_PAYLOAD_PACKETS_MATERIALIZED_NOT_ACCEPTED",
        "canonical packet overall status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_v01",
        "canonical packet next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau evidence payload submission gate must have seven rows")
    require(
        {row["submission_gate_status"] for row in rows} == {"SUBMISSION_GATE_DECLARED_NO_PAYLOAD_RECEIVED"},
        "submission gate must have no received payload",
    )
    require({row["submission_gate_declared"] for row in rows} == {"true"}, "submission gates must be declared")
    require({row["submission_payload_received"] for row in rows} == {"false"}, "submission payloads must remain absent")
    require({row["dimension_payload_received"] for row in rows} == {"false"}, "dimension payloads must remain absent")
    require({row["replay_payload_received"] for row in rows} == {"false"}, "replay payloads must remain absent")
    require({row["firewall_payload_received"] for row in rows} == {"false"}, "firewall payloads must remain absent")
    require({row["submission_accepted"] for row in rows} == {"false"}, "submissions cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring inputs cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "submission gate cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven submission gate no-dark blockers")
    require(all(row["required_submission_object"] for row in rows), "each row needs required submission object")
    require(all(row["submission_validation_rule"] for row in rows), "each row needs submission validation rule")
    require(all(row["endpoint_firewall_requirement"] for row in rows), "each row needs endpoint firewall requirement")
    require(all(row["gate_decision"] == "closed_until_payload_received" for row in rows), "gate must remain closed")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "submission gate cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "submission gate cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload submission gate summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SUBMISSION_GATE_V01", "submission gate summary id mismatch")
    require(row["gate_rows_declared"] == "7", "submission gate row count mismatch")
    require(row["submission_gate_declared_rows"] == "7", "submission gate declared row count mismatch")
    require(row["submission_payload_received_rows"] == "0", "submission payload received rows must be zero")
    require(row["dimension_payload_received_rows"] == "0", "dimension payload received rows must be zero")
    require(row["replay_payload_received_rows"] == "0", "replay payload received rows must be zero")
    require(row["firewall_payload_received_rows"] == "0", "firewall payload received rows must be zero")
    require(row["submission_accepted_rows"] == "0", "submission accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["evidence_payload_submission_gate_satisfied"] == "false", "submission gate must be unsatisfied")
    require(row["scores_computed"] == "false", "submission gate cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "submission gate no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SUBMISSION_GATE_DECLARED_NO_PAYLOAD_RECEIVED",
        "submission gate status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_v01",
        "submission gate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau evidence payload receipt candidate must have seven rows")
    require(
        {row["receipt_candidate_status"] for row in rows} == {"RECEIPT_CANDIDATE_DECLARED_NO_PAYLOAD_RECEIVED"},
        "receipt candidate must have no received payload",
    )
    require({row["receipt_candidate_declared"] for row in rows} == {"true"}, "receipt candidates must be declared")
    require({row["payload_received"] for row in rows} == {"false"}, "payloads must remain absent")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipts cannot be accepted")
    require({row["dimension_payload_received"] for row in rows} == {"false"}, "dimension payloads must remain absent")
    require({row["replay_payload_received"] for row in rows} == {"false"}, "replay payloads must remain absent")
    require({row["firewall_payload_received"] for row in rows} == {"false"}, "firewall payloads must remain absent")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring inputs cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "receipt candidate cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven receipt candidate no-dark blockers")
    require(all(row["expected_receipt_object"] for row in rows), "each row needs an expected receipt object")
    require(all(row["receipt_validation_rule"] for row in rows), "each row needs a receipt validation rule")
    require(all(row["provenance_hash_requirement"] for row in rows), "each row needs a provenance hash requirement")
    require(
        all(row["receipt_acceptance_gate"] == "receipt remains closed until payload is received" for row in rows),
        "receipt gate must remain closed",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "receipt candidate cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "receipt candidate cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload receipt candidate summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_CANDIDATE_V01",
        "receipt candidate summary id mismatch",
    )
    require(row["receipt_rows_declared"] == "7", "receipt candidate row count mismatch")
    require(row["receipt_candidate_declared_rows"] == "7", "receipt candidate declared row count mismatch")
    require(row["payload_received_rows"] == "0", "payload received rows must be zero")
    require(row["receipt_accepted_rows"] == "0", "receipt accepted rows must be zero")
    require(row["dimension_payload_received_rows"] == "0", "dimension payload received rows must be zero")
    require(row["replay_payload_received_rows"] == "0", "replay payload received rows must be zero")
    require(row["firewall_payload_received_rows"] == "0", "firewall payload received rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["evidence_payload_receipt_candidate_satisfied"] == "false", "receipt candidate must be unsatisfied")
    require(row["scores_computed"] == "false", "receipt candidate cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "receipt candidate no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_CANDIDATE_DECLARED_NO_PAYLOAD_RECEIVED",
        "receipt candidate status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01",
        "receipt candidate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_summary_v01.csv")
    require(len(rows) == 7, "Phi Tau evidence payload receipt audit must have seven rows")
    require(
        {row["receipt_audit_status"] for row in rows} == {"RECEIPT_AUDIT_FAILED_NO_PAYLOAD_RECEIVED"},
        "receipt audit must fail without payload",
    )
    require({row["payload_received"] for row in rows} == {"false"}, "payloads must remain absent")
    require({row["receipt_candidate_declared"] for row in rows} == {"true"}, "receipt candidates must be declared")
    require({row["receipt_validated"] for row in rows} == {"false"}, "receipts cannot be validated")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipts cannot be accepted")
    require({row["dimension_payload_received"] for row in rows} == {"false"}, "dimension payloads must remain absent")
    require({row["replay_payload_received"] for row in rows} == {"false"}, "replay payloads must remain absent")
    require({row["firewall_payload_received"] for row in rows} == {"false"}, "firewall payloads must remain absent")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring inputs cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "receipt audit cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven receipt audit no-dark blockers")
    require(all(row["required_receipt_object"] for row in rows), "each row needs a required receipt object")
    require(all(row["audit_validation_rule"] for row in rows), "each row needs an audit validation rule")
    require(all(row["payload_binding_requirement"] for row in rows), "each row needs a payload binding requirement")
    require(all(row["provenance_replay_requirement"] for row in rows), "each row needs a provenance replay requirement")
    require(
        all(row["audit_failure_reason"] == "no payload record is available for receipt validation" for row in rows),
        "receipt audit failure reason mismatch",
    )
    require(
        all(row["audit_decision"] == "failed_until_payload_and_receipt_are_supplied" for row in rows),
        "receipt audit decision mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "receipt audit cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "receipt audit cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload receipt audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_AUDIT_V01",
        "receipt audit summary id mismatch",
    )
    require(row["audit_rows_declared"] == "7", "receipt audit row count mismatch")
    require(row["receipt_candidate_declared_rows"] == "7", "receipt audit declared row count mismatch")
    require(row["payload_received_rows"] == "0", "payload received rows must be zero")
    require(row["receipt_validated_rows"] == "0", "receipt validated rows must be zero")
    require(row["receipt_accepted_rows"] == "0", "receipt accepted rows must be zero")
    require(row["dimension_payload_received_rows"] == "0", "dimension payload received rows must be zero")
    require(row["replay_payload_received_rows"] == "0", "replay payload received rows must be zero")
    require(row["firewall_payload_received_rows"] == "0", "firewall payload received rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["evidence_payload_receipt_audit_satisfied"] == "false", "receipt audit must be unsatisfied")
    require(row["scores_computed"] == "false", "receipt audit cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "receipt audit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_AUDIT_FAILED_NO_PAYLOAD_RECEIVED",
        "receipt audit status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01",
        "receipt audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload receipt remediation plan must have seven rows")
    require(
        {row["remediation_status"] for row in rows} == {"REMEDIATION_DECLARED_NOT_COMPLETED"},
        "remediation plan must remain incomplete",
    )
    require({row["payload_received"] for row in rows} == {"false"}, "payloads must remain absent")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["receipt_validated"] for row in rows} == {"false"}, "receipts cannot be validated")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipts cannot be accepted")
    require({row["dimension_payload_received"] for row in rows} == {"false"}, "dimension payloads must remain absent")
    require({row["replay_payload_received"] for row in rows} == {"false"}, "replay payloads must remain absent")
    require({row["firewall_payload_received"] for row in rows} == {"false"}, "firewall payloads must remain absent")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring inputs cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "remediation plan cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven remediation no-dark blockers")
    require(all(row["missing_payload_object"] for row in rows), "each row needs a missing payload object")
    require(all(row["required_remediation_action"] for row in rows), "each row needs a required remediation action")
    require(all(row["required_receipt_binding"] for row in rows), "each row needs a required receipt binding")
    require(
        all(
            row["required_evidence_bundle"] == "payload object plus provenance hash plus replay command plus artifact path"
            for row in rows
        ),
        "remediation evidence bundle mismatch",
    )
    require(
        all(
            row["acceptance_exit_gate"] == "may exit only after matching payload and receipt are supplied and audit-passed"
            for row in rows
        ),
        "remediation exit gate mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "remediation cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "remediation cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload receipt remediation plan summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_REMEDIATION_PLAN_V01",
        "remediation summary id mismatch",
    )
    require(row["remediation_rows_declared"] == "7", "remediation row count mismatch")
    require(row["payload_received_rows"] == "0", "payload received rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["receipt_validated_rows"] == "0", "receipt validated rows must be zero")
    require(row["receipt_accepted_rows"] == "0", "receipt accepted rows must be zero")
    require(row["dimension_payload_received_rows"] == "0", "dimension payload received rows must be zero")
    require(row["replay_payload_received_rows"] == "0", "replay payload received rows must be zero")
    require(row["firewall_payload_received_rows"] == "0", "firewall payload received rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["evidence_payload_receipt_remediation_plan_satisfied"] == "false", "remediation plan must be unsatisfied")
    require(row["scores_computed"] == "false", "remediation plan cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "remediation no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_REMEDIATION_PLAN_DECLARED_NOT_COMPLETED",
        "remediation status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_v01",
        "remediation next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload materialization packet must have seven rows")
    require(
        {row["materialization_status"] for row in rows}
        == {"MATERIALIZATION_PACKET_DECLARED_NO_PAYLOAD_MATERIALIZED"},
        "materialization packet must remain schema-only",
    )
    require({row["payload_materialized"] for row in rows} == {"false"}, "payloads cannot be materialized")
    require({row["packet_accepted"] for row in rows} == {"false"}, "packets cannot be accepted")
    require({row["receipt_validated"] for row in rows} == {"false"}, "receipts cannot be validated")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipts cannot be accepted")
    require({row["dimension_payload_received"] for row in rows} == {"false"}, "dimension payloads must remain absent")
    require({row["replay_payload_received"] for row in rows} == {"false"}, "replay payloads must remain absent")
    require({row["firewall_payload_received"] for row in rows} == {"false"}, "firewall payloads must remain absent")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring inputs cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "materialization packet cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven materialization no-dark blockers")
    require(all(row["packet_slot_object"] for row in rows), "each row needs a packet slot object")
    require(all(row["materialization_requirement"] for row in rows), "each row needs a materialization requirement")
    require(all(row["dimension_requirement"] for row in rows), "each row needs a dimension requirement")
    require(all(row["replay_requirement"] for row in rows), "each row needs a replay requirement")
    require(all(row["firewall_requirement"] for row in rows), "each row needs a firewall requirement")
    require(all(row["receipt_binding_requirement"] for row in rows), "each row needs a receipt binding requirement")
    require(
        all(
            row["acceptance_exit_gate"] == "may exit only after packet is materialized, receipt-bound, and audit-passed"
            for row in rows
        ),
        "materialization exit gate mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "materialization cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "materialization cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload materialization packet summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_MATERIALIZATION_PACKET_V01",
        "materialization summary id mismatch",
    )
    require(row["packet_rows_declared"] == "7", "materialization row count mismatch")
    require(row["payload_materialized_rows"] == "0", "payload materialized rows must be zero")
    require(row["packet_accepted_rows"] == "0", "packet accepted rows must be zero")
    require(row["receipt_validated_rows"] == "0", "receipt validated rows must be zero")
    require(row["receipt_accepted_rows"] == "0", "receipt accepted rows must be zero")
    require(row["dimension_payload_received_rows"] == "0", "dimension payload received rows must be zero")
    require(row["replay_payload_received_rows"] == "0", "replay payload received rows must be zero")
    require(row["firewall_payload_received_rows"] == "0", "firewall payload received rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["evidence_payload_materialization_packet_satisfied"] == "false", "materialization packet must be unsatisfied")
    require(row["scores_computed"] == "false", "materialization packet cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "materialization no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_MATERIALIZATION_PACKET_DECLARED_NO_PAYLOAD_MATERIALIZED",
        "materialization status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01",
        "materialization next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload materialization audit must have seven rows")
    require(
        {row["materialization_audit_status"] for row in rows}
        == {"MATERIALIZATION_AUDIT_FAILED_NO_PAYLOAD_MATERIALIZED"},
        "materialization audit must fail without payload",
    )
    require({row["payload_materialized"] for row in rows} == {"false"}, "payloads cannot be materialized")
    require({row["packet_accepted"] for row in rows} == {"false"}, "packets cannot be accepted")
    require({row["receipt_validated"] for row in rows} == {"false"}, "receipts cannot be validated")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipts cannot be accepted")
    require({row["dimension_payload_received"] for row in rows} == {"false"}, "dimension payloads must remain absent")
    require({row["replay_payload_received"] for row in rows} == {"false"}, "replay payloads must remain absent")
    require({row["firewall_payload_received"] for row in rows} == {"false"}, "firewall payloads must remain absent")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring inputs cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "materialization audit cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven materialization audit no-dark blockers")
    require(all(row["packet_slot_object"] for row in rows), "each row needs a packet slot object")
    require(all(row["required_materialization_check"] for row in rows), "each row needs a materialization check")
    require(all(row["dimension_check"] for row in rows), "each row needs a dimension check")
    require(all(row["replay_check"] for row in rows), "each row needs a replay check")
    require(all(row["firewall_check"] for row in rows), "each row needs a firewall check")
    require(all(row["receipt_binding_check"] for row in rows), "each row needs a receipt binding check")
    require(
        all(row["audit_failure_reason"] == "no materialized payload packet is available for audit" for row in rows),
        "materialization audit failure reason mismatch",
    )
    require(
        all(row["audit_decision"] == "failed_until_packet_is_materialized_and_receipt_bound" for row in rows),
        "materialization audit decision mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "materialization audit cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "materialization audit cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload materialization audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_MATERIALIZATION_AUDIT_V01",
        "materialization audit summary id mismatch",
    )
    require(row["audit_rows_declared"] == "7", "materialization audit row count mismatch")
    require(row["payload_materialized_rows"] == "0", "payload materialized rows must be zero")
    require(row["packet_accepted_rows"] == "0", "packet accepted rows must be zero")
    require(row["receipt_validated_rows"] == "0", "receipt validated rows must be zero")
    require(row["receipt_accepted_rows"] == "0", "receipt accepted rows must be zero")
    require(row["dimension_payload_received_rows"] == "0", "dimension payload received rows must be zero")
    require(row["replay_payload_received_rows"] == "0", "replay payload received rows must be zero")
    require(row["firewall_payload_received_rows"] == "0", "firewall payload received rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["evidence_payload_materialization_audit_satisfied"] == "false", "materialization audit must be unsatisfied")
    require(row["scores_computed"] == "false", "materialization audit cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "materialization audit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_MATERIALIZATION_AUDIT_FAILED_NO_PAYLOAD_MATERIALIZED",
        "materialization audit status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01",
        "materialization audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload acceptance precheck must have seven rows")
    require(
        {row["acceptance_precheck_status"] for row in rows}
        == {"ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_SATISFIED"},
        "acceptance precheck must fail without materialization audit pass",
    )
    require({row["payload_materialized"] for row in rows} == {"false"}, "payloads cannot be materialized")
    require({row["packet_accepted"] for row in rows} == {"false"}, "packets cannot be accepted")
    require({row["receipt_validated"] for row in rows} == {"false"}, "receipts cannot be validated")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipts cannot be accepted")
    require({row["dimension_payload_received"] for row in rows} == {"false"}, "dimension payloads must remain absent")
    require({row["replay_payload_received"] for row in rows} == {"false"}, "replay payloads must remain absent")
    require({row["firewall_payload_received"] for row in rows} == {"false"}, "firewall payloads must remain absent")
    require({row["acceptance_precheck_passed"] for row in rows} == {"false"}, "acceptance precheck cannot pass")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring inputs cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "acceptance precheck cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven acceptance precheck no-dark blockers")
    require(all(row["required_input_object"] for row in rows), "each row needs a required input object")
    require(all(row["materialization_gate"] for row in rows), "each row needs a materialization gate")
    require(all(row["receipt_gate"] for row in rows), "each row needs a receipt gate")
    require(all(row["dimension_gate"] for row in rows), "each row needs a dimension gate")
    require(all(row["replay_gate"] for row in rows), "each row needs a replay gate")
    require(all(row["firewall_gate"] for row in rows), "each row needs a firewall gate")
    require(
        all(
            row["acceptance_blocker"] == "materialization audit failed because no payload packet is materialized"
            for row in rows
        ),
        "acceptance blocker mismatch",
    )
    require(
        all(
            row["precheck_decision"] == "blocked_until_materialization_receipt_dimension_replay_and_firewall_gates_pass"
            for row in rows
        ),
        "acceptance precheck decision mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "acceptance precheck cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "acceptance precheck cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload acceptance precheck summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_PRECHECK_V01",
        "acceptance precheck summary id mismatch",
    )
    require(row["precheck_rows_declared"] == "7", "acceptance precheck row count mismatch")
    require(row["payload_materialized_rows"] == "0", "payload materialized rows must be zero")
    require(row["packet_accepted_rows"] == "0", "packet accepted rows must be zero")
    require(row["receipt_validated_rows"] == "0", "receipt validated rows must be zero")
    require(row["receipt_accepted_rows"] == "0", "receipt accepted rows must be zero")
    require(row["dimension_payload_received_rows"] == "0", "dimension payload received rows must be zero")
    require(row["replay_payload_received_rows"] == "0", "replay payload received rows must be zero")
    require(row["firewall_payload_received_rows"] == "0", "firewall payload received rows must be zero")
    require(row["acceptance_precheck_passed_rows"] == "0", "acceptance precheck passed rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["evidence_payload_acceptance_precheck_satisfied"] == "false", "acceptance precheck must be unsatisfied")
    require(row["scores_computed"] == "false", "acceptance precheck cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "acceptance precheck no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_SATISFIED",
        "acceptance precheck status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01",
        "acceptance precheck next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload acceptance unblock plan must have seven rows")
    require({row["unblock_status"] for row in rows} == {"UNBLOCK_DECLARED_NOT_COMPLETED"}, "unblock plan must remain incomplete")
    require({row["unblock_completed"] for row in rows} == {"false"}, "unblock steps cannot be completed")
    require({row["payload_materialized"] for row in rows} == {"false"}, "payloads cannot be materialized")
    require({row["packet_accepted"] for row in rows} == {"false"}, "packets cannot be accepted")
    require({row["receipt_validated"] for row in rows} == {"false"}, "receipts cannot be validated")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipts cannot be accepted")
    require({row["dimension_payload_received"] for row in rows} == {"false"}, "dimension payloads must remain absent")
    require({row["replay_payload_received"] for row in rows} == {"false"}, "replay payloads must remain absent")
    require({row["firewall_payload_received"] for row in rows} == {"false"}, "firewall payloads must remain absent")
    require({row["acceptance_precheck_passed"] for row in rows} == {"false"}, "acceptance precheck cannot pass")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring inputs cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "unblock plan cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven unblock no-dark blockers")
    require(all(row["blocked_gate"] for row in rows), "each row needs a blocked gate")
    require(all(row["required_unblock_action"] for row in rows), "each row needs a required unblock action")
    require(all(row["required_evidence_object"] for row in rows), "each row needs a required evidence object")
    require(
        all(
            row["required_exit_condition"] == "gate may exit only after evidence object is supplied and audit-passed"
            for row in rows
        ),
        "unblock exit condition mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "unblock plan cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "unblock plan cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload acceptance unblock plan summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_UNBLOCK_PLAN_V01",
        "unblock summary id mismatch",
    )
    require(row["unblock_rows_declared"] == "7", "unblock row count mismatch")
    require(row["unblock_completed_rows"] == "0", "unblock completed rows must be zero")
    require(row["payload_materialized_rows"] == "0", "payload materialized rows must be zero")
    require(row["packet_accepted_rows"] == "0", "packet accepted rows must be zero")
    require(row["receipt_validated_rows"] == "0", "receipt validated rows must be zero")
    require(row["receipt_accepted_rows"] == "0", "receipt accepted rows must be zero")
    require(row["dimension_payload_received_rows"] == "0", "dimension payload received rows must be zero")
    require(row["replay_payload_received_rows"] == "0", "replay payload received rows must be zero")
    require(row["firewall_payload_received_rows"] == "0", "firewall payload received rows must be zero")
    require(row["acceptance_precheck_passed_rows"] == "0", "acceptance precheck passed rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["evidence_payload_acceptance_unblock_plan_satisfied"] == "false", "unblock plan must be unsatisfied")
    require(row["scores_computed"] == "false", "unblock plan cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "unblock no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED",
        "unblock status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01",
        "unblock next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload acceptance decision gate must have seven rows")
    require(
        {row["decision_gate_status"] for row in rows} == {"ACCEPTANCE_DECISION_CLOSED_UNBLOCK_NOT_COMPLETED"},
        "acceptance decision gate must remain closed",
    )
    require({row["decision_output"] for row in rows} == {"acceptance_closed"}, "decision output must close acceptance")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["unblock_completed"] for row in rows} == {"false"}, "unblock steps cannot be completed")
    require({row["payload_materialized"] for row in rows} == {"false"}, "payloads cannot be materialized")
    require({row["packet_accepted"] for row in rows} == {"false"}, "packets cannot be accepted")
    require({row["receipt_validated"] for row in rows} == {"false"}, "receipts cannot be validated")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipts cannot be accepted")
    require({row["dimension_payload_received"] for row in rows} == {"false"}, "dimension payloads must remain absent")
    require({row["replay_payload_received"] for row in rows} == {"false"}, "replay payloads must remain absent")
    require({row["firewall_payload_received"] for row in rows} == {"false"}, "firewall payloads must remain absent")
    require({row["acceptance_precheck_passed"] for row in rows} == {"false"}, "acceptance precheck cannot pass")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificates cannot pass")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring inputs cannot be accepted")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "decision gate cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven decision no-dark blockers")
    require(all(row["target_gate"] for row in rows), "each row needs a target gate")
    require(all(row["required_prior_pass"] for row in rows), "each row needs a required prior pass")
    require(
        all(
            row["decision_rule"] == "acceptance may open only if all upstream evidence gates are completed and audit-passed"
            for row in rows
        ),
        "acceptance decision rule mismatch",
    )
    require(
        all(row["decision_reason"] == "acceptance unblock plan is not satisfied" for row in rows),
        "acceptance decision reason mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "decision gate cannot allow Tau response claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "decision gate cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload acceptance decision gate summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_DECISION_GATE_V01",
        "decision summary id mismatch",
    )
    require(row["decision_rows_declared"] == "7", "decision row count mismatch")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["unblock_completed_rows"] == "0", "unblock completed rows must be zero")
    require(row["payload_materialized_rows"] == "0", "payload materialized rows must be zero")
    require(row["packet_accepted_rows"] == "0", "packet accepted rows must be zero")
    require(row["receipt_validated_rows"] == "0", "receipt validated rows must be zero")
    require(row["receipt_accepted_rows"] == "0", "receipt accepted rows must be zero")
    require(row["dimension_payload_received_rows"] == "0", "dimension payload received rows must be zero")
    require(row["replay_payload_received_rows"] == "0", "replay payload received rows must be zero")
    require(row["firewall_payload_received_rows"] == "0", "firewall payload received rows must be zero")
    require(row["acceptance_precheck_passed_rows"] == "0", "acceptance precheck passed rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["accepted_rows"] == "0", "accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(row["evidence_payload_acceptance_decision_gate_satisfied"] == "false", "decision gate must be unsatisfied")
    require(row["scores_computed"] == "false", "decision gate cannot compute scores")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood must remain unavailable")
    require(row["no_dark_blockers"] == "7", "decision no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_DECISION_GATE_CLOSED_UNBLOCK_NOT_COMPLETED",
        "decision status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01",
        "decision next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input candidate must have seven rows")
    require(
        {row["scoring_input_candidate_status"] for row in rows}
        == {"SCORING_INPUT_CANDIDATE_DECLARED_ACCEPTANCE_DECISION_CLOSED"},
        "scoring input candidates must remain acceptance-closed",
    )
    require({row["scoring_input_candidate_declared"] for row in rows} == {"true"}, "candidates must be declared")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "candidate cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_accepted_payload"] for row in rows), "each candidate needs a required accepted payload")
    require(all(row["candidate_construction_rule"] for row in rows), "each candidate needs a construction rule")
    require(all(row["required_acceptance_decision"] for row in rows), "each candidate needs an acceptance decision")
    require(all(row["required_scoring_contract"] for row in rows), "each candidate needs a scoring contract")
    require(
        all(row["candidate_blocker"] == "acceptance decision gate is closed" for row in rows),
        "candidate blocker mismatch",
    )
    require(
        all(row["candidate_decision"] == "candidate_declared_but_not_accepted" for row in rows),
        "candidate decision mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "candidate cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "candidate cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload scoring input candidate summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_CANDIDATE_V01",
        "candidate summary id mismatch",
    )
    require(row["candidate_rows_declared"] == "7", "candidate row count mismatch")
    require(row["scoring_input_candidate_declared_rows"] == "7", "declared candidate row count mismatch")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_candidate_satisfied"] == "false",
        "scoring input candidate must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "candidate no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_CANDIDATE_DECLARED_NOT_ACCEPTED",
        "candidate status mismatch",
    )
    require(
        row["next_required_artifact"] == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01",
        "candidate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input audit must have seven rows")
    require(
        {row["audit_status"] for row in rows} == {"SCORING_INPUT_AUDITED_REJECTED_ACCEPTANCE_DECISION_CLOSED"},
        "scoring input audit must reject candidates",
    )
    require({row["scoring_input_candidate_declared"] for row in rows} == {"true"}, "candidates must be declared")
    require({row["scoring_input_audited"] for row in rows} == {"true"}, "candidates must be audited")
    require({row["scoring_input_audit_passed"] for row in rows} == {"false"}, "audit cannot pass")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "audit cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven audit no-dark blockers")
    require(all(row["required_accepted_payload"] for row in rows), "each audit row needs a required accepted payload")
    require(all(row["required_acceptance_decision"] for row in rows), "each audit row needs an acceptance decision")
    require(all(row["required_scoring_contract"] for row in rows), "each audit row needs a scoring contract")
    require(
        all(
            row["audit_finding"] == "required accepted payload is absent because acceptance decision gate is closed"
            for row in rows
        ),
        "audit finding mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "audit cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload scoring input audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_AUDIT_V01",
        "audit summary id mismatch",
    )
    require(row["audit_rows_declared"] == "7", "audit row count mismatch")
    require(row["scoring_input_audited_rows"] == "7", "audited row count mismatch")
    require(row["scoring_input_audit_passed_rows"] == "0", "audit passed rows must be zero")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_audit_satisfied"] == "false",
        "scoring input audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "audit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_AUDIT_REJECTED_ACCEPTANCE_DECISION_CLOSED",
        "audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01",
        "audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01() -> None:
    rows = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01.csv"
    )
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input remediation plan must have seven rows")
    require(
        {row["remediation_status"] for row in rows} == {"REMEDIATION_REQUIRED_NOT_COMPLETED"},
        "remediation status mismatch",
    )
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_audit_passed"] for row in rows} == {"false"}, "scoring audit cannot pass")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "plan cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_remediation_action"] for row in rows), "each row needs a remediation action")
    require(all(row["minimal_acceptance_evidence"] for row in rows), "each row needs minimal acceptance evidence")
    require(all(row["acceptance_exit_condition"] for row in rows), "each row needs an acceptance exit condition")
    require(all(row["scoring_contract_exit_condition"] for row in rows), "each row needs a scoring exit condition")
    require(
        all(
            row["blocking_finding"] == "required accepted payload is absent because acceptance decision gate is closed"
            for row in rows
        ),
        "remediation blocking finding mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "plan cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "plan cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload scoring input remediation plan summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PLAN_V01",
        "remediation summary id mismatch",
    )
    require(row["remediation_rows_declared"] == "7", "remediation row count mismatch")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_audit_passed_rows"] == "0", "audit passed rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_remediation_plan_satisfied"] == "false",
        "remediation plan must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "remediation no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PLAN_DECLARED_NOT_COMPLETED",
        "remediation status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_v01",
        "remediation next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_v01() -> None:
    rows = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_v01.csv"
    )
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input remediation packet must have seven rows")
    require(
        {row["packet_status"] for row in rows} == {"REMEDIATION_PACKET_SCHEMA_DECLARED_NOT_MATERIALIZED"},
        "packet status mismatch",
    )
    require({row["packet_materialized"] for row in rows} == {"false"}, "packet cannot be materialized")
    require({row["packet_submitted"] for row in rows} == {"false"}, "packet cannot be submitted")
    require({row["packet_audit_passed"] for row in rows} == {"false"}, "packet audit cannot pass")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_audit_passed"] for row in rows} == {"false"}, "scoring input audit cannot pass")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "packet cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["packet_slot"] for row in rows), "each row needs a packet slot")
    require(all(row["required_payload_evidence"] for row in rows), "each row needs payload evidence")
    require(all(row["required_packet_schema"] for row in rows), "each row needs a packet schema")
    require(all(row["required_hash_evidence"] for row in rows), "each row needs hash evidence")
    require(all(row["required_firewall_evidence"] for row in rows), "each row needs firewall evidence")
    require(all(row["packet_exit_condition"] for row in rows), "each row needs a packet exit condition")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "packet cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "packet cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload scoring input remediation packet summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PACKET_V01",
        "packet summary id mismatch",
    )
    require(row["packet_rows_declared"] == "7", "packet row count mismatch")
    require(row["packet_materialized_rows"] == "0", "packet materialized rows must be zero")
    require(row["packet_submitted_rows"] == "0", "packet submitted rows must be zero")
    require(row["packet_audit_passed_rows"] == "0", "packet audit passed rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_audit_passed_rows"] == "0", "scoring input audit passed rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_remediation_packet_satisfied"] == "false",
        "remediation packet must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "packet no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PACKET_DECLARED_NOT_MATERIALIZED",
        "packet status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_v01",
        "packet next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input remediation packet audit must have seven rows")
    require(
        {row["packet_audit_status"] for row in rows}
        == {"REMEDIATION_PACKET_AUDIT_REJECTED_NOT_MATERIALIZED"},
        "packet audit status mismatch",
    )
    require({row["packet_materialized"] for row in rows} == {"false"}, "packet cannot be materialized")
    require({row["packet_submitted"] for row in rows} == {"false"}, "packet cannot be submitted")
    require({row["packet_audit_passed"] for row in rows} == {"false"}, "packet audit cannot pass")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_audit_passed"] for row in rows} == {"false"}, "scoring input audit cannot pass")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "packet audit cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_packet_slot"] for row in rows), "each audit row needs a packet slot")
    require(all(row["required_payload_evidence"] for row in rows), "each audit row needs payload evidence")
    require(all(row["required_hash_evidence"] for row in rows), "each audit row needs hash evidence")
    require(all(row["required_firewall_evidence"] for row in rows), "each audit row needs firewall evidence")
    require(
        all(
            row["packet_audit_finding"]
            == "remediation packet schema is declared but no packet is materialized or submitted"
            for row in rows
        ),
        "packet audit finding mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "packet audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "packet audit cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload scoring input remediation packet audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PACKET_AUDIT_V01",
        "packet audit summary id mismatch",
    )
    require(row["packet_audit_rows_declared"] == "7", "packet audit row count mismatch")
    require(row["packet_materialized_rows"] == "0", "packet materialized rows must be zero")
    require(row["packet_submitted_rows"] == "0", "packet submitted rows must be zero")
    require(row["packet_audit_passed_rows"] == "0", "packet audit passed rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_audit_passed_rows"] == "0", "scoring input audit passed rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_remediation_packet_audit_satisfied"] == "false",
        "remediation packet audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "packet audit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PACKET_AUDIT_REJECTED_NOT_MATERIALIZED",
        "packet audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_v01",
        "packet audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input materialization request must have seven rows")
    require(
        {row["request_status"] for row in rows} == {"MATERIALIZATION_REQUEST_DECLARED_NOT_FULFILLED"},
        "materialization request status mismatch",
    )
    require({row["materialization_requested"] for row in rows} == {"true"}, "materialization must be requested")
    require({row["packet_materialized"] for row in rows} == {"false"}, "packet cannot be materialized")
    require({row["packet_submitted"] for row in rows} == {"false"}, "packet cannot be submitted")
    require({row["packet_audit_passed"] for row in rows} == {"false"}, "packet audit cannot pass")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "request cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_packet_slot"] for row in rows), "each request row needs a packet slot")
    require(all(row["required_payload_file"] for row in rows), "each request row needs a payload file")
    require(all(row["required_provenance_file"] for row in rows), "each request row needs a provenance file")
    require(all(row["required_replay_command"] for row in rows), "each request row needs a replay command")
    require(all(row["required_hash_manifest"] for row in rows), "each request row needs a hash manifest")
    require(all(row["required_firewall_attestation"] for row in rows), "each request row needs firewall attestation")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "request cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "request cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload scoring input materialization request summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_REQUEST_V01",
        "materialization request summary id mismatch",
    )
    require(row["materialization_request_rows_declared"] == "7", "materialization request row count mismatch")
    require(row["materialization_requested_rows"] == "7", "materialization requested rows mismatch")
    require(row["packet_materialized_rows"] == "0", "packet materialized rows must be zero")
    require(row["packet_submitted_rows"] == "0", "packet submitted rows must be zero")
    require(row["packet_audit_passed_rows"] == "0", "packet audit passed rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_materialization_request_satisfied"] == "false",
        "materialization request must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "materialization request no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_REQUEST_DECLARED_NOT_FULFILLED",
        "materialization request status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_v01",
        "materialization request next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input materialization request audit must have seven rows")
    require(
        {row["request_audit_status"] for row in rows} == {"MATERIALIZATION_REQUEST_AUDITED_NOT_FULFILLED"},
        "materialization request audit status mismatch",
    )
    require({row["materialization_requested"] for row in rows} == {"true"}, "materialization must be requested")
    require({row["request_audited"] for row in rows} == {"true"}, "request must be audited")
    require({row["request_audit_passed"] for row in rows} == {"false"}, "request audit cannot pass")
    require({row["packet_materialized"] for row in rows} == {"false"}, "packet cannot be materialized")
    require({row["packet_submitted"] for row in rows} == {"false"}, "packet cannot be submitted")
    require({row["packet_audit_passed"] for row in rows} == {"false"}, "packet audit cannot pass")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "request audit cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_packet_slot"] for row in rows), "each request audit row needs a packet slot")
    require(all(row["required_payload_file"] for row in rows), "each request audit row needs a payload file")
    require(all(row["required_provenance_file"] for row in rows), "each request audit row needs a provenance file")
    require(all(row["required_replay_command"] for row in rows), "each request audit row needs a replay command")
    require(all(row["required_hash_manifest"] for row in rows), "each request audit row needs a hash manifest")
    require(all(row["required_firewall_attestation"] for row in rows), "each request audit row needs firewall attestation")
    require(
        all(
            row["request_audit_finding"]
            == "materialization request is declared but no requested packet is materialized or submitted"
            for row in rows
        ),
        "materialization request audit finding mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "request audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "request audit cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload scoring input materialization request audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_REQUEST_AUDIT_V01",
        "materialization request audit summary id mismatch",
    )
    require(row["materialization_request_audit_rows_declared"] == "7", "request audit row count mismatch")
    require(row["materialization_requested_rows"] == "7", "materialization requested rows mismatch")
    require(row["request_audited_rows"] == "7", "request audited rows mismatch")
    require(row["request_audit_passed_rows"] == "0", "request audit passed rows must be zero")
    require(row["packet_materialized_rows"] == "0", "packet materialized rows must be zero")
    require(row["packet_submitted_rows"] == "0", "packet submitted rows must be zero")
    require(row["packet_audit_passed_rows"] == "0", "packet audit passed rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_materialization_request_audit_satisfied"] == "false",
        "materialization request audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "materialization request audit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_REQUEST_AUDIT_NOT_FULFILLED",
        "materialization request audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_v01",
        "materialization request audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_v01() -> None:
    rows = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input materialization packet must have seven rows")
    require(
        {row["packet_status"] for row in rows}
        == {"MATERIALIZATION_PACKET_SHELL_DECLARED_ACTUAL_PAYLOAD_ABSENT"},
        "materialization packet status mismatch",
    )
    require({row["packet_shell_declared"] for row in rows} == {"true"}, "packet shell must be declared")
    require({row["actual_payload_present"] for row in rows} == {"false"}, "actual payload must be absent")
    require({row["actual_provenance_present"] for row in rows} == {"false"}, "actual provenance must be absent")
    require({row["actual_replay_command_present"] for row in rows} == {"false"}, "actual replay command must be absent")
    require({row["actual_hash_manifest_present"] for row in rows} == {"false"}, "actual hash manifest must be absent")
    require(
        {row["actual_firewall_attestation_present"] for row in rows} == {"false"},
        "actual firewall attestation must be absent",
    )
    require({row["packet_materialized"] for row in rows} == {"false"}, "packet cannot be materialized")
    require({row["packet_submitted"] for row in rows} == {"false"}, "packet cannot be submitted")
    require({row["packet_audit_passed"] for row in rows} == {"false"}, "packet audit cannot pass")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "packet shell cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["packet_shell_slot"] for row in rows), "each packet row needs a shell slot")
    require(all(row["expected_payload_file"] for row in rows), "each packet row needs expected payload file")
    require(all(row["expected_provenance_file"] for row in rows), "each packet row needs expected provenance file")
    require(all(row["expected_replay_command_file"] for row in rows), "each packet row needs expected replay file")
    require(all(row["expected_hash_manifest_file"] for row in rows), "each packet row needs expected hash file")
    require(
        all(row["expected_firewall_attestation_file"] for row in rows),
        "each packet row needs expected firewall file",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "packet shell cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "packet shell cannot allow verdicts")
    require(len(summary) == 1, "Phi Tau evidence payload scoring input materialization packet summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_PACKET_V01",
        "materialization packet summary id mismatch",
    )
    require(row["materialization_packet_rows_declared"] == "7", "packet row count mismatch")
    require(row["packet_shell_declared_rows"] == "7", "packet shell declared rows mismatch")
    require(row["actual_payload_present_rows"] == "0", "actual payload rows must be zero")
    require(row["actual_provenance_present_rows"] == "0", "actual provenance rows must be zero")
    require(row["actual_replay_command_present_rows"] == "0", "actual replay command rows must be zero")
    require(row["actual_hash_manifest_present_rows"] == "0", "actual hash manifest rows must be zero")
    require(row["actual_firewall_attestation_present_rows"] == "0", "actual firewall rows must be zero")
    require(row["packet_materialized_rows"] == "0", "packet materialized rows must be zero")
    require(row["packet_submitted_rows"] == "0", "packet submitted rows must be zero")
    require(row["packet_audit_passed_rows"] == "0", "packet audit passed rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_materialization_packet_satisfied"] == "false",
        "materialization packet must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "materialization packet no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_PACKET_SHELL_DECLARED_ACTUAL_PAYLOAD_ABSENT",
        "materialization packet status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_v01",
        "materialization packet next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input materialization packet audit must have seven rows")
    require(
        {row["packet_audit_status"] for row in rows}
        == {"MATERIALIZATION_PACKET_AUDITED_ACTUAL_PAYLOAD_ABSENT"},
        "materialization packet audit status mismatch",
    )
    require({row["packet_shell_declared"] for row in rows} == {"true"}, "packet shell must be declared")
    require({row["packet_shell_audited"] for row in rows} == {"true"}, "packet shell must be audited")
    require({row["actual_payload_present"] for row in rows} == {"false"}, "actual payload must be absent")
    require({row["actual_provenance_present"] for row in rows} == {"false"}, "actual provenance must be absent")
    require({row["actual_replay_command_present"] for row in rows} == {"false"}, "actual replay command must be absent")
    require({row["actual_hash_manifest_present"] for row in rows} == {"false"}, "actual hash manifest must be absent")
    require(
        {row["actual_firewall_attestation_present"] for row in rows} == {"false"},
        "actual firewall attestation must be absent",
    )
    require({row["packet_materialized"] for row in rows} == {"false"}, "packet cannot be materialized")
    require({row["packet_submitted"] for row in rows} == {"false"}, "packet cannot be submitted")
    require({row["packet_audit_passed"] for row in rows} == {"false"}, "packet audit cannot pass")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "packet audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["packet_shell_slot"] for row in rows), "each audit row needs a shell slot")
    require(all(row["expected_payload_file"] for row in rows), "each audit row needs expected payload file")
    require(all(row["expected_provenance_file"] for row in rows), "each audit row needs expected provenance file")
    require(all(row["expected_replay_command_file"] for row in rows), "each audit row needs expected replay file")
    require(all(row["expected_hash_manifest_file"] for row in rows), "each audit row needs expected hash file")
    require(
        all(row["expected_firewall_attestation_file"] for row in rows),
        "each audit row needs expected firewall file",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "packet audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "packet audit cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input materialization packet audit summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_PACKET_AUDIT_V01",
        "materialization packet audit summary id mismatch",
    )
    require(row["materialization_packet_audit_rows_declared"] == "7", "packet audit row count mismatch")
    require(row["packet_shell_declared_rows"] == "7", "packet shell declared rows mismatch")
    require(row["packet_shell_audited_rows"] == "7", "packet shell audited rows mismatch")
    require(row["actual_payload_present_rows"] == "0", "actual payload rows must be zero")
    require(row["actual_provenance_present_rows"] == "0", "actual provenance rows must be zero")
    require(row["actual_replay_command_present_rows"] == "0", "actual replay command rows must be zero")
    require(row["actual_hash_manifest_present_rows"] == "0", "actual hash manifest rows must be zero")
    require(row["actual_firewall_attestation_present_rows"] == "0", "actual firewall rows must be zero")
    require(row["packet_materialized_rows"] == "0", "packet materialized rows must be zero")
    require(row["packet_submitted_rows"] == "0", "packet submitted rows must be zero")
    require(row["packet_audit_passed_rows"] == "0", "packet audit passed rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_materialization_packet_audit_satisfied"] == "false",
        "materialization packet audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "materialization packet audit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_PACKET_AUDITED_ACTUAL_PAYLOAD_ABSENT",
        "materialization packet audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_v01",
        "materialization packet audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input payload fulfillment request must have seven rows")
    require(
        {row["fulfillment_request_status"] for row in rows}
        == {"PAYLOAD_FULFILLMENT_REQUEST_DECLARED_NOT_SUPPLIED"},
        "payload fulfillment request status mismatch",
    )
    require({row["fulfillment_requested"] for row in rows} == {"true"}, "fulfillment must be requested")
    require({row["payload_supplied"] for row in rows} == {"false"}, "payload must not be supplied")
    require({row["provenance_supplied"] for row in rows} == {"false"}, "provenance must not be supplied")
    require({row["replay_supplied"] for row in rows} == {"false"}, "replay must not be supplied")
    require({row["hash_manifest_supplied"] for row in rows} == {"false"}, "hash manifest must not be supplied")
    require(
        {row["firewall_attestation_supplied"] for row in rows} == {"false"},
        "firewall attestation must not be supplied",
    )
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "request cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_payload_file"] for row in rows), "each request row needs payload file")
    require(all(row["required_payload_content"] for row in rows), "each request row needs payload content")
    require(all(row["required_schema_or_units"] for row in rows), "each request row needs schema or units")
    require(all(row["required_provenance_file"] for row in rows), "each request row needs provenance file")
    require(all(row["required_replay_command_file"] for row in rows), "each request row needs replay file")
    require(all(row["required_hash_manifest_file"] for row in rows), "each request row needs hash file")
    require(
        all(row["required_firewall_attestation_file"] for row in rows),
        "each request row needs firewall file",
    )
    require(all(row["endpoint_blind_requirement"] for row in rows), "each request row needs endpoint-blind requirement")
    require(all(row["known_limit_requirement"] for row in rows), "each request row needs known-limit requirement")
    require(all(row["dimension_requirement"] for row in rows), "each request row needs dimension requirement")
    require(all(row["acceptance_rule"] for row in rows), "each request row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "request cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "request cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload fulfillment request summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_FULFILLMENT_REQUEST_V01",
        "payload fulfillment request summary id mismatch",
    )
    require(row["payload_fulfillment_request_rows_declared"] == "7", "payload fulfillment request row count mismatch")
    require(row["fulfillment_requested_rows"] == "7", "fulfillment requested rows mismatch")
    require(row["payload_supplied_rows"] == "0", "payload supplied rows must be zero")
    require(row["provenance_supplied_rows"] == "0", "provenance supplied rows must be zero")
    require(row["replay_supplied_rows"] == "0", "replay supplied rows must be zero")
    require(row["hash_manifest_supplied_rows"] == "0", "hash manifest supplied rows must be zero")
    require(row["firewall_attestation_supplied_rows"] == "0", "firewall supplied rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_fulfillment_request_satisfied"] == "false",
        "payload fulfillment request must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload fulfillment request no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_FULFILLMENT_REQUEST_DECLARED_NOT_SUPPLIED",
        "payload fulfillment request status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_v01",
        "payload fulfillment request next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input payload fulfillment request audit must have seven rows")
    require(
        {row["request_audit_status"] for row in rows}
        == {"PAYLOAD_FULFILLMENT_REQUEST_AUDITED_NOT_SUPPLIED"},
        "payload fulfillment request audit status mismatch",
    )
    require({row["fulfillment_requested"] for row in rows} == {"true"}, "fulfillment must be requested")
    require({row["request_audited"] for row in rows} == {"true"}, "request must be audited")
    require({row["request_audit_passed"] for row in rows} == {"false"}, "request audit cannot pass")
    require({row["payload_supplied"] for row in rows} == {"false"}, "payload must not be supplied")
    require({row["provenance_supplied"] for row in rows} == {"false"}, "provenance must not be supplied")
    require({row["replay_supplied"] for row in rows} == {"false"}, "replay must not be supplied")
    require({row["hash_manifest_supplied"] for row in rows} == {"false"}, "hash manifest must not be supplied")
    require(
        {row["firewall_attestation_supplied"] for row in rows} == {"false"},
        "firewall attestation must not be supplied",
    )
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_payload_file"] for row in rows), "each audit row needs payload file")
    require(all(row["required_payload_content"] for row in rows), "each audit row needs payload content")
    require(all(row["required_schema_or_units"] for row in rows), "each audit row needs schema or units")
    require(all(row["required_provenance_file"] for row in rows), "each audit row needs provenance file")
    require(all(row["required_replay_command_file"] for row in rows), "each audit row needs replay file")
    require(all(row["required_hash_manifest_file"] for row in rows), "each audit row needs hash file")
    require(all(row["required_firewall_attestation_file"] for row in rows), "each audit row needs firewall file")
    require(all(row["endpoint_blind_requirement"] for row in rows), "each audit row needs endpoint-blind requirement")
    require(all(row["known_limit_requirement"] for row in rows), "each audit row needs known-limit requirement")
    require(all(row["dimension_requirement"] for row in rows), "each audit row needs dimension requirement")
    require(all(row["acceptance_rule"] for row in rows), "each audit row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "audit cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload fulfillment request audit summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_FULFILLMENT_REQUEST_AUDIT_V01",
        "payload fulfillment request audit summary id mismatch",
    )
    require(row["payload_fulfillment_request_audit_rows_declared"] == "7", "request audit row count mismatch")
    require(row["fulfillment_requested_rows"] == "7", "fulfillment requested rows mismatch")
    require(row["request_audited_rows"] == "7", "request audited rows mismatch")
    require(row["request_audit_passed_rows"] == "0", "request audit passed rows must be zero")
    require(row["payload_supplied_rows"] == "0", "payload supplied rows must be zero")
    require(row["provenance_supplied_rows"] == "0", "provenance supplied rows must be zero")
    require(row["replay_supplied_rows"] == "0", "replay supplied rows must be zero")
    require(row["hash_manifest_supplied_rows"] == "0", "hash manifest supplied rows must be zero")
    require(row["firewall_attestation_supplied_rows"] == "0", "firewall supplied rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_fulfillment_request_audit_satisfied"] == "false",
        "payload fulfillment request audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload fulfillment request audit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_FULFILLMENT_REQUEST_AUDITED_NOT_SUPPLIED",
        "payload fulfillment request audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_v01",
        "payload fulfillment request audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_v01() -> None:
    rows = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input payload submission packet must have seven rows")
    require(
        {row["submission_packet_status"] for row in rows}
        == {"PAYLOAD_SUBMISSION_PACKET_SHELL_DECLARED_NOT_SUBMITTED"},
        "payload submission packet status mismatch",
    )
    require({row["submission_packet_declared"] for row in rows} == {"true"}, "submission packet must be declared")
    require({row["payload_submitted"] for row in rows} == {"false"}, "payload must not be submitted")
    require({row["provenance_submitted"] for row in rows} == {"false"}, "provenance must not be submitted")
    require({row["replay_submitted"] for row in rows} == {"false"}, "replay must not be submitted")
    require({row["hash_manifest_submitted"] for row in rows} == {"false"}, "hash manifest must not be submitted")
    require(
        {row["firewall_attestation_submitted"] for row in rows} == {"false"},
        "firewall attestation must not be submitted",
    )
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "packet shell cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["submission_packet_slot"] for row in rows), "each packet row needs a submission slot")
    require(all(row["required_payload_file"] for row in rows), "each packet row needs payload file")
    require(all(row["required_payload_content"] for row in rows), "each packet row needs payload content")
    require(all(row["required_schema_or_units"] for row in rows), "each packet row needs schema or units")
    require(all(row["required_provenance_file"] for row in rows), "each packet row needs provenance file")
    require(all(row["required_replay_command_file"] for row in rows), "each packet row needs replay file")
    require(all(row["required_hash_manifest_file"] for row in rows), "each packet row needs hash file")
    require(all(row["required_firewall_attestation_file"] for row in rows), "each packet row needs firewall file")
    require(all(row["endpoint_blind_requirement"] for row in rows), "each packet row needs endpoint-blind requirement")
    require(all(row["known_limit_requirement"] for row in rows), "each packet row needs known-limit requirement")
    require(all(row["dimension_requirement"] for row in rows), "each packet row needs dimension requirement")
    require(all(row["acceptance_rule"] for row in rows), "each packet row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "packet cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "packet cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission packet summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_PACKET_V01",
        "payload submission packet summary id mismatch",
    )
    require(row["payload_submission_packet_rows_declared"] == "7", "payload submission packet row count mismatch")
    require(row["submission_packet_declared_rows"] == "7", "submission packet declared rows mismatch")
    require(row["payload_submitted_rows"] == "0", "payload submitted rows must be zero")
    require(row["provenance_submitted_rows"] == "0", "provenance submitted rows must be zero")
    require(row["replay_submitted_rows"] == "0", "replay submitted rows must be zero")
    require(row["hash_manifest_submitted_rows"] == "0", "hash manifest submitted rows must be zero")
    require(row["firewall_attestation_submitted_rows"] == "0", "firewall submitted rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_packet_satisfied"] == "false",
        "payload submission packet must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission packet no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_PACKET_SHELL_DECLARED_NOT_SUBMITTED",
        "payload submission packet status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01",
        "payload submission packet next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input payload submission packet audit must have seven rows")
    require(
        {row["submission_packet_audit_status"] for row in rows}
        == {"PAYLOAD_SUBMISSION_PACKET_AUDITED_NOT_SUBMITTED"},
        "payload submission packet audit status mismatch",
    )
    require({row["submission_packet_declared"] for row in rows} == {"true"}, "submission packet must be declared")
    require({row["submission_packet_audited"] for row in rows} == {"true"}, "submission packet must be audited")
    require({row["submission_packet_audit_passed"] for row in rows} == {"false"}, "submission packet audit cannot pass")
    require({row["payload_submitted"] for row in rows} == {"false"}, "payload must not be submitted")
    require({row["provenance_submitted"] for row in rows} == {"false"}, "provenance must not be submitted")
    require({row["replay_submitted"] for row in rows} == {"false"}, "replay must not be submitted")
    require({row["hash_manifest_submitted"] for row in rows} == {"false"}, "hash manifest must not be submitted")
    require(
        {row["firewall_attestation_submitted"] for row in rows} == {"false"},
        "firewall attestation must not be submitted",
    )
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "packet audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["submission_packet_slot"] for row in rows), "each audit row needs a submission slot")
    require(all(row["required_payload_file"] for row in rows), "each audit row needs payload file")
    require(all(row["required_payload_content"] for row in rows), "each audit row needs payload content")
    require(all(row["required_schema_or_units"] for row in rows), "each audit row needs schema or units")
    require(all(row["required_provenance_file"] for row in rows), "each audit row needs provenance file")
    require(all(row["required_replay_command_file"] for row in rows), "each audit row needs replay file")
    require(all(row["required_hash_manifest_file"] for row in rows), "each audit row needs hash file")
    require(all(row["required_firewall_attestation_file"] for row in rows), "each audit row needs firewall file")
    require(all(row["endpoint_blind_requirement"] for row in rows), "each audit row needs endpoint-blind requirement")
    require(all(row["known_limit_requirement"] for row in rows), "each audit row needs known-limit requirement")
    require(all(row["dimension_requirement"] for row in rows), "each audit row needs dimension requirement")
    require(all(row["acceptance_rule"] for row in rows), "each audit row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "audit cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission packet audit summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_PACKET_AUDIT_V01",
        "payload submission packet audit summary id mismatch",
    )
    require(row["payload_submission_packet_audit_rows_declared"] == "7", "payload submission packet audit row count mismatch")
    require(row["submission_packet_declared_rows"] == "7", "submission packet declared rows mismatch")
    require(row["submission_packet_audited_rows"] == "7", "submission packet audited rows mismatch")
    require(row["submission_packet_audit_passed_rows"] == "0", "submission packet audit passed rows must be zero")
    require(row["payload_submitted_rows"] == "0", "payload submitted rows must be zero")
    require(row["provenance_submitted_rows"] == "0", "provenance submitted rows must be zero")
    require(row["replay_submitted_rows"] == "0", "replay submitted rows must be zero")
    require(row["hash_manifest_submitted_rows"] == "0", "hash manifest submitted rows must be zero")
    require(row["firewall_attestation_submitted_rows"] == "0", "firewall submitted rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_packet_audit_satisfied"] == "false",
        "payload submission packet audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission packet audit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_PACKET_AUDITED_NOT_SUBMITTED",
        "payload submission packet audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_v01",
        "payload submission packet audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input payload submission remediation plan must have seven rows")
    require(
        {row["remediation_status"] for row in rows}
        == {"SUBMISSION_REMEDIATION_PLANNED_NOT_COMPLETED"},
        "payload submission remediation plan status mismatch",
    )
    require({row["remediation_planned"] for row in rows} == {"true"}, "remediation must be planned")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["payload_submitted"] for row in rows} == {"false"}, "payload must not be submitted")
    require({row["provenance_submitted"] for row in rows} == {"false"}, "provenance must not be submitted")
    require({row["replay_submitted"] for row in rows} == {"false"}, "replay must not be submitted")
    require({row["hash_manifest_submitted"] for row in rows} == {"false"}, "hash manifest must not be submitted")
    require(
        {row["firewall_attestation_submitted"] for row in rows} == {"false"},
        "firewall attestation must not be submitted",
    )
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "plan cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["failed_submission_condition"] for row in rows), "each plan row needs failed condition")
    require(all(row["required_payload_file"] for row in rows), "each plan row needs payload file")
    require(all(row["required_remediation_action"] for row in rows), "each plan row needs remediation action")
    require(all(row["required_completion_evidence"] for row in rows), "each plan row needs completion evidence")
    require(all(row["endpoint_blind_requirement"] for row in rows), "each plan row needs endpoint-blind requirement")
    require(all(row["known_limit_requirement"] for row in rows), "each plan row needs known-limit requirement")
    require(all(row["dimension_requirement"] for row in rows), "each plan row needs dimension requirement")
    require(all(row["acceptance_rule"] for row in rows), "each plan row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "plan cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "plan cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission remediation plan summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PLAN_V01",
        "payload submission remediation plan summary id mismatch",
    )
    require(row["payload_submission_remediation_plan_rows_declared"] == "7", "remediation plan row count mismatch")
    require(row["remediation_planned_rows"] == "7", "remediation planned rows mismatch")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["payload_submitted_rows"] == "0", "payload submitted rows must be zero")
    require(row["provenance_submitted_rows"] == "0", "provenance submitted rows must be zero")
    require(row["replay_submitted_rows"] == "0", "replay submitted rows must be zero")
    require(row["hash_manifest_submitted_rows"] == "0", "hash manifest submitted rows must be zero")
    require(row["firewall_attestation_submitted_rows"] == "0", "firewall submitted rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_remediation_plan_satisfied"] == "false",
        "payload submission remediation plan must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission remediation plan no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PLANNED_NOT_COMPLETED",
        "payload submission remediation plan status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01",
        "payload submission remediation plan next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_summary_v01.csv"
    )
    require(len(rows) == 7, "Phi Tau evidence payload scoring input payload submission remediation packet must have seven rows")
    require(
        {row["remediation_packet_status"] for row in rows}
        == {"SUBMISSION_REMEDIATION_PACKET_SHELL_DECLARED_NOT_MATERIALIZED"},
        "payload submission remediation packet status mismatch",
    )
    require({row["remediation_packet_declared"] for row in rows} == {"true"}, "remediation packet must be declared")
    require({row["remediation_packet_materialized"] for row in rows} == {"false"}, "packet cannot be materialized")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["payload_submitted"] for row in rows} == {"false"}, "payload must not be submitted")
    require({row["provenance_submitted"] for row in rows} == {"false"}, "provenance must not be submitted")
    require({row["replay_submitted"] for row in rows} == {"false"}, "replay must not be submitted")
    require({row["hash_manifest_submitted"] for row in rows} == {"false"}, "hash manifest must not be submitted")
    require(
        {row["firewall_attestation_submitted"] for row in rows} == {"false"},
        "firewall attestation must not be submitted",
    )
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "packet cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["remediation_packet_slot"] for row in rows), "each packet row needs remediation slot")
    require(all(row["required_payload_file"] for row in rows), "each packet row needs payload file")
    require(all(row["required_remediation_action"] for row in rows), "each packet row needs remediation action")
    require(all(row["required_completion_evidence"] for row in rows), "each packet row needs completion evidence")
    require(all(row["expected_completion_evidence_file"] for row in rows), "each packet row needs completion file")
    require(all(row["expected_provenance_file"] for row in rows), "each packet row needs provenance file")
    require(all(row["expected_replay_command_file"] for row in rows), "each packet row needs replay file")
    require(all(row["expected_hash_manifest_file"] for row in rows), "each packet row needs hash file")
    require(all(row["expected_firewall_attestation_file"] for row in rows), "each packet row needs firewall file")
    require(all(row["endpoint_blind_requirement"] for row in rows), "each packet row needs endpoint-blind requirement")
    require(all(row["known_limit_requirement"] for row in rows), "each packet row needs known-limit requirement")
    require(all(row["dimension_requirement"] for row in rows), "each packet row needs dimension requirement")
    require(all(row["acceptance_rule"] for row in rows), "each packet row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "packet cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "packet cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission remediation packet summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PACKET_V01",
        "payload submission remediation packet summary id mismatch",
    )
    require(row["payload_submission_remediation_packet_rows_declared"] == "7", "remediation packet row count mismatch")
    require(row["remediation_packet_declared_rows"] == "7", "remediation packet declared rows mismatch")
    require(row["remediation_packet_materialized_rows"] == "0", "remediation packet materialized rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["payload_submitted_rows"] == "0", "payload submitted rows must be zero")
    require(row["provenance_submitted_rows"] == "0", "provenance submitted rows must be zero")
    require(row["replay_submitted_rows"] == "0", "replay submitted rows must be zero")
    require(row["hash_manifest_submitted_rows"] == "0", "hash manifest submitted rows must be zero")
    require(row["firewall_attestation_submitted_rows"] == "0", "firewall submitted rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_remediation_packet_satisfied"] == "false",
        "payload submission remediation packet must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission remediation packet no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PACKET_SHELL_DECLARED_NOT_MATERIALIZED",
        "payload submission remediation packet status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01",
        "payload submission remediation packet next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission remediation packet audit must have seven rows",
    )
    require(
        {row["packet_audit_status"] for row in rows}
        == {"SUBMISSION_REMEDIATION_PACKET_AUDIT_REJECTED_NOT_MATERIALIZED"},
        "payload submission remediation packet audit status mismatch",
    )
    require({row["packet_declared"] for row in rows} == {"true"}, "packet must be declared")
    require({row["packet_materialized"] for row in rows} == {"false"}, "packet cannot be materialized")
    require({row["packet_submitted"] for row in rows} == {"false"}, "packet cannot be submitted")
    require({row["packet_audit_passed"] for row in rows} == {"false"}, "packet audit cannot pass")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_audit_passed"] for row in rows} == {"false"}, "scoring input audit cannot pass")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_packet_slot"] for row in rows), "each audit row needs packet slot")
    require(all(row["required_payload_evidence"] for row in rows), "each audit row needs payload evidence")
    require(all(row["required_completion_evidence"] for row in rows), "each audit row needs completion evidence")
    require(all(row["required_provenance_evidence"] for row in rows), "each audit row needs provenance evidence")
    require(all(row["required_replay_evidence"] for row in rows), "each audit row needs replay evidence")
    require(all(row["required_hash_evidence"] for row in rows), "each audit row needs hash evidence")
    require(all(row["required_firewall_evidence"] for row in rows), "each audit row needs firewall evidence")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "audit cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission remediation packet audit summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PACKET_AUDIT_V01",
        "payload submission remediation packet audit summary id mismatch",
    )
    require(
        row["payload_submission_remediation_packet_audit_rows_declared"] == "7",
        "remediation packet audit row count mismatch",
    )
    require(row["packet_declared_rows"] == "7", "packet declared rows mismatch")
    require(row["packet_materialized_rows"] == "0", "packet materialized rows must be zero")
    require(row["packet_submitted_rows"] == "0", "packet submitted rows must be zero")
    require(row["packet_audit_passed_rows"] == "0", "packet audit passed rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_audit_passed_rows"] == "0", "scoring input audit rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_remediation_packet_audit_satisfied"] == "false",
        "payload submission remediation packet audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission remediation packet audit no-dark blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PACKET_AUDIT_REJECTED_NOT_MATERIALIZED",
        "payload submission remediation packet audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_v01",
        "payload submission remediation packet audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission materialization request must have seven rows",
    )
    require(
        {row["request_status"] for row in rows} == {"SUBMISSION_MATERIALIZATION_REQUEST_DECLARED_NOT_FULFILLED"},
        "payload submission materialization request status mismatch",
    )
    require({row["materialization_requested"] for row in rows} == {"true"}, "materialization must be requested")
    require({row["packet_materialized"] for row in rows} == {"false"}, "packet cannot be materialized")
    require({row["packet_submitted"] for row in rows} == {"false"}, "packet cannot be submitted")
    require({row["packet_audit_passed"] for row in rows} == {"false"}, "packet audit cannot pass")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "request cannot trigger hard failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_packet_slot"] for row in rows), "each request row needs packet slot")
    require(all(row["required_payload_file"] for row in rows), "each request row needs payload file")
    require(all(row["required_completion_evidence_file"] for row in rows), "each request row needs completion file")
    require(all(row["required_provenance_file"] for row in rows), "each request row needs provenance file")
    require(all(row["required_replay_command_file"] for row in rows), "each request row needs replay file")
    require(all(row["required_hash_manifest_file"] for row in rows), "each request row needs hash file")
    require(all(row["required_firewall_attestation_file"] for row in rows), "each request row needs firewall file")
    require(all(row["endpoint_blind_requirement"] for row in rows), "each request row needs endpoint-blind requirement")
    require(all(row["known_limit_requirement"] for row in rows), "each request row needs known-limit requirement")
    require(all(row["dimension_requirement"] for row in rows), "each request row needs dimension requirement")
    require(all(row["acceptance_rule"] for row in rows), "each request row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "request cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "request cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission materialization request summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_REQUEST_V01",
        "payload submission materialization request summary id mismatch",
    )
    require(
        row["payload_submission_materialization_request_rows_declared"] == "7",
        "payload submission materialization request row count mismatch",
    )
    require(row["materialization_requested_rows"] == "7", "materialization requested rows mismatch")
    require(row["packet_materialized_rows"] == "0", "packet materialized rows must be zero")
    require(row["packet_submitted_rows"] == "0", "packet submitted rows must be zero")
    require(row["packet_audit_passed_rows"] == "0", "packet audit passed rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_materialization_request_satisfied"] == "false",
        "payload submission materialization request must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission materialization request blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_REQUEST_DECLARED_NOT_FULFILLED",
        "payload submission materialization request status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01",
        "payload submission materialization request next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission materialization request audit must have seven rows",
    )
    require(
        {row["request_audit_status"] for row in rows}
        == {"SUBMISSION_MATERIALIZATION_REQUEST_AUDITED_NOT_FULFILLED"},
        "payload submission materialization request audit status mismatch",
    )
    require({row["materialization_requested"] for row in rows} == {"true"}, "materialization must be requested")
    require({row["request_audited"] for row in rows} == {"true"}, "request must be audited")
    require({row["request_audit_passed"] for row in rows} == {"false"}, "request audit cannot pass")
    require({row["packet_materialized"] for row in rows} == {"false"}, "packet cannot be materialized")
    require({row["packet_submitted"] for row in rows} == {"false"}, "packet cannot be submitted")
    require({row["packet_audit_passed"] for row in rows} == {"false"}, "packet audit cannot pass")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_packet_slot"] for row in rows), "each audit row needs packet slot")
    require(all(row["required_payload_file"] for row in rows), "each audit row needs payload file")
    require(all(row["required_completion_evidence_file"] for row in rows), "each audit row needs completion file")
    require(all(row["required_provenance_file"] for row in rows), "each audit row needs provenance file")
    require(all(row["required_replay_command_file"] for row in rows), "each audit row needs replay file")
    require(all(row["required_hash_manifest_file"] for row in rows), "each audit row needs hash file")
    require(all(row["required_firewall_attestation_file"] for row in rows), "each audit row needs firewall file")
    require(all(row["endpoint_blind_requirement"] for row in rows), "each audit row needs endpoint-blind requirement")
    require(all(row["known_limit_requirement"] for row in rows), "each audit row needs known-limit requirement")
    require(all(row["dimension_requirement"] for row in rows), "each audit row needs dimension requirement")
    require(all(row["acceptance_rule"] for row in rows), "each audit row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "audit cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission materialization request audit summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_REQUEST_AUDIT_V01",
        "payload submission materialization request audit summary id mismatch",
    )
    require(
        row["payload_submission_materialization_request_audit_rows_declared"] == "7",
        "payload submission materialization request audit row count mismatch",
    )
    require(row["materialization_requested_rows"] == "7", "materialization requested rows mismatch")
    require(row["request_audited_rows"] == "7", "request audited rows mismatch")
    require(row["request_audit_passed_rows"] == "0", "request audit passed rows must be zero")
    require(row["packet_materialized_rows"] == "0", "packet materialized rows must be zero")
    require(row["packet_submitted_rows"] == "0", "packet submitted rows must be zero")
    require(row["packet_audit_passed_rows"] == "0", "packet audit passed rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_materialization_request_audit_satisfied"] == "false",
        "payload submission materialization request audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission materialization request audit blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_REQUEST_AUDIT_NOT_FULFILLED",
        "payload submission materialization request audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01",
        "payload submission materialization request audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission materialization packet must have seven rows",
    )
    require(
        {row["packet_status"] for row in rows}
        == {"SUBMISSION_MATERIALIZATION_PACKET_SHELL_DECLARED_ACTUAL_PAYLOAD_ABSENT"},
        "payload submission materialization packet status mismatch",
    )
    require({row["packet_shell_declared"] for row in rows} == {"true"}, "packet shell must be declared")
    require({row["actual_payload_present"] for row in rows} == {"false"}, "actual payload must be absent")
    require(
        {row["actual_completion_evidence_present"] for row in rows} == {"false"},
        "completion evidence must be absent",
    )
    require({row["actual_provenance_present"] for row in rows} == {"false"}, "actual provenance must be absent")
    require({row["actual_replay_command_present"] for row in rows} == {"false"}, "actual replay must be absent")
    require({row["actual_hash_manifest_present"] for row in rows} == {"false"}, "actual hash manifest must be absent")
    require(
        {row["actual_firewall_attestation_present"] for row in rows} == {"false"},
        "actual firewall attestation must be absent",
    )
    require({row["packet_materialized"] for row in rows} == {"false"}, "packet cannot be materialized")
    require({row["packet_submitted"] for row in rows} == {"false"}, "packet cannot be submitted")
    require({row["packet_audit_passed"] for row in rows} == {"false"}, "packet audit cannot pass")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "packet cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["packet_shell_slot"] for row in rows), "each packet row needs shell slot")
    require(all(row["expected_payload_file"] for row in rows), "each packet row needs expected payload")
    require(all(row["expected_completion_evidence_file"] for row in rows), "each packet row needs expected completion file")
    require(all(row["expected_provenance_file"] for row in rows), "each packet row needs expected provenance")
    require(all(row["expected_replay_command_file"] for row in rows), "each packet row needs expected replay")
    require(all(row["expected_hash_manifest_file"] for row in rows), "each packet row needs expected hash")
    require(all(row["expected_firewall_attestation_file"] for row in rows), "each packet row needs expected firewall")
    require(all(row["endpoint_blind_requirement"] for row in rows), "each packet row needs endpoint-blind requirement")
    require(all(row["known_limit_requirement"] for row in rows), "each packet row needs known-limit requirement")
    require(all(row["dimension_requirement"] for row in rows), "each packet row needs dimension requirement")
    require(all(row["acceptance_rule"] for row in rows), "each packet row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "packet cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "packet cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission materialization packet summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_PACKET_V01",
        "payload submission materialization packet summary id mismatch",
    )
    require(
        row["payload_submission_materialization_packet_rows_declared"] == "7",
        "payload submission materialization packet row count mismatch",
    )
    require(row["packet_shell_declared_rows"] == "7", "packet shell declared rows mismatch")
    require(row["actual_payload_present_rows"] == "0", "payload present rows must be zero")
    require(row["actual_completion_evidence_present_rows"] == "0", "completion evidence rows must be zero")
    require(row["actual_provenance_present_rows"] == "0", "provenance present rows must be zero")
    require(row["actual_replay_command_present_rows"] == "0", "replay present rows must be zero")
    require(row["actual_hash_manifest_present_rows"] == "0", "hash present rows must be zero")
    require(row["actual_firewall_attestation_present_rows"] == "0", "firewall present rows must be zero")
    require(row["packet_materialized_rows"] == "0", "packet materialized rows must be zero")
    require(row["packet_submitted_rows"] == "0", "packet submitted rows must be zero")
    require(row["packet_audit_passed_rows"] == "0", "packet audit passed rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_materialization_packet_satisfied"] == "false",
        "payload submission materialization packet must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission materialization packet blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_PACKET_SHELL_DECLARED_ACTUAL_PAYLOAD_ABSENT",
        "payload submission materialization packet status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_v01",
        "payload submission materialization packet next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission materialization packet audit must have seven rows",
    )
    require(
        {row["packet_audit_status"] for row in rows}
        == {"SUBMISSION_MATERIALIZATION_PACKET_AUDITED_ACTUAL_PAYLOAD_ABSENT"},
        "payload submission materialization packet audit status mismatch",
    )
    require({row["packet_shell_declared"] for row in rows} == {"true"}, "packet shell must be declared")
    require({row["packet_shell_audited"] for row in rows} == {"true"}, "packet shell must be audited")
    require({row["actual_payload_present"] for row in rows} == {"false"}, "actual payload must be absent")
    require(
        {row["actual_completion_evidence_present"] for row in rows} == {"false"},
        "completion evidence must be absent",
    )
    require({row["actual_provenance_present"] for row in rows} == {"false"}, "actual provenance must be absent")
    require({row["actual_replay_command_present"] for row in rows} == {"false"}, "actual replay must be absent")
    require({row["actual_hash_manifest_present"] for row in rows} == {"false"}, "actual hash manifest must be absent")
    require(
        {row["actual_firewall_attestation_present"] for row in rows} == {"false"},
        "actual firewall attestation must be absent",
    )
    require({row["packet_materialized"] for row in rows} == {"false"}, "packet cannot be materialized")
    require({row["packet_submitted"] for row in rows} == {"false"}, "packet cannot be submitted")
    require({row["packet_audit_passed"] for row in rows} == {"false"}, "packet audit cannot pass")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["acceptance_allowed"] for row in rows} == {"false"}, "acceptance cannot be allowed")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "packet audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["packet_shell_slot"] for row in rows), "each audit row needs shell slot")
    require(all(row["expected_payload_file"] for row in rows), "each audit row needs payload file")
    require(all(row["expected_completion_evidence_file"] for row in rows), "each audit row needs completion file")
    require(all(row["expected_provenance_file"] for row in rows), "each audit row needs provenance file")
    require(all(row["expected_replay_command_file"] for row in rows), "each audit row needs replay file")
    require(all(row["expected_hash_manifest_file"] for row in rows), "each audit row needs hash file")
    require(all(row["expected_firewall_attestation_file"] for row in rows), "each audit row needs firewall file")
    require(all(row["endpoint_blind_requirement"] for row in rows), "each audit row needs endpoint-blind requirement")
    require(all(row["known_limit_requirement"] for row in rows), "each audit row needs known-limit requirement")
    require(all(row["dimension_requirement"] for row in rows), "each audit row needs dimension requirement")
    require(all(row["acceptance_rule"] for row in rows), "each audit row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "packet audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "packet audit cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission materialization packet audit summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_PACKET_AUDIT_V01",
        "payload submission materialization packet audit summary id mismatch",
    )
    require(
        row["payload_submission_materialization_packet_audit_rows_declared"] == "7",
        "payload submission materialization packet audit row count mismatch",
    )
    require(row["packet_shell_declared_rows"] == "7", "packet shell declared rows mismatch")
    require(row["packet_shell_audited_rows"] == "7", "packet shell audited rows mismatch")
    require(row["actual_payload_present_rows"] == "0", "payload present rows must be zero")
    require(row["actual_completion_evidence_present_rows"] == "0", "completion evidence rows must be zero")
    require(row["actual_provenance_present_rows"] == "0", "provenance present rows must be zero")
    require(row["actual_replay_command_present_rows"] == "0", "replay present rows must be zero")
    require(row["actual_hash_manifest_present_rows"] == "0", "hash present rows must be zero")
    require(row["actual_firewall_attestation_present_rows"] == "0", "firewall present rows must be zero")
    require(row["packet_materialized_rows"] == "0", "packet materialized rows must be zero")
    require(row["packet_submitted_rows"] == "0", "packet submitted rows must be zero")
    require(row["packet_audit_passed_rows"] == "0", "packet audit passed rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["acceptance_allowed_rows"] == "0", "acceptance allowed rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_materialization_packet_audit_satisfied"] == "false",
        "payload submission materialization packet audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission materialization packet audit blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_PACKET_AUDITED_ACTUAL_PAYLOAD_ABSENT",
        "payload submission materialization packet audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01",
        "payload submission materialization packet audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission fulfillment request must have seven rows",
    )
    require(
        {row["fulfillment_request_status"] for row in rows}
        == {"SUBMISSION_PAYLOAD_FULFILLMENT_REQUEST_DECLARED_NOT_SUPPLIED"},
        "payload submission fulfillment request status mismatch",
    )
    require({row["fulfillment_requested"] for row in rows} == {"true"}, "fulfillment must be requested")
    require({row["payload_supplied"] for row in rows} == {"false"}, "payload must not be supplied")
    require(
        {row["completion_evidence_supplied"] for row in rows} == {"false"},
        "completion evidence must not be supplied",
    )
    require({row["provenance_supplied"] for row in rows} == {"false"}, "provenance must not be supplied")
    require({row["replay_supplied"] for row in rows} == {"false"}, "replay must not be supplied")
    require({row["hash_manifest_supplied"] for row in rows} == {"false"}, "hash manifest must not be supplied")
    require(
        {row["firewall_attestation_supplied"] for row in rows} == {"false"},
        "firewall attestation must not be supplied",
    )
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "request cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_payload_file"] for row in rows), "each request row needs payload file")
    require(all(row["required_payload_content"] for row in rows), "each request row needs payload content")
    require(all(row["required_schema_or_units"] for row in rows), "each request row needs schema or units")
    require(all(row["required_completion_evidence_file"] for row in rows), "each request row needs completion file")
    require(all(row["required_provenance_file"] for row in rows), "each request row needs provenance file")
    require(all(row["required_replay_command_file"] for row in rows), "each request row needs replay file")
    require(all(row["required_hash_manifest_file"] for row in rows), "each request row needs hash file")
    require(
        all(row["required_firewall_attestation_file"] for row in rows),
        "each request row needs firewall file",
    )
    require(all(row["endpoint_blind_requirement"] for row in rows), "each request row needs endpoint-blind requirement")
    require(all(row["known_limit_requirement"] for row in rows), "each request row needs known-limit requirement")
    require(all(row["dimension_requirement"] for row in rows), "each request row needs dimension requirement")
    require(all(row["acceptance_rule"] for row in rows), "each request row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "request cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "request cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission fulfillment request summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_FULFILLMENT_REQUEST_V01",
        "payload submission fulfillment request summary id mismatch",
    )
    require(
        row["payload_submission_fulfillment_request_rows_declared"] == "7",
        "payload submission fulfillment request row count mismatch",
    )
    require(row["fulfillment_requested_rows"] == "7", "fulfillment requested rows mismatch")
    require(row["payload_supplied_rows"] == "0", "payload supplied rows must be zero")
    require(row["completion_evidence_supplied_rows"] == "0", "completion evidence rows must be zero")
    require(row["provenance_supplied_rows"] == "0", "provenance supplied rows must be zero")
    require(row["replay_supplied_rows"] == "0", "replay supplied rows must be zero")
    require(row["hash_manifest_supplied_rows"] == "0", "hash manifest supplied rows must be zero")
    require(row["firewall_attestation_supplied_rows"] == "0", "firewall supplied rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_fulfillment_request_satisfied"] == "false",
        "payload submission fulfillment request must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission fulfillment request blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_FULFILLMENT_REQUEST_DECLARED_NOT_SUPPLIED",
        "payload submission fulfillment request status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_v01",
        "payload submission fulfillment request next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission fulfillment request audit must have seven rows",
    )
    require(
        {row["request_audit_status"] for row in rows}
        == {"SUBMISSION_PAYLOAD_FULFILLMENT_REQUEST_AUDITED_NOT_SUPPLIED"},
        "payload submission fulfillment request audit status mismatch",
    )
    require({row["fulfillment_requested"] for row in rows} == {"true"}, "fulfillment must be requested")
    require({row["request_audited"] for row in rows} == {"true"}, "request must be audited")
    require({row["request_audit_passed"] for row in rows} == {"false"}, "request audit must not pass")
    require({row["payload_supplied"] for row in rows} == {"false"}, "payload must not be supplied")
    require(
        {row["completion_evidence_supplied"] for row in rows} == {"false"},
        "completion evidence must not be supplied",
    )
    require({row["provenance_supplied"] for row in rows} == {"false"}, "provenance must not be supplied")
    require({row["replay_supplied"] for row in rows} == {"false"}, "replay must not be supplied")
    require({row["hash_manifest_supplied"] for row in rows} == {"false"}, "hash manifest must not be supplied")
    require(
        {row["firewall_attestation_supplied"] for row in rows} == {"false"},
        "firewall attestation must not be supplied",
    )
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "request cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_payload_file"] for row in rows), "each audit row needs payload file")
    require(all(row["required_payload_content"] for row in rows), "each audit row needs payload content")
    require(all(row["required_schema_or_units"] for row in rows), "each audit row needs schema or units")
    require(all(row["required_completion_evidence_file"] for row in rows), "each audit row needs completion file")
    require(all(row["required_provenance_file"] for row in rows), "each audit row needs provenance file")
    require(all(row["required_replay_command_file"] for row in rows), "each audit row needs replay file")
    require(all(row["required_hash_manifest_file"] for row in rows), "each audit row needs hash file")
    require(
        all(row["required_firewall_attestation_file"] for row in rows),
        "each audit row needs firewall file",
    )
    require(all(row["endpoint_blind_requirement"] for row in rows), "each audit row needs endpoint-blind requirement")
    require(all(row["known_limit_requirement"] for row in rows), "each audit row needs known-limit requirement")
    require(all(row["dimension_requirement"] for row in rows), "each audit row needs dimension requirement")
    require(all(row["acceptance_rule"] for row in rows), "each audit row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "audit cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission fulfillment request audit summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_FULFILLMENT_REQUEST_AUDIT_V01",
        "payload submission fulfillment request audit summary id mismatch",
    )
    require(
        row["payload_submission_fulfillment_request_audit_rows_declared"] == "7",
        "payload submission fulfillment request audit row count mismatch",
    )
    require(row["fulfillment_requested_rows"] == "7", "fulfillment requested rows mismatch")
    require(row["request_audited_rows"] == "7", "request audited rows mismatch")
    require(row["request_audit_passed_rows"] == "0", "request audit passed rows must be zero")
    require(row["payload_supplied_rows"] == "0", "payload supplied rows must be zero")
    require(row["completion_evidence_supplied_rows"] == "0", "completion evidence rows must be zero")
    require(row["provenance_supplied_rows"] == "0", "provenance supplied rows must be zero")
    require(row["replay_supplied_rows"] == "0", "replay supplied rows must be zero")
    require(row["hash_manifest_supplied_rows"] == "0", "hash manifest supplied rows must be zero")
    require(row["firewall_attestation_supplied_rows"] == "0", "firewall supplied rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_satisfied"] == "false",
        "payload submission fulfillment request audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission fulfillment request audit blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_FULFILLMENT_REQUEST_AUDITED_NOT_SUPPLIED",
        "payload submission fulfillment request audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01",
        "payload submission fulfillment request audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission execution packet must have seven rows",
    )
    require(
        {row["execution_packet_status"] for row in rows}
        == {"SUBMISSION_EXECUTION_PACKET_DECLARED_BLOCKED_PAYLOAD_NOT_SUPPLIED"},
        "payload submission execution packet status mismatch",
    )
    require({row["execution_packet_declared"] for row in rows} == {"true"}, "execution packet must be declared")
    require({row["can_execute"] for row in rows} == {"false"}, "execution cannot be allowed")
    require({row["execution_attempted"] for row in rows} == {"false"}, "execution cannot be attempted")
    require({row["execution_succeeded"] for row in rows} == {"false"}, "execution cannot succeed")
    require({row["payload_supplied"] for row in rows} == {"false"}, "payload must not be supplied")
    require(
        {row["completion_evidence_supplied"] for row in rows} == {"false"},
        "completion evidence must not be supplied",
    )
    require({row["provenance_supplied"] for row in rows} == {"false"}, "provenance must not be supplied")
    require({row["replay_supplied"] for row in rows} == {"false"}, "replay must not be supplied")
    require({row["hash_manifest_supplied"] for row in rows} == {"false"}, "hash manifest must not be supplied")
    require(
        {row["firewall_attestation_supplied"] for row in rows} == {"false"},
        "firewall attestation must not be supplied",
    )
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "packet cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["execution_command_template"] for row in rows), "each row needs command template")
    require(all(row["execution_prerequisite_rule"] for row in rows), "each row needs prerequisite rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "packet cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "packet cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission execution packet summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_PACKET_V01",
        "payload submission execution packet summary id mismatch",
    )
    require(row["payload_submission_execution_packet_rows_declared"] == "7", "execution packet row count mismatch")
    require(row["execution_packet_declared_rows"] == "7", "execution packet declared rows mismatch")
    require(row["can_execute_rows"] == "0", "can execute rows must be zero")
    require(row["execution_attempted_rows"] == "0", "execution attempted rows must be zero")
    require(row["execution_succeeded_rows"] == "0", "execution succeeded rows must be zero")
    require(row["payload_supplied_rows"] == "0", "payload supplied rows must be zero")
    require(row["completion_evidence_supplied_rows"] == "0", "completion evidence rows must be zero")
    require(row["provenance_supplied_rows"] == "0", "provenance supplied rows must be zero")
    require(row["replay_supplied_rows"] == "0", "replay supplied rows must be zero")
    require(row["hash_manifest_supplied_rows"] == "0", "hash manifest supplied rows must be zero")
    require(row["firewall_attestation_supplied_rows"] == "0", "firewall supplied rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_execution_packet_satisfied"] == "false",
        "payload submission execution packet must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission execution packet blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_PACKET_DECLARED_BLOCKED",
        "payload submission execution packet status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_v01",
        "payload submission execution packet next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission execution packet audit must have seven rows",
    )
    require(
        {row["execution_packet_audit_status"] for row in rows}
        == {"SUBMISSION_EXECUTION_PACKET_AUDITED_BLOCKED_PAYLOAD_NOT_SUPPLIED"},
        "payload submission execution packet audit status mismatch",
    )
    require({row["execution_packet_declared"] for row in rows} == {"true"}, "execution packet must be declared")
    require({row["execution_packet_audited"] for row in rows} == {"true"}, "execution packet must be audited")
    require({row["execution_packet_audit_passed"] for row in rows} == {"false"}, "execution audit cannot pass")
    require({row["can_execute"] for row in rows} == {"false"}, "execution cannot be allowed")
    require({row["execution_attempted"] for row in rows} == {"false"}, "execution cannot be attempted")
    require({row["execution_succeeded"] for row in rows} == {"false"}, "execution cannot succeed")
    require({row["payload_supplied"] for row in rows} == {"false"}, "payload must not be supplied")
    require(
        {row["completion_evidence_supplied"] for row in rows} == {"false"},
        "completion evidence must not be supplied",
    )
    require({row["provenance_supplied"] for row in rows} == {"false"}, "provenance must not be supplied")
    require({row["replay_supplied"] for row in rows} == {"false"}, "replay must not be supplied")
    require({row["hash_manifest_supplied"] for row in rows} == {"false"}, "hash manifest must not be supplied")
    require(
        {row["firewall_attestation_supplied"] for row in rows} == {"false"},
        "firewall attestation must not be supplied",
    )
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["execution_command_template"] for row in rows), "each audit row needs command template")
    require(all(row["execution_prerequisite_rule"] for row in rows), "each audit row needs prerequisite rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "audit cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission execution packet audit summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_PACKET_AUDIT_V01",
        "payload submission execution packet audit summary id mismatch",
    )
    require(row["payload_submission_execution_packet_audit_rows_declared"] == "7", "audit row count mismatch")
    require(row["execution_packet_declared_rows"] == "7", "execution packet declared rows mismatch")
    require(row["execution_packet_audited_rows"] == "7", "execution packet audited rows mismatch")
    require(row["execution_packet_audit_passed_rows"] == "0", "execution audit passed rows must be zero")
    require(row["can_execute_rows"] == "0", "can execute rows must be zero")
    require(row["execution_attempted_rows"] == "0", "execution attempted rows must be zero")
    require(row["execution_succeeded_rows"] == "0", "execution succeeded rows must be zero")
    require(row["payload_supplied_rows"] == "0", "payload supplied rows must be zero")
    require(row["completion_evidence_supplied_rows"] == "0", "completion evidence rows must be zero")
    require(row["provenance_supplied_rows"] == "0", "provenance supplied rows must be zero")
    require(row["replay_supplied_rows"] == "0", "replay supplied rows must be zero")
    require(row["hash_manifest_supplied_rows"] == "0", "hash manifest supplied rows must be zero")
    require(row["firewall_attestation_supplied_rows"] == "0", "firewall supplied rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_execution_packet_audit_satisfied"] == "false",
        "payload submission execution packet audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission execution packet audit blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_PACKET_AUDITED_BLOCKED",
        "payload submission execution packet audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01",
        "payload submission execution packet audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission execution unblock plan must have seven rows",
    )
    require(
        {row["unblock_status"] for row in rows} == {"EXECUTION_UNBLOCK_DECLARED_NOT_COMPLETED"},
        "payload submission execution unblock plan status mismatch",
    )
    require({row["execution_packet_audited"] for row in rows} == {"true"}, "execution packet must be audited")
    require({row["unblock_completed"] for row in rows} == {"false"}, "unblock cannot be completed")
    require({row["can_execute"] for row in rows} == {"false"}, "execution cannot be allowed")
    require({row["execution_attempted"] for row in rows} == {"false"}, "execution cannot be attempted")
    require({row["execution_succeeded"] for row in rows} == {"false"}, "execution cannot succeed")
    require({row["payload_supplied"] for row in rows} == {"false"}, "payload must not be supplied")
    require(
        {row["completion_evidence_supplied"] for row in rows} == {"false"},
        "completion evidence must not be supplied",
    )
    require({row["provenance_supplied"] for row in rows} == {"false"}, "provenance must not be supplied")
    require({row["replay_supplied"] for row in rows} == {"false"}, "replay must not be supplied")
    require({row["hash_manifest_supplied"] for row in rows} == {"false"}, "hash manifest must not be supplied")
    require(
        {row["firewall_attestation_supplied"] for row in rows} == {"false"},
        "firewall attestation must not be supplied",
    )
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "plan cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_unblock_action"] for row in rows), "each row needs unblock action")
    require(all(row["required_evidence_object"] for row in rows), "each row needs evidence object")
    require(all(row["required_exit_condition"] for row in rows), "each row needs exit condition")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "plan cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "plan cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission execution unblock plan summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_UNBLOCK_PLAN_V01",
        "payload submission execution unblock plan summary id mismatch",
    )
    require(row["unblock_rows_declared"] == "7", "unblock row count mismatch")
    require(row["execution_packet_audited_rows"] == "7", "execution packet audited rows mismatch")
    require(row["unblock_completed_rows"] == "0", "unblock completed rows must be zero")
    require(row["payload_supplied_rows"] == "0", "payload supplied rows must be zero")
    require(row["completion_evidence_supplied_rows"] == "0", "completion evidence rows must be zero")
    require(row["provenance_supplied_rows"] == "0", "provenance supplied rows must be zero")
    require(row["replay_supplied_rows"] == "0", "replay supplied rows must be zero")
    require(row["hash_manifest_supplied_rows"] == "0", "hash manifest supplied rows must be zero")
    require(row["firewall_attestation_supplied_rows"] == "0", "firewall supplied rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["can_execute_rows"] == "0", "can execute rows must be zero")
    require(row["execution_attempted_rows"] == "0", "execution attempted rows must be zero")
    require(row["execution_succeeded_rows"] == "0", "execution succeeded rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_execution_unblock_plan_satisfied"] == "false",
        "payload submission execution unblock plan must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission execution unblock plan blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED",
        "payload submission execution unblock plan status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_v01",
        "payload submission execution unblock plan next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission execution unblock plan audit must have seven rows",
    )
    require(
        {row["unblock_plan_audit_status"] for row in rows} == {"EXECUTION_UNBLOCK_PLAN_AUDITED_NOT_COMPLETED"},
        "payload submission execution unblock plan audit status mismatch",
    )
    require({row["execution_packet_audited"] for row in rows} == {"true"}, "execution packet must be audited")
    require({row["unblock_plan_audited"] for row in rows} == {"true"}, "unblock plan must be audited")
    require({row["unblock_plan_audit_passed"] for row in rows} == {"false"}, "unblock plan audit cannot pass")
    require({row["unblock_completed"] for row in rows} == {"false"}, "unblock cannot be completed")
    require({row["can_execute"] for row in rows} == {"false"}, "execution cannot be allowed")
    require({row["execution_attempted"] for row in rows} == {"false"}, "execution cannot be attempted")
    require({row["execution_succeeded"] for row in rows} == {"false"}, "execution cannot succeed")
    require({row["payload_supplied"] for row in rows} == {"false"}, "payload must not be supplied")
    require(
        {row["completion_evidence_supplied"] for row in rows} == {"false"},
        "completion evidence must not be supplied",
    )
    require({row["provenance_supplied"] for row in rows} == {"false"}, "provenance must not be supplied")
    require({row["replay_supplied"] for row in rows} == {"false"}, "replay must not be supplied")
    require({row["hash_manifest_supplied"] for row in rows} == {"false"}, "hash manifest must not be supplied")
    require(
        {row["firewall_attestation_supplied"] for row in rows} == {"false"},
        "firewall attestation must not be supplied",
    )
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_unblock_action"] for row in rows), "each audit row needs unblock action")
    require(all(row["required_evidence_object"] for row in rows), "each audit row needs evidence object")
    require(all(row["required_exit_condition"] for row in rows), "each audit row needs exit condition")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "audit cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission execution unblock plan audit summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_UNBLOCK_PLAN_AUDIT_V01",
        "payload submission execution unblock plan audit summary id mismatch",
    )
    require(row["unblock_plan_audit_rows_declared"] == "7", "unblock audit row count mismatch")
    require(row["execution_packet_audited_rows"] == "7", "execution packet audited rows mismatch")
    require(row["unblock_plan_audited_rows"] == "7", "unblock plan audited rows mismatch")
    require(row["unblock_plan_audit_passed_rows"] == "0", "unblock plan audit passed rows must be zero")
    require(row["unblock_completed_rows"] == "0", "unblock completed rows must be zero")
    require(row["payload_supplied_rows"] == "0", "payload supplied rows must be zero")
    require(row["completion_evidence_supplied_rows"] == "0", "completion evidence rows must be zero")
    require(row["provenance_supplied_rows"] == "0", "provenance supplied rows must be zero")
    require(row["replay_supplied_rows"] == "0", "replay supplied rows must be zero")
    require(row["hash_manifest_supplied_rows"] == "0", "hash manifest supplied rows must be zero")
    require(row["firewall_attestation_supplied_rows"] == "0", "firewall supplied rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["can_execute_rows"] == "0", "can execute rows must be zero")
    require(row["execution_attempted_rows"] == "0", "execution attempted rows must be zero")
    require(row["execution_succeeded_rows"] == "0", "execution succeeded rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_satisfied"] == "false",
        "payload submission execution unblock plan audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission execution unblock plan audit blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_UNBLOCK_PLAN_AUDITED_NOT_COMPLETED",
        "payload submission execution unblock plan audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_v01",
        "payload submission execution unblock plan audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission evidence object request must have seven rows",
    )
    require(
        {row["request_status"] for row in rows} == {"EVIDENCE_OBJECT_REQUESTED_NOT_SUPPLIED"},
        "payload submission evidence object request status mismatch",
    )
    require({row["evidence_requested"] for row in rows} == {"true"}, "evidence must be requested")
    require({row["evidence_supplied"] for row in rows} == {"false"}, "evidence must not be supplied")
    require({row["evidence_audited"] for row in rows} == {"false"}, "evidence must not be audited")
    require({row["evidence_accepted"] for row in rows} == {"false"}, "evidence must not be accepted")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["can_execute"] for row in rows} == {"false"}, "execution cannot be allowed")
    require({row["execution_attempted"] for row in rows} == {"false"}, "execution cannot be attempted")
    require({row["execution_succeeded"] for row in rows} == {"false"}, "execution cannot succeed")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "request cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_evidence_file"] for row in rows), "each row needs evidence file")
    require(all(row["required_evidence_content"] for row in rows), "each row needs evidence content")
    require(all(row["required_schema_or_units"] for row in rows), "each row needs schema or units")
    require(all(row["required_acceptance_check"] for row in rows), "each row needs acceptance check")
    require(all(row["required_firewall_check"] for row in rows), "each row needs firewall check")
    require(all(row["required_replay_check"] for row in rows), "each row needs replay check")
    require(all(row["required_hash_check"] for row in rows), "each row needs hash check")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "request cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "request cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission evidence object request summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_REQUEST_V01",
        "payload submission evidence object request summary id mismatch",
    )
    require(row["evidence_object_request_rows_declared"] == "7", "evidence object request row count mismatch")
    require(row["evidence_requested_rows"] == "7", "evidence requested rows mismatch")
    require(row["evidence_supplied_rows"] == "0", "evidence supplied rows must be zero")
    require(row["evidence_audited_rows"] == "0", "evidence audited rows must be zero")
    require(row["evidence_accepted_rows"] == "0", "evidence accepted rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["can_execute_rows"] == "0", "can execute rows must be zero")
    require(row["execution_attempted_rows"] == "0", "execution attempted rows must be zero")
    require(row["execution_succeeded_rows"] == "0", "execution succeeded rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_request_satisfied"] == "false",
        "payload submission evidence object request must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission evidence object request blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_REQUESTED_NOT_SUPPLIED",
        "payload submission evidence object request status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01",
        "payload submission evidence object request next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission evidence object request audit must have seven rows",
    )
    require(
        {row["request_audit_status"] for row in rows} == {"EVIDENCE_OBJECT_REQUEST_AUDITED_NOT_SUPPLIED"},
        "payload submission evidence object request audit status mismatch",
    )
    require({row["evidence_requested"] for row in rows} == {"true"}, "evidence must be requested")
    require({row["request_audited"] for row in rows} == {"true"}, "request must be audited")
    require({row["request_audit_passed"] for row in rows} == {"false"}, "request audit cannot pass")
    require({row["evidence_supplied"] for row in rows} == {"false"}, "evidence must not be supplied")
    require({row["evidence_audited"] for row in rows} == {"false"}, "evidence must not be audited")
    require({row["evidence_accepted"] for row in rows} == {"false"}, "evidence must not be accepted")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["can_execute"] for row in rows} == {"false"}, "execution cannot be allowed")
    require({row["execution_attempted"] for row in rows} == {"false"}, "execution cannot be attempted")
    require({row["execution_succeeded"] for row in rows} == {"false"}, "execution cannot succeed")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_evidence_file"] for row in rows), "each audit row needs evidence file")
    require(all(row["required_evidence_content"] for row in rows), "each audit row needs evidence content")
    require(all(row["required_schema_or_units"] for row in rows), "each audit row needs schema or units")
    require(all(row["required_acceptance_check"] for row in rows), "each audit row needs acceptance check")
    require(all(row["required_firewall_check"] for row in rows), "each audit row needs firewall check")
    require(all(row["required_replay_check"] for row in rows), "each audit row needs replay check")
    require(all(row["required_hash_check"] for row in rows), "each audit row needs hash check")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "audit cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission evidence object request audit summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_REQUEST_AUDIT_V01",
        "payload submission evidence object request audit summary id mismatch",
    )
    require(row["evidence_object_request_audit_rows_declared"] == "7", "evidence object request audit row count mismatch")
    require(row["evidence_requested_rows"] == "7", "evidence requested rows mismatch")
    require(row["request_audited_rows"] == "7", "request audited rows mismatch")
    require(row["request_audit_passed_rows"] == "0", "request audit passed rows must be zero")
    require(row["evidence_supplied_rows"] == "0", "evidence supplied rows must be zero")
    require(row["evidence_audited_rows"] == "0", "evidence audited rows must be zero")
    require(row["evidence_accepted_rows"] == "0", "evidence accepted rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["can_execute_rows"] == "0", "can execute rows must be zero")
    require(row["execution_attempted_rows"] == "0", "execution attempted rows must be zero")
    require(row["execution_succeeded_rows"] == "0", "execution succeeded rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_satisfied"] == "false",
        "payload submission evidence object request audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission evidence object request audit blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_REQUEST_AUDITED_NOT_SUPPLIED",
        "payload submission evidence object request audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_v01",
        "payload submission evidence object request audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission evidence object receipt gate must have seven rows",
    )
    require(
        {row["receipt_gate_status"] for row in rows} == {"EVIDENCE_OBJECT_RECEIPT_GATE_OPEN_NOT_RECEIVED"},
        "payload submission evidence object receipt gate status mismatch",
    )
    require({row["receipt_gate_open"] for row in rows} == {"true"}, "receipt gate must be open")
    require({row["evidence_received"] for row in rows} == {"false"}, "evidence must not be received")
    require({row["receipt_validated"] for row in rows} == {"false"}, "receipt must not be validated")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipt must not be accepted")
    require({row["evidence_audited"] for row in rows} == {"false"}, "evidence must not be audited")
    require({row["evidence_accepted"] for row in rows} == {"false"}, "evidence must not be accepted")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["can_execute"] for row in rows} == {"false"}, "execution cannot be allowed")
    require({row["execution_attempted"] for row in rows} == {"false"}, "execution cannot be attempted")
    require({row["execution_succeeded"] for row in rows} == {"false"}, "execution cannot succeed")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "receipt gate cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_evidence_file"] for row in rows), "each row needs evidence file")
    require(all(row["receipt_requirement"] for row in rows), "each row needs receipt requirement")
    require(all(row["receipt_validation_rule"] for row in rows), "each row needs validation rule")
    require(all(row["receipt_acceptance_rule"] for row in rows), "each row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "gate cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "gate cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission evidence object receipt gate summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_GATE_V01",
        "payload submission evidence object receipt gate summary id mismatch",
    )
    require(row["evidence_object_receipt_gate_rows_declared"] == "7", "receipt gate row count mismatch")
    require(row["receipt_gate_open_rows"] == "7", "receipt gate open rows mismatch")
    require(row["evidence_received_rows"] == "0", "evidence received rows must be zero")
    require(row["receipt_validated_rows"] == "0", "receipt validated rows must be zero")
    require(row["receipt_accepted_rows"] == "0", "receipt accepted rows must be zero")
    require(row["evidence_audited_rows"] == "0", "evidence audited rows must be zero")
    require(row["evidence_accepted_rows"] == "0", "evidence accepted rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["can_execute_rows"] == "0", "can execute rows must be zero")
    require(row["execution_attempted_rows"] == "0", "execution attempted rows must be zero")
    require(row["execution_succeeded_rows"] == "0", "execution succeeded rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_satisfied"] == "false",
        "payload submission evidence object receipt gate must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission evidence object receipt gate blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_GATE_OPEN_NOT_RECEIVED",
        "payload submission evidence object receipt gate status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_v01",
        "payload submission evidence object receipt gate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission evidence object receipt gate audit must have seven rows",
    )
    require(
        {row["receipt_gate_audit_status"] for row in rows}
        == {"EVIDENCE_OBJECT_RECEIPT_GATE_AUDITED_NOT_RECEIVED"},
        "payload submission evidence object receipt gate audit status mismatch",
    )
    require({row["receipt_gate_open"] for row in rows} == {"true"}, "receipt gate must be open")
    require({row["receipt_gate_audited"] for row in rows} == {"true"}, "receipt gate must be audited")
    require({row["receipt_gate_audit_passed"] for row in rows} == {"false"}, "receipt gate audit cannot pass")
    require({row["evidence_received"] for row in rows} == {"false"}, "evidence must not be received")
    require({row["receipt_validated"] for row in rows} == {"false"}, "receipt must not be validated")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipt must not be accepted")
    require({row["evidence_audited"] for row in rows} == {"false"}, "evidence must not be audited")
    require({row["evidence_accepted"] for row in rows} == {"false"}, "evidence must not be accepted")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["can_execute"] for row in rows} == {"false"}, "execution cannot be allowed")
    require({row["execution_attempted"] for row in rows} == {"false"}, "execution cannot be attempted")
    require({row["execution_succeeded"] for row in rows} == {"false"}, "execution cannot succeed")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "receipt gate audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["required_evidence_file"] for row in rows), "each audit row needs evidence file")
    require(all(row["receipt_requirement"] for row in rows), "each audit row needs receipt requirement")
    require(all(row["receipt_validation_rule"] for row in rows), "each audit row needs validation rule")
    require(all(row["receipt_acceptance_rule"] for row in rows), "each audit row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "audit cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission evidence object receipt gate audit summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_GATE_AUDIT_V01",
        "payload submission evidence object receipt gate audit summary id mismatch",
    )
    require(row["evidence_object_receipt_gate_audit_rows_declared"] == "7", "receipt gate audit row count mismatch")
    require(row["receipt_gate_open_rows"] == "7", "receipt gate open rows mismatch")
    require(row["receipt_gate_audited_rows"] == "7", "receipt gate audited rows mismatch")
    require(row["receipt_gate_audit_passed_rows"] == "0", "receipt gate audit passed rows must be zero")
    require(row["evidence_received_rows"] == "0", "evidence received rows must be zero")
    require(row["receipt_validated_rows"] == "0", "receipt validated rows must be zero")
    require(row["receipt_accepted_rows"] == "0", "receipt accepted rows must be zero")
    require(row["evidence_audited_rows"] == "0", "evidence audited rows must be zero")
    require(row["evidence_accepted_rows"] == "0", "evidence accepted rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["can_execute_rows"] == "0", "can execute rows must be zero")
    require(row["execution_attempted_rows"] == "0", "execution attempted rows must be zero")
    require(row["execution_succeeded_rows"] == "0", "execution succeeded rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_satisfied"] == "false",
        "payload submission evidence object receipt gate audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission evidence object receipt gate audit blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_GATE_AUDITED_NOT_RECEIVED",
        "payload submission evidence object receipt gate audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_v01",
        "payload submission evidence object receipt gate audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission evidence object receipt candidate must have seven rows",
    )
    require(
        {row["receipt_candidate_status"] for row in rows}
        == {"EVIDENCE_OBJECT_RECEIPT_CANDIDATE_DECLARED_NOT_RECEIVED"},
        "payload submission evidence object receipt candidate status mismatch",
    )
    require({row["receipt_candidate_declared"] for row in rows} == {"true"}, "receipt candidates must be declared")
    require({row["receipt_gate_open"] for row in rows} == {"true"}, "receipt gate must be open")
    require({row["receipt_gate_audited"] for row in rows} == {"true"}, "receipt gate must be audited")
    require({row["receipt_gate_audit_passed"] for row in rows} == {"false"}, "receipt gate audit cannot pass")
    require({row["evidence_received"] for row in rows} == {"false"}, "evidence must not be received")
    require({row["receipt_validated"] for row in rows} == {"false"}, "receipt must not be validated")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipt must not be accepted")
    require({row["evidence_audited"] for row in rows} == {"false"}, "evidence must not be audited")
    require({row["evidence_accepted"] for row in rows} == {"false"}, "evidence must not be accepted")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["can_execute"] for row in rows} == {"false"}, "execution cannot be allowed")
    require({row["execution_attempted"] for row in rows} == {"false"}, "execution cannot be attempted")
    require({row["execution_succeeded"] for row in rows} == {"false"}, "execution cannot succeed")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "receipt candidate cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["expected_evidence_file"] for row in rows), "each candidate row needs expected evidence file")
    require(all(row["expected_receipt_object"] for row in rows), "each candidate row needs expected receipt object")
    require(all(row["receipt_candidate_rule"] for row in rows), "each candidate row needs candidate rule")
    require(all(row["receipt_validation_rule"] for row in rows), "each candidate row needs validation rule")
    require(all(row["receipt_acceptance_rule"] for row in rows), "each candidate row needs acceptance rule")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "candidate cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "candidate cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission evidence object receipt candidate summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_CANDIDATE_V01",
        "payload submission evidence object receipt candidate summary id mismatch",
    )
    require(row["evidence_object_receipt_candidate_rows_declared"] == "7", "receipt candidate row count mismatch")
    require(row["receipt_candidate_declared_rows"] == "7", "receipt candidate declared rows mismatch")
    require(row["receipt_gate_open_rows"] == "7", "receipt gate open rows mismatch")
    require(row["receipt_gate_audited_rows"] == "7", "receipt gate audited rows mismatch")
    require(row["receipt_gate_audit_passed_rows"] == "0", "receipt gate audit passed rows must be zero")
    require(row["evidence_received_rows"] == "0", "evidence received rows must be zero")
    require(row["receipt_validated_rows"] == "0", "receipt validated rows must be zero")
    require(row["receipt_accepted_rows"] == "0", "receipt accepted rows must be zero")
    require(row["evidence_audited_rows"] == "0", "evidence audited rows must be zero")
    require(row["evidence_accepted_rows"] == "0", "evidence accepted rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["can_execute_rows"] == "0", "can execute rows must be zero")
    require(row["execution_attempted_rows"] == "0", "execution attempted rows must be zero")
    require(row["execution_succeeded_rows"] == "0", "execution succeeded rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_satisfied"] == "false",
        "payload submission evidence object receipt candidate must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission evidence object receipt candidate blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_CANDIDATE_DECLARED_NOT_RECEIVED",
        "payload submission evidence object receipt candidate status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_v01",
        "payload submission evidence object receipt candidate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission evidence object receipt candidate audit must have seven rows",
    )
    require(
        {row["receipt_candidate_audit_status"] for row in rows}
        == {"EVIDENCE_OBJECT_RECEIPT_CANDIDATE_AUDITED_NOT_RECEIVED"},
        "payload submission evidence object receipt candidate audit status mismatch",
    )
    require({row["receipt_candidate_declared"] for row in rows} == {"true"}, "receipt candidates must be declared")
    require({row["receipt_candidate_audited"] for row in rows} == {"true"}, "receipt candidates must be audited")
    require({row["receipt_candidate_audit_passed"] for row in rows} == {"false"}, "receipt candidate audit cannot pass")
    require({row["receipt_gate_open"] for row in rows} == {"true"}, "receipt gate must be open")
    require({row["receipt_gate_audited"] for row in rows} == {"true"}, "receipt gate must be audited")
    require({row["receipt_gate_audit_passed"] for row in rows} == {"false"}, "receipt gate audit cannot pass")
    require({row["evidence_received"] for row in rows} == {"false"}, "evidence must not be received")
    require({row["receipt_validated"] for row in rows} == {"false"}, "receipt must not be validated")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipt must not be accepted")
    require({row["evidence_audited"] for row in rows} == {"false"}, "evidence must not be audited")
    require({row["evidence_accepted"] for row in rows} == {"false"}, "evidence must not be accepted")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["can_execute"] for row in rows} == {"false"}, "execution cannot be allowed")
    require({row["execution_attempted"] for row in rows} == {"false"}, "execution cannot be attempted")
    require({row["execution_succeeded"] for row in rows} == {"false"}, "execution cannot succeed")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "receipt candidate audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["expected_evidence_file"] for row in rows), "each audit row needs expected evidence file")
    require(all(row["expected_receipt_object"] for row in rows), "each audit row needs expected receipt object")
    require(all(row["candidate_audit_rule"] for row in rows), "each audit row needs candidate audit rule")
    require(
        all(row["audit_failure_reason"] == "receipt candidate is declared, but no evidence object or receipt object is received" for row in rows),
        "receipt candidate audit failure reason mismatch",
    )
    require(
        all(row["audit_decision"] == "failed_until_evidence_object_and_receipt_are_supplied" for row in rows),
        "receipt candidate audit decision mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "candidate audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "candidate audit cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission evidence object receipt candidate audit summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_CANDIDATE_AUDIT_V01",
        "payload submission evidence object receipt candidate audit summary id mismatch",
    )
    require(row["evidence_object_receipt_candidate_audit_rows_declared"] == "7", "receipt candidate audit row count mismatch")
    require(row["receipt_candidate_declared_rows"] == "7", "receipt candidate declared rows mismatch")
    require(row["receipt_candidate_audited_rows"] == "7", "receipt candidate audited rows mismatch")
    require(row["receipt_candidate_audit_passed_rows"] == "0", "receipt candidate audit passed rows must be zero")
    require(row["receipt_gate_open_rows"] == "7", "receipt gate open rows mismatch")
    require(row["receipt_gate_audited_rows"] == "7", "receipt gate audited rows mismatch")
    require(row["receipt_gate_audit_passed_rows"] == "0", "receipt gate audit passed rows must be zero")
    require(row["evidence_received_rows"] == "0", "evidence received rows must be zero")
    require(row["receipt_validated_rows"] == "0", "receipt validated rows must be zero")
    require(row["receipt_accepted_rows"] == "0", "receipt accepted rows must be zero")
    require(row["evidence_audited_rows"] == "0", "evidence audited rows must be zero")
    require(row["evidence_accepted_rows"] == "0", "evidence accepted rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["can_execute_rows"] == "0", "can execute rows must be zero")
    require(row["execution_attempted_rows"] == "0", "execution attempted rows must be zero")
    require(row["execution_succeeded_rows"] == "0", "execution succeeded rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_satisfied"] == "false",
        "payload submission evidence object receipt candidate audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission evidence object receipt candidate audit blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_CANDIDATE_AUDITED_NOT_RECEIVED",
        "payload submission evidence object receipt candidate audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_v01",
        "payload submission evidence object receipt candidate audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_summary_v01.csv"
    )
    require(
        len(rows) == 7,
        "Phi Tau evidence payload scoring input payload submission evidence object receipt candidate remediation plan must have seven rows",
    )
    require(
        {row["remediation_status"] for row in rows}
        == {"RECEIPT_CANDIDATE_REMEDIATION_DECLARED_NOT_COMPLETED"},
        "payload submission evidence object receipt candidate remediation status mismatch",
    )
    require({row["receipt_candidate_declared"] for row in rows} == {"true"}, "receipt candidates must be declared")
    require({row["receipt_candidate_audited"] for row in rows} == {"true"}, "receipt candidates must be audited")
    require({row["receipt_candidate_audit_passed"] for row in rows} == {"false"}, "receipt candidate audit cannot pass")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["evidence_received"] for row in rows} == {"false"}, "evidence must not be received")
    require({row["receipt_validated"] for row in rows} == {"false"}, "receipt must not be validated")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipt must not be accepted")
    require({row["evidence_audited"] for row in rows} == {"false"}, "evidence must not be audited")
    require({row["evidence_accepted"] for row in rows} == {"false"}, "evidence must not be accepted")
    require({row["payload_accepted"] for row in rows} == {"false"}, "payload cannot be accepted")
    require({row["scoring_input_accepted"] for row in rows} == {"false"}, "scoring input cannot be accepted")
    require({row["can_execute"] for row in rows} == {"false"}, "execution cannot be allowed")
    require({row["execution_attempted"] for row in rows} == {"false"}, "execution cannot be attempted")
    require({row["execution_succeeded"] for row in rows} == {"false"}, "execution cannot succeed")
    require({row["evidence_package_passed"] for row in rows} == {"false"}, "evidence package cannot pass")
    require({row["certificate_passed"] for row in rows} == {"false"}, "certificate cannot pass")
    require({row["phi_tau_eff_derived"] for row in rows} == {"false"}, "Phi_tau_eff cannot be derived")
    require({row["scores_computed"] for row in rows} == {"false"}, "scores cannot be computed")
    require({row["cmb_likelihood_available"] for row in rows} == {"false"}, "CMB likelihood cannot be available")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "remediation plan cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["missing_evidence_object"] for row in rows), "each remediation row needs missing evidence object")
    require(all(row["missing_receipt_object"] for row in rows), "each remediation row needs missing receipt object")
    require(all(row["required_remediation_action"] for row in rows), "each remediation row needs action")
    require(all(row["required_receipt_binding"] for row in rows), "each remediation row needs receipt binding")
    require(all(row["required_evidence_bundle"] for row in rows), "each remediation row needs evidence bundle")
    require(
        all(
            row["acceptance_exit_gate"]
            == "may exit only after evidence object and receipt are supplied, validated, and audit-passed without endpoint leakage"
            for row in rows
        ),
        "receipt candidate remediation exit gate mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "remediation plan cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "remediation plan cannot allow verdicts")
    require(
        len(summary) == 1,
        "Phi Tau evidence payload scoring input payload submission evidence object receipt candidate remediation plan summary must have one row",
    )
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_CANDIDATE_REMEDIATION_PLAN_V01",
        "payload submission evidence object receipt candidate remediation summary id mismatch",
    )
    require(
        row["evidence_object_receipt_candidate_remediation_rows_declared"] == "7",
        "receipt candidate remediation row count mismatch",
    )
    require(row["receipt_candidate_declared_rows"] == "7", "receipt candidate declared rows mismatch")
    require(row["receipt_candidate_audited_rows"] == "7", "receipt candidate audited rows mismatch")
    require(row["receipt_candidate_audit_passed_rows"] == "0", "receipt candidate audit passed rows must be zero")
    require(row["remediation_completed_rows"] == "0", "remediation completed rows must be zero")
    require(row["evidence_received_rows"] == "0", "evidence received rows must be zero")
    require(row["receipt_validated_rows"] == "0", "receipt validated rows must be zero")
    require(row["receipt_accepted_rows"] == "0", "receipt accepted rows must be zero")
    require(row["evidence_audited_rows"] == "0", "evidence audited rows must be zero")
    require(row["evidence_accepted_rows"] == "0", "evidence accepted rows must be zero")
    require(row["payload_accepted_rows"] == "0", "payload accepted rows must be zero")
    require(row["scoring_input_accepted_rows"] == "0", "scoring input accepted rows must be zero")
    require(row["can_execute_rows"] == "0", "can execute rows must be zero")
    require(row["execution_attempted_rows"] == "0", "execution attempted rows must be zero")
    require(row["execution_succeeded_rows"] == "0", "execution succeeded rows must be zero")
    require(row["evidence_package_passed_rows"] == "0", "evidence package passed rows must be zero")
    require(row["certificate_passed_rows"] == "0", "certificate passed rows must be zero")
    require(row["phi_tau_eff_derived_rows"] == "0", "Phi rows must be zero")
    require(row["scores_computed_rows"] == "0", "score rows must be zero")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood rows must be zero")
    require(row["hard_failures_triggered"] == "0", "hard failures must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_satisfied"]
        == "false",
        "payload submission evidence object receipt candidate remediation plan must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "payload submission evidence object receipt candidate remediation blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_CANDIDATE_REMEDIATION_DECLARED_NOT_COMPLETED",
        "payload submission evidence object receipt candidate remediation status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01",
        "payload submission evidence object receipt candidate remediation next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_summary_v01.csv"
    )
    require(len(rows) == 7, "evidence object receipt materialization packet must have seven rows")
    require(
        {row["materialization_status"] for row in rows}
        == {"EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_PACKET_DECLARED_NO_EVIDENCE_MATERIALIZED"},
        "evidence object receipt materialization packet status mismatch",
    )
    require({row["packet_declared"] for row in rows} == {"true"}, "packets must be declared")
    false_fields = [
        "evidence_materialized",
        "receipt_validated",
        "receipt_accepted",
        "evidence_audited",
        "evidence_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]
    for field in false_fields:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "materialization packet cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    for field in [
        "packet_slot_object",
        "required_evidence_file",
        "required_receipt_file",
        "materialization_requirement",
        "provenance_requirement",
        "replay_requirement",
        "firewall_requirement",
        "acceptance_exit_gate",
    ]:
        require(all(row[field] for row in rows), f"each row needs {field}")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "materialization packet cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "materialization packet cannot allow verdicts")
    require(len(summary) == 1, "materialization packet summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_PACKET_V01",
        "materialization packet summary id mismatch",
    )
    require(row["evidence_object_receipt_materialization_packet_rows_declared"] == "7", "materialization packet row count mismatch")
    require(row["packet_declared_rows"] == "7", "packet declared rows mismatch")
    zero_fields = [
        "evidence_materialized_rows",
        "receipt_validated_rows",
        "receipt_accepted_rows",
        "evidence_audited_rows",
        "evidence_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]
    for field in zero_fields:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_satisfied"]
        == "false",
        "materialization packet must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "materialization packet blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_PACKET_DECLARED_NO_EVIDENCE_MATERIALIZED",
        "materialization packet status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_v01",
        "materialization packet next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "evidence object receipt materialization audit must have seven rows")
    require(
        {row["materialization_audit_status"] for row in rows}
        == {"EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_AUDIT_FAILED_NO_EVIDENCE_MATERIALIZED"},
        "evidence object receipt materialization audit status mismatch",
    )
    require({row["packet_declared"] for row in rows} == {"true"}, "packets must be declared")
    false_fields = [
        "evidence_materialized",
        "receipt_validated",
        "receipt_accepted",
        "evidence_audited",
        "evidence_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]
    for field in false_fields:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "materialization audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(
        all(row["audit_failure_reason"] == "no materialized evidence object or receipt object is available for audit" for row in rows),
        "materialization audit failure reason mismatch",
    )
    require(
        all(row["audit_decision"] == "failed_until_evidence_object_and_receipt_are_materialized" for row in rows),
        "materialization audit decision mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "materialization audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "materialization audit cannot allow verdicts")
    require(len(summary) == 1, "materialization audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_AUDIT_V01",
        "materialization audit summary id mismatch",
    )
    require(row["evidence_object_receipt_materialization_audit_rows_declared"] == "7", "materialization audit row count mismatch")
    require(row["packet_declared_rows"] == "7", "packet declared rows mismatch")
    for field in [
        "evidence_materialized_rows",
        "receipt_validated_rows",
        "receipt_accepted_rows",
        "evidence_audited_rows",
        "evidence_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_satisfied"]
        == "false",
        "materialization audit must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "materialization audit blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_AUDIT_FAILED_NO_EVIDENCE_MATERIALIZED",
        "materialization audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_v01",
        "materialization audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_summary_v01.csv"
    )
    require(len(rows) == 7, "evidence object receipt acceptance precheck must have seven rows")
    require(
        {row["acceptance_precheck_status"] for row in rows}
        == {"EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_SATISFIED"},
        "evidence object receipt acceptance precheck status mismatch",
    )
    require({row["packet_declared"] for row in rows} == {"true"}, "packets must be declared")
    false_fields = [
        "evidence_materialized",
        "receipt_validated",
        "receipt_accepted",
        "evidence_audited",
        "evidence_accepted",
        "acceptance_precheck_passed",
        "payload_accepted",
        "scoring_input_accepted",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]
    for field in false_fields:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    for field in ["materialization_gate", "receipt_gate", "provenance_gate", "replay_gate", "firewall_gate"]:
        require(all(row[field] for row in rows), f"{field} must be populated")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "acceptance precheck cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(
        all(row["acceptance_blocker"] == "materialization audit failed because no evidence object is materialized" for row in rows),
        "acceptance blocker mismatch",
    )
    require(
        all(
            row["precheck_decision"] == "blocked_until_materialization_receipt_provenance_replay_and_firewall_gates_pass"
            for row in rows
        ),
        "acceptance precheck decision mismatch",
    )
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "acceptance precheck cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "acceptance precheck cannot allow verdicts")
    require(len(summary) == 1, "acceptance precheck summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_PRECHECK_V01",
        "acceptance precheck summary id mismatch",
    )
    require(row["evidence_object_receipt_acceptance_precheck_rows_declared"] == "7", "acceptance precheck row count mismatch")
    require(row["packet_declared_rows"] == "7", "packet declared rows mismatch")
    for field in [
        "evidence_materialized_rows",
        "receipt_validated_rows",
        "receipt_accepted_rows",
        "evidence_audited_rows",
        "evidence_accepted_rows",
        "acceptance_precheck_passed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_satisfied"]
        == "false",
        "acceptance precheck must be unsatisfied",
    )
    require(row["no_dark_blockers"] == "7", "acceptance precheck blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_SATISFIED",
        "acceptance precheck status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_v01",
        "acceptance precheck next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_summary_v01.csv"
    )
    require(len(rows) == 7, "evidence object receipt acceptance unblock plan must have seven rows")
    require(
        {row["unblock_status"] for row in rows}
        == {"EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_UNBLOCK_DECLARED_NOT_COMPLETED"},
        "evidence object receipt acceptance unblock status mismatch",
    )
    require({row["packet_declared"] for row in rows} == {"true"}, "packets must be declared")
    false_fields = [
        "evidence_materialized",
        "receipt_validated",
        "receipt_accepted",
        "provenance_bound",
        "replay_bound",
        "firewall_passed",
        "evidence_audited",
        "evidence_accepted",
        "acceptance_precheck_passed",
        "unblock_completed",
        "payload_accepted",
        "scoring_input_accepted",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]
    for field in false_fields:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(all(row["required_unblock_action"] for row in rows), "each row needs an unblock action")
    require(all(row["required_exit_condition"] for row in rows), "each row needs an exit condition")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "unblock plan cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "unblock plan cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "unblock plan cannot allow verdicts")
    require(len(summary) == 1, "unblock plan summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_V01",
        "unblock plan summary id mismatch",
    )
    require(row["evidence_object_receipt_acceptance_unblock_plan_rows_declared"] == "7", "unblock plan row count mismatch")
    require(row["packet_declared_rows"] == "7", "packet declared rows mismatch")
    for field in [
        "unblock_completed_rows",
        "evidence_materialized_rows",
        "receipt_validated_rows",
        "receipt_accepted_rows",
        "provenance_bound_rows",
        "replay_bound_rows",
        "firewall_passed_rows",
        "evidence_audited_rows",
        "evidence_accepted_rows",
        "acceptance_precheck_passed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_satisfied"]
        == "false",
        "unblock plan must be unsatisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "unblock plan blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED",
        "unblock plan status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_v01",
        "unblock plan next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "evidence object receipt acceptance unblock plan audit must have seven rows")
    require(
        {row["unblock_plan_audit_status"] for row in rows}
        == {"EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_AUDITED_NOT_COMPLETED"},
        "evidence object receipt acceptance unblock plan audit status mismatch",
    )
    require({row["unblock_plan_audited"] for row in rows} == {"true"}, "unblock plan must be audited")
    require({row["packet_declared"] for row in rows} == {"true"}, "packets must be declared")
    false_fields = [
        "unblock_plan_audit_passed",
        "evidence_materialized",
        "receipt_validated",
        "receipt_accepted",
        "provenance_bound",
        "replay_bound",
        "firewall_passed",
        "evidence_audited",
        "evidence_accepted",
        "acceptance_precheck_passed",
        "unblock_completed",
        "payload_accepted",
        "scoring_input_accepted",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]
    for field in false_fields:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(all(row["unblock_plan_audit_rule"] for row in rows), "each row needs an audit rule")
    require(all(row["unblock_plan_audit_finding"] for row in rows), "each row needs an audit finding")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "unblock plan audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "unblock plan audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "unblock plan audit cannot allow verdicts")
    require(len(summary) == 1, "unblock plan audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_AUDIT_V01",
        "unblock plan audit summary id mismatch",
    )
    require(row["evidence_object_receipt_acceptance_unblock_plan_audit_rows_declared"] == "7", "unblock plan audit row count mismatch")
    require(row["unblock_plan_audited_rows"] == "7", "unblock plan audited rows mismatch")
    require(row["packet_declared_rows"] == "7", "packet declared rows mismatch")
    for field in [
        "unblock_plan_audit_passed_rows",
        "unblock_completed_rows",
        "evidence_materialized_rows",
        "receipt_validated_rows",
        "receipt_accepted_rows",
        "provenance_bound_rows",
        "replay_bound_rows",
        "firewall_passed_rows",
        "evidence_audited_rows",
        "evidence_accepted_rows",
        "acceptance_precheck_passed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_satisfied"]
        == "false",
        "unblock plan audit must be unsatisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "unblock plan audit blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_AUDITED_NOT_COMPLETED",
        "unblock plan audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_v01",
        "unblock plan audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_summary_v01.csv"
    )
    require(len(rows) == 7, "evidence object receipt acceptance decision gate must have seven rows")
    require(
        {row["decision_gate_status"] for row in rows}
        == {"ACCEPTANCE_DECISION_CLOSED_UNBLOCK_AUDIT_NOT_PASSED"},
        "evidence object receipt acceptance decision status mismatch",
    )
    require({row["decision_output"] for row in rows} == {"acceptance_closed"}, "decision output must close acceptance")
    require({row["packet_declared"] for row in rows} == {"true"}, "packets must be declared")
    require({row["unblock_plan_audited"] for row in rows} == {"true"}, "unblock plan must be audited")
    false_fields = [
        "unblock_plan_audit_passed",
        "unblock_completed",
        "evidence_materialized",
        "receipt_validated",
        "receipt_accepted",
        "provenance_bound",
        "replay_bound",
        "firewall_passed",
        "evidence_audited",
        "evidence_accepted",
        "acceptance_precheck_passed",
        "acceptance_allowed",
        "payload_accepted",
        "scoring_input_accepted",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]
    for field in false_fields:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(all(row["target_gate"] for row in rows), "each row needs a target gate")
    require(all(row["required_prior_pass"] for row in rows), "each row needs a prior pass")
    require(
        all(
            row["decision_rule"]
            == "acceptance may open only if receipt unblock plan audit passes and all upstream evidence gates are completed"
            for row in rows
        ),
        "acceptance decision rule mismatch",
    )
    require(
        all(row["decision_reason"] == "receipt acceptance unblock plan audit is not satisfied" for row in rows),
        "acceptance decision reason mismatch",
    )
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "decision gate cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "decision gate cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "decision gate cannot allow verdicts")
    require(len(summary) == 1, "decision gate summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_DECISION_GATE_V01",
        "decision gate summary id mismatch",
    )
    require(row["evidence_object_receipt_acceptance_decision_gate_rows_declared"] == "7", "decision row count mismatch")
    require(row["packet_declared_rows"] == "7", "packet declared rows mismatch")
    require(row["unblock_plan_audited_rows"] == "7", "unblock plan audited rows mismatch")
    for field in [
        "unblock_plan_audit_passed_rows",
        "acceptance_allowed_rows",
        "unblock_completed_rows",
        "evidence_materialized_rows",
        "receipt_validated_rows",
        "receipt_accepted_rows",
        "provenance_bound_rows",
        "replay_bound_rows",
        "firewall_passed_rows",
        "evidence_audited_rows",
        "evidence_accepted_rows",
        "acceptance_precheck_passed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_satisfied"]
        == "false",
        "decision gate must be unsatisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "decision gate blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_DECISION_GATE_CLOSED_UNBLOCK_AUDIT_NOT_PASSED",
        "decision gate status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_v01",
        "decision gate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "evidence object receipt acceptance decision gate audit must have seven rows")
    require(
        {row["decision_gate_audit_status"] for row in rows}
        == {"ACCEPTANCE_DECISION_GATE_AUDITED_ACCEPTANCE_CLOSED"},
        "decision gate audit status mismatch",
    )
    require({row["decision_output"] for row in rows} == {"acceptance_closed"}, "decision output must close acceptance")
    require({row["packet_declared"] for row in rows} == {"true"}, "packets must be declared")
    require({row["decision_gate_audited"] for row in rows} == {"true"}, "decision gate must be audited")
    require({row["decision_gate_audit_passed"] for row in rows} == {"true"}, "closed decision audit must pass")
    require({row["unblock_plan_audited"] for row in rows} == {"true"}, "unblock plan must be audited")
    false_fields = [
        "unblock_plan_audit_passed",
        "unblock_completed",
        "evidence_materialized",
        "receipt_validated",
        "receipt_accepted",
        "provenance_bound",
        "replay_bound",
        "firewall_passed",
        "evidence_audited",
        "evidence_accepted",
        "acceptance_precheck_passed",
        "acceptance_allowed",
        "payload_accepted",
        "scoring_input_accepted",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]
    for field in false_fields:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(all(row["decision_gate_audit_rule"] for row in rows), "each row needs an audit rule")
    require(all(row["decision_gate_audit_finding"] for row in rows), "each row needs an audit finding")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "decision gate audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "decision audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "decision audit cannot allow verdicts")
    require(len(summary) == 1, "decision gate audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_DECISION_GATE_AUDIT_V01",
        "decision gate audit summary id mismatch",
    )
    require(row["evidence_object_receipt_acceptance_decision_gate_audit_rows_declared"] == "7", "audit row count mismatch")
    require(row["packet_declared_rows"] == "7", "packet declared rows mismatch")
    require(row["decision_gate_audited_rows"] == "7", "decision audited rows mismatch")
    require(row["decision_gate_audit_passed_rows"] == "7", "decision audit passed rows mismatch")
    require(row["unblock_plan_audited_rows"] == "7", "unblock plan audited rows mismatch")
    for field in [
        "unblock_plan_audit_passed_rows",
        "acceptance_allowed_rows",
        "unblock_completed_rows",
        "evidence_materialized_rows",
        "receipt_validated_rows",
        "receipt_accepted_rows",
        "provenance_bound_rows",
        "replay_bound_rows",
        "firewall_passed_rows",
        "evidence_audited_rows",
        "evidence_accepted_rows",
        "acceptance_precheck_passed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_satisfied"]
        == "true",
        "closed decision gate audit must be satisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "decision audit blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_DECISION_GATE_AUDITED_ACCEPTANCE_CLOSED",
        "decision gate audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_v01",
        "decision gate audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_summary_v01.csv"
    )
    require(len(rows) == 7, "evidence object receipt acceptance record must have seven rows")
    require(
        {row["acceptance_record_status"] for row in rows}
        == {"ACCEPTANCE_RECORD_WRITTEN_ACCEPTANCE_CLOSED"},
        "acceptance record status mismatch",
    )
    require({row["record_output"] for row in rows} == {"acceptance_closed_recorded"}, "record output mismatch")
    true_fields = ["packet_declared", "decision_gate_audited", "decision_gate_audit_passed", "acceptance_recorded"]
    for field in true_fields:
        require({row[field] for row in rows} == {"true"}, f"{field} must be true")
    false_fields = [
        "acceptance_allowed",
        "unblock_plan_audit_passed",
        "unblock_completed",
        "evidence_materialized",
        "receipt_validated",
        "receipt_accepted",
        "provenance_bound",
        "replay_bound",
        "firewall_passed",
        "evidence_audited",
        "evidence_accepted",
        "acceptance_precheck_passed",
        "payload_accepted",
        "scoring_input_accepted",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]
    for field in false_fields:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(all(row["record_rule"] for row in rows), "each row needs a record rule")
    require(all(row["record_finding"] for row in rows), "each row needs a record finding")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "acceptance record cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven no-dark blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "record cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "record cannot allow verdicts")
    require(len(summary) == 1, "acceptance record summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_RECORD_V01",
        "acceptance record summary id mismatch",
    )
    require(row["evidence_object_receipt_acceptance_record_rows_declared"] == "7", "record row count mismatch")
    require(row["packet_declared_rows"] == "7", "packet declared rows mismatch")
    require(row["decision_gate_audited_rows"] == "7", "decision audited rows mismatch")
    require(row["decision_gate_audit_passed_rows"] == "7", "decision audit passed rows mismatch")
    require(row["acceptance_recorded_rows"] == "7", "acceptance recorded rows mismatch")
    for field in [
        "acceptance_allowed_rows",
        "unblock_plan_audit_passed_rows",
        "unblock_completed_rows",
        "evidence_materialized_rows",
        "receipt_validated_rows",
        "receipt_accepted_rows",
        "provenance_bound_rows",
        "replay_bound_rows",
        "firewall_passed_rows",
        "evidence_audited_rows",
        "evidence_accepted_rows",
        "acceptance_precheck_passed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_satisfied"]
        == "true",
        "closed acceptance record must be satisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "CMB likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "record blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_RECORD_WRITTEN_ACCEPTANCE_CLOSED",
        "acceptance record status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_v01",
        "acceptance record next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_summary_v01.csv"
    )
    require(len(rows) == 7, "scoring handoff precheck must have seven rows")
    require(
        {row["scoring_handoff_precheck_status"] for row in rows}
        == {"SCORING_HANDOFF_PRECHECK_CLOSED_ACCEPTANCE_NOT_ALLOWED"},
        "scoring handoff precheck status mismatch",
    )
    require({row["handoff_output"] for row in rows} == {"handoff_closed"}, "handoff output mismatch")
    require({row["acceptance_recorded"] for row in rows} == {"true"}, "acceptance must be recorded")
    for field in [
        "acceptance_allowed",
        "evidence_accepted",
        "receipt_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(all(row["handoff_rule"] for row in rows), "each row needs a handoff rule")
    require(all(row["handoff_blocker"] for row in rows), "each row needs a handoff blocker")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "handoff precheck cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "handoff cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "handoff cannot allow verdicts")
    require(len(summary) == 1, "handoff summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_PRECHECK_V01",
        "handoff summary id mismatch",
    )
    require(row["evidence_object_receipt_scoring_handoff_precheck_rows_declared"] == "7", "handoff row count mismatch")
    require(row["acceptance_recorded_rows"] == "7", "acceptance recorded rows mismatch")
    for field in [
        "acceptance_allowed_rows",
        "evidence_accepted_rows",
        "receipt_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "can_handoff_to_scoring_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_satisfied"]
        == "false",
        "handoff precheck must be unsatisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_PRECHECK_CLOSED_ACCEPTANCE_NOT_ALLOWED",
        "handoff status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_v01",
        "handoff next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_summary_v01.csv"
    )
    require(len(rows) == 7, "scoring handoff unblock plan must have seven rows")
    require(
        {row["scoring_handoff_unblock_status"] for row in rows}
        == {"SCORING_HANDOFF_UNBLOCK_DECLARED_NOT_COMPLETED"},
        "scoring handoff unblock status mismatch",
    )
    require({row["acceptance_recorded"] for row in rows} == {"true"}, "acceptance must be recorded")
    for field in [
        "acceptance_allowed",
        "evidence_accepted",
        "receipt_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(all(row["required_unblock_action"] for row in rows), "each row needs an unblock action")
    require(all(row["required_exit_condition"] for row in rows), "each row needs an exit condition")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "unblock plan cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "unblock plan cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "unblock plan cannot allow verdicts")
    require(len(summary) == 1, "unblock plan summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_PLAN_V01",
        "unblock plan summary id mismatch",
    )
    require(row["evidence_object_receipt_scoring_handoff_unblock_plan_rows_declared"] == "7", "unblock row count mismatch")
    require(row["acceptance_recorded_rows"] == "7", "acceptance recorded rows mismatch")
    for field in [
        "acceptance_allowed_rows",
        "evidence_accepted_rows",
        "receipt_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_handoff_to_scoring_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_satisfied"]
        == "false",
        "handoff unblock plan must be unsatisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED",
        "unblock plan status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_v01",
        "unblock plan next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "scoring handoff unblock plan audit must have seven rows")
    require(
        {row["scoring_handoff_unblock_plan_audit_status"] for row in rows}
        == {"SCORING_HANDOFF_UNBLOCK_PLAN_AUDIT_PASSED_HANDOFF_STILL_BLOCKED"},
        "scoring handoff unblock plan audit status mismatch",
    )
    require({row["audit_passed"] for row in rows} == {"true"}, "audit must pass for plan consistency")
    require({row["acceptance_recorded"] for row in rows} == {"true"}, "acceptance must be recorded")
    for field in [
        "acceptance_allowed",
        "evidence_accepted",
        "receipt_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(all(row["audited_condition"] for row in rows), "each row needs an audited condition")
    require(
        {row["audit_result"] for row in rows} == {"plan_condition_declared_and_handoff_remains_blocked"},
        "audit result mismatch",
    )
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "unblock audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "unblock audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "unblock audit cannot allow verdicts")
    require(len(summary) == 1, "unblock plan audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_PLAN_AUDIT_V01",
        "unblock plan audit summary id mismatch",
    )
    require(row["evidence_object_receipt_scoring_handoff_unblock_plan_audit_rows_declared"] == "7", "audit row count mismatch")
    require(row["audit_passed_rows"] == "7", "audit passed rows mismatch")
    require(row["acceptance_recorded_rows"] == "7", "acceptance recorded rows mismatch")
    for field in [
        "acceptance_allowed_rows",
        "evidence_accepted_rows",
        "receipt_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_handoff_to_scoring_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_satisfied"]
        == "true",
        "handoff unblock plan audit must be satisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_PLAN_AUDIT_PASSED_HANDOFF_STILL_BLOCKED",
        "unblock plan audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_v01",
        "unblock plan audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_summary_v01.csv"
    )
    require(len(rows) == 7, "scoring handoff decision gate must have seven rows")
    require(
        {row["scoring_handoff_decision_gate_status"] for row in rows}
        == {"SCORING_HANDOFF_DECISION_GATE_CLOSED_ACCEPTANCE_NOT_SATISFIED"},
        "scoring handoff decision gate status mismatch",
    )
    require({row["decision_result"] for row in rows} == {"handoff_closed"}, "handoff decision must be closed")
    require({row["audit_passed"] for row in rows} == {"true"}, "audit must pass before closed decision")
    require({row["acceptance_recorded"] for row in rows} == {"true"}, "acceptance must be recorded")
    for field in [
        "acceptance_allowed",
        "evidence_accepted",
        "receipt_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(all(row["decision_rule"] for row in rows), "each row needs a decision rule")
    require(all(row["decision_reason"] for row in rows), "each row needs a decision reason")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "decision gate cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "decision gate cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "decision gate cannot allow verdicts")
    require(len(summary) == 1, "decision gate summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_DECISION_GATE_V01",
        "decision gate summary id mismatch",
    )
    require(row["evidence_object_receipt_scoring_handoff_decision_gate_rows_declared"] == "7", "decision row count mismatch")
    require(row["audit_passed_rows"] == "7", "audit passed rows mismatch")
    require(row["closed_decision_rows"] == "7", "closed decision rows mismatch")
    require(row["open_decision_rows"] == "0", "open decision rows must be zero")
    require(row["acceptance_recorded_rows"] == "7", "acceptance recorded rows mismatch")
    for field in [
        "acceptance_allowed_rows",
        "evidence_accepted_rows",
        "receipt_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_handoff_to_scoring_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_satisfied"]
        == "true",
        "handoff decision gate must be satisfied as a closed decision",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_DECISION_GATE_CLOSED_ACCEPTANCE_NOT_SATISFIED",
        "decision gate status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_v01",
        "decision gate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "scoring handoff decision gate audit must have seven rows")
    require(
        {row["scoring_handoff_decision_gate_audit_status"] for row in rows}
        == {"SCORING_HANDOFF_DECISION_GATE_AUDIT_PASSED_CLOSED_DECISION_CONSISTENT"},
        "scoring handoff decision gate audit status mismatch",
    )
    require({row["audit_passed"] for row in rows} == {"true"}, "decision audit must pass")
    require({row["decision_result"] for row in rows} == {"handoff_closed"}, "audited decision must remain closed")
    require({row["acceptance_recorded"] for row in rows} == {"true"}, "acceptance must be recorded")
    for field in [
        "acceptance_allowed",
        "evidence_accepted",
        "receipt_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["audited_decision"] for row in rows} == {"handoff_closed"}, "audited decision mismatch")
    require(
        {row["audit_result"] for row in rows}
        == {"closed_decision_consistent_with_missing_acceptance_conditions"},
        "decision audit result mismatch",
    )
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "decision audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "decision audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "decision audit cannot allow verdicts")
    require(len(summary) == 1, "decision gate audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_DECISION_GATE_AUDIT_V01",
        "decision gate audit summary id mismatch",
    )
    require(row["evidence_object_receipt_scoring_handoff_decision_gate_audit_rows_declared"] == "7", "audit row count mismatch")
    require(row["audit_passed_rows"] == "7", "audit passed rows mismatch")
    require(row["closed_decision_rows"] == "7", "closed decision rows mismatch")
    require(row["open_decision_rows"] == "0", "open decision rows must be zero")
    require(row["acceptance_recorded_rows"] == "7", "acceptance recorded rows mismatch")
    for field in [
        "acceptance_allowed_rows",
        "evidence_accepted_rows",
        "receipt_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_handoff_to_scoring_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_satisfied"]
        == "true",
        "handoff decision gate audit must be satisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_DECISION_GATE_AUDIT_PASSED_CLOSED_DECISION_CONSISTENT",
        "decision gate audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_v01",
        "decision gate audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_summary_v01.csv"
    )
    require(len(rows) == 7, "scoring handoff acceptance record must have seven rows")
    require(
        {row["scoring_handoff_acceptance_record_status"] for row in rows}
        == {"SCORING_HANDOFF_ACCEPTANCE_RECORD_PASSED_CLOSED_HANDOFF_RECORDED"},
        "scoring handoff acceptance record status mismatch",
    )
    require({row["record_passed"] for row in rows} == {"true"}, "record must pass")
    require({row["decision_audit_passed"] for row in rows} == {"true"}, "decision audit must pass")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "recorded decision must be closed")
    require({row["record_result"] for row in rows} == {"closed_handoff_recorded"}, "record result mismatch")
    require({row["acceptance_recorded"] for row in rows} == {"true"}, "acceptance must be recorded")
    for field in [
        "acceptance_allowed",
        "evidence_accepted",
        "receipt_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "record cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "record cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "record cannot allow verdicts")
    require(len(summary) == 1, "scoring handoff acceptance record summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_ACCEPTANCE_RECORD_V01",
        "acceptance record summary id mismatch",
    )
    require(row["evidence_object_receipt_scoring_handoff_acceptance_record_rows_declared"] == "7", "record row count mismatch")
    require(row["record_passed_rows"] == "7", "record passed rows mismatch")
    require(row["decision_audit_passed_rows"] == "7", "decision audit passed rows mismatch")
    require(row["closed_handoff_record_rows"] == "7", "closed handoff record rows mismatch")
    require(row["open_handoff_record_rows"] == "0", "open handoff record rows must be zero")
    require(row["acceptance_recorded_rows"] == "7", "acceptance recorded rows mismatch")
    for field in [
        "acceptance_allowed_rows",
        "evidence_accepted_rows",
        "receipt_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_handoff_to_scoring_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_satisfied"]
        == "true",
        "scoring handoff acceptance record must be satisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_ACCEPTANCE_RECORD_PASSED_CLOSED_HANDOFF_RECORDED",
        "acceptance record status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_v01",
        "acceptance record next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "scoring handoff acceptance record audit must have seven rows")
    require(
        {row["scoring_handoff_acceptance_record_audit_status"] for row in rows}
        == {"SCORING_HANDOFF_ACCEPTANCE_RECORD_AUDIT_PASSED_CLOSED_HANDOFF_RECORD_CONSISTENT"},
        "scoring handoff acceptance record audit status mismatch",
    )
    require({row["audit_passed"] for row in rows} == {"true"}, "record audit must pass")
    require({row["record_passed"] for row in rows} == {"true"}, "record must pass")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "recorded decision must be closed")
    require({row["audited_record"] for row in rows} == {"closed_handoff_recorded"}, "audited record mismatch")
    require(
        {row["audit_result"] for row in rows}
        == {"closed_handoff_record_consistent_with_missing_acceptance_conditions"},
        "record audit result mismatch",
    )
    require({row["acceptance_recorded"] for row in rows} == {"true"}, "acceptance must be recorded")
    for field in [
        "acceptance_allowed",
        "evidence_accepted",
        "receipt_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "record audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "record audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "record audit cannot allow verdicts")
    require(len(summary) == 1, "scoring handoff acceptance record audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_ACCEPTANCE_RECORD_AUDIT_V01",
        "acceptance record audit summary id mismatch",
    )
    require(row["evidence_object_receipt_scoring_handoff_acceptance_record_audit_rows_declared"] == "7", "record audit row count mismatch")
    require(row["audit_passed_rows"] == "7", "audit passed rows mismatch")
    require(row["record_passed_rows"] == "7", "record passed rows mismatch")
    require(row["closed_handoff_record_rows"] == "7", "closed handoff record rows mismatch")
    require(row["open_handoff_record_rows"] == "0", "open handoff record rows must be zero")
    require(row["acceptance_recorded_rows"] == "7", "acceptance recorded rows mismatch")
    for field in [
        "acceptance_allowed_rows",
        "evidence_accepted_rows",
        "receipt_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_handoff_to_scoring_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_satisfied"]
        == "true",
        "scoring handoff acceptance record audit must be satisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_ACCEPTANCE_RECORD_AUDIT_PASSED_CLOSED_HANDOFF_RECORD_CONSISTENT",
        "acceptance record audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_v01",
        "acceptance record audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_summary_v01.csv"
    )
    require(len(rows) == 7, "final pre-score lock must have seven rows")
    require(
        {row["final_pre_score_lock_status"] for row in rows}
        == {"FINAL_PRE_SCORE_LOCK_PASSED_SCORING_STILL_BLOCKED"},
        "final pre-score lock status mismatch",
    )
    require({row["lock_result"] for row in rows} == {"pre_score_locked"}, "lock result mismatch")
    require({row["lock_passed"] for row in rows} == {"true"}, "lock must pass")
    require({row["acceptance_record_audit_passed"] for row in rows} == {"true"}, "acceptance record audit must pass")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "recorded decision must be closed")
    require({row["acceptance_recorded"] for row in rows} == {"true"}, "acceptance must be recorded")
    for field in [
        "acceptance_allowed",
        "evidence_accepted",
        "receipt_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "lock cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "lock cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "lock cannot allow verdicts")
    require(len(summary) == 1, "final pre-score lock summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_FINAL_PRE_SCORE_LOCK_V01",
        "final pre-score lock summary id mismatch",
    )
    require(row["evidence_object_receipt_scoring_handoff_final_pre_score_lock_rows_declared"] == "7", "lock row count mismatch")
    require(row["lock_passed_rows"] == "7", "lock passed rows mismatch")
    require(row["acceptance_record_audit_passed_rows"] == "7", "acceptance audit passed rows mismatch")
    require(row["closed_handoff_rows"] == "7", "closed handoff rows mismatch")
    require(row["open_handoff_rows"] == "0", "open handoff rows must be zero")
    require(row["acceptance_recorded_rows"] == "7", "acceptance recorded rows mismatch")
    for field in [
        "acceptance_allowed_rows",
        "evidence_accepted_rows",
        "receipt_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_handoff_to_scoring_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_satisfied"]
        == "true",
        "final pre-score lock must be satisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_FINAL_PRE_SCORE_LOCK_PASSED_SCORING_STILL_BLOCKED",
        "final pre-score lock status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_v01",
        "final pre-score lock next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "final pre-score lock audit must have seven rows")
    require(
        {row["final_pre_score_lock_audit_status"] for row in rows}
        == {"FINAL_PRE_SCORE_LOCK_AUDIT_PASSED_SCORING_STILL_BLOCKED"},
        "final pre-score lock audit status mismatch",
    )
    require({row["audited_lock"] for row in rows} == {"pre_score_locked"}, "audited lock mismatch")
    require(
        {row["audit_result"] for row in rows}
        == {"pre_score_lock_consistent_with_missing_acceptance_conditions"},
        "final pre-score lock audit result mismatch",
    )
    require({row["audit_passed"] for row in rows} == {"true"}, "audit must pass")
    require({row["lock_passed"] for row in rows} == {"true"}, "lock must pass")
    require({row["lock_result"] for row in rows} == {"pre_score_locked"}, "lock result mismatch")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "recorded decision must be closed")
    require({row["acceptance_recorded"] for row in rows} == {"true"}, "acceptance must be recorded")
    for field in [
        "acceptance_allowed",
        "evidence_accepted",
        "receipt_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "audit cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "audit cannot allow verdicts")
    require(len(summary) == 1, "final pre-score lock audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_FINAL_PRE_SCORE_LOCK_AUDIT_V01",
        "final pre-score lock audit summary id mismatch",
    )
    require(
        row["evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_rows_declared"] == "7",
        "audit row count mismatch",
    )
    require(row["audit_passed_rows"] == "7", "audit passed rows mismatch")
    require(row["lock_passed_rows"] == "7", "lock passed rows mismatch")
    require(row["pre_score_locked_rows"] == "7", "locked rows mismatch")
    require(row["scoring_unlocked_rows"] == "0", "unlocked rows must be zero")
    require(row["closed_handoff_rows"] == "7", "closed handoff rows mismatch")
    require(row["open_handoff_rows"] == "0", "open handoff rows must be zero")
    require(row["acceptance_recorded_rows"] == "7", "acceptance recorded rows mismatch")
    for field in [
        "acceptance_allowed_rows",
        "evidence_accepted_rows",
        "receipt_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_handoff_to_scoring_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_satisfied"]
        == "true",
        "final pre-score lock audit must be satisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_FINAL_PRE_SCORE_LOCK_AUDIT_PASSED_SCORING_STILL_BLOCKED",
        "final pre-score lock audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_v01",
        "final pre-score lock audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_summary_v01.csv"
    )
    require(len(rows) == 7, "score attempt blocker certificate must have seven rows")
    require(
        {row["score_attempt_blocker_certificate_status"] for row in rows}
        == {"SCORE_ATTEMPT_BLOCKER_CERTIFICATE_PASSED_SCORING_STILL_BLOCKED"},
        "score attempt blocker certificate status mismatch",
    )
    require(
        {row["certified_blocker"] for row in rows}
        == {"score_attempt_blocked_by_missing_acceptance_conditions"},
        "certified blocker mismatch",
    )
    require({row["certificate_passed"] for row in rows} == {"true"}, "certificate must pass")
    require(
        {row["final_pre_score_lock_audit_passed"] for row in rows} == {"true"},
        "final pre-score lock audit must pass",
    )
    require({row["lock_result"] for row in rows} == {"pre_score_locked"}, "lock result mismatch")
    require({row["score_attempt_allowed"] for row in rows} == {"false"}, "score attempt cannot be allowed")
    require({row["score_attempt_blocked"] for row in rows} == {"true"}, "score attempt must be blocked")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "recorded decision must be closed")
    require({row["acceptance_recorded"] for row in rows} == {"true"}, "acceptance must be recorded")
    for field in [
        "acceptance_allowed",
        "evidence_accepted",
        "receipt_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "input_certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["hard_failure_triggered"] == "true" for row in rows) == 0, "certificate cannot trigger failures")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "certificate cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "certificate cannot allow verdicts")
    require(len(summary) == 1, "score attempt blocker certificate summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_SCORE_ATTEMPT_BLOCKER_CERTIFICATE_V01",
        "score attempt blocker certificate summary id mismatch",
    )
    require(
        row["evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_rows_declared"] == "7",
        "certificate row count mismatch",
    )
    require(row["certificate_passed_rows"] == "7", "certificate passed rows mismatch")
    require(row["final_pre_score_lock_audit_passed_rows"] == "7", "lock audit passed rows mismatch")
    require(row["pre_score_locked_rows"] == "7", "locked rows mismatch")
    require(row["score_attempt_allowed_rows"] == "0", "score attempts allowed must be zero")
    require(row["score_attempt_blocked_rows"] == "7", "score attempts blocked mismatch")
    require(row["closed_handoff_rows"] == "7", "closed handoff rows mismatch")
    require(row["open_handoff_rows"] == "0", "open handoff rows must be zero")
    require(row["acceptance_recorded_rows"] == "7", "acceptance recorded rows mismatch")
    for field in [
        "acceptance_allowed_rows",
        "evidence_accepted_rows",
        "receipt_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_handoff_to_scoring_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "input_certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
        "hard_failures_triggered",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(
        row["evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_satisfied"]
        == "true",
        "score attempt blocker certificate must be satisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_SCORE_ATTEMPT_BLOCKER_CERTIFICATE_PASSED_SCORING_STILL_BLOCKED",
        "score attempt blocker certificate status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01",
        "score attempt blocker certificate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_summary_v01.csv"
    )
    require(len(rows) == 7, "score attempt unblock conditions must have seven rows")
    require(
        {row["score_attempt_unblock_condition_status"] for row in rows}
        == {"SCORE_ATTEMPT_UNBLOCK_CONDITION_DECLARED_NOT_SATISFIED"},
        "score attempt unblock condition status mismatch",
    )
    require({row["condition_required"] for row in rows} == {"true"}, "all unblock conditions must be required")
    require({row["condition_satisfied"] for row in rows} == {"false"}, "no unblock condition can be satisfied")
    require({row["condition_gap"] for row in rows} == {"missing_accepted_record"}, "condition gap mismatch")
    require({row["score_attempt_allowed_if_satisfied"] for row in rows} == {"true"}, "unblock implication mismatch")
    require({row["score_attempt_allowed_now"] for row in rows} == {"false"}, "score attempt cannot be allowed now")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must be blocked now")
    require({row["blocker_certificate_passed"] for row in rows} == {"true"}, "blocker certificate must pass")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "recorded decision must be closed")
    for field in [
        "acceptance_allowed",
        "evidence_accepted",
        "receipt_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "input_certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "conditions cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "conditions cannot allow verdicts")
    require(len(summary) == 1, "score attempt unblock conditions summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_SCORE_ATTEMPT_UNBLOCK_CONDITIONS_V01",
        "score attempt unblock conditions summary id mismatch",
    )
    require(row["score_attempt_unblock_condition_rows_declared"] == "7", "condition row count mismatch")
    require(row["condition_required_rows"] == "7", "required condition count mismatch")
    require(row["condition_satisfied_rows"] == "0", "satisfied condition count must be zero")
    require(row["condition_gap_rows"] == "7", "condition gap count mismatch")
    require(row["score_attempt_allowed_if_satisfied_rows"] == "7", "conditional allow count mismatch")
    require(row["score_attempt_allowed_now_rows"] == "0", "score attempts allowed now must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["blocker_certificate_passed_rows"] == "7", "blocker certificate count mismatch")
    for field in [
        "open_handoff_rows",
        "acceptance_allowed_rows",
        "evidence_accepted_rows",
        "receipt_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "input_certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_unblock_conditions_satisfied"] == "false", "unblock conditions cannot be satisfied")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "SCORE_ATTEMPT_UNBLOCK_CONDITIONS_DECLARED_SCORING_STILL_BLOCKED",
        "score attempt unblock conditions status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_v01",
        "score attempt unblock conditions next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_summary_v01.csv"
    )
    require(len(rows) == 7, "unblock condition evidence request must have seven rows")
    require(
        {row["evidence_request_status"] for row in rows}
        == {"UNBLOCK_CONDITION_EVIDENCE_REQUEST_OPEN_SCORING_STILL_BLOCKED"},
        "unblock condition evidence request status mismatch",
    )
    require({row["request_open"] for row in rows} == {"true"}, "requests must be open")
    require({row["evidence_requested"] for row in rows} == {"true"}, "evidence must be requested")
    require({row["evidence_received"] for row in rows} == {"false"}, "evidence cannot be received")
    require({row["evidence_accepted"] for row in rows} == {"false"}, "evidence cannot be accepted")
    require({row["condition_satisfied"] for row in rows} == {"false"}, "conditions cannot be satisfied")
    require({row["score_attempt_allowed_now"] for row in rows} == {"false"}, "score attempt cannot be allowed")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must be blocked")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "handoff must remain closed")
    for field in [
        "acceptance_allowed",
        "receipt_accepted",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "input_certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "request cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "request cannot allow verdicts")
    require(len(summary) == 1, "unblock condition evidence request summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_REQUEST_V01",
        "unblock condition evidence request summary id mismatch",
    )
    require(row["unblock_condition_evidence_request_rows_declared"] == "7", "request row count mismatch")
    require(row["request_open_rows"] == "7", "open request count mismatch")
    require(row["evidence_requested_rows"] == "7", "requested evidence count mismatch")
    for field in [
        "evidence_received_rows",
        "evidence_accepted_rows",
        "condition_satisfied_rows",
        "score_attempt_allowed_now_rows",
        "open_handoff_rows",
        "acceptance_allowed_rows",
        "receipt_accepted_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "input_certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["unblock_condition_evidence_request_satisfied"] == "true", "evidence request must be satisfied")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "UNBLOCK_CONDITION_EVIDENCE_REQUEST_OPEN_SCORING_STILL_BLOCKED",
        "unblock condition evidence request status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_v01",
        "unblock condition evidence request next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_summary_v01.csv"
    )
    require(len(rows) == 7, "unblock condition evidence receipt candidate must have seven rows")
    require(
        {row["receipt_candidate_status"] for row in rows}
        == {"UNBLOCK_CONDITION_EVIDENCE_RECEIPT_CANDIDATE_PREPARED_SCORING_STILL_BLOCKED"},
        "unblock condition evidence receipt candidate status mismatch",
    )
    require({row["request_open"] for row in rows} == {"true"}, "requests must be open")
    require({row["evidence_requested"] for row in rows} == {"true"}, "evidence must be requested")
    require({row["receipt_candidate_prepared"] for row in rows} == {"true"}, "receipt candidates must be prepared")
    require({row["evidence_received"] for row in rows} == {"false"}, "evidence cannot be received")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipts cannot be accepted")
    require({row["evidence_accepted"] for row in rows} == {"false"}, "evidence cannot be accepted")
    require({row["condition_satisfied"] for row in rows} == {"false"}, "conditions cannot be satisfied")
    require({row["score_attempt_allowed_now"] for row in rows} == {"false"}, "score attempt cannot be allowed")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must be blocked")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "handoff must remain closed")
    for field in [
        "acceptance_allowed",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "input_certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "candidate cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "candidate cannot allow verdicts")
    require(len(summary) == 1, "unblock condition evidence receipt candidate summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_CANDIDATE_V01",
        "unblock condition evidence receipt candidate summary id mismatch",
    )
    require(row["unblock_condition_evidence_receipt_candidate_rows_declared"] == "7", "receipt candidate row count mismatch")
    require(row["request_open_rows"] == "7", "open request count mismatch")
    require(row["evidence_requested_rows"] == "7", "requested evidence count mismatch")
    require(row["receipt_candidate_prepared_rows"] == "7", "receipt candidate count mismatch")
    for field in [
        "evidence_received_rows",
        "receipt_accepted_rows",
        "evidence_accepted_rows",
        "condition_satisfied_rows",
        "score_attempt_allowed_now_rows",
        "open_handoff_rows",
        "acceptance_allowed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "input_certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(
        row["unblock_condition_evidence_receipt_candidate_satisfied"] == "true",
        "receipt candidate must be satisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_CANDIDATE_PREPARED_SCORING_STILL_BLOCKED",
        "unblock condition evidence receipt candidate status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_v01",
        "unblock condition evidence receipt candidate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "unblock condition evidence receipt candidate audit must have seven rows")
    require(
        {row["receipt_candidate_audit_status"] for row in rows}
        == {"UNBLOCK_CONDITION_EVIDENCE_RECEIPT_CANDIDATE_AUDIT_PASSED_SCORING_STILL_BLOCKED"},
        "unblock condition evidence receipt candidate audit status mismatch",
    )
    require(
        {row["audit_result"] for row in rows}
        == {"receipt_candidate_consistent_with_no_received_or_accepted_evidence"},
        "unblock condition evidence receipt candidate audit result mismatch",
    )
    require({row["audit_passed"] for row in rows} == {"true"}, "receipt candidate audit must pass")
    require({row["request_open"] for row in rows} == {"true"}, "requests must remain open")
    require({row["evidence_requested"] for row in rows} == {"true"}, "evidence must remain requested")
    require({row["receipt_candidate_prepared"] for row in rows} == {"true"}, "receipt candidates must remain prepared")
    require({row["evidence_received"] for row in rows} == {"false"}, "evidence cannot be received")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipts cannot be accepted")
    require({row["evidence_accepted"] for row in rows} == {"false"}, "evidence cannot be accepted")
    require({row["condition_satisfied"] for row in rows} == {"false"}, "conditions cannot be satisfied")
    require({row["score_attempt_allowed_now"] for row in rows} == {"false"}, "score attempt cannot be allowed")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must be blocked")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "handoff must remain closed")
    for field in [
        "acceptance_allowed",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "input_certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "audit cannot allow verdicts")
    require(len(summary) == 1, "unblock condition evidence receipt candidate audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_CANDIDATE_AUDIT_V01",
        "unblock condition evidence receipt candidate audit summary id mismatch",
    )
    require(row["unblock_condition_evidence_receipt_candidate_audit_rows_declared"] == "7", "audit row count mismatch")
    require(row["audit_passed_rows"] == "7", "audit pass count mismatch")
    require(row["request_open_rows"] == "7", "open request count mismatch")
    require(row["evidence_requested_rows"] == "7", "requested evidence count mismatch")
    require(row["receipt_candidate_prepared_rows"] == "7", "receipt candidate count mismatch")
    for field in [
        "evidence_received_rows",
        "receipt_accepted_rows",
        "evidence_accepted_rows",
        "condition_satisfied_rows",
        "score_attempt_allowed_now_rows",
        "open_handoff_rows",
        "acceptance_allowed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "input_certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(
        row["unblock_condition_evidence_receipt_candidate_audit_satisfied"] == "true",
        "receipt candidate audit must be satisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_CANDIDATE_AUDIT_PASSED_SCORING_STILL_BLOCKED",
        "unblock condition evidence receipt candidate audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_v01",
        "unblock condition evidence receipt candidate audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_summary_v01.csv"
    )
    require(len(rows) == 7, "unblock condition evidence receipt remediation plan must have seven rows")
    require(
        {row["remediation_status"] for row in rows}
        == {"UNBLOCK_CONDITION_EVIDENCE_RECEIPT_REMEDIATION_DECLARED_NOT_COMPLETED"},
        "unblock condition evidence receipt remediation status mismatch",
    )
    require({row["request_open"] for row in rows} == {"true"}, "requests must remain open")
    require({row["evidence_requested"] for row in rows} == {"true"}, "evidence must remain requested")
    require({row["receipt_candidate_prepared"] for row in rows} == {"true"}, "receipt candidates must remain prepared")
    require({row["receipt_candidate_audited"] for row in rows} == {"true"}, "receipt candidates must remain audited")
    require({row["receipt_candidate_audit_passed"] for row in rows} == {"true"}, "receipt candidate audit must pass")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["evidence_received"] for row in rows} == {"false"}, "evidence cannot be received")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipts cannot be accepted")
    require({row["evidence_accepted"] for row in rows} == {"false"}, "evidence cannot be accepted")
    require({row["condition_satisfied"] for row in rows} == {"false"}, "conditions cannot be satisfied")
    require({row["score_attempt_allowed_now"] for row in rows} == {"false"}, "score attempt cannot be allowed")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must be blocked")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "handoff must remain closed")
    for field in [
        "acceptance_allowed",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "input_certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "plan cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "plan cannot allow verdicts")
    require(len(summary) == 1, "unblock condition evidence receipt remediation plan summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_REMEDIATION_PLAN_V01",
        "unblock condition evidence receipt remediation plan summary id mismatch",
    )
    require(row["unblock_condition_evidence_receipt_remediation_rows_declared"] == "7", "remediation row count mismatch")
    require(row["request_open_rows"] == "7", "open request count mismatch")
    require(row["evidence_requested_rows"] == "7", "requested evidence count mismatch")
    require(row["receipt_candidate_prepared_rows"] == "7", "receipt candidate count mismatch")
    require(row["receipt_candidate_audited_rows"] == "7", "receipt candidate audited count mismatch")
    require(row["receipt_candidate_audit_passed_rows"] == "7", "receipt candidate audit passed count mismatch")
    for field in [
        "remediation_completed_rows",
        "evidence_received_rows",
        "receipt_accepted_rows",
        "evidence_accepted_rows",
        "condition_satisfied_rows",
        "score_attempt_allowed_now_rows",
        "open_handoff_rows",
        "acceptance_allowed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "input_certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(
        row["unblock_condition_evidence_receipt_remediation_plan_satisfied"] == "false",
        "receipt remediation plan must remain unsatisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_REMEDIATION_DECLARED_NOT_COMPLETED_SCORING_STILL_BLOCKED",
        "unblock condition evidence receipt remediation plan status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_v01",
        "unblock condition evidence receipt remediation plan next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_summary_v01.csv"
    )
    require(len(rows) == 7, "unblock condition evidence receipt materialization packet must have seven rows")
    require(
        {row["materialization_status"] for row in rows}
        == {"UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_PACKET_DECLARED_NO_EVIDENCE_MATERIALIZED"},
        "unblock condition evidence receipt materialization status mismatch",
    )
    for field in [
        "request_open",
        "evidence_requested",
        "receipt_candidate_prepared",
        "receipt_candidate_audited",
        "receipt_candidate_audit_passed",
        "remediation_declared",
        "packet_declared",
    ]:
        require({row[field] for row in rows} == {"true"}, f"{field} must remain true")
    require({row["remediation_completed"] for row in rows} == {"false"}, "remediation cannot be completed")
    require({row["evidence_materialized"] for row in rows} == {"false"}, "evidence cannot be materialized")
    require({row["evidence_received"] for row in rows} == {"false"}, "evidence cannot be received")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipts cannot be accepted")
    require({row["evidence_accepted"] for row in rows} == {"false"}, "evidence cannot be accepted")
    require({row["condition_satisfied"] for row in rows} == {"false"}, "conditions cannot be satisfied")
    require({row["score_attempt_allowed_now"] for row in rows} == {"false"}, "score attempt cannot be allowed")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must be blocked")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "handoff must remain closed")
    for field in [
        "acceptance_allowed",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "input_certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "packet cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "packet cannot allow verdicts")
    require(len(summary) == 1, "unblock condition evidence receipt materialization packet summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_PACKET_V01",
        "unblock condition evidence receipt materialization packet summary id mismatch",
    )
    require(row["unblock_condition_evidence_receipt_materialization_packet_rows_declared"] == "7", "packet row count mismatch")
    require(row["request_open_rows"] == "7", "open request count mismatch")
    require(row["evidence_requested_rows"] == "7", "requested evidence count mismatch")
    require(row["receipt_candidate_prepared_rows"] == "7", "receipt candidate count mismatch")
    require(row["receipt_candidate_audited_rows"] == "7", "receipt candidate audited count mismatch")
    require(row["receipt_candidate_audit_passed_rows"] == "7", "receipt candidate audit passed count mismatch")
    require(row["remediation_declared_rows"] == "7", "remediation declared count mismatch")
    require(row["packet_declared_rows"] == "7", "packet declared count mismatch")
    for field in [
        "remediation_completed_rows",
        "evidence_materialized_rows",
        "evidence_received_rows",
        "receipt_accepted_rows",
        "evidence_accepted_rows",
        "condition_satisfied_rows",
        "score_attempt_allowed_now_rows",
        "open_handoff_rows",
        "acceptance_allowed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "input_certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(
        row["unblock_condition_evidence_receipt_materialization_packet_satisfied"] == "false",
        "receipt materialization packet must remain unsatisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_PACKET_DECLARED_NO_EVIDENCE_MATERIALIZED_SCORING_STILL_BLOCKED",
        "unblock condition evidence receipt materialization packet status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01",
        "unblock condition evidence receipt materialization packet next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "unblock condition evidence receipt materialization audit must have seven rows")
    require(
        {row["materialization_audit_status"] for row in rows}
        == {"UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_AUDIT_FAILED_NO_EVIDENCE_MATERIALIZED"},
        "unblock condition evidence receipt materialization audit status mismatch",
    )
    for field in [
        "request_open",
        "evidence_requested",
        "receipt_candidate_prepared",
        "receipt_candidate_audited",
        "receipt_candidate_audit_passed",
        "remediation_declared",
        "packet_declared",
        "packet_audited",
    ]:
        require({row[field] for row in rows} == {"true"}, f"{field} must remain true")
    require({row["materialization_audit_passed"] for row in rows} == {"false"}, "materialization audit cannot pass")
    require({row["evidence_materialized"] for row in rows} == {"false"}, "evidence cannot be materialized")
    require({row["evidence_received"] for row in rows} == {"false"}, "evidence cannot be received")
    require({row["receipt_accepted"] for row in rows} == {"false"}, "receipts cannot be accepted")
    require({row["evidence_accepted"] for row in rows} == {"false"}, "evidence cannot be accepted")
    require({row["condition_satisfied"] for row in rows} == {"false"}, "conditions cannot be satisfied")
    require({row["score_attempt_allowed_now"] for row in rows} == {"false"}, "score attempt cannot be allowed")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must be blocked")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "handoff must remain closed")
    for field in [
        "acceptance_allowed",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "input_certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "audit cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "audit cannot allow verdicts")
    require(len(summary) == 1, "unblock condition evidence receipt materialization audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_AUDIT_V01",
        "unblock condition evidence receipt materialization audit summary id mismatch",
    )
    require(row["unblock_condition_evidence_receipt_materialization_audit_rows_declared"] == "7", "audit row count mismatch")
    require(row["request_open_rows"] == "7", "open request count mismatch")
    require(row["evidence_requested_rows"] == "7", "requested evidence count mismatch")
    require(row["receipt_candidate_prepared_rows"] == "7", "receipt candidate count mismatch")
    require(row["receipt_candidate_audited_rows"] == "7", "receipt candidate audited count mismatch")
    require(row["receipt_candidate_audit_passed_rows"] == "7", "receipt candidate audit passed count mismatch")
    require(row["remediation_declared_rows"] == "7", "remediation declared count mismatch")
    require(row["packet_declared_rows"] == "7", "packet declared count mismatch")
    require(row["packet_audited_rows"] == "7", "packet audited count mismatch")
    for field in [
        "materialization_audit_passed_rows",
        "evidence_materialized_rows",
        "evidence_received_rows",
        "receipt_accepted_rows",
        "evidence_accepted_rows",
        "condition_satisfied_rows",
        "score_attempt_allowed_now_rows",
        "open_handoff_rows",
        "acceptance_allowed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "input_certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(
        row["unblock_condition_evidence_receipt_materialization_audit_satisfied"] == "false",
        "receipt materialization audit must remain unsatisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_AUDIT_FAILED_NO_EVIDENCE_MATERIALIZED_SCORING_STILL_BLOCKED",
        "unblock condition evidence receipt materialization audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01",
        "unblock condition evidence receipt materialization audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_summary_v01.csv"
    )
    require(len(rows) == 7, "unblock condition evidence receipt acceptance precheck must have seven rows")
    require(
        {row["acceptance_precheck_status"] for row in rows}
        == {"UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_PASSED"},
        "unblock condition evidence receipt acceptance precheck status mismatch",
    )
    for field in [
        "materialization_audit_passed",
        "evidence_materialized",
        "evidence_received",
        "receipt_accepted",
        "evidence_accepted",
        "acceptance_precheck_passed",
        "condition_satisfied",
        "score_attempt_allowed_now",
        "acceptance_allowed",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "input_certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "handoff must remain closed")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(all(row["allows_tau_response_claim"] == "false" for row in rows), "precheck cannot allow Tau claims")
    require(all(row["allows_dark_sector_verdict"] == "false" for row in rows), "precheck cannot allow verdicts")
    require(len(summary) == 1, "unblock condition evidence receipt acceptance precheck summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_PRECHECK_V01",
        "unblock condition evidence receipt acceptance precheck summary id mismatch",
    )
    require(row["unblock_condition_evidence_receipt_acceptance_precheck_rows_declared"] == "7", "precheck row count mismatch")
    for field in [
        "materialization_audit_passed_rows",
        "evidence_materialized_rows",
        "evidence_received_rows",
        "receipt_accepted_rows",
        "evidence_accepted_rows",
        "acceptance_precheck_passed_rows",
        "condition_satisfied_rows",
        "score_attempt_allowed_now_rows",
        "open_handoff_rows",
        "acceptance_allowed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "input_certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(
        row["unblock_condition_evidence_receipt_acceptance_precheck_satisfied"] == "false",
        "receipt acceptance precheck must remain unsatisfied",
    )
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_PASSED_SCORING_STILL_BLOCKED",
        "unblock condition evidence receipt acceptance precheck status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_v01",
        "unblock condition evidence receipt acceptance precheck next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_summary_v01.csv"
    )
    require(len(rows) == 7, "unblock condition evidence receipt acceptance unblock plan must have seven rows")
    require(
        {row["unblock_plan_status"] for row in rows}
        == {"UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED"},
        "unblock condition evidence receipt acceptance unblock plan status mismatch",
    )
    for field in [
        "materialization_audit_required",
        "receipt_acceptance_required",
        "evidence_acceptance_required",
        "handoff_open_required",
    ]:
        require({row[field] for row in rows} == {"true"}, f"{field} must be required")
    for field in [
        "materialization_audit_passed",
        "evidence_materialized",
        "evidence_received",
        "receipt_accepted",
        "evidence_accepted",
        "acceptance_precheck_passed",
        "unblock_completed",
        "condition_satisfied",
        "score_attempt_allowed_now",
        "acceptance_allowed",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "input_certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "handoff must remain closed")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(len(summary) == 1, "unblock condition evidence receipt acceptance unblock plan summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_V01",
        "unblock condition evidence receipt acceptance unblock plan summary id mismatch",
    )
    require(row["unblock_condition_evidence_receipt_acceptance_unblock_plan_rows_declared"] == "7", "plan row count mismatch")
    for field in [
        "materialization_audit_required_rows",
        "receipt_acceptance_required_rows",
        "evidence_acceptance_required_rows",
        "handoff_open_required_rows",
    ]:
        require(row[field] == "7", f"{field} must be seven")
    for field in [
        "materialization_audit_passed_rows",
        "evidence_materialized_rows",
        "evidence_received_rows",
        "receipt_accepted_rows",
        "evidence_accepted_rows",
        "acceptance_precheck_passed_rows",
        "unblock_completed_rows",
        "condition_satisfied_rows",
        "score_attempt_allowed_now_rows",
        "open_handoff_rows",
        "acceptance_allowed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "input_certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["unblock_condition_evidence_receipt_acceptance_unblock_plan_satisfied"] == "false", "plan must be unsatisfied")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED_SCORING_STILL_BLOCKED",
        "unblock condition evidence receipt acceptance unblock plan status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_v01",
        "unblock condition evidence receipt acceptance unblock plan next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "unblock condition evidence receipt acceptance unblock plan audit must have seven rows")
    require(
        {row["unblock_plan_audit_status"] for row in rows}
        == {"UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_AUDITED_NOT_COMPLETED"},
        "unblock condition evidence receipt acceptance unblock plan audit status mismatch",
    )
    require({row["unblock_plan_audited"] for row in rows} == {"true"}, "unblock plan must be audited")
    require({row["unblock_plan_audit_passed"] for row in rows} == {"false"}, "unblock plan audit cannot pass")
    for field in [
        "materialization_audit_passed",
        "evidence_materialized",
        "evidence_received",
        "receipt_accepted",
        "evidence_accepted",
        "acceptance_precheck_passed",
        "unblock_completed",
        "condition_satisfied",
        "score_attempt_allowed_now",
        "acceptance_allowed",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_handoff_to_scoring",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "input_certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "handoff must remain closed")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(len(summary) == 1, "unblock condition evidence receipt acceptance unblock plan audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_AUDIT_V01",
        "unblock condition evidence receipt acceptance unblock plan audit summary id mismatch",
    )
    require(row["unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_rows_declared"] == "7", "audit row count mismatch")
    require(row["unblock_plan_audited_rows"] == "7", "audited row count mismatch")
    for field in [
        "unblock_plan_audit_passed_rows",
        "materialization_audit_passed_rows",
        "evidence_materialized_rows",
        "evidence_received_rows",
        "receipt_accepted_rows",
        "evidence_accepted_rows",
        "acceptance_precheck_passed_rows",
        "unblock_completed_rows",
        "condition_satisfied_rows",
        "score_attempt_allowed_now_rows",
        "open_handoff_rows",
        "acceptance_allowed_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "handoff_unblocked_rows",
        "can_execute_rows",
        "execution_attempted_rows",
        "execution_succeeded_rows",
        "evidence_package_passed_rows",
        "input_certificate_passed_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_satisfied"] == "false", "audit must be unsatisfied")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_AUDITED_NOT_COMPLETED_SCORING_STILL_BLOCKED",
        "unblock condition evidence receipt acceptance unblock plan audit status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_v01",
        "unblock condition evidence receipt acceptance unblock plan audit next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_summary_v01.csv"
    )
    require(len(rows) == 7, "unblock condition evidence receipt acceptance decision gate must have seven rows")
    require(
        {row["decision_gate_status"] for row in rows}
        == {"ACCEPTANCE_DECISION_GATE_CLOSED_UNBLOCK_PLAN_AUDIT_NOT_PASSED"},
        "decision gate status mismatch",
    )
    require({row["decision_output"] for row in rows} == {"acceptance_closed"}, "decision gate must be closed")
    for field in [
        "unblock_plan_audit_passed",
        "receipt_accepted",
        "evidence_accepted",
        "score_attempt_allowed_now",
        "acceptance_allowed",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "input_certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "handoff must remain closed")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(len(summary) == 1, "decision gate summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_DECISION_GATE_V01",
        "decision gate summary id mismatch",
    )
    require(row["unblock_condition_evidence_receipt_acceptance_decision_gate_rows_declared"] == "7", "decision gate row count mismatch")
    require(row["decision_gate_closed_rows"] == "7", "closed decision gate count mismatch")
    require(row["unblock_plan_audit_passed_rows"] == "0", "unblock plan audit cannot pass")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["unblock_condition_evidence_receipt_acceptance_decision_gate_satisfied"] == "false", "decision gate must remain unsatisfied")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_DECISION_GATE_CLOSED_SCORING_STILL_BLOCKED",
        "decision gate status mismatch",
    )
    require(
        row["next_required_artifact"]
        == "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit_v01",
        "decision gate next artifact mismatch",
    )


def validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit_summary_v01.csv"
    )
    require(len(rows) == 7, "unblock condition evidence receipt acceptance decision gate audit must have seven rows")
    require(
        {row["decision_gate_audit_status"] for row in rows}
        == {"ACCEPTANCE_DECISION_GATE_AUDITED_CLOSED_SCORING_BLOCKED"},
        "decision gate audit status mismatch",
    )
    require({row["decision_gate_audited"] for row in rows} == {"true"}, "decision gate must be audited")
    require({row["decision_gate_audit_passed"] for row in rows} == {"true"}, "closed decision gate audit must pass")
    require({row["decision_output"] for row in rows} == {"acceptance_closed"}, "audited decision gate must remain closed")
    for field in [
        "unblock_plan_audit_passed",
        "receipt_accepted",
        "evidence_accepted",
        "score_attempt_allowed_now",
        "acceptance_allowed",
        "payload_accepted",
        "scoring_input_accepted",
        "handoff_unblocked",
        "can_execute",
        "execution_attempted",
        "execution_succeeded",
        "evidence_package_passed",
        "input_certificate_passed",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require({row["recorded_decision"] for row in rows} == {"handoff_closed"}, "handoff must remain closed")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(len(summary) == 1, "decision gate audit summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_DECISION_GATE_AUDIT_V01",
        "decision gate audit summary id mismatch",
    )
    require(row["unblock_condition_evidence_receipt_acceptance_decision_gate_audit_rows_declared"] == "7", "audit row count mismatch")
    require(row["decision_gate_audited_rows"] == "7", "audited row count mismatch")
    require(row["decision_gate_audit_passed_rows"] == "7", "audit pass count mismatch")
    require(row["decision_gate_closed_rows"] == "7", "closed gate count mismatch")
    require(row["unblock_plan_audit_passed_rows"] == "0", "unblock plan audit cannot pass")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["scores_computed_rows"] == "0", "scores cannot be computed")
    require(row["cmb_likelihood_available_rows"] == "0", "likelihood cannot be available")
    require(row["unblock_condition_evidence_receipt_acceptance_decision_gate_audit_satisfied"] == "true", "closed decision gate audit must pass")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_DECISION_GATE_AUDITED_CLOSED_SCORING_STILL_BLOCKED",
        "decision gate audit status mismatch",
    )


def validate_tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_summary_v01.csv"
    )
    require(len(rows) == 7, "acceptance evidence fulfillment package must have seven rows")
    require(
        {row["fulfillment_status"] for row in rows}
        == {"ACCEPTANCE_EVIDENCE_FULFILLMENT_PACKAGE_DECLARED_NOT_MATERIALIZED"},
        "fulfillment package status mismatch",
    )
    require({row["requirements_declared"] for row in rows} == {"true"}, "requirements must be declared")
    require({row["required_material_count"] for row in rows} == {"7"}, "each row must require seven materials")
    for field in [
        "evidence_materialized",
        "hash_manifest_present",
        "provenance_record_present",
        "replay_record_present",
        "firewall_record_present",
        "acceptance_record_present",
        "scoring_handoff_record_present",
        "receipt_accepted",
        "evidence_accepted",
        "decision_gate_reopen_allowed",
        "score_attempt_allowed_now",
        "payload_accepted",
        "scoring_input_accepted",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(len(summary) == 1, "fulfillment package summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_FULFILLMENT_PACKAGE_V01", "summary id mismatch")
    require(row["acceptance_evidence_fulfillment_package_rows_declared"] == "7", "row count mismatch")
    require(row["requirements_declared_rows"] == "7", "declared requirement count mismatch")
    require(row["required_material_count_total"] == "49", "required material count mismatch")
    for field in [
        "evidence_materialized_rows",
        "hash_manifest_present_rows",
        "provenance_record_present_rows",
        "replay_record_present_rows",
        "firewall_record_present_rows",
        "acceptance_record_present_rows",
        "scoring_handoff_record_present_rows",
        "receipt_accepted_rows",
        "evidence_accepted_rows",
        "decision_gate_reopen_allowed_rows",
        "score_attempt_allowed_now_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["acceptance_evidence_fulfillment_package_satisfied"] == "false", "fulfillment package cannot be satisfied")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "ACCEPTANCE_EVIDENCE_FULFILLMENT_PACKAGE_DECLARED_NOT_MATERIALIZED_SCORING_STILL_BLOCKED",
        "fulfillment package status mismatch",
    )


def validate_tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_v01.csv")
    manifest = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_v01_manifest.csv"
    )
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_summary_v01.csv"
    )
    require(len(rows) == 7, "acceptance evidence materialization package must have seven rows")
    require(len(manifest) == 49, "acceptance evidence materialization manifest must have forty-nine rows")
    require(
        {row["materialization_status"] for row in rows}
        == {"ACCEPTANCE_EVIDENCE_MATERIALS_CREATED_HASHED_NOT_ACCEPTED"},
        "materialization package status mismatch",
    )
    for field in [
        "materialized_evidence_object_present",
        "hash_manifest_present",
        "provenance_record_present",
        "replay_record_present",
        "firewall_record_present",
        "acceptance_record_present",
        "scoring_handoff_record_present",
    ]:
        require({row[field] for row in rows} == {"true"}, f"{field} must be true")
    for field in [
        "receipt_accepted",
        "evidence_accepted",
        "decision_gate_reopen_allowed",
        "score_attempt_allowed_now",
        "payload_accepted",
        "scoring_input_accepted",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require({row["material_records_created"] for row in rows} == {"7"}, "each row must create seven records")
    require({row["material_records_hashed"] for row in rows} == {"7"}, "each row must hash seven records")
    require({row["material_present"] for row in manifest} == {"true"}, "all manifest materials must be present")
    require({row["endpoint_blind"] for row in manifest} == {"true"}, "all manifest rows must be endpoint-blind")
    for manifest_row in manifest:
        material_path = ROOT / manifest_row["material_path"]
        require(material_path.exists(), f"missing material path {material_path}")
        payload = material_path.read_bytes()
        require(hashlib.sha256(payload).hexdigest() == manifest_row["sha256"], "material hash mismatch")
        require(len(payload) == int(manifest_row["byte_size"]), "material byte-size mismatch")
    require(len(summary) == 1, "materialization package summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_MATERIALIZATION_PACKAGE_V01",
        "summary id mismatch",
    )
    require(row["acceptance_evidence_materialization_package_rows_declared"] == "7", "row count mismatch")
    require(row["material_records_required"] == "49", "required material count mismatch")
    require(row["material_records_created"] == "49", "created material count mismatch")
    require(row["material_records_hashed"] == "49", "hashed material count mismatch")
    for field in [
        "materialized_evidence_object_present_rows",
        "hash_manifest_present_rows",
        "provenance_record_present_rows",
        "replay_record_present_rows",
        "firewall_record_present_rows",
        "acceptance_record_present_rows",
        "scoring_handoff_record_present_rows",
    ]:
        require(row[field] == "7", f"{field} must be seven")
    for field in [
        "receipt_accepted_rows",
        "evidence_accepted_rows",
        "decision_gate_reopen_allowed_rows",
        "score_attempt_allowed_now_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["acceptance_evidence_materialization_package_satisfied"] == "false", "materialization package cannot be satisfied")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "ACCEPTANCE_EVIDENCE_MATERIALS_CREATED_HASHED_NOT_ACCEPTED_SCORING_STILL_BLOCKED",
        "materialization package status mismatch",
    )


def validate_tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_v01() -> None:
    rows = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_summary_v01.csv"
    )
    require(len(rows) == 7, "materialization audit acceptance precheck must have seven rows")
    require(
        {row["materialization_audit_status"] for row in rows}
        == {"MATERIALIZATION_AUDIT_PASSED_HASHED_ENDPOINT_BLIND_MATERIALS_PRESENT"},
        "materialization audit status mismatch",
    )
    require({row["materialization_audit_passed"] for row in rows} == {"true"}, "materialization audit must pass")
    require(
        {row["receipt_acceptance_precheck_passed"] for row in rows} == {"true"},
        "receipt acceptance precheck must pass",
    )
    require(
        {row["evidence_acceptance_precheck_passed"] for row in rows} == {"true"},
        "evidence acceptance precheck must pass",
    )
    require({row["material_records_expected"] for row in rows} == {"7"}, "expected seven material records per row")
    require({row["material_records_found"] for row in rows} == {"7"}, "must find seven material records per row")
    require({row["material_hashes_verified"] for row in rows} == {"7"}, "must verify seven material hashes per row")
    require({row["endpoint_blind_materials"] for row in rows} == {"true"}, "materials must be endpoint-blind")
    require({row["all_required_material_types_present"] for row in rows} == {"true"}, "all material types must be present")
    for field in [
        "receipt_accepted",
        "evidence_accepted",
        "decision_gate_reopen_allowed",
        "score_attempt_allowed_now",
        "payload_accepted",
        "scoring_input_accepted",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(len(summary) == 1, "materialization audit acceptance precheck summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_MATERIALIZATION_AUDIT_ACCEPTANCE_PRECHECK_V01",
        "summary id mismatch",
    )
    require(row["materialization_audit_acceptance_precheck_rows_declared"] == "7", "row count mismatch")
    require(row["materialization_audit_passed_rows"] == "7", "materialization audit pass count mismatch")
    require(row["receipt_acceptance_precheck_passed_rows"] == "7", "receipt precheck pass count mismatch")
    require(row["evidence_acceptance_precheck_passed_rows"] == "7", "evidence precheck pass count mismatch")
    require(row["material_records_expected_total"] == "49", "expected material total mismatch")
    require(row["material_records_found_total"] == "49", "found material total mismatch")
    require(row["material_hashes_verified_total"] == "49", "verified material hash total mismatch")
    require(row["endpoint_blind_material_rows"] == "7", "endpoint-blind material row count mismatch")
    require(row["all_required_material_types_present_rows"] == "7", "material type coverage count mismatch")
    for field in [
        "receipt_accepted_rows",
        "evidence_accepted_rows",
        "decision_gate_reopen_allowed_rows",
        "score_attempt_allowed_now_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["materialization_audit_acceptance_precheck_satisfied"] == "true", "precheck must be satisfied")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "MATERIALIZATION_AUDIT_AND_ACCEPTANCE_PRECHECK_PASSED_RECEIPTS_NOT_YET_ACCEPTED_SCORING_STILL_BLOCKED",
        "materialization audit acceptance precheck status mismatch",
    )


def validate_tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_v01() -> None:
    rows = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_summary_v01.csv"
    )
    require(len(rows) == 7, "receipt evidence acceptance reopen gate must have seven rows")
    require(
        {row["acceptance_status"] for row in rows}
        == {"RECEIPT_AND_EVIDENCE_ACCEPTED_DECISION_GATE_REOPEN_ALLOWED"},
        "receipt/evidence acceptance status mismatch",
    )
    for field in [
        "materialization_audit_passed",
        "receipt_acceptance_precheck_passed",
        "evidence_acceptance_precheck_passed",
        "endpoint_blind_materials",
        "all_required_material_types_present",
        "receipt_accepted",
        "evidence_accepted",
        "acceptance_record_created",
        "decision_gate_reopen_allowed",
    ]:
        require({row[field] for row in rows} == {"true"}, f"{field} must be true")
    require({row["material_records_expected"] for row in rows} == {"7"}, "expected seven material records per row")
    require({row["material_records_found"] for row in rows} == {"7"}, "must find seven material records per row")
    require({row["material_hashes_verified"] for row in rows} == {"7"}, "must verify seven material hashes per row")
    for field in [
        "score_attempt_allowed_now",
        "payload_accepted",
        "scoring_input_accepted",
        "scoring_handoff_opened",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(len(summary) == 1, "receipt evidence acceptance reopen gate summary must have one row")
    row = summary[0]
    require(
        row["summary_id"]
        == "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_RECEIPT_EVIDENCE_ACCEPTANCE_REOPEN_GATE_V01",
        "summary id mismatch",
    )
    require(row["receipt_evidence_acceptance_reopen_gate_rows_declared"] == "7", "row count mismatch")
    require(row["materialization_audit_passed_rows"] == "7", "materialization audit pass count mismatch")
    require(row["receipt_acceptance_precheck_passed_rows"] == "7", "receipt precheck pass count mismatch")
    require(row["evidence_acceptance_precheck_passed_rows"] == "7", "evidence precheck pass count mismatch")
    require(row["material_records_expected_total"] == "49", "expected material total mismatch")
    require(row["material_records_found_total"] == "49", "found material total mismatch")
    require(row["material_hashes_verified_total"] == "49", "verified material hash total mismatch")
    for field in [
        "endpoint_blind_material_rows",
        "all_required_material_types_present_rows",
        "receipt_accepted_rows",
        "evidence_accepted_rows",
        "acceptance_record_created_rows",
        "decision_gate_reopen_allowed_rows",
    ]:
        require(row[field] == "7", f"{field} must be seven")
    for field in [
        "score_attempt_allowed_now_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "scoring_handoff_opened_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["receipt_evidence_acceptance_reopen_gate_satisfied"] == "true", "reopen gate must be satisfied")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "RECEIPT_AND_EVIDENCE_ACCEPTED_DECISION_GATE_REOPEN_ALLOWED_SCORING_INPUT_STILL_BLOCKED",
        "receipt evidence acceptance reopen gate status mismatch",
    )


def validate_tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_v01() -> None:
    rows = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_v01.csv"
    )
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_summary_v01.csv"
    )
    require(len(rows) == 7, "scoring handoff package must have seven rows")
    require(
        {row["handoff_status"] for row in rows}
        == {"SCORING_HANDOFF_PACKAGE_OPENED_FROM_ACCEPTED_EVIDENCE"},
        "scoring handoff package status mismatch",
    )
    for field in [
        "receipt_accepted",
        "evidence_accepted",
        "acceptance_record_created",
        "decision_gate_reopen_allowed",
        "endpoint_blind_handoff",
        "scoring_handoff_package_created",
        "scoring_handoff_opened",
        "scoring_input_candidate_created",
    ]:
        require({row[field] for row in rows} == {"true"}, f"{field} must be true")
    for field in [
        "score_attempt_allowed_now",
        "payload_accepted",
        "scoring_input_accepted",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require({row["next_gate"] for row in rows} == {"scoring_input_acceptance_gate"}, "next gate mismatch")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(len(summary) == 1, "scoring handoff package summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_SCORING_HANDOFF_PACKAGE_V01",
        "summary id mismatch",
    )
    require(row["scoring_handoff_package_rows_declared"] == "7", "row count mismatch")
    for field in [
        "receipt_accepted_rows",
        "evidence_accepted_rows",
        "acceptance_record_created_rows",
        "decision_gate_reopen_allowed_rows",
        "endpoint_blind_handoff_rows",
        "scoring_handoff_package_created_rows",
        "scoring_handoff_opened_rows",
        "scoring_input_candidate_created_rows",
    ]:
        require(row[field] == "7", f"{field} must be seven")
    for field in [
        "score_attempt_allowed_now_rows",
        "payload_accepted_rows",
        "scoring_input_accepted_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["scoring_handoff_package_satisfied"] == "true", "scoring handoff package must be satisfied")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "SCORING_HANDOFF_PACKAGE_OPENED_FROM_ACCEPTED_EVIDENCE_SCORING_INPUT_STILL_BLOCKED",
        "scoring handoff package status mismatch",
    )


def validate_tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_v01() -> None:
    rows = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_summary_v01.csv"
    )
    require(len(rows) == 7, "scoring input decision package must have seven rows")
    require(
        {row["decision_status"] for row in rows}
        == {"SCORING_INPUT_DECISION_CLOSED_BY_EXPLICIT_NULL_RESPONSE"},
        "scoring input decision status mismatch",
    )
    for field in [
        "scoring_handoff_opened",
        "scoring_input_candidate_created",
        "scoring_input_acceptance_decision_closed",
        "explicit_null_response_routed",
    ]:
        require({row[field] for row in rows} == {"true"}, f"{field} must be true")
    for field in [
        "scoring_input_accepted",
        "score_ready_input_available",
        "score_attempt_allowed_now",
        "payload_accepted",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require(
        {row["next_gate"] for row in rows} == {"score_attempt_guard_or_wait_for_real_score_ready_input"},
        "next gate mismatch",
    )
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(len(summary) == 1, "scoring input decision package summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_SCORING_INPUT_DECISION_PACKAGE_V01",
        "summary id mismatch",
    )
    require(row["scoring_input_decision_package_rows_declared"] == "7", "row count mismatch")
    for field in [
        "scoring_handoff_opened_rows",
        "scoring_input_candidate_created_rows",
        "scoring_input_acceptance_decision_closed_rows",
        "explicit_null_response_routed_rows",
    ]:
        require(row[field] == "7", f"{field} must be seven")
    for field in [
        "scoring_input_accepted_rows",
        "score_ready_input_available_rows",
        "score_attempt_allowed_now_rows",
        "payload_accepted_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["scoring_input_decision_package_satisfied"] == "true", "scoring input decision package must pass")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "SCORING_INPUT_DECISION_CLOSED_BY_EXPLICIT_NULL_RESPONSE_SCORE_STILL_BLOCKED",
        "scoring input decision package status mismatch",
    )


def validate_tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_summary_v01.csv"
    )
    require(len(rows) == 7, "score attempt guard must have seven rows")
    require(
        {row["guard_status"] for row in rows}
        == {"SCORE_ATTEMPT_GUARD_EXECUTED_DENIED_NO_SCORE_READY_INPUT"},
        "score attempt guard status mismatch",
    )
    for field in [
        "score_attempt_guard_executed",
        "scoring_input_acceptance_decision_closed",
        "explicit_null_response_routed",
        "score_attempt_denied",
    ]:
        require({row[field] for row in rows} == {"true"}, f"{field} must be true")
    for field in [
        "score_ready_input_available",
        "scoring_input_accepted",
        "score_attempt_allowed_now",
        "payload_accepted",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require(
        {row["required_unblock_condition"] for row in rows}
        == {"supply_real_score_ready_input_with_accepted_scoring_input"},
        "required unblock condition mismatch",
    )
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(len(summary) == 1, "score attempt guard summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_SCORE_ATTEMPT_GUARD_V01",
        "summary id mismatch",
    )
    require(row["score_attempt_guard_rows_declared"] == "7", "row count mismatch")
    for field in [
        "score_attempt_guard_executed_rows",
        "scoring_input_acceptance_decision_closed_rows",
        "explicit_null_response_routed_rows",
        "score_attempt_denied_rows",
    ]:
        require(row[field] == "7", f"{field} must be seven")
    for field in [
        "score_ready_input_available_rows",
        "scoring_input_accepted_rows",
        "score_attempt_allowed_now_rows",
        "payload_accepted_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["score_attempt_guard_satisfied"] == "true", "score attempt guard must pass")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "SCORE_ATTEMPT_GUARD_EXECUTED_DENIED_NO_SCORE_READY_INPUT",
        "score attempt guard status mismatch",
    )


def validate_tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_summary_v01.csv"
    )
    require(len(rows) == 7, "null response lock must have seven rows")
    require(
        {row["lock_status"] for row in rows} == {"NULL_RESPONSE_LOCKED_AFTER_SCORE_GUARD_DENIAL"},
        "null response lock status mismatch",
    )
    for field in [
        "score_attempt_guard_executed",
        "score_attempt_denied",
        "explicit_null_response_routed",
        "null_response_locked",
    ]:
        require({row[field] for row in rows} == {"true"}, f"{field} must be true")
    for field in [
        "score_ready_input_available",
        "scoring_input_accepted",
        "score_attempt_allowed_now",
        "payload_accepted",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require(
        {row["required_unlock_condition"] for row in rows}
        == {"replace_null_response_with_real_score_ready_input_and_accepted_scoring_input"},
        "required unlock condition mismatch",
    )
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(len(summary) == 1, "null response lock summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_NULL_RESPONSE_LOCK_V01",
        "summary id mismatch",
    )
    require(row["null_response_lock_rows_declared"] == "7", "row count mismatch")
    for field in [
        "score_attempt_guard_executed_rows",
        "score_attempt_denied_rows",
        "explicit_null_response_routed_rows",
        "null_response_locked_rows",
    ]:
        require(row[field] == "7", f"{field} must be seven")
    for field in [
        "score_ready_input_available_rows",
        "scoring_input_accepted_rows",
        "score_attempt_allowed_now_rows",
        "payload_accepted_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["null_response_lock_satisfied"] == "true", "null response lock must pass")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "NULL_RESPONSE_LOCKED_AFTER_SCORE_GUARD_DENIAL",
        "null response lock status mismatch",
    )


def validate_tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_v01() -> None:
    rows = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_v01.csv"
    )
    summary = read_csv(
        ROOT
        / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_summary_v01.csv"
    )
    require(len(rows) == 7, "route completion certificate must have seven rows")
    require(
        {row["certificate_status"] for row in rows}
        == {"ROUTE_COMPLETED_TO_NULL_RESPONSE_LOCKED_TERMINAL_STATE"},
        "route completion certificate status mismatch",
    )
    for field in [
        "route_completed",
        "terminal_state_reached",
        "null_response_locked",
        "score_attempt_guard_executed",
        "score_attempt_denied",
    ]:
        require({row[field] for row in rows} == {"true"}, f"{field} must be true")
    for field in [
        "score_ready_input_available",
        "scoring_input_accepted",
        "score_attempt_allowed_now",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require({row["terminal_state"] for row in rows} == {"null_response_locked"}, "terminal state mismatch")
    require(
        {row["required_unlock_condition"] for row in rows}
        == {"real_score_ready_input_with_accepted_scoring_input"},
        "required unlock condition mismatch",
    )
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(len(summary) == 1, "route completion certificate summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_ROUTE_COMPLETION_CERTIFICATE_V01",
        "summary id mismatch",
    )
    require(row["route_completion_certificate_rows_declared"] == "7", "row count mismatch")
    for field in [
        "route_completed_rows",
        "terminal_state_reached_rows",
        "null_response_locked_rows",
        "score_attempt_guard_executed_rows",
        "score_attempt_denied_rows",
    ]:
        require(row[field] == "7", f"{field} must be seven")
    for field in [
        "score_ready_input_available_rows",
        "scoring_input_accepted_rows",
        "score_attempt_allowed_now_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["route_completion_certificate_satisfied"] == "true", "route completion certificate must pass")
    require(row["terminal_state"] == "null_response_locked", "terminal state summary mismatch")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "ROUTE_COMPLETED_TO_NULL_RESPONSE_LOCKED_TERMINAL_STATE",
        "route completion certificate status mismatch",
    )


def validate_tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_summary_v01.csv"
    )
    require(len(rows) == 7, "real score-ready input supply contract must have seven rows")
    require(
        {row["contract_status"] for row in rows}
        == {"REAL_SCORE_READY_INPUT_REQUIRED_TO_UNLOCK_NULL_RESPONSE"},
        "real score-ready input supply contract status mismatch",
    )
    require({row["terminal_state"] for row in rows} == {"null_response_locked"}, "terminal state mismatch")
    require({row["route_completed"] for row in rows} == {"true"}, "route must be completed")
    require({row["null_response_locked"] for row in rows} == {"true"}, "null response must be locked")
    for field in [
        "requires_phi_tau_eff_source",
        "requires_dimension_replay",
        "requires_normalization_binding",
        "requires_endpoint_blind_provenance",
        "requires_cmb_readout_mapping",
        "requires_likelihood_adapter",
        "requires_acceptance_replay",
    ]:
        require({row[field] for row in rows} == {"true"}, f"{field} must be required")
    require({row["required_materials_count"] for row in rows} == {"7"}, "each row must require seven materials")
    for field in [
        "supplied_materials_count",
        "real_score_ready_input_supplied",
        "scoring_input_accepted",
        "reopen_scoring_route_allowed_now",
        "score_attempt_allowed_now",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        expected = {"0"} if field == "supplied_materials_count" else {"false"}
        require({row[field] for row in rows} == expected, f"{field} must remain unsupplied/false")
    require({row["score_attempt_blocked_now"] for row in rows} == {"true"}, "score attempt must remain blocked")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7, "expected seven blockers")
    require(len(summary) == 1, "real score-ready input supply contract summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_REAL_SCORE_READY_INPUT_SUPPLY_CONTRACT_V01",
        "summary id mismatch",
    )
    require(row["real_score_ready_input_supply_contract_rows_declared"] == "7", "row count mismatch")
    require(row["route_completed_rows"] == "7", "route completed rows mismatch")
    require(row["null_response_locked_rows"] == "7", "null response locked rows mismatch")
    require(row["required_materials_total"] == "49", "required material total mismatch")
    require(row["supplied_materials_total"] == "0", "supplied material total must be zero")
    for field in [
        "real_score_ready_input_supplied_rows",
        "scoring_input_accepted_rows",
        "reopen_scoring_route_allowed_now_rows",
        "score_attempt_allowed_now_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "7", "blocked score attempt count mismatch")
    require(row["real_score_ready_input_supply_contract_satisfied"] == "true", "contract declaration must pass")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "7", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "REAL_SCORE_READY_INPUT_SUPPLY_CONTRACT_DECLARED_INPUT_NOT_SUPPLIED_ROUTE_REMAINS_LOCKED",
        "real score-ready input supply contract status mismatch",
    )


def validate_tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_summary_v01.csv"
    )
    require(len(rows) == 49, "real score-ready payload slot spec must have 49 rows")
    require(len({row["contract_row_id"] for row in rows}) == 7, "payload slot spec must cover seven contracts")
    require(
        {row["material_class"] for row in rows}
        == {
            "phi_tau_eff_source",
            "dimension_replay",
            "normalization_binding",
            "endpoint_blind_provenance",
            "cmb_readout_mapping",
            "likelihood_adapter",
            "acceptance_replay",
        },
        "payload slot material classes mismatch",
    )
    require(
        {row["slot_status"] for row in rows} == {"PAYLOAD_SLOT_DECLARED_INPUT_NOT_MATERIALIZED"},
        "payload slot status mismatch",
    )
    require(all(row["expected_artifact_path"] for row in rows), "each payload slot needs an expected path")
    require(all(row["required_schema_fields"] for row in rows), "each payload slot needs schema fields")
    require(all(row["validation_rule"] for row in rows), "each payload slot needs a validation rule")
    for field in [
        "payload_materialized",
        "payload_hash_bound",
        "dimension_replay_passed",
        "endpoint_blind_firewall_passed",
        "slot_accepted",
        "scoring_input_accepted",
        "reopen_scoring_route_allowed_now",
        "score_attempt_allowed_now",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 49, "expected 49 blockers")
    require({row["allows_tau_response_claim"] for row in rows} == {"false"}, "Tau response claim must be blocked")
    require({row["allows_dark_sector_verdict"] for row in rows} == {"false"}, "dark verdict must be blocked")
    require(len(summary) == 1, "real score-ready payload slot spec summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_REAL_SCORE_READY_PAYLOAD_SLOT_SPEC_V01",
        "summary id mismatch",
    )
    require(row["contract_rows"] == "7", "contract row count mismatch")
    require(row["payload_slot_rows_declared"] == "49", "slot row count mismatch")
    require(row["material_classes_per_contract_row"] == "7", "material class count mismatch")
    require(row["expected_artifact_paths_declared"] == "49", "artifact path count mismatch")
    for field in [
        "payload_materialized_rows",
        "payload_hash_bound_rows",
        "dimension_replay_passed_rows",
        "endpoint_blind_firewall_passed_rows",
        "slot_accepted_rows",
        "scoring_input_accepted_rows",
        "reopen_scoring_route_allowed_now_rows",
        "score_attempt_allowed_now_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "49", "blocked slot count mismatch")
    require(row["payload_slot_spec_satisfied"] == "true", "payload slot spec must be satisfied")
    require(row["all_required_slots_materialized"] == "false", "required slots cannot be materialized")
    require(row["all_required_slots_accepted"] == "false", "required slots cannot be accepted")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "49", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "PAYLOAD_SLOT_SPEC_DECLARED_INPUT_NOT_MATERIALIZED_ROUTE_REMAINS_LOCKED",
        "real score-ready payload slot spec status mismatch",
    )


def validate_tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_v01.csv")
    summary = read_csv(
        ROOT / "data/derived/tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_summary_v01.csv"
    )
    require(len(rows) == 49, "real score-ready payload template manifest must have 49 rows")
    require(len({row["contract_row_id"] for row in rows}) == 7, "template manifest must cover seven contracts")
    require(len({row["template_path"] for row in rows}) == 7, "template manifest must declare seven templates")
    require({row["template_file_exists"] for row in rows} == {"true"}, "all template files must exist")
    require(
        {row["template_status"] for row in rows} == {"TEMPLATE_BOUND_REAL_PAYLOAD_NOT_MATERIALIZED"},
        "template status mismatch",
    )
    for row in rows:
        require((ROOT / row["template_path"]).exists(), f"missing template file {row['template_path']}")
        require(row["expected_artifact_path"].startswith("data/score_ready_input/"), "expected payload path mismatch")
    for field in [
        "real_payload_materialized",
        "payload_hash_bound",
        "slot_accepted",
        "scoring_input_accepted",
        "reopen_scoring_route_allowed_now",
        "score_attempt_allowed_now",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 49, "expected 49 blockers")
    require({row["allows_tau_response_claim"] for row in rows} == {"false"}, "Tau response claim must be blocked")
    require({row["allows_dark_sector_verdict"] for row in rows} == {"false"}, "dark verdict must be blocked")
    require(len(summary) == 1, "real score-ready payload template manifest summary must have one row")
    row = summary[0]
    require(
        row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_REAL_SCORE_READY_PAYLOAD_TEMPLATE_MANIFEST_V01",
        "summary id mismatch",
    )
    require(row["slot_rows_consumed"] == "49", "slot rows consumed mismatch")
    require(row["template_bindings_declared"] == "49", "template binding count mismatch")
    require(row["template_files_declared"] == "7", "template file declaration mismatch")
    require(row["template_files_written"] == "7", "template file write count mismatch")
    for field in [
        "real_payload_materialized_rows",
        "payload_hash_bound_rows",
        "slot_accepted_rows",
        "scoring_input_accepted_rows",
        "reopen_scoring_route_allowed_now_rows",
        "score_attempt_allowed_now_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "49", "blocked template count mismatch")
    require(row["payload_template_manifest_satisfied"] == "true", "payload template manifest must pass")
    require(row["all_real_payloads_materialized"] == "false", "real payloads cannot be materialized")
    require(row["all_slots_accepted"] == "false", "slots cannot be accepted")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "49", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"]
        == "PAYLOAD_TEMPLATE_MANIFEST_DECLARED_REAL_PAYLOAD_NOT_MATERIALIZED_ROUTE_REMAINS_LOCKED",
        "real score-ready payload template manifest status mismatch",
    )


def validate_tau_cmb_phi_tau_parent_real_payload_import_precheck_v01() -> None:
    rows = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_real_payload_import_precheck_v01.csv")
    summary = read_csv(ROOT / "data/derived/tau_cmb_phi_tau_parent_real_payload_import_precheck_summary_v01.csv")
    require(len(rows) == 49, "real payload import precheck must have 49 rows")
    require(len({row["contract_row_id"] for row in rows}) == 7, "import precheck must cover seven contracts")
    require({row["real_payload_path_exists"] for row in rows} == {"false"}, "real payload paths must be missing")
    require({row["real_payload_readable"] for row in rows} == {"false"}, "real payloads cannot be readable")
    require({row["real_payload_nonempty"] for row in rows} == {"false"}, "real payloads cannot be nonempty")
    require({row["payload_sha256"] for row in rows} == {""}, "payload hashes must be empty")
    require(
        {row["schema_check_status"] for row in rows} == {"SCHEMA_NOT_CHECKED_MISSING_REAL_PAYLOAD"},
        "schema status mismatch",
    )
    require(
        {row["import_precheck_status"] for row in rows} == {"IMPORT_PRECHECK_FAIL_MISSING_REAL_PAYLOAD"},
        "import precheck status mismatch",
    )
    for field in [
        "payload_import_accepted",
        "payload_hash_bound",
        "slot_accepted",
        "scoring_input_accepted",
        "reopen_scoring_route_allowed_now",
        "score_attempt_allowed_now",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        require({row[field] for row in rows} == {"false"}, f"{field} must remain false")
    require(sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 49, "expected 49 blockers")
    require(len(summary) == 1, "real payload import precheck summary must have one row")
    row = summary[0]
    require(row["summary_id"] == "TAU_CMB_PHI_TAU_PARENT_REAL_PAYLOAD_IMPORT_PRECHECK_V01", "summary id mismatch")
    require(row["template_bindings_consumed"] == "49", "template binding count mismatch")
    require(row["import_precheck_rows_declared"] == "49", "precheck row count mismatch")
    require(row["real_payload_paths_expected"] == "49", "expected payload path count mismatch")
    require(row["real_payload_paths_present"] == "0", "payload paths present must be zero")
    require(row["real_payload_paths_missing"] == "49", "payload paths missing mismatch")
    for field in [
        "real_payload_readable_rows",
        "real_payload_nonempty_rows",
        "payload_hash_bound_rows",
        "schema_pass_rows",
        "payload_import_accepted_rows",
        "slot_accepted_rows",
        "scoring_input_accepted_rows",
        "reopen_scoring_route_allowed_now_rows",
        "score_attempt_allowed_now_rows",
        "phi_tau_eff_derived_rows",
        "scores_computed_rows",
        "cmb_likelihood_available_rows",
    ]:
        require(row[field] == "0", f"{field} must be zero")
    require(row["score_attempt_blocked_now_rows"] == "49", "blocked import count mismatch")
    require(row["real_payload_import_precheck_satisfied"] == "true", "import precheck must be satisfied")
    require(row["all_real_payloads_present"] == "false", "real payloads cannot be present")
    require(row["all_payload_imports_accepted"] == "false", "real payload imports cannot be accepted")
    require(row["scores_computed"] == "false", "scores cannot be computed")
    require(row["cmb_likelihood_available"] == "false", "likelihood cannot be available")
    require(row["no_dark_blockers"] == "49", "blocker count mismatch")
    require(row["no_dark_cmb_verdict_allowed"] == "false", "no-dark verdict must be blocked")
    require(row["tau_response_claim_allowed"] == "false", "Tau response claim must be blocked")
    require(row["dark_sector_verdict_allowed"] == "false", "dark-sector verdict must be blocked")
    require(
        row["overall_status"] == "REAL_PAYLOAD_IMPORT_PRECHECK_FAILS_MISSING_REAL_PAYLOADS_ROUTE_REMAINS_LOCKED",
        "real payload import precheck status mismatch",
    )


def validate_arxiv_zip() -> None:
    path = ROOT / "arxiv_submission_source.zip"
    require(path.exists(), "missing arxiv source zip")
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
    require("main.tex" in names, "arxiv zip missing main.tex")
    require("refs.bib" in names, "arxiv zip missing refs.bib")
    require("main.pdf" not in names, "arxiv zip must not include PDF")


def main() -> None:
    validate_external_reference_manifest()
    validate_decision_ladder()
    validate_cmb_constraint_map()
    validate_tau_cmb_effective_source_equation_v01()
    validate_tau_cmb_known_limit_and_dimension_audit_v01()
    validate_tau_cmb_minimal_source_term_candidate_v01()
    validate_tau_cmb_source_term_dimensional_precheck_v01()
    validate_tau_cmb_lcdm_role_scoring_rubric_v01()
    validate_tau_cmb_role_scorecard_template_v01()
    validate_tau_cmb_score_input_unblock_plan_v01()
    validate_tau_cmb_known_limit_failure_map_v01()
    validate_tau_cmb_density_amplitude_derivation_v01()
    validate_tau_cmb_acoustic_role_reduced_benchmark_v01()
    validate_tau_cmb_lensing_transfer_benchmark_v01()
    validate_tau_cmb_growth_transfer_kernel_v01()
    validate_tau_cmb_radiation_guard_bound_check_v01()
    validate_tau_cmb_scorecard_readiness_audit_v01()
    validate_tau_cmb_scorecard_blocker_closure_plan_v01()
    validate_tau_cmb_density_amplitude_closure_v01()
    validate_tau_cmb_acoustic_reduced_evaluation_v01()
    validate_tau_cmb_lensing_transfer_reduced_evaluation_v01()
    validate_tau_cmb_growth_transfer_kernel_closure_v01()
    validate_tau_cmb_radiation_guard_evaluation_v01()
    validate_tau_cmb_known_limit_decision_update_v01()
    validate_tau_cmb_scorecard_prescore_blocker_summary_v01()
    validate_tau_cmb_minimal_scoring_input_contract_v01()
    validate_tau_cmb_scoring_execution_gate_v01()
    validate_tau_cmb_scoring_input_fulfillment_plan_v01()
    validate_tau_cmb_planck_pr3_peak_source_freeze_packet_v01()
    validate_tau_cmb_planck_pr3_peak_extraction_rule_v01()
    validate_tau_cmb_planck_pr3_peak_scoring_input_candidate_v01()
    validate_tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01()
    validate_tau_cmb_planck_pr3_peak_score_attempt_guard_v01()
    validate_tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01()
    validate_tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01()
    validate_tau_cmb_acoustic_tau_prediction_source_derivation_v01()
    validate_tau_cmb_acoustic_source_operator_payload_v01()
    validate_tau_cmb_acoustic_source_operator_payload_supply_v01()
    validate_tau_cmb_acoustic_minimal_operator_model_attempt_v01()
    validate_tau_cmb_acoustic_operator_dependency_unblock_plan_v01()
    validate_tau_cmb_acoustic_domain_basis_lock_acceptance_v01()
    validate_tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01()
    validate_tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01()
    validate_tau_cmb_effective_potential_source_handoff_v01()
    validate_tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01()
    validate_tau_cmb_phi_tau_parent_input_provenance_v01()
    validate_tau_cmb_phi_tau_parent_input_candidate_manifest_v01()
    validate_tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01()
    validate_tau_cmb_phi_tau_parent_input_firewall_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_payload_stub_v01()
    validate_tau_cmb_phi_tau_parent_input_firewall_execution_v01()
    validate_tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01()
    validate_tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01()
    validate_tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01()
    validate_tau_cmb_phi_tau_parent_source_content_closure_decision_v01()
    validate_tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01()
    validate_tau_cmb_phi_tau_parent_input_certificate_candidate_v01()
    validate_tau_cmb_phi_tau_parent_input_certificate_audit_v01()
    validate_tau_cmb_phi_tau_parent_certificate_closure_decision_v01()
    validate_tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01()
    validate_tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01()
    validate_tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01()
    validate_tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01()
    validate_tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01()
    validate_tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01()
    validate_tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01()
    validate_tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01()
    validate_tau_cmb_phi_tau_parent_evidence_payload_acquisition_v01()
    validate_tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01()
    validate_tau_cmb_phi_tau_parent_canonical_payload_packet_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_v01()
    validate_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit_v01()
    validate_tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_v01()
    validate_tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_v01()
    validate_tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_v01()
    validate_tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_v01()
    validate_tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_v01()
    validate_tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_v01()
    validate_tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_v01()
    validate_tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_v01()
    validate_tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_v01()
    validate_tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_v01()
    validate_tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_v01()
    validate_tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_v01()
    validate_tau_cmb_phi_tau_parent_real_payload_import_precheck_v01()
    validate_arxiv_zip()
    print("PAPER13_PROTOCOL_MANIFESTS_VALID")


if __name__ == "__main__":
    main()
