from __future__ import annotations

import csv
import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_files_exist() -> None:
    required = [
        "README.md",
        "DATA_NOTICE.md",
        "LICENSE",
        "CITATION.cff",
        "requirements.txt",
        "paper13_submission_source/main.tex",
        "paper13_submission_source/refs.bib",
        "docs/cmb_constraint_map_v01.md",
        "docs/tau_cmb_effective_source_equation_v01.md",
        "docs/tau_cmb_known_limit_and_dimension_audit_v01.md",
        "docs/tau_cmb_minimal_source_term_candidate_v01.md",
        "docs/tau_cmb_source_term_dimensional_precheck_v01.md",
        "docs/tau_cmb_lcdm_role_scoring_rubric_v01.md",
        "docs/tau_cmb_role_scorecard_template_v01.md",
        "docs/tau_cmb_score_input_unblock_plan_v01.md",
        "docs/tau_cmb_known_limit_failure_map_v01.md",
        "docs/tau_cmb_density_amplitude_derivation_v01.md",
        "docs/tau_cmb_acoustic_role_reduced_benchmark_v01.md",
        "docs/tau_cmb_lensing_transfer_benchmark_v01.md",
        "docs/tau_cmb_growth_transfer_kernel_v01.md",
        "docs/tau_cmb_radiation_guard_bound_check_v01.md",
        "docs/tau_cmb_scorecard_readiness_audit_v01.md",
        "docs/tau_cmb_scorecard_blocker_closure_plan_v01.md",
        "docs/tau_cmb_density_amplitude_closure_v01.md",
        "docs/tau_cmb_acoustic_reduced_evaluation_v01.md",
        "docs/tau_cmb_lensing_transfer_reduced_evaluation_v01.md",
        "docs/tau_cmb_growth_transfer_kernel_closure_v01.md",
        "docs/tau_cmb_radiation_guard_evaluation_v01.md",
        "docs/tau_cmb_known_limit_decision_update_v01.md",
        "docs/tau_cmb_scorecard_prescore_blocker_summary_v01.md",
        "docs/tau_cmb_minimal_scoring_input_contract_v01.md",
        "docs/tau_cmb_scoring_execution_gate_v01.md",
        "docs/tau_cmb_scoring_input_fulfillment_plan_v01.md",
        "docs/tau_cmb_planck_pr3_peak_source_freeze_packet_v01.md",
        "docs/tau_cmb_planck_pr3_peak_extraction_rule_v01.md",
        "docs/tau_cmb_planck_pr3_peak_scoring_input_candidate_v01.md",
        "docs/tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01.md",
        "docs/tau_cmb_planck_pr3_peak_score_attempt_guard_v01.md",
        "docs/tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01.md",
        "docs/tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01.md",
        "docs/tau_cmb_acoustic_tau_prediction_source_derivation_v01.md",
        "docs/tau_cmb_acoustic_source_operator_payload_v01.md",
        "docs/tau_cmb_acoustic_source_operator_payload_supply_v01.md",
        "docs/tau_cmb_acoustic_minimal_operator_model_attempt_v01.md",
        "docs/tau_cmb_acoustic_operator_dependency_unblock_plan_v01.md",
        "docs/tau_cmb_acoustic_domain_basis_lock_acceptance_v01.md",
        "docs/tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01.md",
        "docs/tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01.md",
        "docs/tau_cmb_effective_potential_source_handoff_v01.md",
        "docs/tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_provenance_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_candidate_manifest_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_firewall_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_payload_stub_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_firewall_execution_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_source_content_closure_decision_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_certificate_candidate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_certificate_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_certificate_closure_decision_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01.md",
        "docs/tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01.md",
        "docs/tau_cmb_phi_tau_parent_canonical_payload_packet_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_v01.md",
        "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit_v01.md",
        "docs/tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_v01.md",
        "docs/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_v01.md",
        "docs/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_v01.md",
        "docs/tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_v01.md",
        "docs/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_v01.md",
        "docs/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_v01.md",
        "docs/tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_v01.md",
        "docs/tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_v01.md",
        "docs/tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_v01.md",
        "docs/tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_v01.md",
        "docs/tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_v01.md",
        "docs/tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_v01.md",
        "docs/tau_cmb_phi_tau_parent_real_payload_import_precheck_v01.md",
        "data/source_manifest/cmb_external_reference_manifest_v01.csv",
        "data/source_manifest/tau_core_cmb_decision_ladder_v01.csv",
        "data/derived/cmb_constraint_map_v01.csv",
        "data/derived/tau_core_dark_sector_requirement_map_v01.csv",
        "data/derived/paper13_readiness_summary_v01.csv",
        "data/derived/tau_cmb_effective_source_equation_v01.csv",
        "data/derived/tau_cmb_effective_source_equation_summary_v01.csv",
        "data/derived/tau_cmb_known_limit_and_dimension_audit_v01.csv",
        "data/derived/tau_cmb_known_limit_and_dimension_audit_summary_v01.csv",
        "data/derived/tau_cmb_minimal_source_term_candidate_v01.csv",
        "data/derived/tau_cmb_minimal_source_term_candidate_summary_v01.csv",
        "data/derived/tau_cmb_source_term_dimensional_precheck_v01.csv",
        "data/derived/tau_cmb_source_term_dimensional_precheck_summary_v01.csv",
        "data/derived/tau_cmb_lcdm_role_scoring_rubric_v01.csv",
        "data/derived/tau_cmb_lcdm_role_scoring_rubric_summary_v01.csv",
        "data/derived/tau_cmb_role_scorecard_template_v01.csv",
        "data/derived/tau_cmb_role_scorecard_template_summary_v01.csv",
        "data/derived/tau_cmb_score_input_unblock_plan_v01.csv",
        "data/derived/tau_cmb_score_input_unblock_plan_summary_v01.csv",
        "data/derived/tau_cmb_known_limit_failure_map_v01.csv",
        "data/derived/tau_cmb_known_limit_failure_map_summary_v01.csv",
        "data/derived/tau_cmb_density_amplitude_derivation_v01.csv",
        "data/derived/tau_cmb_density_amplitude_derivation_summary_v01.csv",
        "data/derived/tau_cmb_acoustic_role_reduced_benchmark_v01.csv",
        "data/derived/tau_cmb_acoustic_role_reduced_benchmark_summary_v01.csv",
        "data/derived/tau_cmb_lensing_transfer_benchmark_v01.csv",
        "data/derived/tau_cmb_lensing_transfer_benchmark_summary_v01.csv",
        "data/derived/tau_cmb_growth_transfer_kernel_v01.csv",
        "data/derived/tau_cmb_growth_transfer_kernel_summary_v01.csv",
        "data/derived/tau_cmb_radiation_guard_bound_check_v01.csv",
        "data/derived/tau_cmb_radiation_guard_bound_check_summary_v01.csv",
        "data/derived/tau_cmb_scorecard_readiness_audit_v01.csv",
        "data/derived/tau_cmb_scorecard_readiness_audit_summary_v01.csv",
        "data/derived/tau_cmb_scorecard_blocker_closure_plan_v01.csv",
        "data/derived/tau_cmb_scorecard_blocker_closure_plan_summary_v01.csv",
        "data/derived/tau_cmb_density_amplitude_closure_v01.csv",
        "data/derived/tau_cmb_density_amplitude_closure_summary_v01.csv",
        "data/derived/tau_cmb_acoustic_reduced_evaluation_v01.csv",
        "data/derived/tau_cmb_acoustic_reduced_evaluation_summary_v01.csv",
        "data/derived/tau_cmb_lensing_transfer_reduced_evaluation_v01.csv",
        "data/derived/tau_cmb_lensing_transfer_reduced_evaluation_summary_v01.csv",
        "data/derived/tau_cmb_growth_transfer_kernel_closure_v01.csv",
        "data/derived/tau_cmb_growth_transfer_kernel_closure_summary_v01.csv",
        "data/derived/tau_cmb_radiation_guard_evaluation_v01.csv",
        "data/derived/tau_cmb_radiation_guard_evaluation_summary_v01.csv",
        "data/derived/tau_cmb_known_limit_decision_update_v01.csv",
        "data/derived/tau_cmb_known_limit_decision_update_summary_v01.csv",
        "data/derived/tau_cmb_scorecard_prescore_blocker_summary_v01.csv",
        "data/derived/tau_cmb_scorecard_prescore_blocker_summary_summary_v01.csv",
        "data/derived/tau_cmb_minimal_scoring_input_contract_v01.csv",
        "data/derived/tau_cmb_minimal_scoring_input_contract_summary_v01.csv",
        "data/derived/tau_cmb_scoring_execution_gate_v01.csv",
        "data/derived/tau_cmb_scoring_execution_gate_summary_v01.csv",
        "data/derived/tau_cmb_scoring_input_fulfillment_plan_v01.csv",
        "data/derived/tau_cmb_scoring_input_fulfillment_plan_summary_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_source_freeze_packet_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_source_freeze_packet_summary_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_source_freeze_packet_v01.json",
        "data/derived/tau_cmb_planck_pr3_source_receipt_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_observable_table_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_extraction_rule_summary_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_extraction_rule_v01.json",
        "data/derived/tau_cmb_planck_pr3_peak_scoring_input_candidate_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_scoring_input_candidate_summary_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_scoring_input_candidate_v01.json",
        "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_summary_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01.json",
        "data/derived/tau_cmb_planck_pr3_peak_score_attempt_guard_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_score_attempt_guard_summary_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_score_attempt_guard_v01.json",
        "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_materialization_summary_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01.json",
        "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_summary_v01.csv",
        "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01.json",
        "data/derived/tau_cmb_acoustic_tau_prediction_source_derivation_v01.csv",
        "data/derived/tau_cmb_acoustic_tau_prediction_source_derivation_summary_v01.csv",
        "data/derived/tau_cmb_acoustic_tau_prediction_source_derivation_v01.json",
        "data/derived/tau_cmb_acoustic_source_operator_payload_v01.csv",
        "data/derived/tau_cmb_acoustic_source_operator_payload_summary_v01.csv",
        "data/derived/tau_cmb_acoustic_source_operator_payload_v01.json",
        "data/derived/tau_cmb_acoustic_source_operator_payload_supply_v01.csv",
        "data/derived/tau_cmb_acoustic_source_operator_payload_supply_summary_v01.csv",
        "data/derived/tau_cmb_acoustic_source_operator_payload_supply_v01.json",
        "data/derived/tau_cmb_acoustic_minimal_operator_model_attempt_v01.csv",
        "data/derived/tau_cmb_acoustic_minimal_operator_model_attempt_summary_v01.csv",
        "data/derived/tau_cmb_acoustic_minimal_operator_model_attempt_v01.json",
        "data/derived/tau_cmb_acoustic_operator_dependency_unblock_plan_v01.csv",
        "data/derived/tau_cmb_acoustic_operator_dependency_unblock_plan_summary_v01.csv",
        "data/derived/tau_cmb_acoustic_operator_dependency_unblock_plan_v01.json",
        "data/derived/tau_cmb_acoustic_domain_basis_lock_acceptance_v01.csv",
        "data/derived/tau_cmb_acoustic_domain_basis_lock_acceptance_summary_v01.csv",
        "data/derived/tau_cmb_acoustic_domain_basis_lock_acceptance_v01.json",
        "data/derived/tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01.csv",
        "data/derived/tau_cmb_phi_tau_eff_acoustic_input_acceptance_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01.json",
        "data/derived/tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01.csv",
        "data/derived/tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01.json",
        "data/derived/tau_cmb_effective_potential_source_handoff_v01.csv",
        "data/derived/tau_cmb_effective_potential_source_handoff_summary_v01.csv",
        "data/derived/tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.csv",
        "data/derived/tau_cmb_endpoint_blind_phi_tau_derivation_contract_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_provenance_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_provenance_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01.json",
        "data/derived/tau_cmb_phi_tau_parent_input_firewall_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_firewall_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_payload_stub_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_payload_stub_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_firewall_execution_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_firewall_execution_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_requirements_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_candidate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_payload_firewall_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_source_content_closure_decision_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_source_content_closure_decision_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_source_content_closure_decision_v01.json",
        "data/derived/tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_dimension_replay_certificate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_certificate_candidate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_certificate_candidate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_certificate_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_certificate_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_certificate_closure_decision_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_certificate_closure_decision_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_certificate_closure_decision_v01.json",
        "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_request_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_evidence_package_closure_decision_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01.json",
        "data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01.json",
        "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01.json",
        "data/derived/tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01.json",
        "data/derived/tau_cmb_phi_tau_parent_canonical_payload_packet_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_canonical_payload_packet_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_canonical_payload_packet_v01.json",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_v01_manifest.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_summary_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_real_payload_import_precheck_v01.csv",
        "data/derived/tau_cmb_phi_tau_parent_real_payload_import_precheck_summary_v01.csv",
        "data/score_ready_input_templates/phi_tau_eff_source_template.csv",
        "data/score_ready_input_templates/dimension_replay_template.json",
        "data/score_ready_input_templates/normalization_binding_template.csv",
        "data/score_ready_input_templates/endpoint_blind_provenance_template.json",
        "data/score_ready_input_templates/cmb_readout_mapping_template.csv",
        "data/score_ready_input_templates/likelihood_adapter_template.json",
        "data/score_ready_input_templates/acceptance_replay_template.json",
        "scripts/build_cmb_constraint_map.py",
        "scripts/build_tau_cmb_effective_source_equation.py",
        "scripts/build_tau_cmb_known_limit_and_dimension_audit.py",
        "scripts/build_tau_cmb_minimal_source_term_candidate.py",
        "scripts/build_tau_cmb_source_term_dimensional_precheck.py",
        "scripts/build_tau_cmb_lcdm_role_scoring_rubric.py",
        "scripts/build_tau_cmb_role_scorecard_template.py",
        "scripts/build_tau_cmb_score_input_unblock_plan.py",
        "scripts/build_tau_cmb_known_limit_failure_map.py",
        "scripts/build_tau_cmb_density_amplitude_derivation.py",
        "scripts/build_tau_cmb_acoustic_role_reduced_benchmark.py",
        "scripts/build_tau_cmb_lensing_transfer_benchmark.py",
        "scripts/build_tau_cmb_growth_transfer_kernel.py",
        "scripts/build_tau_cmb_radiation_guard_bound_check.py",
        "scripts/build_tau_cmb_scorecard_readiness_audit.py",
        "scripts/build_tau_cmb_scorecard_blocker_closure_plan.py",
        "scripts/build_tau_cmb_density_amplitude_closure.py",
        "scripts/build_tau_cmb_acoustic_reduced_evaluation.py",
        "scripts/build_tau_cmb_lensing_transfer_reduced_evaluation.py",
        "scripts/build_tau_cmb_growth_transfer_kernel_closure.py",
        "scripts/build_tau_cmb_radiation_guard_evaluation.py",
        "scripts/build_tau_cmb_known_limit_decision_update.py",
        "scripts/build_tau_cmb_scorecard_prescore_blocker_summary.py",
        "scripts/build_tau_cmb_minimal_scoring_input_contract.py",
        "scripts/build_tau_cmb_scoring_execution_gate.py",
        "scripts/build_tau_cmb_scoring_input_fulfillment_plan.py",
        "scripts/build_tau_cmb_planck_pr3_peak_source_freeze_packet.py",
        "scripts/build_tau_cmb_planck_pr3_peak_extraction_rule.py",
        "scripts/build_tau_cmb_planck_pr3_peak_scoring_input_candidate.py",
        "scripts/build_tau_cmb_planck_pr3_peak_tau_prediction_or_null_response.py",
        "scripts/build_tau_cmb_planck_pr3_peak_score_attempt_guard.py",
        "scripts/build_tau_cmb_planck_pr3_peak_tau_prediction_materialization.py",
        "scripts/build_tau_cmb_planck_pr3_peak_tau_prediction_payload_supply.py",
        "scripts/build_tau_cmb_acoustic_tau_prediction_source_derivation.py",
        "scripts/build_tau_cmb_acoustic_source_operator_payload.py",
        "scripts/build_tau_cmb_acoustic_source_operator_payload_supply.py",
        "scripts/build_tau_cmb_acoustic_minimal_operator_model_attempt.py",
        "scripts/build_tau_cmb_acoustic_operator_dependency_unblock_plan.py",
        "scripts/build_tau_cmb_acoustic_domain_basis_lock_acceptance.py",
        "scripts/build_tau_cmb_phi_tau_eff_acoustic_input_acceptance.py",
        "scripts/build_tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance.py",
        "scripts/build_tau_cmb_effective_potential_source_handoff.py",
        "scripts/build_tau_cmb_endpoint_blind_phi_tau_derivation_contract.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_provenance.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_candidate_manifest.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_firewall_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_payload_stub.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_firewall_execution.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_concrete_payload_requirements.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_concrete_payload_candidate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_payload_firewall_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_source_content_closure_decision.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_dimension_replay_certificate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_certificate_candidate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_certificate_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_certificate_closure_decision.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_certificate_evidence_request.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_evidence_package_closure_decision.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_populated_evidence_package_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate.py",
        "scripts/build_tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision.py",
        "scripts/build_tau_cmb_phi_tau_parent_canonical_payload_packet.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate.py",
        "scripts/build_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit.py",
        "scripts/build_tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package.py",
        "scripts/build_tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package.py",
        "scripts/build_tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck.py",
        "scripts/build_tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate.py",
        "scripts/build_tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package.py",
        "scripts/build_tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package.py",
        "scripts/build_tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard.py",
        "scripts/build_tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock.py",
        "scripts/build_tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate.py",
        "scripts/build_tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract.py",
        "scripts/build_tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec.py",
        "scripts/build_tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest.py",
        "scripts/build_tau_cmb_phi_tau_parent_real_payload_import_precheck.py",
        "scripts/build_arxiv_source.py",
        "scripts/validate_protocol_manifests.py",
        "scripts/reproduce.py",
        "arxiv_submission_source.zip",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_cmb_constraint_map_blocks_verdicts() -> None:
    constraints = list(csv.DictReader((ROOT / "data/derived/cmb_constraint_map_v01.csv").open()))
    requirements = list(csv.DictReader((ROOT / "data/derived/tau_core_dark_sector_requirement_map_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/paper13_readiness_summary_v01.csv").open()))
    assert len(constraints) == 5
    assert len(requirements) == 5
    assert sum(row["necessity_pressure"] == "HIGH" for row in constraints) == 4
    assert {row["current_protocol_status"] for row in constraints} == {"MAPPED_NOT_SOLVED"}
    assert all(row["allows_dark_sector_verdict"] == "false" for row in requirements)
    assert sum(row["blocks_no_dark_claim"] == "true" for row in requirements) == 4
    assert summary == [
        {
            "summary_id": "PAPER13_CMB_CONSTRAINT_MAP_V01",
            "external_references_registered": "3",
            "cmb_constraints_mapped": "5",
            "requirements_written": "5",
            "high_pressure_constraints": "4",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_verdict_allowed": "false",
            "overall_status": "CMB_CONSTRAINTS_MAP_TO_TAU_RESPONSE_REQUIREMENTS_VERDICT_BLOCKED",
            "next_required_artifact": "tau_cmb_effective_source_equation_v01",
            "claim_boundary": "paper13_cmb_constraint_map_only_no_likelihood_no_dark_sector_verdict",
        }
    ]


def test_tau_cmb_effective_source_equation_target_is_unfilled() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_effective_source_equation_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_effective_source_equation_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_effective_source_equation_v01.md").read_text()

    assert len(rows) == 8
    assert [row["target_component"] for row in rows] == [
        "base_carrier",
        "disturbance_seed",
        "response_operator",
        "effective_density",
        "effective_potential",
        "transfer_response",
        "radiation_guard",
        "known_limit_gate",
    ]
    assert {row["current_status"] for row in rows} == {"DECLARED_NOT_FILLED"}
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_EFFECTIVE_SOURCE_EQUATION_V01",
            "equation_target": "tau_cmb_effective_source_equation_v01",
            "components_declared": "8",
            "lcdm_role_checks_declared": "8",
            "dimension_roles_declared": "8",
            "source_equation_filled": "false",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "EFFECTIVE_SOURCE_EQUATION_TARGET_DECLARED_NOT_FILLED",
            "next_required_artifact": "tau_cmb_known_limit_and_dimension_audit_v01",
            "claim_boundary": "tau_cmb_effective_source_equation_v01_target_only_no_cmb_solution_no_verdict",
        }
    ]
    assert "does not solve the target" in note
    assert "no CMB likelihood" in note


def test_tau_cmb_known_limit_dimension_audit_blocks_formula_claims() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_known_limit_and_dimension_audit_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_known_limit_and_dimension_audit_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_known_limit_and_dimension_audit_v01.md").read_text()

    assert len(rows) == 8
    assert {row["formula_available"] for row in rows} == {"false"}
    assert {row["dimensional_consistency_proved"] for row in rows} == {"false"}
    assert all("DECLARED" in row["dimension_slot_status"] for row in rows)
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_KNOWN_LIMIT_AND_DIMENSION_AUDIT_V01",
            "audited_components": "8",
            "dimension_slots_declared": "8",
            "formula_available_components": "0",
            "dimensional_consistency_proved_components": "0",
            "lcdm_roles_matched": "0",
            "lcdm_roles_unmatched": "8",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "KNOWN_LIMIT_DIMENSION_SLOTS_DECLARED_FORMULA_AND_LCDM_MATCH_BLOCKED",
            "next_required_artifact": "tau_cmb_minimal_source_term_candidate_v01",
            "claim_boundary": "tau_cmb_known_limit_and_dimension_audit_v01_no_formula_no_likelihood_no_verdict",
        }
    ]
    assert "no component has an available formula" in note
    assert "no CMB likelihood" in note


def test_tau_cmb_minimal_source_term_candidate_is_only_a_skeleton() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_minimal_source_term_candidate_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_minimal_source_term_candidate_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_minimal_source_term_candidate_v01.md").read_text()

    assert len(rows) == 6
    assert [row["source_term_component"] for row in rows] == [
        "carrier_to_response_state",
        "effective_density_source",
        "effective_potential_poisson_slot",
        "transfer_kernel_slot",
        "radiation_guard_slot",
        "known_limit_branch",
    ]
    assert {row["current_status"] for row in rows} == {"CANDIDATE_SKELETON_DECLARED_NOT_VALIDATED"}
    assert sum(row["dimensional_precheck_status"].startswith("CONDITIONALLY_PRECHECKABLE") for row in rows) == 3
    assert {row["lcdm_role_match_status"] for row in rows} == {"LCDM_ROLE_DECLARED_NOT_MATCHED"}
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_MINIMAL_SOURCE_TERM_CANDIDATE_V01",
            "candidate_components_declared": "6",
            "formula_skeletons_declared": "6",
            "dimensionally_precheckable_skeletons": "3",
            "dimensional_consistency_proved_components": "0",
            "lcdm_role_matches_claimed": "0",
            "no_dark_blockers": "5",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "MINIMAL_SOURCE_TERM_CANDIDATE_DECLARED_NOT_VALIDATED",
            "next_required_artifact": "tau_cmb_source_term_dimensional_precheck_v01",
            "claim_boundary": "tau_cmb_minimal_source_term_candidate_v01_skeleton_only_no_likelihood_no_verdict",
        }
    ]
    assert "standard-form comparison slot" in note
    assert "no CMB likelihood" in note


def test_tau_cmb_source_term_dimensional_precheck_is_partial_and_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_source_term_dimensional_precheck_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_source_term_dimensional_precheck_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_source_term_dimensional_precheck_v01.md").read_text()

    assert len(rows) == 6
    assert sum(row["precheck_result"].startswith("CONDITIONAL_PASS") for row in rows) == 3
    assert sum(row["precheck_result"].startswith("BLOCKED") for row in rows) == 3
    assert sum(row["blocks_scoring"] == "true" for row in rows) == 3
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_SOURCE_TERM_DIMENSIONAL_PRECHECK_V01",
            "prechecked_components": "6",
            "conditional_dimension_passes": "3",
            "blocked_dimension_rows": "3",
            "full_dimensional_proofs": "0",
            "scoring_blockers": "3",
            "no_dark_blockers": "5",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SOURCE_TERM_DIMENSIONAL_PRECHECK_PARTIAL_CONDITIONAL_SCORING_BLOCKED",
            "next_required_artifact": "tau_cmb_lcdm_role_scoring_rubric_v01",
            "claim_boundary": "tau_cmb_source_term_dimensional_precheck_v01_conditional_only_no_likelihood_no_verdict",
        }
    ]
    assert "Three rows are conditionally precheckable" in note
    assert "no Tau-response or dark-sector verdict" in note


def test_tau_cmb_lcdm_role_scoring_rubric_declares_rules_without_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_lcdm_role_scoring_rubric_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_lcdm_role_scoring_rubric_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_lcdm_role_scoring_rubric_v01.md").read_text()

    assert len(rows) == 6
    assert [row["cmb_role"] for row in rows] == [
        "acoustic_peak_phase_and_height",
        "omega_c_h2_density_inference",
        "cmb_lensing_potential",
        "damping_tail_and_radiation_guard",
        "growth_seed_and_transfer_consistency",
        "known_limit_or_explicit_failure",
    ]
    assert all(row["score_0_condition"] for row in rows)
    assert all(row["score_1_condition"] for row in rows)
    assert all(row["score_2_condition"] for row in rows)
    assert all(row["hard_failure_condition"] for row in rows)
    assert {row["currently_scoreable"] for row in rows} == {"false"}
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_LCDM_ROLE_SCORING_RUBRIC_V01",
            "rubric_rows_declared": "6",
            "score_levels_declared_per_row": "3",
            "currently_scoreable_rows": "0",
            "hard_failure_rules_declared": "6",
            "no_dark_blockers": "5",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "LCDM_ROLE_SCORING_RUBRIC_DECLARED_NO_SCORES_COMPUTED",
            "next_required_artifact": "tau_cmb_role_scorecard_template_v01",
            "claim_boundary": "tau_cmb_lcdm_role_scoring_rubric_v01_rubric_only_no_scores_no_likelihood_no_verdict",
        }
    ]
    assert "0 = role absent" in note
    assert "computes no numerical result" in note


def test_tau_cmb_role_scorecard_template_blocks_all_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_role_scorecard_template_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_role_scorecard_template_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_role_scorecard_template_v01.md").read_text()

    assert len(rows) == 6
    assert {row["score_status"] for row in rows} == {"NOT_COMPUTED_INPUT_BLOCKED"}
    assert {row["assigned_score"] for row in rows} == {"NA"}
    assert {row["score_evidence_pointer"] for row in rows} == {"NA"}
    assert all(row["minimum_unblock_artifact"] for row in rows)
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_ROLE_SCORECARD_TEMPLATE_V01",
            "scorecard_rows_declared": "6",
            "scores_computed": "0",
            "not_computed_rows": "6",
            "hard_failures_triggered": "0",
            "blocked_rows": "6",
            "no_dark_blockers": "5",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ROLE_SCORECARD_TEMPLATE_DECLARED_ALL_SCORES_BLOCKED",
            "next_required_artifact": "tau_cmb_score_input_unblock_plan_v01",
            "claim_boundary": "tau_cmb_role_scorecard_template_v01_template_only_no_scores_no_likelihood_no_verdict",
        }
    ]
    assert "NOT_COMPUTED_INPUT_BLOCKED" in note
    assert "computes no scores" in note


def test_tau_cmb_score_input_unblock_plan_prioritizes_next_inputs() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_score_input_unblock_plan_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_score_input_unblock_plan_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_score_input_unblock_plan_v01.md").read_text()

    assert len(rows) == 6
    assert [row["priority_rank"] for row in rows] == ["1", "2", "3", "4", "5", "6"]
    assert [row["minimum_unblock_artifact"] for row in rows] == [
        "tau_cmb_known_limit_failure_map_v01",
        "tau_cmb_density_amplitude_derivation_v01",
        "tau_cmb_acoustic_role_reduced_benchmark_v01",
        "tau_cmb_lensing_transfer_benchmark_v01",
        "tau_cmb_growth_transfer_kernel_v01",
        "tau_cmb_radiation_guard_bound_check_v01",
    ]
    assert all(row["unblock_goal"] for row in rows)
    assert all(row["why_this_priority"] for row in rows)
    assert sum(row["can_unlock_score_without_likelihood"] == "true" for row in rows) == 5
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_SCORE_INPUT_UNBLOCK_PLAN_V01",
            "unblock_rows_declared": "6",
            "ranked_rows": "6",
            "immediate_next_artifact": "tau_cmb_known_limit_failure_map_v01",
            "likelihood_required_for_verdict": "true",
            "scores_computed": "false",
            "no_dark_blockers": "5",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORE_INPUT_UNBLOCK_PLAN_DECLARED_NO_SCORES_COMPUTED",
            "next_required_artifact": "tau_cmb_known_limit_failure_map_v01",
            "claim_boundary": "tau_cmb_score_input_unblock_plan_v01_plan_only_no_scores_no_likelihood_no_verdict",
        }
    ]
    assert "tau_cmb_known_limit_failure_map_v01" in note
    assert "computes no scores" in note


def test_tau_cmb_known_limit_failure_map_declares_unresolved_decision_states() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_known_limit_failure_map_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_known_limit_failure_map_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_known_limit_failure_map_v01.md").read_text()

    assert len(rows) == 6
    assert {row["allowed_decision_states"] for row in rows} == {"REPRODUCE;APPROXIMATE;FAIL;UNRESOLVED"}
    assert {row["current_decision_state"] for row in rows} == {"UNRESOLVED_INPUT_MISSING"}
    assert all(row["minimum_evidence_for_reproduce"] for row in rows)
    assert all(row["minimum_evidence_for_approximate"] for row in rows)
    assert all(row["minimum_evidence_for_fail"] for row in rows)
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_KNOWN_LIMIT_FAILURE_MAP_V01",
            "known_limit_rows_declared": "6",
            "allowed_decision_states_per_row": "4",
            "resolved_rows": "0",
            "unresolved_rows": "6",
            "failures_declared": "0",
            "reproductions_declared": "0",
            "approximations_declared": "0",
            "no_dark_blockers": "5",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "KNOWN_LIMIT_FAILURE_MAP_DECLARED_ALL_ROLES_UNRESOLVED",
            "next_required_artifact": "tau_cmb_density_amplitude_derivation_v01",
            "claim_boundary": "tau_cmb_known_limit_failure_map_v01_map_only_no_scores_no_likelihood_no_verdict",
        }
    ]
    assert "UNRESOLVED_INPUT_MISSING" in note
    assert "declares no reproduction" in note


def test_tau_cmb_density_amplitude_derivation_is_conditional_only() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_density_amplitude_derivation_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_density_amplitude_derivation_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_density_amplitude_derivation_v01.md").read_text()

    assert len(rows) == 5
    assert [row["derivation_component"] for row in rows] == [
        "reference_density_normalization",
        "tau_effective_density_slot",
        "dimensionless_amplitude_definition",
        "endpoint_blindness_gate",
        "omega_c_h2_comparison_gate",
    ]
    assert sum(row["dimension_status"].startswith("CONDITIONAL_DIMENSION_PASS") for row in rows) == 1
    assert all(
        "NOT_SUPPLIED" in row["endpoint_blindness_status"]
        or "NOT_PROVED" in row["endpoint_blindness_status"]
        or "NOT_TAU_DERIVED" in row["endpoint_blindness_status"]
        or "WAITING" in row["endpoint_blindness_status"]
        for row in rows
    )
    assert all("MATCHED" not in row["omega_c_h2_role_status"] for row in rows)
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_DENSITY_AMPLITUDE_DERIVATION_V01",
            "density_rows_declared": "5",
            "conditional_dimension_passes": "1",
            "endpoint_blind_derivations_available": "0",
            "omega_c_h2_role_matches": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "5",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "DENSITY_AMPLITUDE_DEFINITION_DECLARED_DERIVATION_AND_MATCH_BLOCKED",
            "next_required_artifact": "tau_cmb_acoustic_role_reduced_benchmark_v01",
            "claim_boundary": "tau_cmb_density_amplitude_derivation_v01_conditional_definition_no_fit_no_likelihood_no_verdict",
        }
    ]
    assert "A_tau(a,k) := rho_tau_eff(a,k) / rho_cdm_ref(a)" in note
    assert "matches no Omega_c h^2 role" in note


def test_tau_cmb_acoustic_role_reduced_benchmark_is_declared_not_evaluated() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_role_reduced_benchmark_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_role_reduced_benchmark_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_acoustic_role_reduced_benchmark_v01.md").read_text()

    assert len(rows) == 6
    assert [row["benchmark_component"] for row in rows] == [
        "potential_source_presence",
        "acoustic_phase_support",
        "relative_peak_height_support",
        "baryon_loading_compatibility",
        "scale_horizon_convention",
        "explicit_failure_branch",
    ]
    assert {row["current_status"] for row in rows} == {"DECLARED_NOT_EVALUATED"}
    assert all(row["reduced_benchmark_condition"] for row in rows)
    assert all(row["required_input"] for row in rows)
    assert all(row["hard_failure_if"] for row in rows)
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_ACOUSTIC_ROLE_REDUCED_BENCHMARK_V01",
            "benchmark_rows_declared": "6",
            "evaluated_rows": "0",
            "hard_failures_triggered": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "6",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACOUSTIC_REDUCED_BENCHMARK_DECLARED_NOT_EVALUATED",
            "next_required_artifact": "tau_cmb_lensing_transfer_benchmark_v01",
            "claim_boundary": "tau_cmb_acoustic_role_reduced_benchmark_v01_benchmark_only_no_fit_no_likelihood_no_verdict",
        }
    ]
    assert "DECLARED_NOT_EVALUATED" in note
    assert "computes no score" in note


def test_tau_cmb_lensing_transfer_benchmark_is_declared_not_evaluated() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_lensing_transfer_benchmark_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_lensing_transfer_benchmark_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_lensing_transfer_benchmark_v01.md").read_text()

    assert len(rows) == 6
    assert [row["benchmark_component"] for row in rows] == [
        "lensing_potential_source_presence",
        "transfer_kernel_presence",
        "projection_geometry_convention",
        "amplitude_shape_support",
        "cross_readout_consistency",
        "explicit_failure_branch",
    ]
    assert {row["current_status"] for row in rows} == {"DECLARED_NOT_EVALUATED"}
    assert all(row["reduced_benchmark_condition"] for row in rows)
    assert all(row["required_input"] for row in rows)
    assert all(row["hard_failure_if"] for row in rows)
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_LENSING_TRANSFER_BENCHMARK_V01",
            "benchmark_rows_declared": "6",
            "evaluated_rows": "0",
            "hard_failures_triggered": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "6",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "LENSING_TRANSFER_BENCHMARK_DECLARED_NOT_EVALUATED",
            "next_required_artifact": "tau_cmb_growth_transfer_kernel_v01",
            "claim_boundary": "tau_cmb_lensing_transfer_benchmark_v01_benchmark_only_no_fit_no_likelihood_no_verdict",
        }
    ]
    assert "DECLARED_NOT_EVALUATED" in note
    assert "evaluates no lensing spectrum" in note


def test_tau_cmb_growth_transfer_kernel_is_declared_not_specified() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_growth_transfer_kernel_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_growth_transfer_kernel_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_growth_transfer_kernel_v01.md").read_text()

    assert len(rows) == 6
    assert [row["kernel_component"] for row in rows] == [
        "domain_specification",
        "codomain_specification",
        "time_scale_convention",
        "operator_rule",
        "cross_role_consistency",
        "explicit_failure_branch",
    ]
    assert {row["current_status"] for row in rows} == {"DECLARED_NOT_SPECIFIED"}
    assert all(row["required_specification"] for row in rows)
    assert all(row["dimension_or_normalization_status"] for row in rows)
    assert all(row["hard_failure_if"] for row in rows)
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_GROWTH_TRANSFER_KERNEL_V01",
            "kernel_rows_declared": "6",
            "specified_rows": "0",
            "dimension_or_normalization_rows_declared": "6",
            "hard_failures_triggered": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "6",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "GROWTH_TRANSFER_KERNEL_DECLARED_NOT_SPECIFIED",
            "next_required_artifact": "tau_cmb_radiation_guard_bound_check_v01",
            "claim_boundary": "tau_cmb_growth_transfer_kernel_v01_kernel_spec_only_no_fit_no_likelihood_no_verdict",
        }
    ]
    assert "DECLARED_NOT_SPECIFIED" in note
    assert "supplies no operator rule" in note


def test_tau_cmb_radiation_guard_bound_check_is_declared_not_evaluated() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_radiation_guard_bound_check_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_radiation_guard_bound_check_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_radiation_guard_bound_check_v01.md").read_text()

    assert len(rows) == 5
    assert [row["guard_component"] for row in rows] == [
        "tau_radiation_like_contribution",
        "external_bound_convention",
        "damping_tail_guard",
        "cross_role_consistency",
        "explicit_failure_branch",
    ]
    assert {row["current_status"] for row in rows} == {"DECLARED_NOT_EVALUATED"}
    assert all(row["required_check"] for row in rows)
    assert all(row["dimension_status"] for row in rows)
    assert all(row["hard_failure_if"] for row in rows)
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 0
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_RADIATION_GUARD_BOUND_CHECK_V01",
            "guard_rows_declared": "5",
            "evaluated_rows": "0",
            "dimensionless_rows_declared": "3",
            "hard_failures_triggered": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "0",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "RADIATION_GUARD_BOUND_CHECK_DECLARED_NOT_EVALUATED",
            "next_required_artifact": "tau_cmb_scorecard_readiness_audit_v01",
            "claim_boundary": "tau_cmb_radiation_guard_bound_check_v01_guard_only_no_bound_eval_no_likelihood_no_verdict",
        }
    ]
    assert "DECLARED_NOT_EVALUATED" in note
    assert "evaluates no bound" in note


def test_tau_cmb_scorecard_readiness_audit_blocks_all_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_scorecard_readiness_audit_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_scorecard_readiness_audit_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_scorecard_readiness_audit_v01.md").read_text()

    assert len(rows) == 6
    assert [row["cmb_role"] for row in rows] == [
        "acoustic_peak_phase_and_height",
        "omega_c_h2_density_inference",
        "cmb_lensing_potential",
        "damping_tail_and_radiation_guard",
        "growth_seed_and_transfer_consistency",
        "known_limit_or_explicit_failure",
    ]
    assert {row["can_compute_score"] for row in rows} == {"false"}
    assert all(row["score_readiness_status"].startswith("NOT_READY") for row in rows)
    assert all(row["minimum_missing_input"] for row in rows)
    assert len({row["input_artifact_checked"] for row in rows}) == 6
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_SCORECARD_READINESS_AUDIT_V01",
            "readiness_rows_declared": "6",
            "input_artifacts_checked": "6",
            "score_ready_rows": "0",
            "score_blocked_rows": "6",
            "direct_no_dark_blockers": "5",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORECARD_NOT_READY_ALL_ROWS_BLOCKED",
            "next_required_artifact": "tau_cmb_scorecard_blocker_closure_plan_v01",
            "claim_boundary": "tau_cmb_scorecard_readiness_audit_v01_audit_only_no_scores_no_likelihood_no_verdict",
        }
    ]
    assert "score_ready_rows = 0" in note
    assert "permits no no-dark or" in note


def test_tau_cmb_scorecard_blocker_closure_plan_ranks_closures_without_scores() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_scorecard_blocker_closure_plan_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_scorecard_blocker_closure_plan_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_scorecard_blocker_closure_plan_v01.md").read_text()

    assert len(rows) == 6
    assert [row["priority_rank"] for row in rows] == ["1", "2", "3", "4", "5", "6"]
    assert [row["next_artifact_to_build"] for row in rows] == [
        "tau_cmb_density_amplitude_closure_v01",
        "tau_cmb_acoustic_reduced_evaluation_v01",
        "tau_cmb_lensing_transfer_reduced_evaluation_v01",
        "tau_cmb_growth_transfer_kernel_closure_v01",
        "tau_cmb_radiation_guard_evaluation_v01",
        "tau_cmb_known_limit_decision_update_v01",
    ]
    assert all(row["closure_action"] for row in rows)
    assert all(row["closure_criterion"] for row in rows)
    assert all(row["stop_rule"] for row in rows)
    assert {row["can_compute_score_after_closure"] for row in rows} == {"true"}
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_SCORECARD_BLOCKER_CLOSURE_PLAN_V01",
            "closure_rows_declared": "6",
            "ranked_rows": "6",
            "immediate_next_artifact": "tau_cmb_density_amplitude_closure_v01",
            "closures_completed": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "5",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "BLOCKER_CLOSURE_PLAN_DECLARED_NO_CLOSURES_COMPLETED",
            "next_required_artifact": "tau_cmb_density_amplitude_closure_v01",
            "claim_boundary": "tau_cmb_scorecard_blocker_closure_plan_v01_plan_only_no_scores_no_likelihood_no_verdict",
        }
    ]
    assert "tau_cmb_density_amplitude_closure_v01" in note
    assert "completes no closure" in note


def test_tau_cmb_density_amplitude_closure_is_partial_and_score_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_density_amplitude_closure_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_density_amplitude_closure_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_density_amplitude_closure_v01.md").read_text()

    assert len(rows) == 5
    assert [row["closure_check"] for row in rows] == [
        "density_ratio_dimension_check",
        "tau_effective_density_formula",
        "endpoint_blind_amplitude_derivation",
        "omega_c_h2_role_comparison",
        "density_stop_rule",
    ]
    assert sum(row["closure_result"].startswith("CLOSED") for row in rows) == 1
    assert sum(row["closure_result"].startswith("BLOCKED") for row in rows) == 3
    assert sum(row["closure_result"].startswith("PARTIAL_CLOSURE") for row in rows) == 1
    assert {row["can_compute_density_score"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_DENSITY_AMPLITUDE_CLOSURE_V01",
            "closure_rows_declared": "5",
            "closed_rows": "1",
            "partial_closure_rows": "1",
            "blocked_rows": "3",
            "hard_failures_triggered": "0",
            "can_compute_density_score": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "5",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "DENSITY_AMPLITUDE_PARTIAL_CLOSURE_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_acoustic_reduced_evaluation_v01",
            "claim_boundary": "tau_cmb_density_amplitude_closure_v01_partial_closure_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "partial closure" in note
    assert "density score therefore remains blocked" in note


def test_tau_cmb_acoustic_reduced_evaluation_is_partial_and_score_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_reduced_evaluation_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_reduced_evaluation_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_acoustic_reduced_evaluation_v01.md").read_text()

    assert len(rows) == 6
    assert [row["benchmark_component"] for row in rows] == [
        "potential_source_presence",
        "acoustic_phase_support",
        "relative_peak_height_support",
        "baryon_loading_compatibility",
        "scale_horizon_convention",
        "explicit_failure_branch",
    ]
    assert sum(row["evaluation_result"].startswith("CLOSED") for row in rows) == 1
    assert sum(row["evaluation_result"].startswith("BLOCKED") for row in rows) == 4
    assert sum(row["evaluation_result"].startswith("PARTIAL_EVALUATION") for row in rows) == 1
    assert {row["can_compute_acoustic_score"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_ACOUSTIC_REDUCED_EVALUATION_V01",
            "evaluation_rows_declared": "6",
            "closed_rows": "1",
            "partial_evaluation_rows": "1",
            "blocked_rows": "4",
            "hard_failures_triggered": "0",
            "can_compute_acoustic_score": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "6",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACOUSTIC_REDUCED_EVALUATION_PARTIAL_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_lensing_transfer_reduced_evaluation_v01",
            "claim_boundary": "tau_cmb_acoustic_reduced_evaluation_v01_partial_evaluation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "partial evaluation" in note
    assert "acoustic score therefore remains blocked" in note


def test_tau_cmb_lensing_transfer_reduced_evaluation_is_partial_and_score_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_lensing_transfer_reduced_evaluation_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_lensing_transfer_reduced_evaluation_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_lensing_transfer_reduced_evaluation_v01.md").read_text()

    assert len(rows) == 6
    assert [row["benchmark_component"] for row in rows] == [
        "lensing_potential_source_presence",
        "transfer_kernel_presence",
        "projection_geometry_convention",
        "amplitude_shape_support",
        "cross_readout_consistency",
        "explicit_failure_branch",
    ]
    assert sum(row["evaluation_result"].startswith("CLOSED") for row in rows) == 1
    assert sum(row["evaluation_result"].startswith("BLOCKED") for row in rows) == 4
    assert sum(row["evaluation_result"].startswith("PARTIAL_EVALUATION") for row in rows) == 1
    assert {row["can_compute_lensing_score"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_LENSING_TRANSFER_REDUCED_EVALUATION_V01",
            "evaluation_rows_declared": "6",
            "closed_rows": "1",
            "partial_evaluation_rows": "1",
            "blocked_rows": "4",
            "hard_failures_triggered": "0",
            "can_compute_lensing_score": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "6",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "LENSING_TRANSFER_REDUCED_EVALUATION_PARTIAL_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_growth_transfer_kernel_closure_v01",
            "claim_boundary": "tau_cmb_lensing_transfer_reduced_evaluation_v01_partial_evaluation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "partial evaluation" in note
    assert "lensing score therefore remains blocked" in note


def test_tau_cmb_growth_transfer_kernel_closure_is_partial_and_score_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_growth_transfer_kernel_closure_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_growth_transfer_kernel_closure_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_growth_transfer_kernel_closure_v01.md").read_text()

    assert len(rows) == 6
    assert [row["kernel_component"] for row in rows] == [
        "domain_specification",
        "codomain_specification",
        "time_scale_convention",
        "operator_rule",
        "cross_role_consistency",
        "explicit_failure_branch",
    ]
    assert sum(row["closure_result"].startswith("CLOSED") for row in rows) == 1
    assert sum(row["closure_result"].startswith("PARTIAL_CLOSURE") for row in rows) == 3
    assert sum(row["closure_result"].startswith("BLOCKED") for row in rows) == 2
    assert {row["can_compute_growth_score"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_GROWTH_TRANSFER_KERNEL_CLOSURE_V01",
            "closure_rows_declared": "6",
            "closed_rows": "1",
            "partial_closure_rows": "3",
            "blocked_rows": "2",
            "hard_failures_triggered": "0",
            "can_compute_growth_score": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "6",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "GROWTH_TRANSFER_KERNEL_PARTIAL_CLOSURE_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_radiation_guard_evaluation_v01",
            "claim_boundary": "tau_cmb_growth_transfer_kernel_closure_v01_partial_closure_no_operator_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "partial closure" in note
    assert "growth score therefore remains blocked" in note


def test_tau_cmb_radiation_guard_evaluation_is_partial_and_score_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_radiation_guard_evaluation_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_radiation_guard_evaluation_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_radiation_guard_evaluation_v01.md").read_text()

    assert len(rows) == 5
    assert [row["guard_component"] for row in rows] == [
        "tau_radiation_like_contribution",
        "external_bound_convention",
        "damping_tail_guard",
        "cross_role_consistency",
        "explicit_failure_branch",
    ]
    assert sum(row["evaluation_result"].startswith("CLOSED") for row in rows) == 1
    assert sum(row["evaluation_result"].startswith("PARTIAL_EVALUATION") for row in rows) == 1
    assert sum(row["evaluation_result"].startswith("BLOCKED") for row in rows) == 3
    assert {row["can_compute_radiation_score"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 0
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_RADIATION_GUARD_EVALUATION_V01",
            "evaluation_rows_declared": "5",
            "closed_rows": "1",
            "partial_evaluation_rows": "1",
            "blocked_rows": "3",
            "hard_failures_triggered": "0",
            "can_compute_radiation_score": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "0",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "RADIATION_GUARD_EVALUATION_PARTIAL_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_known_limit_decision_update_v01",
            "claim_boundary": "tau_cmb_radiation_guard_evaluation_v01_partial_evaluation_no_bound_score_no_likelihood_no_verdict",
        }
    ]
    assert "partial evaluation" in note
    assert "radiation score therefore remains blocked" in note


def test_tau_cmb_known_limit_decision_update_keeps_all_roles_unresolved() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_known_limit_decision_update_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_known_limit_decision_update_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_known_limit_decision_update_v01.md").read_text()

    assert len(rows) == 6
    assert [row["cmb_role"] for row in rows] == [
        "acoustic_peak_phase_and_height",
        "omega_c_h2_density_inference",
        "cmb_lensing_potential",
        "damping_tail_and_radiation_guard",
        "growth_seed_and_transfer_consistency",
        "known_limit_or_explicit_failure",
    ]
    assert {row["prior_decision_state"] for row in rows} == {"UNRESOLVED_INPUT_MISSING"}
    assert {row["updated_decision_state"] for row in rows} == {"UNRESOLVED_EVIDENCE_INSUFFICIENT"}
    assert {row["score_ready"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_KNOWN_LIMIT_DECISION_UPDATE_V01",
            "decision_rows_declared": "6",
            "resolved_rows": "0",
            "unresolved_rows": "6",
            "failures_declared": "0",
            "reproductions_declared": "0",
            "approximations_declared": "0",
            "hard_failures_triggered": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "5",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "KNOWN_LIMIT_DECISION_UPDATE_ALL_ROLES_UNRESOLVED_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_scorecard_prescore_blocker_summary_v01",
            "claim_boundary": "tau_cmb_known_limit_decision_update_v01_no_role_resolved_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "No role is promoted" in note
    assert "scorecard blocked" in note


def test_tau_cmb_scorecard_prescore_blocker_summary_blocks_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_scorecard_prescore_blocker_summary_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_scorecard_prescore_blocker_summary_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_scorecard_prescore_blocker_summary_v01.md").read_text()

    assert len(rows) == 6
    assert [row["cmb_role"] for row in rows] == [
        "acoustic_peak_phase_and_height",
        "omega_c_h2_density_inference",
        "cmb_lensing_potential",
        "damping_tail_and_radiation_guard",
        "growth_seed_and_transfer_consistency",
        "known_limit_or_explicit_failure",
    ]
    assert {row["decision_state"] for row in rows} == {"UNRESOLVED_EVIDENCE_INSUFFICIENT"}
    assert {row["score_gate_status"] for row in rows} == {"SCORE_BLOCKED_UNRESOLVED_EVIDENCE"}
    assert {row["score_ready"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_SCORECARD_PRESCORE_BLOCKER_SUMMARY_V01",
            "blocker_rows_declared": "6",
            "score_ready_rows": "0",
            "score_blocked_rows": "6",
            "unresolved_rows": "6",
            "hard_failures_triggered": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "5",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PRESCORE_BLOCKERS_SUMMARIZED_ALL_SCORE_ROWS_BLOCKED",
            "next_required_artifact": "tau_cmb_minimal_scoring_input_contract_v01",
            "claim_boundary": "tau_cmb_scorecard_prescore_blocker_summary_v01_summary_only_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "score_ready_rows = 0" in note
    assert "prevents a premature scorecard" in note


def test_tau_cmb_minimal_scoring_input_contract_blocks_score_entry() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_minimal_scoring_input_contract_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_minimal_scoring_input_contract_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_minimal_scoring_input_contract_v01.md").read_text()

    assert len(rows) == 6
    assert [row["cmb_role"] for row in rows] == [
        "acoustic_peak_phase_and_height",
        "omega_c_h2_density_inference",
        "cmb_lensing_potential",
        "damping_tail_and_radiation_guard",
        "growth_seed_and_transfer_consistency",
        "known_limit_or_explicit_failure",
    ]
    assert {row["current_contract_status"] for row in rows} == {"UNSATISFIED_INPUT_MISSING"}
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert all(row["required_scoring_input"] for row in rows)
    assert all(row["contract_requirement"] for row in rows)
    assert all(row["missing_condition"] for row in rows)
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_MINIMAL_SCORING_INPUT_CONTRACT_V01",
            "contract_rows_declared": "6",
            "satisfied_rows": "0",
            "unsatisfied_rows": "6",
            "score_entry_allowed_rows": "0",
            "hard_failures_triggered": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "5",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "MINIMAL_SCORING_INPUT_CONTRACT_DECLARED_ALL_INPUTS_UNSATISFIED",
            "next_required_artifact": "tau_cmb_scoring_execution_gate_v01",
            "claim_boundary": "tau_cmb_minimal_scoring_input_contract_v01_contract_only_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "UNSATISFIED_INPUT_MISSING" in note
    assert "score_entry_allowed_rows = 0" in note


def test_tau_cmb_scoring_execution_gate_blocks_run() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_scoring_execution_gate_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_scoring_execution_gate_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_scoring_execution_gate_v01.md").read_text()

    assert len(rows) == 6
    assert [row["cmb_role"] for row in rows] == [
        "acoustic_peak_phase_and_height",
        "omega_c_h2_density_inference",
        "cmb_lensing_potential",
        "damping_tail_and_radiation_guard",
        "growth_seed_and_transfer_consistency",
        "known_limit_or_explicit_failure",
    ]
    assert {row["contract_status"] for row in rows} == {"UNSATISFIED_INPUT_MISSING"}
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["execution_gate_decision"] for row in rows} == {"SCORING_BLOCKED"}
    assert {row["score_computed"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["blocking_reason"] for row in rows)
    assert all(row["required_before_run"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_SCORING_EXECUTION_GATE_V01",
            "gate_rows_declared": "6",
            "run_allowed_rows": "0",
            "run_blocked_rows": "6",
            "score_computed_rows": "0",
            "hard_failures_triggered": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "5",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORING_EXECUTION_GATE_BLOCKED_ALL_ROWS",
            "next_required_artifact": "tau_cmb_scoring_input_fulfillment_plan_v01",
            "claim_boundary": "tau_cmb_scoring_execution_gate_v01_gate_only_scoring_blocked_no_likelihood_no_verdict",
        }
    ]
    assert "SCORING_BLOCKED" in note
    assert "score_computed_rows = 0" in note


def test_tau_cmb_scoring_input_fulfillment_plan_is_ranked_and_pending() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_scoring_input_fulfillment_plan_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_scoring_input_fulfillment_plan_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_scoring_input_fulfillment_plan_v01.md").read_text()

    assert len(rows) == 6
    assert [row["priority_rank"] for row in rows] == ["1", "2", "3", "4", "5", "6"]
    assert [row["cmb_role"] for row in rows] == [
        "acoustic_peak_phase_and_height",
        "omega_c_h2_density_inference",
        "growth_seed_and_transfer_consistency",
        "cmb_lensing_potential",
        "damping_tail_and_radiation_guard",
        "known_limit_or_explicit_failure",
    ]
    assert {row["blocked_gate_decision"] for row in rows} == {"SCORING_BLOCKED"}
    assert {row["completed_in_v01"] for row in rows} == {"false"}
    assert {row["score_entry_allowed_after_completion"] for row in rows} == {"true"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["fulfillment_action"] for row in rows)
    assert all(row["acceptance_criterion"] for row in rows)
    assert all(row["required_artifact_to_build"] for row in rows)
    assert all(row["stop_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_SCORING_INPUT_FULFILLMENT_PLAN_V01",
            "fulfillment_rows_declared": "6",
            "ranked_rows": "6",
            "completed_rows": "0",
            "pending_rows": "6",
            "hard_failures_triggered": "0",
            "score_entry_allowed_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "5",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORING_INPUT_FULFILLMENT_PLAN_DECLARED_NO_INPUTS_COMPLETED",
            "next_required_artifact": "tau_cmb_effective_potential_source_handoff_v01",
            "claim_boundary": "tau_cmb_scoring_input_fulfillment_plan_v01_plan_only_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "completed_rows = 0" in note
    assert "tau_cmb_effective_potential_source_handoff_v01" in note


def test_tau_cmb_planck_pr3_peak_source_freeze_packet_selects_sources_without_scoring() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_source_freeze_packet_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_source_freeze_packet_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_planck_pr3_peak_source_freeze_packet_v01.md").read_text()

    assert len(rows) == 4
    assert [row["artifact_id"] for row in rows] == [
        "PLANCK_PR3_PEAKSRC_001",
        "PLANCK_PR3_PEAKSRC_002",
        "PLANCK_PR3_PEAKSRC_003",
        "PLANCK_PR3_PEAKSRC_004",
    ]
    assert {row["cmb_role"] for row in rows} == {
        "acoustic_peak_phase_and_height",
        "known_limit_or_explicit_failure",
    }
    assert all(
        row["official_url"].startswith(
            "https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/cosmoparams/"
        )
        for row in rows
    )
    assert {row["download_status"] for row in rows} == {"NOT_DOWNLOADED_BY_REPRO_PACKAGE"}
    assert {row["raw_artifact_hash"] for row in rows} == {"NOT_COMPUTED"}
    assert {row["extraction_status"] for row in rows} == {"DECLARED_NOT_EXECUTED"}
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PLANCK_PR3_PEAK_SOURCE_FREEZE_PACKET_V01",
            "artifact_rows_declared": "4",
            "artifact_urls_selected": "4",
            "local_hashes_computed": "0",
            "extraction_rules_declared": "2",
            "extraction_rules_executed": "0",
            "score_ready": "false",
            "score_entry_allowed_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PLANCK_PR3_ARTIFACT_URLS_SELECTED_EXTRACTION_FREEZE_PENDING",
            "next_required_artifact": "tau_cmb_planck_pr3_peak_extraction_rule_v01",
            "claim_boundary": "tau_cmb_planck_pr3_peak_source_freeze_packet_v01_source_freeze_only_no_download_no_extraction_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "artifact_urls_selected = 4" in note
    assert "score_ready = false" in note
    assert "tau_cmb_planck_pr3_peak_extraction_rule_v01" in note


def test_tau_cmb_planck_pr3_peak_extraction_rule_materializes_observable_table_without_scoring() -> None:
    receipts = list(csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_source_receipt_v01.csv").open()))
    peaks = list(csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_observable_table_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_extraction_rule_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_planck_pr3_peak_extraction_rule_v01.md").read_text()

    assert len(receipts) == 4
    assert len(peaks) == 36
    assert {row["download_status"] for row in receipts} == {"DOWNLOADED_TO_GITIGNORED_EXTERNAL_CACHE"}
    assert all(len(row["sha256"]) == 64 for row in receipts)
    assert sum(row["spectrum"] == "TT" for row in peaks) == 10
    assert sum(row["spectrum"] == "TE" for row in peaks) == 13
    assert sum(row["spectrum"] == "EE" for row in peaks) == 13
    assert peaks[0]["peak_id"] == "TT_PEAK_01"
    assert peaks[0]["ell_center"] == "225.164945"
    assert peaks[0]["D_ell"] == "5793.43954"
    assert peaks[0]["best_fit_D_ell"] == "5726.93135"
    assert {row["score_entry_allowed"] for row in peaks} == {"false"}
    assert {row["allows_tau_response_claim"] for row in peaks} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in peaks} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PLANCK_PR3_PEAK_EXTRACTION_RULE_V01",
            "source_artifacts_declared": "4",
            "source_artifacts_downloaded": "4",
            "source_hashes_computed": "4",
            "spectra_peak_extracted": "3",
            "peak_rows_extracted": "36",
            "tt_peak_rows": "10",
            "te_extremum_rows": "13",
            "ee_peak_rows": "13",
            "minimum_theory_reference_downloaded": "true",
            "parser_rule_frozen": "true",
            "observable_table_materialized": "true",
            "score_ready": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PLANCK_PR3_PEAK_OBSERVABLE_TABLE_MATERIALIZED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_planck_pr3_peak_scoring_input_candidate_v01",
            "claim_boundary": "tau_cmb_planck_pr3_peak_extraction_rule_v01_observable_extraction_only_no_tau_prediction_no_likelihood_no_score_no_dark_sector_verdict",
        }
    ]
    assert "peak_rows_extracted = 36" in note
    assert "score_ready = false" in note
    assert "tau_cmb_planck_pr3_peak_scoring_input_candidate_v01" in note


def test_tau_cmb_planck_pr3_peak_scoring_input_candidate_observed_side_ready_but_score_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_scoring_input_candidate_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_scoring_input_candidate_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_planck_pr3_peak_scoring_input_candidate_v01.md").read_text()

    assert len(rows) == 36
    assert {row["cmb_role"] for row in rows} == {"acoustic_peak_phase_and_height"}
    assert {row["observable_family"] for row in rows} == {"planck_pr3_binned_peak_observable"}
    assert sum(row["spectrum"] == "TT" for row in rows) == 10
    assert sum(row["spectrum"] == "TE" for row in rows) == 13
    assert sum(row["spectrum"] == "EE" for row in rows) == 13
    assert {row["observed_side_ready"] for row in rows} == {"true"}
    assert {row["tau_prediction_required"] for row in rows} == {"true"}
    assert {row["tau_prediction_supplied"] for row in rows} == {"false"}
    assert {row["null_response_supplied"] for row in rows} == {"false"}
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["score_blocker"] for row in rows} == {"TAU_PREDICTION_OR_NULL_RESPONSE_NOT_SUPPLIED"}
    assert rows[0]["candidate_id"] == "TCMBP3PSC01_001"
    assert rows[0]["source_peak_id"] == "TT_PEAK_01"
    assert rows[0]["ell_center"] == "225.164945"
    assert summary == [
        {
            "summary_id": "TAU_CMB_PLANCK_PR3_PEAK_SCORING_INPUT_CANDIDATE_V01",
            "candidate_rows_declared": "36",
            "observed_side_ready_rows": "36",
            "comparison_rule_declared_rows": "36",
            "tau_prediction_required_rows": "36",
            "tau_prediction_supplied_rows": "0",
            "null_response_supplied_rows": "0",
            "score_ready_rows": "0",
            "observed_side_fulfillment_score": "1.000000",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "OBSERVED_PEAK_SCORING_INPUT_CANDIDATE_READY_TAU_PREDICTION_MISSING_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01",
            "claim_boundary": "tau_cmb_planck_pr3_peak_scoring_input_candidate_v01_observed_side_candidate_only_no_tau_prediction_no_score_no_likelihood_no_dark_sector_verdict",
        }
    ]
    assert "observed_side_fulfillment_score = 1.000000" in note
    assert "score_ready_rows = 0" in note
    assert "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01" in note


def test_tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_blocks_score() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01.md").read_text()

    assert len(rows) == 36
    assert {row["tau_prediction_status"] for row in rows} == {"NOT_SUPPLIED"}
    assert {row["null_response_status"] for row in rows} == {"NOT_SUPPLIED"}
    assert {row["admissible_response_status"] for row in rows} == {"NO_ADMISSIBLE_TAU_RESPONSE_OR_NULL_RESPONSE"}
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["score_blocker"] for row in rows} == {"TAU_SIDE_PREDICTION_AND_NULL_RESPONSE_BOTH_MISSING"}
    assert {row["hard_failure_triggered"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PLANCK_PR3_PEAK_TAU_PREDICTION_OR_NULL_RESPONSE_V01",
            "response_rows_declared": "36",
            "observed_candidate_rows_checked": "36",
            "tau_prediction_required_rows": "36",
            "tau_prediction_supplied_rows": "0",
            "null_response_supplied_rows": "0",
            "admissible_response_rows": "0",
            "score_ready_rows": "0",
            "explicit_missing_response_rows": "36",
            "hard_failures_triggered": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "TAU_SIDE_PEAK_RESPONSE_AUDITED_NO_PREDICTION_OR_NULL_RESPONSE_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_planck_pr3_peak_score_attempt_guard_v01",
            "claim_boundary": "tau_cmb_planck_pr3_peak_tau_prediction_or_null_response_v01_tau_side_response_audit_only_no_prediction_no_null_response_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "score_ready_rows = 0" in note
    assert "tau_cmb_planck_pr3_peak_score_attempt_guard_v01" in note


def test_tau_cmb_planck_pr3_peak_score_attempt_guard_blocks_score() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_score_attempt_guard_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_score_attempt_guard_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_planck_pr3_peak_score_attempt_guard_v01.md").read_text()

    assert len(rows) == 3
    assert sum(row["guard_decision"] == "GUARD_PASSED" for row in rows) == 1
    assert sum(row["guard_decision"] == "SCORE_ATTEMPT_BLOCKED" for row in rows) == 2
    assert {row["hard_failure_triggered"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PLANCK_PR3_PEAK_SCORE_ATTEMPT_GUARD_V01",
            "guard_rows_declared": "3",
            "guard_pass_rows": "1",
            "guard_block_rows": "2",
            "observed_side_ready": "true",
            "tau_side_response_ready": "false",
            "score_attempt_allowed": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "hard_failures_triggered": "0",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PLANCK_PR3_PEAK_SCORE_ATTEMPT_BLOCKED_TAU_SIDE_RESPONSE_MISSING",
            "next_required_artifact": "tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01",
            "claim_boundary": "tau_cmb_planck_pr3_peak_score_attempt_guard_v01_guard_only_score_blocked_no_likelihood_no_tau_response_claim_no_dark_sector_verdict",
        }
    ]
    assert "observed_side_ready = true" in note
    assert "tau_side_response_ready = false" in note
    assert "score_attempt_allowed = false" in note


def test_tau_cmb_planck_pr3_peak_tau_prediction_materialization_spec_blocks_score_until_payload_exists() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_materialization_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01.md").read_text()

    assert len(rows) == 36
    assert {row["tau_prediction_value_status"] for row in rows} == {"MISSING"}
    assert {row["tau_prediction_ell_status"] for row in rows} == {"MISSING"}
    assert {row["tau_prediction_amplitude_status"] for row in rows} == {"MISSING"}
    assert {row["tau_prediction_source_artifact_status"] for row in rows} == {"MISSING"}
    assert {row["materialization_acceptance_status"] for row in rows} == {
        "BLOCKED_TAU_PREDICTION_PAYLOAD_NOT_MATERIALIZED"
    }
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["score_blocker"] for row in rows} == {"ENDPOINT_BLIND_TAU_PEAK_PREDICTION_PAYLOAD_MISSING"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PLANCK_PR3_PEAK_TAU_PREDICTION_MATERIALIZATION_V01",
            "materialization_rows_declared": "36",
            "observed_candidate_rows_checked": "36",
            "required_tau_payload_rows": "36",
            "tau_prediction_value_rows": "0",
            "tau_prediction_ell_rows": "0",
            "tau_prediction_amplitude_rows": "0",
            "tau_prediction_source_artifact_rows": "0",
            "endpoint_blind_attestation_rows": "0",
            "convention_lock_rows": "0",
            "uncertainty_model_rows": "0",
            "accepted_materialization_rows": "0",
            "score_ready_rows": "0",
            "missing_prediction_rows": "36",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "TAU_PEAK_PREDICTION_MATERIALIZATION_SPEC_READY_PAYLOAD_MISSING_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01",
            "claim_boundary": "tau_cmb_planck_pr3_peak_tau_prediction_materialization_v01_materialization_spec_only_no_tau_prediction_no_score_no_likelihood_no_dark_sector_verdict",
        }
    ]
    assert "score_ready_rows = 0" in note
    assert "tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01" in note
    assert "not a Tau acoustic prediction" in note


def test_tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_explicitly_closes_empty_payload_path() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01.md").read_text()

    assert len(rows) == 36
    assert {row["supply_mode"] for row in rows} == {
        "EXPLICIT_EMPTY_SUPPLY_NO_ENDPOINT_BLIND_TAU_ACOUSTIC_PREDICTION_AVAILABLE"
    }
    assert {row["endpoint_blind_derivation_trace_status"] for row in rows} == {"MISSING"}
    assert {row["predicted_ell_center"] for row in rows} == {"NA"}
    assert {row["predicted_observable_value"] for row in rows} == {"NA"}
    assert {row["prediction_uncertainty"] for row in rows} == {"NA"}
    assert {row["endpoint_blind_attestation_status"] for row in rows} == {"MISSING"}
    assert {row["null_response_control_status"] for row in rows} == {"NOT_SUPPLIED"}
    assert {row["payload_acceptance_decision"] for row in rows} == {
        "REJECTED_NO_TAU_PREDICTION_OR_NULL_RESPONSE_PAYLOAD"
    }
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["score_blocker"] for row in rows} == {"TAU_PEAK_PAYLOAD_SUPPLY_EXPLICITLY_EMPTY"}
    assert {row["hard_failure_triggered"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PLANCK_PR3_PEAK_TAU_PREDICTION_PAYLOAD_SUPPLY_V01",
            "payload_supply_rows_declared": "36",
            "materialization_rows_checked": "36",
            "explicit_empty_supply_rows": "36",
            "tau_prediction_payload_rows": "0",
            "null_response_control_rows": "0",
            "endpoint_blind_attestation_rows": "0",
            "convention_lock_rows": "0",
            "comparison_rule_rows": "0",
            "accepted_payload_rows": "0",
            "rejected_payload_rows": "36",
            "score_ready_rows": "0",
            "hard_failures_triggered": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "TAU_PEAK_PREDICTION_PAYLOAD_SUPPLY_EXPLICIT_EMPTY_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_acoustic_tau_prediction_source_derivation_v01",
            "claim_boundary": "tau_cmb_planck_pr3_peak_tau_prediction_payload_supply_v01_explicit_empty_supply_no_tau_prediction_no_null_response_no_score_no_likelihood_no_dark_sector_verdict",
        }
    ]
    assert "explicit_empty_supply_rows = 36" in note
    assert "tau_cmb_acoustic_tau_prediction_source_derivation_v01" in note
    assert "not a Tau acoustic prediction" in note


def test_tau_cmb_acoustic_tau_prediction_source_derivation_declares_spine_without_score() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_tau_prediction_source_derivation_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_tau_prediction_source_derivation_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_acoustic_tau_prediction_source_derivation_v01.md").read_text()

    assert len(rows) == 8
    assert any(
        row["symbolic_object"] == "S_tau_ac(k,a)"
        and row["derivation_status"] == "FORMAL_DEFINITION_ONLY_NOT_DERIVED"
        for row in rows
    )
    assert sum(row["derivation_status"].startswith("BLOCKED") for row in rows) == 6
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_ACOUSTIC_TAU_PREDICTION_SOURCE_DERIVATION_V01",
            "derivation_rows_declared": "8",
            "formal_definition_rows": "1",
            "dependency_rows": "5",
            "missing_dependency_rows": "6",
            "derived_source_rows": "0",
            "executable_prediction_rows": "0",
            "accepted_planck_payload_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACOUSTIC_TAU_PREDICTION_SOURCE_DERIVATION_SPINE_DECLARED_SOURCE_NOT_DERIVED_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_acoustic_source_operator_payload_v01",
            "claim_boundary": "tau_cmb_acoustic_tau_prediction_source_derivation_v01_derivation_spine_only_no_acoustic_source_solution_no_peak_prediction_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "S_tau_ac(k,a) := P_ac[Phi_tau_eff,A_tau,Theta_tau_ac,C_rec](k,a)" in note
    assert "derived_source_rows = 0" in note
    assert "not a physical CMB solution" in note


def test_tau_cmb_acoustic_source_operator_payload_contract_keeps_score_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_source_operator_payload_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_source_operator_payload_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_acoustic_source_operator_payload_v01.md").read_text()

    assert len(rows) == 8
    assert [row["operator_component"] for row in rows] == [
        "domain_and_basis_lock",
        "effective_potential_input",
        "amplitude_input",
        "oscillator_kernel_rule",
        "baryon_loading_coupling",
        "projection_rule_to_peak_payload",
        "uncertainty_and_null_policy",
        "score_firewall",
    ]
    assert sum(row["payload_status"] == "REQUIRED_NOT_SUPPLIED" for row in rows) == 7
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_V01",
            "operator_rows_declared": "8",
            "required_operator_payload_rows": "7",
            "payload_supplied_rows": "0",
            "payload_accepted_rows": "0",
            "payload_rejected_rows": "7",
            "endpoint_blind_pass_rows": "1",
            "dimension_convention_pass_rows": "1",
            "derived_source_rows": "0",
            "executable_prediction_rows": "0",
            "accepted_planck_payload_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_CONTRACT_DECLARED_PAYLOAD_NOT_SUPPLIED_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_acoustic_source_operator_payload_supply_v01",
            "claim_boundary": "tau_cmb_acoustic_source_operator_payload_v01_operator_payload_contract_only_no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "required_operator_payload_rows = 7" in note
    assert "tau_cmb_acoustic_source_operator_payload_supply_v01" in note
    assert "does not solve the acoustic operator" in note


def test_tau_cmb_acoustic_source_operator_payload_supply_explicitly_blocks_score() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_source_operator_payload_supply_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_source_operator_payload_supply_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_acoustic_source_operator_payload_supply_v01.md").read_text()

    assert len(rows) == 8
    assert [row["operator_component"] for row in rows] == [
        "domain_and_basis_lock",
        "effective_potential_input",
        "amplitude_input",
        "oscillator_kernel_rule",
        "baryon_loading_coupling",
        "projection_rule_to_peak_payload",
        "uncertainty_and_null_policy",
        "score_firewall",
    ]
    assert sum(row["supply_mode"] == "EXPLICIT_EMPTY_OPERATOR_PAYLOAD_SUPPLY" for row in rows) == 7
    assert sum(row["acceptance_decision"] == "REJECTED_OPERATOR_PAYLOAD_SUPPLY_EMPTY" for row in rows) == 7
    assert sum(row["supply_mode"] == "FIREWALL_PRESERVED" for row in rows) == 1
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_SUPPLY_V01",
            "supply_rows_declared": "8",
            "required_operator_payload_rows_checked": "7",
            "operator_payload_supplied_rows": "0",
            "operator_payload_accepted_rows": "0",
            "operator_payload_rejected_rows": "7",
            "firewall_preserved_rows": "1",
            "derived_source_rows": "0",
            "executable_prediction_rows": "0",
            "accepted_planck_payload_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACOUSTIC_SOURCE_OPERATOR_PAYLOAD_SUPPLY_EXPLICIT_EMPTY_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_acoustic_minimal_operator_model_attempt_v01",
            "claim_boundary": "tau_cmb_acoustic_source_operator_payload_supply_v01_explicit_empty_supply_no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "operator_payload_rejected_rows = 7" in note
    assert "tau_cmb_acoustic_minimal_operator_model_attempt_v01" in note
    assert "does not solve the acoustic operator" in note


def test_tau_cmb_acoustic_minimal_operator_model_attempt_declares_formula_scaffold_without_score() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_minimal_operator_model_attempt_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_minimal_operator_model_attempt_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_acoustic_minimal_operator_model_attempt_v01.md").read_text()

    assert len(rows) == 8
    assert [row["operator_component"] for row in rows] == [
        "domain_and_basis_lock",
        "effective_potential_input",
        "amplitude_input",
        "oscillator_kernel_rule",
        "baryon_loading_coupling",
        "projection_rule_to_peak_payload",
        "uncertainty_and_null_policy",
        "score_firewall",
    ]
    assert sum(row["attempt_status"] == "FORMULA_SCAFFOLD_DECLARED_NOT_EXECUTABLE" for row in rows) == 3
    assert sum(row["attempt_status"] == "DEPENDENCY_BLOCKED" for row in rows) == 3
    assert sum(row["attempt_status"] == "CANDIDATE_RULE_DECLARED_NOT_ACCEPTED" for row in rows) == 1
    assert sum(row["attempt_status"] == "FIREWALL_PRESERVED" for row in rows) == 1
    assert {row["acceptance_decision"] for row in rows} == {"REJECTED_OPERATOR_MODEL_ROW_NOT_EXECUTABLE"}
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_ACOUSTIC_MINIMAL_OPERATOR_MODEL_ATTEMPT_V01",
            "model_rows_declared": "8",
            "candidate_rule_rows_declared": "4",
            "dependency_blocked_rows": "3",
            "dimensionally_closed_rows": "0",
            "known_limit_closed_rows": "0",
            "operator_model_accepted_rows": "0",
            "derived_source_rows": "0",
            "executable_prediction_rows": "0",
            "accepted_planck_payload_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACOUSTIC_MINIMAL_OPERATOR_MODEL_ATTEMPT_DECLARED_NOT_EXECUTABLE_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_acoustic_operator_dependency_unblock_plan_v01",
            "claim_boundary": "tau_cmb_acoustic_minimal_operator_model_attempt_v01_model_scaffold_only_no_executable_operator_no_peak_prediction_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "Theta_tau_ac(k,a_rec) = integral da G_tau_ac(k,a;a_rec) S_tau_ac(k,a)" in note
    assert "tau_cmb_acoustic_operator_dependency_unblock_plan_v01" in note
    assert "does not solve the acoustic operator" in note


def test_tau_cmb_acoustic_operator_dependency_unblock_plan_orders_blockers_without_score() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_operator_dependency_unblock_plan_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_operator_dependency_unblock_plan_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_acoustic_operator_dependency_unblock_plan_v01.md").read_text()

    assert len(rows) == 8
    assert [row["operator_component"] for row in rows] == [
        "domain_and_basis_lock",
        "effective_potential_input",
        "amplitude_input",
        "oscillator_kernel_rule",
        "baryon_loading_coupling",
        "projection_rule_to_peak_payload",
        "uncertainty_and_null_policy",
        "score_firewall",
    ]
    assert [row["priority_order"] for row in rows] == [str(i) for i in range(1, 9)]
    assert rows[0]["required_unblock_artifact"] == "tau_cmb_acoustic_domain_basis_lock_acceptance_v01"
    assert {row["unblock_status"] for row in rows} == {"DECLARED_NOT_COMPLETED"}
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_ACOUSTIC_OPERATOR_DEPENDENCY_UNBLOCK_PLAN_V01",
            "unblock_rows_declared": "8",
            "critical_unblock_rows": "7",
            "completed_unblock_rows": "0",
            "pending_unblock_rows": "8",
            "operator_model_accepted_rows": "0",
            "derived_source_rows": "0",
            "executable_prediction_rows": "0",
            "accepted_planck_payload_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACOUSTIC_OPERATOR_DEPENDENCY_UNBLOCK_PLAN_DECLARED_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_acoustic_domain_basis_lock_acceptance_v01",
            "claim_boundary": "tau_cmb_acoustic_operator_dependency_unblock_plan_v01_unblock_plan_only_no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "critical_unblock_rows = 7" in note
    assert "tau_cmb_acoustic_domain_basis_lock_acceptance_v01" in note
    assert "does not solve the acoustic operator" in note


def test_tau_cmb_acoustic_domain_basis_lock_acceptance_closes_first_convention_row_without_score() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_domain_basis_lock_acceptance_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_acoustic_domain_basis_lock_acceptance_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_acoustic_domain_basis_lock_acceptance_v01.md").read_text()

    assert len(rows) == 7
    assert [row["basis_component"] for row in rows] == [
        "wavenumber_domain",
        "scale_readout_domain",
        "recombination_readout_slice",
        "angular_peak_coordinate",
        "integration_measure_placeholder",
        "spectrum_role_basis",
        "comparison_boundary",
    ]
    assert {row["acceptance_decision"] for row in rows} == {"ACCEPTED_DOMAIN_BASIS_LOCK_ROW"}
    assert {row["endpoint_blind_status"] for row in rows} == {"PASS_NO_ENDPOINT_RESIDUALS_READ"}
    assert {row["dimension_convention_status"] for row in rows} == {"LOCKED_CONVENTION_ONLY"}
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_ACOUSTIC_DOMAIN_BASIS_LOCK_ACCEPTANCE_V01",
            "lock_rows_declared": "7",
            "lock_rows_accepted": "7",
            "endpoint_blind_pass_rows": "7",
            "dimension_convention_locked_rows": "7",
            "domain_basis_lock_accepted": "true",
            "operator_model_accepted_rows": "1",
            "derived_source_rows": "0",
            "executable_prediction_rows": "0",
            "accepted_planck_payload_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACOUSTIC_DOMAIN_BASIS_LOCK_ACCEPTED_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01",
            "claim_boundary": "tau_cmb_acoustic_domain_basis_lock_acceptance_v01_convention_lock_only_no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "domain_basis_lock_accepted = true" in note
    assert "tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01" in note
    assert "does not solve the acoustic operator" in note


def test_tau_cmb_phi_tau_eff_acoustic_input_acceptance_accepts_identity_only_without_score() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_eff_acoustic_input_acceptance_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01.md").read_text()

    assert len(rows) == 6
    assert [row["input_component"] for row in rows] == [
        "source_slot_identity",
        "endpoint_blind_provenance",
        "normalization_convention",
        "timing_sign_convention",
        "baryon_photon_coupling_role",
        "score_firewall",
    ]
    assert sum(row["acceptance_status"].startswith("ACCEPTED") for row in rows) == 1
    assert sum(row["acceptance_status"].startswith("BLOCKED") for row in rows) == 3
    assert sum(row["acceptance_status"].startswith("PARTIAL") for row in rows) == 1
    assert sum(row["acceptance_status"] == "FIREWALL_PRESERVED" for row in rows) == 1
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_EFF_ACOUSTIC_INPUT_ACCEPTANCE_V01",
            "acceptance_rows_declared": "6",
            "accepted_rows": "1",
            "blocked_rows": "3",
            "partial_rows": "1",
            "phi_tau_eff_source_slot_accepted": "true",
            "phi_tau_eff_acoustic_input_accepted": "false",
            "operator_model_accepted_rows": "1",
            "derived_source_rows": "0",
            "executable_prediction_rows": "0",
            "accepted_planck_payload_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_EFF_ACOUSTIC_INPUT_IDENTITY_ACCEPTED_INPUT_BLOCKED_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01",
            "claim_boundary": "tau_cmb_phi_tau_eff_acoustic_input_acceptance_v01_acceptance_audit_only_no_accepted_effective_potential_no_operator_solution_no_peak_prediction_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "phi_tau_eff_source_slot_accepted = true" in note
    assert "phi_tau_eff_acoustic_input_accepted = false" in note
    assert "tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01" in note


def test_tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_policy_only() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01.md").read_text()

    assert len(rows) == 6
    assert [row["provenance_component"] for row in rows] == [
        "endpoint_exclusion_rule",
        "parent_input_manifest",
        "parent_side_content",
        "derivation_rule",
        "audit_replay_package",
        "failure_branch",
    ]
    assert sum(row["acceptance_status"].startswith("ACCEPTED_POLICY") for row in rows) == 1
    assert sum(row["acceptance_status"].startswith("BLOCKED") for row in rows) == 4
    assert sum(row["acceptance_status"].startswith("PARTIAL") for row in rows) == 1
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_EFF_ENDPOINT_BLIND_PROVENANCE_ACCEPTANCE_V01",
            "provenance_acceptance_rows_declared": "6",
            "accepted_policy_rows": "1",
            "blocked_rows": "4",
            "partial_rows": "1",
            "endpoint_exclusion_rule_accepted": "true",
            "parent_input_manifest_supplied": "false",
            "derivation_rule_supplied": "false",
            "replay_package_supplied": "false",
            "endpoint_blind_provenance_accepted": "false",
            "phi_tau_eff_acoustic_input_accepted": "false",
            "operator_model_accepted_rows": "1",
            "derived_source_rows": "0",
            "executable_prediction_rows": "0",
            "accepted_planck_payload_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_EFF_ENDPOINT_BLIND_PROVENANCE_POLICY_ACCEPTED_PROVENANCE_BLOCKED_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01",
            "claim_boundary": "tau_cmb_phi_tau_eff_endpoint_blind_provenance_acceptance_v01_policy_only_no_accepted_provenance_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "endpoint_exclusion_rule_accepted = true" in note
    assert "endpoint_blind_provenance_accepted = false" in note
    assert "does not accept endpoint-blind provenance" in note


def test_tau_cmb_effective_potential_source_handoff_is_declared_but_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_effective_potential_source_handoff_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_effective_potential_source_handoff_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_effective_potential_source_handoff_v01.md").read_text()

    assert len(rows) == 6
    assert [row["handoff_component"] for row in rows] == [
        "source_slot_identity",
        "endpoint_blind_provenance",
        "normalization_convention",
        "timing_sign_convention",
        "baryon_photon_coupling_role",
        "lensing_projection_handoff",
    ]
    assert sum(row["handoff_status"].startswith("DECLARED") for row in rows) == 1
    assert sum(row["handoff_status"].startswith("PARTIAL") for row in rows) == 1
    assert sum(row["handoff_status"].startswith("BLOCKED") for row in rows) == 4
    assert {row["source_handoff_completed"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6
    assert all(row["handoff_requirement"] for row in rows)
    assert all(row["remaining_blocker"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_EFFECTIVE_POTENTIAL_SOURCE_HANDOFF_V01",
            "handoff_rows_declared": "6",
            "declared_rows": "1",
            "partial_rows": "1",
            "blocked_rows": "4",
            "completed_rows": "0",
            "hard_failures_triggered": "0",
            "source_handoff_completed": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "6",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "EFFECTIVE_POTENTIAL_SOURCE_HANDOFF_DECLARED_BUT_BLOCKED",
            "next_required_artifact": "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01",
            "claim_boundary": "tau_cmb_effective_potential_source_handoff_v01_handoff_only_no_source_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "It does not derive `Phi_tau_eff`" in note
    assert "source handoff is not completed" in note


def test_tau_cmb_endpoint_blind_phi_tau_derivation_contract_is_unsatisfied() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_endpoint_blind_phi_tau_derivation_contract_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.md").read_text()

    assert len(rows) == 6
    assert [row["contract_component"] for row in rows] == [
        "parent_side_input_provenance",
        "endpoint_exclusion_rule",
        "derivation_rule_required",
        "normalization_lock",
        "audit_replay_package",
        "failure_branch",
    ]
    assert sum(row["contract_status"].startswith("DECLARED") for row in rows) == 1
    assert sum(row["contract_status"].startswith("PARTIAL") for row in rows) == 2
    assert sum(row["contract_status"].startswith("BLOCKED") for row in rows) == 3
    assert {row["endpoint_blind_contract_satisfied"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 6
    assert all(row["contract_requirement"] for row in rows)
    assert all(row["endpoint_exclusion_rule"] for row in rows)
    assert all(row["remaining_blocker"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_ENDPOINT_BLIND_PHI_TAU_DERIVATION_CONTRACT_V01",
            "contract_rows_declared": "6",
            "declared_rows": "1",
            "partial_rows": "2",
            "blocked_rows": "3",
            "satisfied_rows": "0",
            "hard_failures_triggered": "0",
            "endpoint_blind_contract_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "6",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ENDPOINT_BLIND_PHI_TAU_DERIVATION_CONTRACT_DECLARED_UNSATISFIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_provenance_v01",
            "claim_boundary": "tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01_contract_only_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "It does not derive `Phi_tau_eff`" in note
    assert "endpoint-blind contract is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_provenance_is_unsatisfied() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_provenance_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_provenance_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_provenance_v01.md").read_text()

    assert len(rows) == 7
    assert [row["parent_input_component"] for row in rows] == [
        "parent_input_manifest_identity",
        "tau_base_field_state",
        "morphological_seed_descriptor",
        "response_operator_inputs",
        "gauge_normalization_metadata",
        "endpoint_firewall_audit",
        "provenance_replay_status",
    ]
    assert sum(row["provenance_status"].startswith("DECLARED") for row in rows) == 1
    assert sum(row["provenance_status"].startswith("PARTIAL") for row in rows) == 2
    assert sum(row["provenance_status"].startswith("BLOCKED") for row in rows) == 4
    assert {row["parent_input_supplied"] for row in rows} == {"false"}
    assert {row["provenance_satisfied"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_parent_side_content"] for row in rows)
    assert all(row["endpoint_firewall_rule"] for row in rows)
    assert all(row["remaining_blocker"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_PROVENANCE_V01",
            "provenance_rows_declared": "7",
            "declared_rows": "1",
            "partial_rows": "2",
            "blocked_rows": "4",
            "supplied_rows": "0",
            "satisfied_rows": "0",
            "hard_failures_triggered": "0",
            "parent_input_provenance_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_PROVENANCE_DECLARED_UNSATISFIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_provenance_v01_provenance_slots_only_no_parent_inputs_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "It does not supply parent inputs" in note
    assert "parent-input provenance is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_candidate_manifest_is_unaccepted() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_candidate_manifest_v01.md").read_text()

    assert len(rows) == 7
    assert [row["candidate_component"] for row in rows] == [
        "candidate_manifest_identity",
        "base_field_state_candidate",
        "morphological_seed_candidate",
        "response_operator_candidate",
        "gauge_normalization_candidate",
        "endpoint_firewall_candidate",
        "provenance_replay_candidate",
    ]
    assert sum(row["candidate_status"].startswith("DECLARED") for row in rows) == 1
    assert sum(row["candidate_status"].startswith("CANDIDATE") for row in rows) == 3
    assert sum(row["candidate_status"].startswith("PARTIAL") for row in rows) == 2
    assert sum(row["candidate_status"].startswith("BLOCKED") for row in rows) == 1
    assert {row["candidate_declared"] for row in rows} == {"true"}
    assert {row["candidate_accepted"] for row in rows} == {"false"}
    assert {row["manifest_satisfied"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["candidate_parent_side_role"] for row in rows)
    assert all(row["endpoint_exclusion_rule"] for row in rows)
    assert all(row["acceptance_requirement"] for row in rows)
    assert all(row["remaining_blocker"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_V01",
            "manifest_rows_declared": "7",
            "declared_rows": "1",
            "candidate_rows": "3",
            "partial_rows": "2",
            "blocked_rows": "1",
            "accepted_rows": "0",
            "satisfied_rows": "0",
            "hard_failures_triggered": "0",
            "candidate_manifest_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_DECLARED_UNACCEPTED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_candidate_manifest_v01_candidate_classes_only_no_accepted_inputs_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "It does not accept any candidate input" in note
    assert "candidate manifest is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_identity_only() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01.md").read_text()

    assert len(rows) == 7
    assert [row["candidate_component"] for row in rows] == [
        "candidate_manifest_identity",
        "base_field_state_candidate",
        "morphological_seed_candidate",
        "response_operator_candidate",
        "gauge_normalization_candidate",
        "endpoint_firewall_candidate",
        "provenance_replay_candidate",
    ]
    assert sum(row["acceptance_status"].startswith("ACCEPTED_IDENTITY") for row in rows) == 1
    assert sum(row["acceptance_status"].startswith("BLOCKED") for row in rows) == 4
    assert sum(row["acceptance_status"].startswith("PARTIAL") for row in rows) == 2
    assert {row["accepted_as_parent_input"] for row in rows} == {"false"}
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_ACCEPTANCE_V01",
            "candidate_acceptance_rows_declared": "7",
            "accepted_identity_rows": "1",
            "accepted_parent_input_rows": "0",
            "blocked_rows": "4",
            "partial_rows": "2",
            "candidate_packet_identity_accepted": "true",
            "base_field_state_accepted": "false",
            "morphological_seed_accepted": "false",
            "response_operator_accepted": "false",
            "gauge_normalization_locked": "false",
            "endpoint_firewall_executed": "false",
            "provenance_replay_supplied": "false",
            "candidate_manifest_acceptance_satisfied": "false",
            "endpoint_blind_provenance_accepted": "false",
            "phi_tau_eff_acoustic_input_accepted": "false",
            "operator_model_accepted_rows": "1",
            "derived_source_rows": "0",
            "executable_prediction_rows": "0",
            "accepted_planck_payload_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CANDIDATE_MANIFEST_IDENTITY_ACCEPTED_INPUTS_BLOCKED_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_firewall_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_candidate_manifest_acceptance_v01_identity_only_no_accepted_parent_inputs_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "accepted_parent_input_rows = 0" in note
    assert "candidate_manifest_acceptance_satisfied = false" in note
    assert "accepts no base-field state" in note


def test_tau_cmb_phi_tau_parent_input_firewall_audit_is_blocked_by_missing_payload() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_firewall_audit_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_firewall_audit_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_firewall_audit_v01.md").read_text()

    assert len(rows) == 7
    assert [row["audited_candidate_component"] for row in rows] == [
        "candidate_manifest_identity",
        "base_field_state_candidate",
        "morphological_seed_candidate",
        "response_operator_candidate",
        "gauge_normalization_candidate",
        "endpoint_firewall_candidate",
        "provenance_replay_candidate",
    ]
    assert sum(row["audit_status"].startswith("DECLARED") for row in rows) == 1
    assert sum(row["audit_status"].startswith("PARTIAL") for row in rows) == 1
    assert sum(row["audit_status"].startswith("BLOCKED") for row in rows) == 5
    assert {row["observed_endpoint_dependency"] for row in rows} == {"false"}
    assert {row["endpoint_firewall_passed"] for row in rows} == {"false"}
    assert {row["candidate_accepted"] for row in rows} == {"false"}
    assert {row["audit_satisfied"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["audit_rule"] for row in rows)
    assert all(row["audit_evidence"] for row in rows)
    assert all(row["remaining_blocker"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_FIREWALL_AUDIT_V01",
            "audit_rows_declared": "7",
            "declared_rows": "1",
            "partial_rows": "1",
            "blocked_rows": "5",
            "passed_rows": "0",
            "accepted_rows": "0",
            "satisfied_rows": "0",
            "endpoint_dependencies_detected": "0",
            "hard_failures_triggered": "0",
            "endpoint_firewall_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_FIREWALL_AUDIT_DECLARED_BLOCKED_BY_MISSING_PAYLOAD",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_payload_stub_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_firewall_audit_v01_audit_rules_only_no_payload_pass_no_accepted_inputs_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "does not pass the endpoint firewall" in note
    assert "there is no payload to inspect" in note


def test_tau_cmb_phi_tau_parent_input_payload_stub_has_no_concrete_values() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_payload_stub_v01.csv").open()))
    summary = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_payload_stub_summary_v01.csv").open()))
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_payload_stub_v01.md").read_text()

    assert len(rows) == 7
    assert [row["payload_component"] for row in rows] == [
        "payload_manifest_identity",
        "base_field_state_payload_stub",
        "morphological_seed_payload_stub",
        "response_operator_payload_stub",
        "gauge_normalization_payload_stub",
        "endpoint_firewall_payload_stub",
        "provenance_replay_payload_stub",
    ]
    assert sum(row["payload_status"].startswith("DECLARED") for row in rows) == 1
    assert sum(row["payload_status"].startswith("STUB") for row in rows) == 4
    assert sum(row["payload_status"].startswith("PARTIAL") for row in rows) == 1
    assert sum(row["payload_status"].startswith("BLOCKED") for row in rows) == 1
    assert {row["payload_stub_declared"] for row in rows} == {"true"}
    assert {row["concrete_payload_supplied"] for row in rows} == {"false"}
    assert {row["endpoint_firewall_executable"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["payload_satisfied"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["stub_content"] for row in rows)
    assert all(row["endpoint_exclusion_metadata"] for row in rows)
    assert all(row["payload_limitation"] for row in rows)
    assert all(row["remaining_blocker"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_PAYLOAD_STUB_V01",
            "payload_rows_declared": "7",
            "declared_rows": "1",
            "stub_rows": "4",
            "partial_rows": "1",
            "blocked_rows": "1",
            "concrete_payload_rows": "0",
            "firewall_executable_rows": "0",
            "accepted_rows": "0",
            "satisfied_rows": "0",
            "hard_failures_triggered": "0",
            "payload_stub_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_PAYLOAD_STUB_DECLARED_NO_CONCRETE_VALUES",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_firewall_execution_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_payload_stub_v01_stub_schema_only_no_concrete_parent_values_no_firewall_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "does not supply concrete parent-input values" in note
    assert "payload stub is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_firewall_execution_schema_passes_but_payload_is_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_firewall_execution_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_firewall_execution_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_firewall_execution_v01.md").read_text()

    assert len(rows) == 7
    assert [row["inspected_payload_component"] for row in rows] == [
        "payload_manifest_identity",
        "base_field_state_payload_stub",
        "morphological_seed_payload_stub",
        "response_operator_payload_stub",
        "gauge_normalization_payload_stub",
        "endpoint_firewall_payload_stub",
        "provenance_replay_payload_stub",
    ]
    assert sum(row["schema_firewall_executed"] == "true" for row in rows) == 6
    assert sum(row["schema_firewall_passed"] == "true" for row in rows) == 6
    assert sum(row["execution_status"].startswith("BLOCKED") for row in rows) == 1
    assert {row["forbidden_endpoint_fields_present"] for row in rows} == {"false"}
    assert {row["concrete_payload_supplied"] for row in rows} == {"false"}
    assert {row["payload_firewall_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["forbidden_endpoint_fields_checked"] for row in rows)
    assert all(row["execution_evidence"] for row in rows)
    assert all(row["remaining_blocker"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_FIREWALL_EXECUTION_V01",
            "execution_rows_declared": "7",
            "schema_executed_rows": "6",
            "schema_passed_rows": "6",
            "payload_passed_rows": "0",
            "accepted_rows": "0",
            "blocked_rows": "1",
            "forbidden_endpoint_fields_detected": "0",
            "concrete_payload_rows": "0",
            "hard_failures_triggered": "0",
            "schema_firewall_execution_satisfied": "true",
            "payload_firewall_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_FIREWALL_EXECUTION_SCHEMA_PASS_PAYLOAD_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_firewall_execution_v01_schema_firewall_only_no_payload_pass_no_accepted_inputs_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "schema-level firewall passes" in note
    assert "not a payload-level pass" in note


def test_tau_cmb_phi_tau_parent_input_concrete_payload_requirements_are_unsatisfied() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_requirements_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01.md").read_text()

    assert len(rows) == 7
    assert [row["payload_component"] for row in rows] == [
        "requirements_manifest_identity",
        "base_field_state_payload",
        "morphological_seed_payload",
        "response_operator_payload",
        "gauge_normalization_payload",
        "endpoint_firewall_payload",
        "provenance_replay_payload",
    ]
    assert sum(row["requirement_status"].startswith("DECLARED") for row in rows) == 1
    assert sum(row["requirement_status"].startswith("REQUIREMENT") for row in rows) == 5
    assert sum(row["requirement_status"].startswith("BLOCKED") for row in rows) == 1
    assert {row["concrete_payload_supplied"] for row in rows} == {"false"}
    assert {row["requirement_satisfied"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_payload_type"] for row in rows)
    assert all(row["required_parent_side_content"] for row in rows)
    assert all(row["dimensional_or_units_requirement"] for row in rows)
    assert all(row["endpoint_blind_evidence_required"] for row in rows)
    assert all(row["replay_requirement"] for row in rows)
    assert all(row["acceptance_criterion"] for row in rows)
    assert all(row["remaining_blocker"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_REQUIREMENTS_V01",
            "requirement_rows_declared": "7",
            "declared_rows": "1",
            "requirement_rows": "5",
            "blocked_rows": "1",
            "concrete_payload_rows": "0",
            "satisfied_rows": "0",
            "hard_failures_triggered": "0",
            "concrete_payload_requirements_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_REQUIREMENTS_DECLARED_UNSATISFIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01_requirements_only_no_concrete_payload_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "does not supply concrete parent-input values" in note
    assert "concrete payload requirements are not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_concrete_payload_candidate_is_unaccepted() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_candidate_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01.md").read_text()

    assert len(rows) == 7
    assert [row["payload_component"] for row in rows] == [
        "candidate_payload_manifest_identity",
        "base_field_state_payload_candidate",
        "morphological_seed_payload_candidate",
        "response_operator_payload_candidate",
        "gauge_normalization_payload_candidate",
        "endpoint_firewall_payload_candidate",
        "provenance_replay_payload_candidate",
    ]
    assert sum(row["candidate_status"].startswith("MANIFEST") for row in rows) == 1
    assert sum(row["candidate_status"].startswith("CANDIDATE") for row in rows) == 4
    assert sum(row["candidate_status"].startswith("BLOCKED") for row in rows) == 2
    assert {row["candidate_payload_declared"] for row in rows} == {"true"}
    assert sum(row["concrete_payload_supplied"] == "true" for row in rows) == 5
    assert {row["dimension_check_passed"] for row in rows} == {"false"}
    assert {row["endpoint_firewall_passed"] for row in rows} == {"false"}
    assert {row["replay_available"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["candidate_payload_content"] for row in rows)
    assert all(row["dimension_or_units_status"] for row in rows)
    assert all(row["endpoint_blind_status"] for row in rows)
    assert all(row["replay_status"] for row in rows)
    assert all(row["acceptance_blocker"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_CANDIDATE_V01",
            "candidate_rows_declared": "7",
            "manifest_rows": "1",
            "candidate_payload_rows": "4",
            "blocked_rows": "2",
            "concrete_payload_rows": "5",
            "dimension_passed_rows": "0",
            "firewall_passed_rows": "0",
            "replay_available_rows": "0",
            "accepted_rows": "0",
            "hard_failures_triggered": "0",
            "concrete_payload_candidate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CONCRETE_PAYLOAD_CANDIDATE_DECLARED_UNACCEPTED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01_candidate_payload_only_no_accepted_inputs_no_payload_firewall_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "does not accept any candidate payload" in note
    assert "concrete payload candidate is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_payload_firewall_audit_is_endpoint_clean_but_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_payload_firewall_audit_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01.md").read_text()

    assert len(rows) == 7
    assert [row["audited_payload_component"] for row in rows] == [
        "candidate_payload_manifest_identity",
        "base_field_state_payload_candidate",
        "morphological_seed_payload_candidate",
        "response_operator_payload_candidate",
        "gauge_normalization_payload_candidate",
        "endpoint_firewall_payload_candidate",
        "provenance_replay_payload_candidate",
    ]
    assert sum(row["payload_firewall_audited"] == "true" for row in rows) == 7
    assert {row["endpoint_fields_detected"] for row in rows} == {"false"}
    assert sum(row["audit_status"].startswith("BLOCKED") for row in rows) == 2
    assert {row["payload_firewall_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["endpoint_fields_checked"] for row in rows)
    assert all(row["dimension_check_status"] for row in rows)
    assert all(row["firewall_certificate_status"] == "certificate_missing" for row in rows)
    assert all(row["replay_status"] == "replay_missing" for row in rows)
    assert all(row["payload_firewall_result"].startswith("BLOCKED") for row in rows)
    assert all(row["audit_evidence"] for row in rows)
    assert all(row["remaining_blocker"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_PAYLOAD_FIREWALL_AUDIT_V01",
            "audit_rows_declared": "7",
            "audited_rows": "7",
            "endpoint_clean_rows": "7",
            "dimension_passed_rows": "0",
            "certificate_supplied_rows": "0",
            "replay_available_rows": "0",
            "payload_passed_rows": "0",
            "accepted_rows": "0",
            "blocked_rows": "2",
            "endpoint_fields_detected": "0",
            "hard_failures_triggered": "0",
            "payload_firewall_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_PAYLOAD_FIREWALL_AUDIT_ENDPOINT_CLEAN_BUT_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_source_content_closure_decision_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01_payload_audit_only_no_payload_pass_no_accepted_inputs_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "detects no populated endpoint-derived fields" in note
    assert "does not pass the payload-level firewall" in note


def test_tau_cmb_phi_tau_parent_source_content_closure_decision_is_endpoint_clean_but_unclosed() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_source_content_closure_decision_v01.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_source_content_closure_decision_summary_v01.csv").open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_source_content_closure_decision_v01.md").read_text()

    assert len(rows) == 7
    assert [row["source_content_component"] for row in rows] == [
        "candidate_payload_manifest_identity",
        "base_field_state_payload_candidate",
        "morphological_seed_payload_candidate",
        "response_operator_payload_candidate",
        "gauge_normalization_payload_candidate",
        "endpoint_firewall_payload_candidate",
        "provenance_replay_payload_candidate",
    ]
    assert sum(row["candidate_content_present"] == "true" for row in rows) == 5
    assert {row["endpoint_clean"] for row in rows} == {"true"}
    assert {row["dimension_or_lock_passed"] for row in rows} == {"false"}
    assert {row["payload_firewall_passed"] for row in rows} == {"false"}
    assert {row["replay_available"] for row in rows} == {"false"}
    assert {row["accepted_as_parent_input"] for row in rows} == {"false"}
    assert sum(row["closure_decision"].startswith("BLOCKED") for row in rows) == 5
    assert sum(row["closure_decision"].startswith("PARTIAL") for row in rows) == 2
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_SOURCE_CONTENT_CLOSURE_DECISION_V01",
            "source_content_rows_declared": "7",
            "candidate_content_rows": "5",
            "endpoint_clean_rows": "7",
            "dimension_or_lock_passed_rows": "0",
            "payload_firewall_passed_rows": "0",
            "replay_available_rows": "0",
            "accepted_parent_input_rows": "0",
            "closed_rows": "0",
            "blocked_rows": "5",
            "partial_rows": "2",
            "phi_tau_parent_source_content_closed": "false",
            "endpoint_blind_provenance_accepted": "false",
            "phi_tau_eff_source_derivation_allowed": "false",
            "phi_tau_eff_acoustic_input_accepted": "false",
            "operator_model_accepted_rows": "1",
            "derived_source_rows": "0",
            "executable_prediction_rows": "0",
            "accepted_planck_payload_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_SOURCE_CONTENT_ENDPOINT_CLEAN_BUT_UNCLOSED_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_source_content_closure_decision_v01_decision_only_endpoint_clean_but_unclosed_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "endpoint-clean candidate content exists" in note
    assert "not closed" in note
    assert "does not derive `Phi_tau_eff`" in note


def test_tau_cmb_phi_tau_parent_input_dimension_replay_certificate_is_unsupplied() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_dimension_replay_certificate_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01.md").read_text()

    assert len(rows) == 7
    assert [row["certificate_component"] for row in rows] == [
        "certificate_manifest_identity",
        "base_field_dimension_replay_certificate",
        "seed_dimension_replay_certificate",
        "operator_dimension_replay_certificate",
        "gauge_normalization_replay_certificate",
        "payload_firewall_certificate",
        "executable_replay_certificate",
    ]
    assert sum(row["certificate_status"].startswith("DECLARED") for row in rows) == 1
    assert sum(row["certificate_status"].startswith("REQUIREMENT") for row in rows) == 4
    assert sum(row["certificate_status"].startswith("BLOCKED") for row in rows) == 2
    assert {row["dimension_certificate_supplied"] for row in rows} == {"false"}
    assert {row["replay_certificate_supplied"] for row in rows} == {"false"}
    assert {row["firewall_certificate_supplied"] for row in rows} == {"false"}
    assert {row["certificate_satisfied"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["dimension_certificate_requirement"] for row in rows)
    assert all(row["replay_certificate_requirement"] for row in rows)
    assert all(row["firewall_certificate_requirement"] for row in rows)
    assert all(row["remaining_blocker"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_DIMENSION_REPLAY_CERTIFICATE_V01",
            "certificate_rows_declared": "7",
            "declared_rows": "1",
            "requirement_rows": "4",
            "blocked_rows": "2",
            "dimension_certificates_supplied": "0",
            "replay_certificates_supplied": "0",
            "firewall_certificates_supplied": "0",
            "satisfied_rows": "0",
            "accepted_rows": "0",
            "hard_failures_triggered": "0",
            "dimension_replay_certificate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_DIMENSION_REPLAY_CERTIFICATE_DECLARED_UNSUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_certificate_candidate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_dimension_replay_certificate_v01_certificate_requirements_only_no_certificate_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "supplies no certificate package" in note
    assert "dimension/replay certificate is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_certificate_candidate_is_unpassed() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_candidate_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_candidate_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_certificate_candidate_v01.md").read_text()

    assert len(rows) == 7
    assert [row["certificate_component"] for row in rows] == [
        "certificate_candidate_manifest_identity",
        "base_field_dimension_replay_certificate_candidate",
        "seed_dimension_replay_certificate_candidate",
        "operator_dimension_replay_certificate_candidate",
        "gauge_normalization_replay_certificate_candidate",
        "payload_firewall_certificate_candidate",
        "executable_replay_certificate_candidate",
    ]
    assert sum(row["candidate_status"].startswith("MANIFEST") for row in rows) == 1
    assert sum(row["candidate_status"].startswith("CANDIDATE") for row in rows) == 4
    assert sum(row["candidate_status"].startswith("BLOCKED") for row in rows) == 2
    assert {row["certificate_candidate_declared"] for row in rows} == {"true"}
    assert {row["dimension_certificate_supplied"] for row in rows} == {"false"}
    assert {row["replay_certificate_supplied"] for row in rows} == {"false"}
    assert {row["firewall_certificate_supplied"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["candidate_certificate_content"] for row in rows)
    assert all(row["dimension_certificate_status"] for row in rows)
    assert all(row["replay_certificate_status"] for row in rows)
    assert all(row["firewall_certificate_status"] for row in rows)
    assert all(row["acceptance_blocker"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_CANDIDATE_V01",
            "candidate_rows_declared": "7",
            "manifest_rows": "1",
            "candidate_certificate_rows": "4",
            "blocked_rows": "2",
            "dimension_certificates_supplied": "0",
            "replay_certificates_supplied": "0",
            "firewall_certificates_supplied": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "hard_failures_triggered": "0",
            "certificate_candidate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CERTIFICATE_CANDIDATE_DECLARED_UNPASSED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_certificate_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_certificate_candidate_v01_candidate_certificates_only_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "does not pass any certificate" in note
    assert "certificate candidate is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_certificate_audit_fails_without_evidence() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_audit_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_audit_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_certificate_audit_v01.md").read_text()

    assert len(rows) == 7
    assert [row["certificate_component"] for row in rows] == [
        "certificate_candidate_manifest_identity",
        "base_field_dimension_replay_certificate_candidate",
        "seed_dimension_replay_certificate_candidate",
        "operator_dimension_replay_certificate_candidate",
        "gauge_normalization_replay_certificate_candidate",
        "payload_firewall_certificate_candidate",
        "executable_replay_certificate_candidate",
    ]
    assert {row["audit_status"] for row in rows} == {"AUDIT_FAIL_MISSING_CERTIFICATE_EVIDENCE"}
    assert {row["candidate_audited"] for row in rows} == {"true"}
    assert {row["certificate_evidence_supplied"] for row in rows} == {"false"}
    assert {row["dimension_audit_passed"] for row in rows} == {"false"}
    assert {row["replay_audit_passed"] for row in rows} == {"false"}
    assert {row["firewall_audit_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["audit_finding"] for row in rows)
    assert all(row["missing_evidence"] for row in rows)
    assert all(row["acceptance_decision"] == "reject_for_scoring_input_acceptance" for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_AUDIT_V01",
            "audit_rows_declared": "7",
            "audited_rows": "7",
            "audit_passed_rows": "0",
            "audit_failed_rows": "7",
            "certificate_evidence_supplied_rows": "0",
            "dimension_audit_passed_rows": "0",
            "replay_audit_passed_rows": "0",
            "firewall_audit_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "hard_failures_triggered": "0",
            "certificate_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CERTIFICATE_AUDIT_FAILED_MISSING_EVIDENCE",
            "next_required_artifact": "tau_cmb_phi_tau_parent_certificate_closure_decision_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_certificate_audit_v01_candidate_audit_only_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "All seven candidates fail the audit" in note
    assert "certificate audit is not satisfied" in note


def test_tau_cmb_phi_tau_parent_certificate_closure_decision_is_unclosed() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_certificate_closure_decision_v01.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_certificate_closure_decision_summary_v01.csv").open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_certificate_closure_decision_v01.md").read_text()

    assert len(rows) == 7
    assert [row["certificate_component"] for row in rows] == [
        "certificate_candidate_manifest_identity",
        "base_field_dimension_replay_certificate_candidate",
        "seed_dimension_replay_certificate_candidate",
        "operator_dimension_replay_certificate_candidate",
        "gauge_normalization_replay_certificate_candidate",
        "payload_firewall_certificate_candidate",
        "executable_replay_certificate_candidate",
    ]
    assert {row["requirement_declared"] for row in rows} == {"true"}
    assert {row["candidate_declared"] for row in rows} == {"true"}
    assert {row["candidate_audited"] for row in rows} == {"true"}
    assert {row["certificate_evidence_supplied"] for row in rows} == {"false"}
    assert {row["dimension_passed"] for row in rows} == {"false"}
    assert {row["replay_passed"] for row in rows} == {"false"}
    assert {row["firewall_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["closure_decision"] for row in rows} == {"BLOCKED_CERTIFICATE_NOT_CLOSED"}
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["allows_tau_response_claim"] for row in rows} == {"false"}
    assert {row["allows_dark_sector_verdict"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_CERTIFICATE_CLOSURE_DECISION_V01",
            "certificate_closure_rows_declared": "7",
            "requirements_declared_rows": "7",
            "candidate_declared_rows": "7",
            "candidate_audited_rows": "7",
            "certificate_evidence_supplied_rows": "0",
            "dimension_passed_rows": "0",
            "replay_passed_rows": "0",
            "firewall_passed_rows": "0",
            "certificate_passed_rows": "0",
            "payload_accepted_rows": "0",
            "closed_rows": "0",
            "blocked_rows": "7",
            "phi_tau_parent_certificates_closed": "false",
            "phi_tau_parent_source_content_closed": "false",
            "endpoint_blind_provenance_accepted": "false",
            "phi_tau_eff_source_derivation_allowed": "false",
            "phi_tau_eff_acoustic_input_accepted": "false",
            "operator_model_accepted_rows": "1",
            "derived_source_rows": "0",
            "executable_prediction_rows": "0",
            "accepted_planck_payload_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_CERTIFICATES_DECLARED_AND_AUDITED_BUT_UNCLOSED_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_certificate_closure_decision_v01_decision_only_certificates_unpassed_no_parent_input_acceptance_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "requirements and candidates are declared and audited" in note
    assert "not closed" in note
    assert "does not derive `Phi_tau_eff`" in note


def test_tau_cmb_phi_tau_parent_input_certificate_evidence_request_is_unsupplied() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_request_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01.md").read_text()

    assert len(rows) == 7
    assert [row["certificate_component"] for row in rows] == [
        "certificate_candidate_manifest_identity",
        "base_field_dimension_replay_certificate_candidate",
        "seed_dimension_replay_certificate_candidate",
        "operator_dimension_replay_certificate_candidate",
        "gauge_normalization_replay_certificate_candidate",
        "payload_firewall_certificate_candidate",
        "executable_replay_certificate_candidate",
    ]
    assert {row["request_status"] for row in rows} == {"EVIDENCE_REQUESTED_NOT_SUPPLIED"}
    assert {row["evidence_requested"] for row in rows} == {"true"}
    assert {row["evidence_supplied"] for row in rows} == {"false"}
    assert {row["dimension_evidence_supplied"] for row in rows} == {"false"}
    assert {row["replay_evidence_supplied"] for row in rows} == {"false"}
    assert {row["firewall_evidence_supplied"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_evidence_bundle"] for row in rows)
    assert all(row["dimension_evidence_request"] for row in rows)
    assert all(row["replay_evidence_request"] for row in rows)
    assert all(row["firewall_evidence_request"] for row in rows)
    assert all(row["acceptance_criterion"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_REQUEST_V01",
            "request_rows_declared": "7",
            "evidence_requested_rows": "7",
            "evidence_supplied_rows": "0",
            "dimension_evidence_supplied_rows": "0",
            "replay_evidence_supplied_rows": "0",
            "firewall_evidence_supplied_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "hard_failures_triggered": "0",
            "certificate_evidence_request_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_REQUESTED_NOT_SUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_certificate_evidence_request_v01_evidence_request_only_no_evidence_supplied_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "All seven rows request evidence" in note
    assert "certificate evidence request is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_is_unpopulated() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_summary_v01.csv").open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01.md").read_text()

    assert len(rows) == 7
    assert [row["certificate_component"] for row in rows] == [
        "certificate_candidate_manifest_identity",
        "base_field_dimension_replay_certificate_candidate",
        "seed_dimension_replay_certificate_candidate",
        "operator_dimension_replay_certificate_candidate",
        "gauge_normalization_replay_certificate_candidate",
        "payload_firewall_certificate_candidate",
        "executable_replay_certificate_candidate",
    ]
    assert {row["package_candidate_status"] for row in rows} == {"EVIDENCE_PACKAGE_CANDIDATE_DECLARED_UNPOPULATED"}
    assert {row["package_candidate_declared"] for row in rows} == {"true"}
    assert {row["dimension_evidence_slot_declared"] for row in rows} == {"true"}
    assert {row["replay_evidence_slot_declared"] for row in rows} == {"true"}
    assert {row["firewall_evidence_slot_declared"] for row in rows} == {"true"}
    assert {row["evidence_payload_supplied"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["package_candidate_content"] for row in rows)
    assert all(row["required_dimension_evidence_slot"] for row in rows)
    assert all(row["required_replay_evidence_slot"] for row in rows)
    assert all(row["required_firewall_evidence_slot"] for row in rows)
    assert all(row["package_acceptance_gate"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_CANDIDATE_V01",
            "package_rows_declared": "7",
            "package_candidate_rows": "7",
            "dimension_slots_declared": "7",
            "replay_slots_declared": "7",
            "firewall_slots_declared": "7",
            "evidence_payload_supplied_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "hard_failures_triggered": "0",
            "certificate_evidence_package_candidate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_CANDIDATE_DECLARED_UNPOPULATED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_certificate_evidence_package_candidate_v01_package_candidate_only_no_evidence_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "All seven rows declare package slots" in note
    assert "certificate evidence package candidate is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_fails_unpopulated() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_summary_v01.csv").open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01.md").read_text()

    assert len(rows) == 7
    assert [row["certificate_component"] for row in rows] == [
        "certificate_candidate_manifest_identity",
        "base_field_dimension_replay_certificate_candidate",
        "seed_dimension_replay_certificate_candidate",
        "operator_dimension_replay_certificate_candidate",
        "gauge_normalization_replay_certificate_candidate",
        "payload_firewall_certificate_candidate",
        "executable_replay_certificate_candidate",
    ]
    assert {row["package_audit_status"] for row in rows} == {"PACKAGE_AUDIT_FAIL_UNPOPULATED_EVIDENCE_PAYLOAD"}
    assert {row["package_candidate_audited"] for row in rows} == {"true"}
    assert {row["evidence_payload_supplied"] for row in rows} == {"false"}
    assert {row["dimension_payload_supplied"] for row in rows} == {"false"}
    assert {row["replay_payload_supplied"] for row in rows} == {"false"}
    assert {row["firewall_payload_supplied"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["audit_finding"] for row in rows)
    assert all(row["missing_payload"] for row in rows)
    assert all(row["package_acceptance_decision"] == "reject_package_for_scoring_input_acceptance" for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_AUDIT_V01",
            "audit_rows_declared": "7",
            "package_candidate_audited_rows": "7",
            "package_audit_passed_rows": "0",
            "package_audit_failed_rows": "7",
            "evidence_payload_supplied_rows": "0",
            "dimension_payload_supplied_rows": "0",
            "replay_payload_supplied_rows": "0",
            "firewall_payload_supplied_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "hard_failures_triggered": "0",
            "certificate_evidence_package_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_CERTIFICATE_EVIDENCE_PACKAGE_AUDIT_FAILED_UNPOPULATED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_certificate_evidence_package_audit_v01_package_audit_only_no_evidence_payload_no_evidence_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "All seven rows fail the" in note
    assert "certificate evidence package audit is not satisfied" in note


def test_tau_cmb_phi_tau_parent_evidence_package_closure_decision_is_unclosed() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01.csv").open()))
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_package_closure_decision_summary_v01.csv").open()
        )
    )
    payload = json.loads((ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01.json").read_text())
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01.md").read_text()

    assert len(rows) == 7
    assert [row["evidence_component"] for row in rows] == [
        "certificate_candidate_manifest_identity",
        "base_field_dimension_replay_certificate_candidate",
        "seed_dimension_replay_certificate_candidate",
        "operator_dimension_replay_certificate_candidate",
        "gauge_normalization_replay_certificate_candidate",
        "payload_firewall_certificate_candidate",
        "executable_replay_certificate_candidate",
    ]
    assert {row["evidence_requested"] for row in rows} == {"true"}
    assert {row["package_candidate_declared"] for row in rows} == {"true"}
    assert {row["package_audited"] for row in rows} == {"true"}
    assert {row["evidence_payload_supplied"] for row in rows} == {"false"}
    assert {row["dimension_evidence_supplied"] for row in rows} == {"false"}
    assert {row["replay_evidence_supplied"] for row in rows} == {"false"}
    assert {row["firewall_evidence_supplied"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["closure_decision"] for row in rows} == {"BLOCKED_EVIDENCE_PACKAGE_NOT_CLOSED"}
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert all(row["remaining_blocker"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PACKAGE_CLOSURE_DECISION_V01",
            "evidence_closure_rows_declared": "7",
            "evidence_requested_rows": "7",
            "package_candidate_declared_rows": "7",
            "package_audited_rows": "7",
            "evidence_payload_supplied_rows": "0",
            "dimension_evidence_supplied_rows": "0",
            "replay_evidence_supplied_rows": "0",
            "firewall_evidence_supplied_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "payload_accepted_rows": "0",
            "closed_rows": "0",
            "blocked_rows": "7",
            "phi_tau_parent_evidence_package_closed": "false",
            "phi_tau_parent_certificates_closed": "false",
            "phi_tau_parent_source_content_closed": "false",
            "endpoint_blind_provenance_accepted": "false",
            "phi_tau_eff_source_derivation_allowed": "false",
            "phi_tau_eff_acoustic_input_accepted": "false",
            "operator_model_accepted_rows": "1",
            "derived_source_rows": "0",
            "executable_prediction_rows": "0",
            "accepted_planck_payload_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_EVIDENCE_PACKAGE_DECLARED_AND_AUDITED_BUT_UNCLOSED_SCORE_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_evidence_package_closure_decision_v01_decision_only_evidence_package_unpopulated_no_certificate_pass_no_parent_input_acceptance_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert payload["summary"] == summary[0]
    assert "evidence package not closed" in note
    assert "does not derive `Phi_tau_eff`" in note


def test_tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_is_blocked() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01.md").read_text()

    assert len(rows) == 5
    assert [row["acceptance_component"] for row in rows] == [
        "evidence_package_acceptance",
        "certificate_acceptance",
        "payload_acceptance",
        "phi_tau_eff_derivation_acceptance",
        "cmb_scoring_acceptance",
    ]
    assert {row["precheck_status"] for row in rows} == {"SCORING_ACCEPTANCE_PRECHECK_BLOCKED"}
    assert {row["precheck_executed"] for row in rows} == {"true"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derivable"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["blocking_condition"] for row in rows)
    assert all(row["required_unblock_condition"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_PRECHECK_V01",
            "precheck_rows_declared": "5",
            "precheck_executed_rows": "5",
            "blocked_rows": "5",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "payload_accepted_rows": "0",
            "phi_tau_eff_derivable_rows": "0",
            "scoring_input_accepted_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "hard_failures_triggered": "0",
            "scoring_acceptance_precheck_satisfied": "false",
            "no_dark_blockers": "5",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_PRECHECK_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_scoring_acceptance_precheck_v01_acceptance_precheck_only_no_scoring_acceptance_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "All five precheck rows are blocked" in note
    assert "scoring acceptance precheck is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_is_open() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_summary_v01.csv").open())
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01.md").read_text()

    assert len(rows) == 5
    assert [row["acceptance_component"] for row in rows] == [
        "evidence_package_acceptance",
        "certificate_acceptance",
        "payload_acceptance",
        "phi_tau_eff_derivation_acceptance",
        "cmb_scoring_acceptance",
    ]
    assert [row["rank"] for row in rows] == ["1", "2", "3", "4", "5"]
    assert {row["plan_declared"] for row in rows} == {"true"}
    assert {row["unblock_completed"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derivable"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 5
    assert all(row["unblock_target_artifact"] for row in rows)
    assert all(row["unblock_action"] for row in rows)
    assert all(row["completion_criterion"] for row in rows)
    assert all(row["stop_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_UNBLOCK_PLAN_V01",
            "plan_rows_declared": "5",
            "plan_declared_rows": "5",
            "unblock_completed_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "payload_accepted_rows": "0",
            "phi_tau_eff_derivable_rows": "0",
            "scoring_input_accepted_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "hard_failures_triggered": "0",
            "scoring_acceptance_unblock_plan_satisfied": "false",
            "no_dark_blockers": "5",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_SCORING_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_OPEN",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_scoring_acceptance_unblock_plan_v01_unblock_plan_only_no_unblock_completed_no_scoring_acceptance_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "No unblock step is completed" in note
    assert "scoring acceptance unblock plan is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_is_not_supplied() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_summary_v01.csv").open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01.md").read_text()

    assert len(rows) == 7
    assert {row["populated_candidate_status"] for row in rows} == {"POPULATED_EVIDENCE_PACKAGE_CANDIDATE_DECLARED_NOT_SUPPLIED"}
    assert {row["populated_candidate_declared"] for row in rows} == {"true"}
    assert {row["payload_record_declared"] for row in rows} == {"true"}
    assert {row["evidence_payload_supplied"] for row in rows} == {"false"}
    assert {row["dimension_payload_supplied"] for row in rows} == {"false"}
    assert {row["replay_payload_supplied"] for row in rows} == {"false"}
    assert {row["firewall_payload_supplied"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_payload_record"] for row in rows)
    assert all(row["payload_population_rule"] for row in rows)
    assert all(row["endpoint_blindness_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_CANDIDATE_V01",
            "candidate_rows_declared": "7",
            "populated_candidate_declared_rows": "7",
            "payload_record_declared_rows": "7",
            "evidence_payload_supplied_rows": "0",
            "dimension_payload_supplied_rows": "0",
            "replay_payload_supplied_rows": "0",
            "firewall_payload_supplied_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "hard_failures_triggered": "0",
            "populated_evidence_package_candidate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_CANDIDATE_DECLARED_NOT_SUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_populated_evidence_package_candidate_v01_populated_candidate_only_no_evidence_payload_supplied_no_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "It does not supply those payloads" in note
    assert "populated evidence package candidate is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_fails_without_payloads() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_summary_v01.csv").open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01.md").read_text()

    assert len(rows) == 7
    assert {row["populated_audit_status"] for row in rows} == {"POPULATED_EVIDENCE_PACKAGE_AUDIT_FAIL_PAYLOAD_NOT_SUPPLIED"}
    assert {row["populated_candidate_audited"] for row in rows} == {"true"}
    assert {row["payload_record_declared"] for row in rows} == {"true"}
    assert {row["evidence_payload_supplied"] for row in rows} == {"false"}
    assert {row["dimension_payload_supplied"] for row in rows} == {"false"}
    assert {row["replay_payload_supplied"] for row in rows} == {"false"}
    assert {row["firewall_payload_supplied"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["audit_finding"] for row in rows)
    assert all(row["missing_payload_record"] for row in rows)
    assert all(row["payload_population_audit_result"] == "fail_payload_not_supplied" for row in rows)
    assert all(row["package_acceptance_decision"] == "reject_populated_package_for_scoring_input_acceptance" for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_AUDIT_V01",
            "audit_rows_declared": "7",
            "populated_candidate_audited_rows": "7",
            "payload_record_declared_rows": "7",
            "populated_audit_passed_rows": "0",
            "populated_audit_failed_rows": "7",
            "evidence_payload_supplied_rows": "0",
            "dimension_payload_supplied_rows": "0",
            "replay_payload_supplied_rows": "0",
            "firewall_payload_supplied_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "hard_failures_triggered": "0",
            "populated_evidence_package_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_POPULATED_EVIDENCE_PACKAGE_AUDIT_FAILED_PAYLOAD_NOT_SUPPLIED",
                "next_required_artifact": "tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_populated_evidence_package_audit_v01_populated_audit_only_no_evidence_payload_supplied_no_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "All seven rows" in note
    assert "populated evidence package audit is not satisfied" in note


def test_tau_cmb_phi_tau_parent_evidence_payload_acquisition_is_candidate_only() -> None:
    candidate_rows = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01.csv").open())
    )
    candidate_summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_summary_v01.csv").open()
        )
    )
    audit_rows = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01.csv").open())
    )
    audit_summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_summary_v01.csv").open()
        )
    )
    candidate_payload = json.loads((ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01.json").read_text())
    audit_payload = json.loads((ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01.json").read_text())
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01.md").read_text()

    assert len(candidate_rows) == 7
    assert len(audit_rows) == 7
    assert {row["source_artifact_present"] for row in candidate_rows} == {"true"}
    assert {row["hash_bound"] for row in candidate_rows} == {"true"}
    assert {row["endpoint_blind_candidate"] for row in candidate_rows} == {"true"}
    assert {row["semantic_replay_candidate"] for row in candidate_rows} == {"true"}
    assert {row["candidate_payload_supplied"] for row in candidate_rows} == {"true"}
    assert {row["certificate_passed"] for row in candidate_rows} == {"false"}
    assert {row["parent_payload_accepted"] for row in candidate_rows} == {"false"}
    assert {row["score_entry_allowed"] for row in candidate_rows} == {"false"}
    assert {row["candidate_payload_audit_passed"] for row in audit_rows} == {"true"}
    assert {row["parent_acceptance_decision"] for row in audit_rows} == {"reject_for_parent_acceptance_until_certificate_pass"}
    assert {row["certificate_passed"] for row in audit_rows} == {"false"}
    assert {row["parent_payload_accepted"] for row in audit_rows} == {"false"}
    assert {row["score_entry_allowed"] for row in audit_rows} == {"false"}
    assert candidate_summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PAYLOAD_ACQUISITION_CANDIDATE_V01",
            "payload_candidate_rows_declared": "7",
            "source_artifact_present_rows": "7",
            "hash_bound_rows": "7",
            "endpoint_blind_candidate_rows": "7",
            "semantic_replay_candidate_rows": "7",
            "candidate_payload_supplied_rows": "7",
            "dimension_payload_supplied_rows": "4",
            "replay_payload_supplied_rows": "6",
            "firewall_payload_supplied_rows": "3",
            "certificate_pass_candidate_rows": "7",
            "certificate_passed_rows": "0",
            "parent_payload_accepted_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_EVIDENCE_PAYLOAD_CANDIDATES_ACQUIRED_NOT_ACCEPTED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_evidence_payload_acquisition_candidate_v01_payload_candidate_only_semantic_replay_sources_hash_bound_not_parent_input_accepted_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert audit_summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PAYLOAD_ACQUISITION_AUDIT_V01",
            "audit_rows_declared": "7",
            "source_artifact_present_rows": "7",
            "hash_bound_rows": "7",
            "endpoint_blind_candidate_rows": "7",
            "semantic_replay_candidate_rows": "7",
            "candidate_payload_supplied_rows": "7",
            "candidate_payload_audit_passed_rows": "7",
            "certificate_passed_rows": "0",
            "parent_payload_accepted_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_EVIDENCE_PAYLOAD_CANDIDATES_AUDITED_PRESENT_BUT_NOT_ACCEPTED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_evidence_payload_acquisition_audit_v01_audit_only_payload_candidates_present_hash_bound_but_not_parent_accepted_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert candidate_payload["summary"] == candidate_summary[0]
    assert audit_payload["summary"] == audit_summary[0]
    assert "candidate payloads are present and hash-bound" in note
    assert "does not accept parent-side Tau inputs" in note


def test_tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_requires_repackaging() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_summary_v01.csv").open()
        )
    )
    payload = json.loads((ROOT / "data/derived/tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01.json").read_text())
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01.md").read_text()

    assert len(rows) == 7
    assert {row["bridge_status"] for row in rows} == {"CANDIDATE_PAYLOAD_ACQUIRED_REPACKAGING_REQUIRED"}
    assert {row["candidate_payload_audit_passed"] for row in rows} == {"true"}
    assert {row["canonical_submission_packet_present"] for row in rows} == {"false"}
    assert {row["receipt_binding_present"] for row in rows} == {"false"}
    assert {row["dimension_receipt_ready"] for row in rows} == {"false"}
    assert {row["replay_receipt_ready"] for row in rows} == {"false"}
    assert {row["firewall_receipt_ready"] for row in rows} == {"false"}
    assert {row["canonical_repackaging_required"] for row in rows} == {"true"}
    assert {row["intake_bridge_passed"] for row in rows} == {"false"}
    assert {row["parent_payload_accepted"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert {row["bridge_decision"] for row in rows} == {"ROUTE_TO_CANONICAL_PAYLOAD_PACKET_AND_RECEIPT_BINDING"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_EVIDENCE_PAYLOAD_INTAKE_BRIDGE_DECISION_V01",
            "bridge_rows_declared": "7",
            "candidate_payload_audit_passed_rows": "7",
            "canonical_submission_packet_present_rows": "0",
            "receipt_binding_present_rows": "0",
            "dimension_receipt_ready_rows": "0",
            "replay_receipt_ready_rows": "0",
            "firewall_receipt_ready_rows": "0",
            "canonical_repackaging_required_rows": "7",
            "intake_bridge_passed_rows": "0",
            "parent_payload_accepted_rows": "0",
            "certificate_passed_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_EVIDENCE_PAYLOAD_CANDIDATE_ACQUIRED_CANONICAL_REPACKAGING_REQUIRED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_canonical_payload_packet_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_evidence_payload_intake_bridge_decision_v01_bridge_decision_only_candidate_payload_acquired_but_requires_canonical_repackaging_no_parent_acceptance_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert payload["summary"] == summary[0]
    assert "canonical repackaging" in note
    assert "score_ready_rows=0" in note


def test_tau_cmb_phi_tau_parent_canonical_payload_packet_is_materialized_not_accepted() -> None:
    rows = list(csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_canonical_payload_packet_v01.csv").open()))
    summary = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_canonical_payload_packet_summary_v01.csv").open())
    )
    payload = json.loads((ROOT / "data/derived/tau_cmb_phi_tau_parent_canonical_payload_packet_v01.json").read_text())
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_canonical_payload_packet_v01.md").read_text()

    assert len(rows) == 7
    assert {row["canonical_packet_present"] for row in rows} == {"true"}
    assert {row["receipt_binding_present"] for row in rows} == {"true"}
    assert sum(row["dimension_binding_present"] == "true" for row in rows) == 4
    assert sum(row["replay_binding_present"] == "true" for row in rows) == 6
    assert sum(row["firewall_binding_present"] == "true" for row in rows) == 3
    assert {row["canonical_repackaging_completed"] for row in rows} == {"true"}
    assert {row["binding_triads_complete"] for row in rows} == {"false"}
    assert {row["parent_acceptance_ready"] for row in rows} == {"false"}
    assert {row["parent_payload_accepted"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["score_entry_allowed"] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_CANONICAL_PAYLOAD_PACKET_V01",
            "packet_rows_declared": "7",
            "canonical_packet_present_rows": "7",
            "receipt_binding_present_rows": "7",
            "dimension_binding_present_rows": "4",
            "replay_binding_present_rows": "6",
            "firewall_binding_present_rows": "3",
            "canonical_repackaging_completed_rows": "7",
            "binding_triads_complete_rows": "0",
            "parent_acceptance_ready_rows": "0",
            "parent_payload_accepted_rows": "0",
            "certificate_passed_rows": "0",
            "score_ready_rows": "0",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_CANONICAL_PAYLOAD_PACKETS_MATERIALIZED_NOT_ACCEPTED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_canonical_payload_packet_v01_packet_materialization_only_candidate_payloads_repackaged_no_parent_acceptance_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert payload["summary"] == summary[0]
    assert "candidate payloads repackaged as canonical packets" in note
    assert "score_ready_rows=0" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_is_closed() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_v01.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_summary_v01.csv").open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_v01.md").read_text()

    assert len(rows) == 7
    assert {row["submission_gate_status"] for row in rows} == {"SUBMISSION_GATE_DECLARED_NO_PAYLOAD_RECEIVED"}
    assert {row["submission_gate_declared"] for row in rows} == {"true"}
    assert {row["submission_payload_received"] for row in rows} == {"false"}
    assert {row["dimension_payload_received"] for row in rows} == {"false"}
    assert {row["replay_payload_received"] for row in rows} == {"false"}
    assert {row["firewall_payload_received"] for row in rows} == {"false"}
    assert {row["submission_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_submission_object"] for row in rows)
    assert all(row["submission_validation_rule"] for row in rows)
    assert all(row["endpoint_firewall_requirement"] for row in rows)
    assert all(row["gate_decision"] == "closed_until_payload_received" for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SUBMISSION_GATE_V01",
            "gate_rows_declared": "7",
            "submission_gate_declared_rows": "7",
            "submission_payload_received_rows": "0",
            "dimension_payload_received_rows": "0",
            "replay_payload_received_rows": "0",
            "firewall_payload_received_rows": "0",
            "submission_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_submission_gate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SUBMISSION_GATE_DECLARED_NO_PAYLOAD_RECEIVED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_submission_gate_v01_submission_gate_only_no_payload_received_no_submission_accepted_no_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "No submission payload is received or accepted" in note
    assert "evidence payload submission gate is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_is_empty() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_v01.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_summary_v01.csv").open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_v01.md").read_text()

    assert len(rows) == 7
    assert {row["receipt_candidate_status"] for row in rows} == {"RECEIPT_CANDIDATE_DECLARED_NO_PAYLOAD_RECEIVED"}
    assert {row["receipt_candidate_declared"] for row in rows} == {"true"}
    assert {row["payload_received"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["dimension_payload_received"] for row in rows} == {"false"}
    assert {row["replay_payload_received"] for row in rows} == {"false"}
    assert {row["firewall_payload_received"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["expected_receipt_object"] for row in rows)
    assert all(row["receipt_validation_rule"] for row in rows)
    assert all(row["provenance_hash_requirement"] for row in rows)
    assert all(row["receipt_acceptance_gate"] == "receipt remains closed until payload is received" for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_CANDIDATE_V01",
            "receipt_rows_declared": "7",
            "receipt_candidate_declared_rows": "7",
            "payload_received_rows": "0",
            "receipt_accepted_rows": "0",
            "dimension_payload_received_rows": "0",
            "replay_payload_received_rows": "0",
            "firewall_payload_received_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_receipt_candidate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_CANDIDATE_DECLARED_NO_PAYLOAD_RECEIVED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_candidate_v01_receipt_candidate_only_no_payload_received_no_receipt_accepted_no_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "No payload is received and no receipt is accepted" in note
    assert "evidence payload receipt candidate is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_fails_without_payload() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_summary_v01.csv").open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01.md").read_text()

    assert len(rows) == 7
    assert {row["receipt_audit_status"] for row in rows} == {"RECEIPT_AUDIT_FAILED_NO_PAYLOAD_RECEIVED"}
    assert {row["payload_received"] for row in rows} == {"false"}
    assert {row["receipt_candidate_declared"] for row in rows} == {"true"}
    assert {row["receipt_validated"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["dimension_payload_received"] for row in rows} == {"false"}
    assert {row["replay_payload_received"] for row in rows} == {"false"}
    assert {row["firewall_payload_received"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_receipt_object"] for row in rows)
    assert all(row["audit_validation_rule"] for row in rows)
    assert all(row["payload_binding_requirement"] for row in rows)
    assert all(row["provenance_replay_requirement"] for row in rows)
    assert all(row["audit_failure_reason"] == "no payload record is available for receipt validation" for row in rows)
    assert all(row["audit_decision"] == "failed_until_payload_and_receipt_are_supplied" for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_AUDIT_V01",
            "audit_rows_declared": "7",
            "receipt_candidate_declared_rows": "7",
            "payload_received_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "dimension_payload_received_rows": "0",
            "replay_payload_received_rows": "0",
            "firewall_payload_received_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_receipt_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_AUDIT_FAILED_NO_PAYLOAD_RECEIVED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_audit_v01_receipt_audit_only_no_payload_received_no_receipt_validated_no_receipt_accepted_no_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "No payload record is available" in note
    assert "evidence payload receipt audit is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_is_not_completed() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01.md").read_text()

    assert len(rows) == 7
    assert {row["remediation_status"] for row in rows} == {"REMEDIATION_DECLARED_NOT_COMPLETED"}
    assert {row["payload_received"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["receipt_validated"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["dimension_payload_received"] for row in rows} == {"false"}
    assert {row["replay_payload_received"] for row in rows} == {"false"}
    assert {row["firewall_payload_received"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["missing_payload_object"] for row in rows)
    assert all(row["required_remediation_action"] for row in rows)
    assert all(row["required_receipt_binding"] for row in rows)
    assert all(row["required_evidence_bundle"] == "payload object plus provenance hash plus replay command plus artifact path" for row in rows)
    assert all(
        row["acceptance_exit_gate"] == "may exit only after matching payload and receipt are supplied and audit-passed"
        for row in rows
    )
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_REMEDIATION_PLAN_V01",
            "remediation_rows_declared": "7",
            "payload_received_rows": "0",
            "remediation_completed_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "dimension_payload_received_rows": "0",
            "replay_payload_received_rows": "0",
            "firewall_payload_received_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_receipt_remediation_plan_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_RECEIPT_REMEDIATION_PLAN_DECLARED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_receipt_remediation_plan_v01_remediation_plan_only_no_payload_materialized_no_remediation_completed_no_receipt_validated_no_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "It does not supply or validate any payload" in note
    assert "evidence payload receipt remediation plan is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_is_schema_only() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_v01.md").read_text()

    assert len(rows) == 7
    assert {row["materialization_status"] for row in rows} == {
        "MATERIALIZATION_PACKET_DECLARED_NO_PAYLOAD_MATERIALIZED"
    }
    assert {row["payload_materialized"] for row in rows} == {"false"}
    assert {row["packet_accepted"] for row in rows} == {"false"}
    assert {row["receipt_validated"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["dimension_payload_received"] for row in rows} == {"false"}
    assert {row["replay_payload_received"] for row in rows} == {"false"}
    assert {row["firewall_payload_received"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["packet_slot_object"] for row in rows)
    assert all(row["materialization_requirement"] for row in rows)
    assert all(row["dimension_requirement"] for row in rows)
    assert all(row["replay_requirement"] for row in rows)
    assert all(row["firewall_requirement"] for row in rows)
    assert all(row["receipt_binding_requirement"] for row in rows)
    assert all(
        row["acceptance_exit_gate"] == "may exit only after packet is materialized, receipt-bound, and audit-passed"
        for row in rows
    )
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_MATERIALIZATION_PACKET_V01",
            "packet_rows_declared": "7",
            "payload_materialized_rows": "0",
            "packet_accepted_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "dimension_payload_received_rows": "0",
            "replay_payload_received_rows": "0",
            "firewall_payload_received_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_materialization_packet_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_MATERIALIZATION_PACKET_DECLARED_NO_PAYLOAD_MATERIALIZED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_materialization_packet_v01_packet_schema_only_no_payload_materialized_no_packet_accepted_no_receipt_validated_no_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "It does not materialize or accept any payload" in note
    assert "evidence payload materialization packet is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_fails_without_packet() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01.md").read_text()

    assert len(rows) == 7
    assert {row["materialization_audit_status"] for row in rows} == {
        "MATERIALIZATION_AUDIT_FAILED_NO_PAYLOAD_MATERIALIZED"
    }
    assert {row["payload_materialized"] for row in rows} == {"false"}
    assert {row["packet_accepted"] for row in rows} == {"false"}
    assert {row["receipt_validated"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["dimension_payload_received"] for row in rows} == {"false"}
    assert {row["replay_payload_received"] for row in rows} == {"false"}
    assert {row["firewall_payload_received"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["packet_slot_object"] for row in rows)
    assert all(row["required_materialization_check"] for row in rows)
    assert all(row["dimension_check"] for row in rows)
    assert all(row["replay_check"] for row in rows)
    assert all(row["firewall_check"] for row in rows)
    assert all(row["receipt_binding_check"] for row in rows)
    assert all(row["audit_failure_reason"] == "no materialized payload packet is available for audit" for row in rows)
    assert all(row["audit_decision"] == "failed_until_packet_is_materialized_and_receipt_bound" for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_MATERIALIZATION_AUDIT_V01",
            "audit_rows_declared": "7",
            "payload_materialized_rows": "0",
            "packet_accepted_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "dimension_payload_received_rows": "0",
            "replay_payload_received_rows": "0",
            "firewall_payload_received_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_materialization_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_MATERIALIZATION_AUDIT_FAILED_NO_PAYLOAD_MATERIALIZED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_materialization_audit_v01_materialization_audit_only_no_payload_materialized_no_packet_accepted_no_receipt_validated_no_package_pass_no_certificate_pass_no_payload_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "No materialized payload packet is available for audit" in note
    assert "evidence payload materialization audit is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_blocks_without_materialization() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_summary_v01.csv").open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01.md").read_text()

    assert len(rows) == 7
    assert {row["acceptance_precheck_status"] for row in rows} == {
        "ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_SATISFIED"
    }
    assert {row["payload_materialized"] for row in rows} == {"false"}
    assert {row["packet_accepted"] for row in rows} == {"false"}
    assert {row["receipt_validated"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["dimension_payload_received"] for row in rows} == {"false"}
    assert {row["replay_payload_received"] for row in rows} == {"false"}
    assert {row["firewall_payload_received"] for row in rows} == {"false"}
    assert {row["acceptance_precheck_passed"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_input_object"] for row in rows)
    assert all(row["materialization_gate"] for row in rows)
    assert all(row["receipt_gate"] for row in rows)
    assert all(row["dimension_gate"] for row in rows)
    assert all(row["replay_gate"] for row in rows)
    assert all(row["firewall_gate"] for row in rows)
    assert all(row["acceptance_blocker"] == "materialization audit failed because no payload packet is materialized" for row in rows)
    assert all(
        row["precheck_decision"] == "blocked_until_materialization_receipt_dimension_replay_and_firewall_gates_pass"
        for row in rows
    )
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_PRECHECK_V01",
            "precheck_rows_declared": "7",
            "payload_materialized_rows": "0",
            "packet_accepted_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "dimension_payload_received_rows": "0",
            "replay_payload_received_rows": "0",
            "firewall_payload_received_rows": "0",
            "acceptance_precheck_passed_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_acceptance_precheck_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_SATISFIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_precheck_v01_acceptance_precheck_only_no_payload_materialized_no_packet_accepted_no_receipt_validated_no_acceptance_pass_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "no payload is accepted" in note
    assert "evidence payload acceptance precheck is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_is_not_completed() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01.md").read_text()

    assert len(rows) == 7
    assert {row["unblock_status"] for row in rows} == {"UNBLOCK_DECLARED_NOT_COMPLETED"}
    assert {row["unblock_completed"] for row in rows} == {"false"}
    assert {row["payload_materialized"] for row in rows} == {"false"}
    assert {row["packet_accepted"] for row in rows} == {"false"}
    assert {row["receipt_validated"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["dimension_payload_received"] for row in rows} == {"false"}
    assert {row["replay_payload_received"] for row in rows} == {"false"}
    assert {row["firewall_payload_received"] for row in rows} == {"false"}
    assert {row["acceptance_precheck_passed"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["blocked_gate"] for row in rows)
    assert all(row["required_unblock_action"] for row in rows)
    assert all(row["required_evidence_object"] for row in rows)
    assert all(
        row["required_exit_condition"] == "gate may exit only after evidence object is supplied and audit-passed"
        for row in rows
    )
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_UNBLOCK_PLAN_V01",
            "unblock_rows_declared": "7",
            "unblock_completed_rows": "0",
            "payload_materialized_rows": "0",
            "packet_accepted_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "dimension_payload_received_rows": "0",
            "replay_payload_received_rows": "0",
            "firewall_payload_received_rows": "0",
            "acceptance_precheck_passed_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_acceptance_unblock_plan_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_unblock_plan_v01_unblock_plan_only_no_unblock_completed_no_payload_materialized_no_packet_accepted_no_acceptance_pass_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "No unblock action is completed and no payload is accepted" in note
    assert "evidence payload acceptance unblock plan is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_is_closed() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01.md").read_text()

    assert len(rows) == 7
    assert {row["decision_gate_status"] for row in rows} == {"ACCEPTANCE_DECISION_CLOSED_UNBLOCK_NOT_COMPLETED"}
    assert {row["decision_output"] for row in rows} == {"acceptance_closed"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["unblock_completed"] for row in rows} == {"false"}
    assert {row["payload_materialized"] for row in rows} == {"false"}
    assert {row["packet_accepted"] for row in rows} == {"false"}
    assert {row["receipt_validated"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["dimension_payload_received"] for row in rows} == {"false"}
    assert {row["replay_payload_received"] for row in rows} == {"false"}
    assert {row["firewall_payload_received"] for row in rows} == {"false"}
    assert {row["acceptance_precheck_passed"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["target_gate"] for row in rows)
    assert all(row["required_prior_pass"] for row in rows)
    assert all(row["decision_rule"] == "acceptance may open only if all upstream evidence gates are completed and audit-passed" for row in rows)
    assert all(row["decision_reason"] == "acceptance unblock plan is not satisfied" for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_DECISION_GATE_V01",
            "decision_rows_declared": "7",
            "acceptance_allowed_rows": "0",
            "unblock_completed_rows": "0",
            "payload_materialized_rows": "0",
            "packet_accepted_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "dimension_payload_received_rows": "0",
            "replay_payload_received_rows": "0",
            "firewall_payload_received_rows": "0",
            "acceptance_precheck_passed_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_acceptance_decision_gate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_ACCEPTANCE_DECISION_GATE_CLOSED_UNBLOCK_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_acceptance_decision_gate_v01_decision_gate_only_no_acceptance_allowed_no_payload_accepted_no_scoring_input_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "acceptance remains closed" in note
    assert "evidence payload acceptance decision gate is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_is_not_accepted() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01.md").read_text()

    assert len(rows) == 7
    assert {row["scoring_input_candidate_status"] for row in rows} == {
        "SCORING_INPUT_CANDIDATE_DECLARED_ACCEPTANCE_DECISION_CLOSED"
    }
    assert {row["scoring_input_candidate_declared"] for row in rows} == {"true"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_accepted_payload"] for row in rows)
    assert all(row["candidate_construction_rule"] for row in rows)
    assert all(row["required_acceptance_decision"] for row in rows)
    assert all(row["required_scoring_contract"] for row in rows)
    assert all(row["candidate_blocker"] == "acceptance decision gate is closed" for row in rows)
    assert all(row["candidate_decision"] == "candidate_declared_but_not_accepted" for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_CANDIDATE_V01",
            "candidate_rows_declared": "7",
            "scoring_input_candidate_declared_rows": "7",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_candidate_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_CANDIDATE_DECLARED_NOT_ACCEPTED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_candidate_v01_candidate_only_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "no scoring input is accepted" in note
    assert "evidence payload scoring input candidate is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_rejects_candidates() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_summary_v01.csv").open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01.md").read_text()

    assert len(rows) == 7
    assert {row["audit_status"] for row in rows} == {
        "SCORING_INPUT_AUDITED_REJECTED_ACCEPTANCE_DECISION_CLOSED"
    }
    assert {row["scoring_input_candidate_declared"] for row in rows} == {"true"}
    assert {row["scoring_input_audited"] for row in rows} == {"true"}
    assert {row["scoring_input_audit_passed"] for row in rows} == {"false"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_accepted_payload"] for row in rows)
    assert all(row["required_acceptance_decision"] for row in rows)
    assert all(row["required_scoring_contract"] for row in rows)
    assert all(
        row["audit_finding"] == "required accepted payload is absent because acceptance decision gate is closed"
        for row in rows
    )
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_AUDIT_V01",
            "audit_rows_declared": "7",
            "scoring_input_audited_rows": "7",
            "scoring_input_audit_passed_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_AUDIT_REJECTED_ACCEPTANCE_DECISION_CLOSED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_audit_v01_audit_only_scoring_input_rejected_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "audits the declared scoring-input candidates" in note
    assert "evidence payload scoring input audit is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_is_not_completed() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["remediation_status"] for row in rows} == {"REMEDIATION_REQUIRED_NOT_COMPLETED"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_audit_passed"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_remediation_action"] for row in rows)
    assert all(row["minimal_acceptance_evidence"] for row in rows)
    assert all(row["acceptance_exit_condition"] for row in rows)
    assert all(row["scoring_contract_exit_condition"] for row in rows)
    assert all(
        row["blocking_finding"] == "required accepted payload is absent because acceptance decision gate is closed"
        for row in rows
    )
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PLAN_V01",
            "remediation_rows_declared": "7",
            "remediation_completed_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_audit_passed_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_remediation_plan_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PLAN_DECLARED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_plan_v01_plan_only_remediation_not_completed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "minimal remediation actions" in note
    assert "evidence payload scoring input remediation plan is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_is_schema_only() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["packet_status"] for row in rows} == {"REMEDIATION_PACKET_SCHEMA_DECLARED_NOT_MATERIALIZED"}
    assert {row["packet_materialized"] for row in rows} == {"false"}
    assert {row["packet_submitted"] for row in rows} == {"false"}
    assert {row["packet_audit_passed"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_audit_passed"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["packet_slot"] for row in rows)
    assert all(row["required_payload_evidence"] for row in rows)
    assert all(row["required_packet_schema"] for row in rows)
    assert all(row["required_hash_evidence"] for row in rows)
    assert all(row["required_firewall_evidence"] for row in rows)
    assert all(row["packet_exit_condition"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PACKET_V01",
            "packet_rows_declared": "7",
            "packet_materialized_rows": "0",
            "packet_submitted_rows": "0",
            "packet_audit_passed_rows": "0",
            "remediation_completed_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_audit_passed_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_remediation_packet_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PACKET_DECLARED_NOT_MATERIALIZED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_v01_packet_schema_only_packet_not_materialized_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "packet-schema" in note
    assert "requirements" in note
    assert "evidence payload scoring input remediation packet is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_rejects_unmaterialized_packet() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["packet_audit_status"] for row in rows} == {
        "REMEDIATION_PACKET_AUDIT_REJECTED_NOT_MATERIALIZED"
    }
    assert {row["packet_materialized"] for row in rows} == {"false"}
    assert {row["packet_submitted"] for row in rows} == {"false"}
    assert {row["packet_audit_passed"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_audit_passed"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_packet_slot"] for row in rows)
    assert all(row["required_payload_evidence"] for row in rows)
    assert all(row["required_hash_evidence"] for row in rows)
    assert all(row["required_firewall_evidence"] for row in rows)
    assert all(
        row["packet_audit_finding"] == "remediation packet schema is declared but no packet is materialized or submitted"
        for row in rows
    )
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PACKET_AUDIT_V01",
            "packet_audit_rows_declared": "7",
            "packet_materialized_rows": "0",
            "packet_submitted_rows": "0",
            "packet_audit_passed_rows": "0",
            "remediation_completed_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_audit_passed_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_remediation_packet_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_REMEDIATION_PACKET_AUDIT_REJECTED_NOT_MATERIALIZED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_remediation_packet_audit_v01_audit_only_packet_audit_rejected_not_materialized_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "audits the remediation packet schema" in note
    assert "evidence payload scoring input remediation packet audit is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_is_unfulfilled() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["request_status"] for row in rows} == {"MATERIALIZATION_REQUEST_DECLARED_NOT_FULFILLED"}
    assert {row["materialization_requested"] for row in rows} == {"true"}
    assert {row["packet_materialized"] for row in rows} == {"false"}
    assert {row["packet_submitted"] for row in rows} == {"false"}
    assert {row["packet_audit_passed"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_packet_slot"] for row in rows)
    assert all(row["required_payload_file"] for row in rows)
    assert all(row["required_provenance_file"] for row in rows)
    assert all(row["required_replay_command"] for row in rows)
    assert all(row["required_hash_manifest"] for row in rows)
    assert all(row["required_firewall_attestation"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_REQUEST_V01",
            "materialization_request_rows_declared": "7",
            "materialization_requested_rows": "7",
            "packet_materialized_rows": "0",
            "packet_submitted_rows": "0",
            "packet_audit_passed_rows": "0",
            "remediation_completed_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_materialization_request_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_REQUEST_DECLARED_NOT_FULFILLED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_v01_request_only_materialization_not_fulfilled_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "materialization request needed" in note
    assert "evidence payload scoring input materialization request is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_is_not_fulfilled() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["request_audit_status"] for row in rows} == {"MATERIALIZATION_REQUEST_AUDITED_NOT_FULFILLED"}
    assert {row["materialization_requested"] for row in rows} == {"true"}
    assert {row["request_audited"] for row in rows} == {"true"}
    assert {row["request_audit_passed"] for row in rows} == {"false"}
    assert {row["packet_materialized"] for row in rows} == {"false"}
    assert {row["packet_submitted"] for row in rows} == {"false"}
    assert {row["packet_audit_passed"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_packet_slot"] for row in rows)
    assert all(row["required_payload_file"] for row in rows)
    assert all(row["required_provenance_file"] for row in rows)
    assert all(row["required_replay_command"] for row in rows)
    assert all(row["required_hash_manifest"] for row in rows)
    assert all(row["required_firewall_attestation"] for row in rows)
    assert all(
        row["request_audit_finding"]
        == "materialization request is declared but no requested packet is materialized or submitted"
        for row in rows
    )
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_REQUEST_AUDIT_V01",
            "materialization_request_audit_rows_declared": "7",
            "materialization_requested_rows": "7",
            "request_audited_rows": "7",
            "request_audit_passed_rows": "0",
            "packet_materialized_rows": "0",
            "packet_submitted_rows": "0",
            "packet_audit_passed_rows": "0",
            "remediation_completed_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_materialization_request_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_REQUEST_AUDIT_NOT_FULFILLED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_request_audit_v01_audit_only_materialization_request_unfulfilled_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "audits the materialization request" in note
    assert "evidence payload scoring input materialization request audit is not" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_is_shell_only() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["packet_status"] for row in rows} == {
        "MATERIALIZATION_PACKET_SHELL_DECLARED_ACTUAL_PAYLOAD_ABSENT"
    }
    assert {row["packet_shell_declared"] for row in rows} == {"true"}
    assert {row["actual_payload_present"] for row in rows} == {"false"}
    assert {row["actual_provenance_present"] for row in rows} == {"false"}
    assert {row["actual_replay_command_present"] for row in rows} == {"false"}
    assert {row["actual_hash_manifest_present"] for row in rows} == {"false"}
    assert {row["actual_firewall_attestation_present"] for row in rows} == {"false"}
    assert {row["packet_materialized"] for row in rows} == {"false"}
    assert {row["packet_submitted"] for row in rows} == {"false"}
    assert {row["packet_audit_passed"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["packet_shell_slot"] for row in rows)
    assert all(row["expected_payload_file"] for row in rows)
    assert all(row["expected_provenance_file"] for row in rows)
    assert all(row["expected_replay_command_file"] for row in rows)
    assert all(row["expected_hash_manifest_file"] for row in rows)
    assert all(row["expected_firewall_attestation_file"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_PACKET_V01",
            "materialization_packet_rows_declared": "7",
            "packet_shell_declared_rows": "7",
            "actual_payload_present_rows": "0",
            "actual_provenance_present_rows": "0",
            "actual_replay_command_present_rows": "0",
            "actual_hash_manifest_present_rows": "0",
            "actual_firewall_attestation_present_rows": "0",
            "packet_materialized_rows": "0",
            "packet_submitted_rows": "0",
            "packet_audit_passed_rows": "0",
            "remediation_completed_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_materialization_packet_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_PACKET_SHELL_DECLARED_ACTUAL_PAYLOAD_ABSENT",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_v01_packet_shell_only_actual_payload_absent_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "materialization packet shell" in note
    assert "evidence payload scoring input materialization packet is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_is_not_satisfied() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["packet_audit_status"] for row in rows} == {
        "MATERIALIZATION_PACKET_AUDITED_ACTUAL_PAYLOAD_ABSENT"
    }
    assert {row["packet_shell_declared"] for row in rows} == {"true"}
    assert {row["packet_shell_audited"] for row in rows} == {"true"}
    assert {row["actual_payload_present"] for row in rows} == {"false"}
    assert {row["actual_provenance_present"] for row in rows} == {"false"}
    assert {row["actual_replay_command_present"] for row in rows} == {"false"}
    assert {row["actual_hash_manifest_present"] for row in rows} == {"false"}
    assert {row["actual_firewall_attestation_present"] for row in rows} == {"false"}
    assert {row["packet_materialized"] for row in rows} == {"false"}
    assert {row["packet_submitted"] for row in rows} == {"false"}
    assert {row["packet_audit_passed"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["packet_shell_slot"] for row in rows)
    assert all(row["expected_payload_file"] for row in rows)
    assert all(row["expected_provenance_file"] for row in rows)
    assert all(row["expected_replay_command_file"] for row in rows)
    assert all(row["expected_hash_manifest_file"] for row in rows)
    assert all(row["expected_firewall_attestation_file"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_PACKET_AUDIT_V01",
            "materialization_packet_audit_rows_declared": "7",
            "packet_shell_declared_rows": "7",
            "packet_shell_audited_rows": "7",
            "actual_payload_present_rows": "0",
            "actual_provenance_present_rows": "0",
            "actual_replay_command_present_rows": "0",
            "actual_hash_manifest_present_rows": "0",
            "actual_firewall_attestation_present_rows": "0",
            "packet_materialized_rows": "0",
            "packet_submitted_rows": "0",
            "packet_audit_passed_rows": "0",
            "remediation_completed_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_materialization_packet_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_MATERIALIZATION_PACKET_AUDITED_ACTUAL_PAYLOAD_ABSENT",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_materialization_packet_audit_v01_audit_only_packet_shell_audited_actual_payload_absent_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "audits the materialization packet shell" in note
    assert "evidence payload scoring input materialization packet audit is not" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_is_not_supplied() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["fulfillment_request_status"] for row in rows} == {
        "PAYLOAD_FULFILLMENT_REQUEST_DECLARED_NOT_SUPPLIED"
    }
    assert {row["fulfillment_requested"] for row in rows} == {"true"}
    assert {row["payload_supplied"] for row in rows} == {"false"}
    assert {row["provenance_supplied"] for row in rows} == {"false"}
    assert {row["replay_supplied"] for row in rows} == {"false"}
    assert {row["hash_manifest_supplied"] for row in rows} == {"false"}
    assert {row["firewall_attestation_supplied"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_payload_file"] for row in rows)
    assert all(row["required_payload_content"] for row in rows)
    assert all(row["required_schema_or_units"] for row in rows)
    assert all(row["required_provenance_file"] for row in rows)
    assert all(row["required_replay_command_file"] for row in rows)
    assert all(row["required_hash_manifest_file"] for row in rows)
    assert all(row["required_firewall_attestation_file"] for row in rows)
    assert all(row["endpoint_blind_requirement"] for row in rows)
    assert all(row["known_limit_requirement"] for row in rows)
    assert all(row["dimension_requirement"] for row in rows)
    assert all(row["acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_FULFILLMENT_REQUEST_V01",
            "payload_fulfillment_request_rows_declared": "7",
            "fulfillment_requested_rows": "7",
            "payload_supplied_rows": "0",
            "provenance_supplied_rows": "0",
            "replay_supplied_rows": "0",
            "hash_manifest_supplied_rows": "0",
            "firewall_attestation_supplied_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_fulfillment_request_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_FULFILLMENT_REQUEST_DECLARED_NOT_SUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_v01_request_only_payload_fulfillment_not_supplied_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "concrete payload fulfillment request" in note
    assert "evidence payload scoring input payload fulfillment request is not" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_is_not_supplied() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["request_audit_status"] for row in rows} == {
        "PAYLOAD_FULFILLMENT_REQUEST_AUDITED_NOT_SUPPLIED"
    }
    assert {row["fulfillment_requested"] for row in rows} == {"true"}
    assert {row["request_audited"] for row in rows} == {"true"}
    assert {row["request_audit_passed"] for row in rows} == {"false"}
    assert {row["payload_supplied"] for row in rows} == {"false"}
    assert {row["provenance_supplied"] for row in rows} == {"false"}
    assert {row["replay_supplied"] for row in rows} == {"false"}
    assert {row["hash_manifest_supplied"] for row in rows} == {"false"}
    assert {row["firewall_attestation_supplied"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_payload_file"] for row in rows)
    assert all(row["required_payload_content"] for row in rows)
    assert all(row["required_schema_or_units"] for row in rows)
    assert all(row["required_provenance_file"] for row in rows)
    assert all(row["required_replay_command_file"] for row in rows)
    assert all(row["required_hash_manifest_file"] for row in rows)
    assert all(row["required_firewall_attestation_file"] for row in rows)
    assert all(row["endpoint_blind_requirement"] for row in rows)
    assert all(row["known_limit_requirement"] for row in rows)
    assert all(row["dimension_requirement"] for row in rows)
    assert all(row["acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_FULFILLMENT_REQUEST_AUDIT_V01",
            "payload_fulfillment_request_audit_rows_declared": "7",
            "fulfillment_requested_rows": "7",
            "request_audited_rows": "7",
            "request_audit_passed_rows": "0",
            "payload_supplied_rows": "0",
            "provenance_supplied_rows": "0",
            "replay_supplied_rows": "0",
            "hash_manifest_supplied_rows": "0",
            "firewall_attestation_supplied_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_fulfillment_request_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_FULFILLMENT_REQUEST_AUDITED_NOT_SUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_fulfillment_request_audit_v01_audit_only_payload_fulfillment_request_audited_not_supplied_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "audits the concrete payload fulfillment request" in note
    assert "evidence payload scoring input payload fulfillment request audit is not" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_is_not_submitted() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["submission_packet_status"] for row in rows} == {
        "PAYLOAD_SUBMISSION_PACKET_SHELL_DECLARED_NOT_SUBMITTED"
    }
    assert {row["submission_packet_declared"] for row in rows} == {"true"}
    assert {row["payload_submitted"] for row in rows} == {"false"}
    assert {row["provenance_submitted"] for row in rows} == {"false"}
    assert {row["replay_submitted"] for row in rows} == {"false"}
    assert {row["hash_manifest_submitted"] for row in rows} == {"false"}
    assert {row["firewall_attestation_submitted"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["submission_packet_slot"] for row in rows)
    assert all(row["required_payload_file"] for row in rows)
    assert all(row["required_payload_content"] for row in rows)
    assert all(row["required_schema_or_units"] for row in rows)
    assert all(row["required_provenance_file"] for row in rows)
    assert all(row["required_replay_command_file"] for row in rows)
    assert all(row["required_hash_manifest_file"] for row in rows)
    assert all(row["required_firewall_attestation_file"] for row in rows)
    assert all(row["endpoint_blind_requirement"] for row in rows)
    assert all(row["known_limit_requirement"] for row in rows)
    assert all(row["dimension_requirement"] for row in rows)
    assert all(row["acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_PACKET_V01",
            "payload_submission_packet_rows_declared": "7",
            "submission_packet_declared_rows": "7",
            "payload_submitted_rows": "0",
            "provenance_submitted_rows": "0",
            "replay_submitted_rows": "0",
            "hash_manifest_submitted_rows": "0",
            "firewall_attestation_submitted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_packet_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_PACKET_SHELL_DECLARED_NOT_SUBMITTED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_v01_packet_shell_only_payload_not_submitted_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission packet shell" in note
    assert "evidence payload scoring input payload submission packet is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_is_not_submitted() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["submission_packet_audit_status"] for row in rows} == {
        "PAYLOAD_SUBMISSION_PACKET_AUDITED_NOT_SUBMITTED"
    }
    assert {row["submission_packet_declared"] for row in rows} == {"true"}
    assert {row["submission_packet_audited"] for row in rows} == {"true"}
    assert {row["submission_packet_audit_passed"] for row in rows} == {"false"}
    assert {row["payload_submitted"] for row in rows} == {"false"}
    assert {row["provenance_submitted"] for row in rows} == {"false"}
    assert {row["replay_submitted"] for row in rows} == {"false"}
    assert {row["hash_manifest_submitted"] for row in rows} == {"false"}
    assert {row["firewall_attestation_submitted"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["submission_packet_slot"] for row in rows)
    assert all(row["required_payload_file"] for row in rows)
    assert all(row["required_payload_content"] for row in rows)
    assert all(row["required_schema_or_units"] for row in rows)
    assert all(row["required_provenance_file"] for row in rows)
    assert all(row["required_replay_command_file"] for row in rows)
    assert all(row["required_hash_manifest_file"] for row in rows)
    assert all(row["required_firewall_attestation_file"] for row in rows)
    assert all(row["endpoint_blind_requirement"] for row in rows)
    assert all(row["known_limit_requirement"] for row in rows)
    assert all(row["dimension_requirement"] for row in rows)
    assert all(row["acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_PACKET_AUDIT_V01",
            "payload_submission_packet_audit_rows_declared": "7",
            "submission_packet_declared_rows": "7",
            "submission_packet_audited_rows": "7",
            "submission_packet_audit_passed_rows": "0",
            "payload_submitted_rows": "0",
            "provenance_submitted_rows": "0",
            "replay_submitted_rows": "0",
            "hash_manifest_submitted_rows": "0",
            "firewall_attestation_submitted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_packet_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_PACKET_AUDITED_NOT_SUBMITTED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_packet_audit_v01_audit_only_submission_packet_audited_payload_not_submitted_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "audits the payload submission packet shell" in note
    assert "evidence payload scoring input payload submission packet audit is not" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_is_not_completed() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["remediation_status"] for row in rows} == {
        "SUBMISSION_REMEDIATION_PLANNED_NOT_COMPLETED"
    }
    assert {row["remediation_planned"] for row in rows} == {"true"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["payload_submitted"] for row in rows} == {"false"}
    assert {row["provenance_submitted"] for row in rows} == {"false"}
    assert {row["replay_submitted"] for row in rows} == {"false"}
    assert {row["hash_manifest_submitted"] for row in rows} == {"false"}
    assert {row["firewall_attestation_submitted"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["failed_submission_condition"] for row in rows)
    assert all(row["required_payload_file"] for row in rows)
    assert all(row["required_remediation_action"] for row in rows)
    assert all(row["required_completion_evidence"] for row in rows)
    assert all(row["endpoint_blind_requirement"] for row in rows)
    assert all(row["known_limit_requirement"] for row in rows)
    assert all(row["dimension_requirement"] for row in rows)
    assert all(row["acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PLAN_V01",
            "payload_submission_remediation_plan_rows_declared": "7",
            "remediation_planned_rows": "7",
            "remediation_completed_rows": "0",
            "payload_submitted_rows": "0",
            "provenance_submitted_rows": "0",
            "replay_submitted_rows": "0",
            "hash_manifest_submitted_rows": "0",
            "firewall_attestation_submitted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_remediation_plan_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PLANNED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_plan_v01_plan_only_submission_remediation_not_completed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "targeted remediation plan" in note
    assert "evidence payload scoring input payload submission remediation plan is not" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_is_not_materialized() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["remediation_packet_status"] for row in rows} == {
        "SUBMISSION_REMEDIATION_PACKET_SHELL_DECLARED_NOT_MATERIALIZED"
    }
    assert {row["remediation_packet_declared"] for row in rows} == {"true"}
    assert {row["remediation_packet_materialized"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["payload_submitted"] for row in rows} == {"false"}
    assert {row["provenance_submitted"] for row in rows} == {"false"}
    assert {row["replay_submitted"] for row in rows} == {"false"}
    assert {row["hash_manifest_submitted"] for row in rows} == {"false"}
    assert {row["firewall_attestation_submitted"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["remediation_packet_slot"] for row in rows)
    assert all(row["required_payload_file"] for row in rows)
    assert all(row["required_remediation_action"] for row in rows)
    assert all(row["required_completion_evidence"] for row in rows)
    assert all(row["expected_completion_evidence_file"] for row in rows)
    assert all(row["expected_provenance_file"] for row in rows)
    assert all(row["expected_replay_command_file"] for row in rows)
    assert all(row["expected_hash_manifest_file"] for row in rows)
    assert all(row["expected_firewall_attestation_file"] for row in rows)
    assert all(row["endpoint_blind_requirement"] for row in rows)
    assert all(row["known_limit_requirement"] for row in rows)
    assert all(row["dimension_requirement"] for row in rows)
    assert all(row["acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PACKET_V01",
            "payload_submission_remediation_packet_rows_declared": "7",
            "remediation_packet_declared_rows": "7",
            "remediation_packet_materialized_rows": "0",
            "remediation_completed_rows": "0",
            "payload_submitted_rows": "0",
            "provenance_submitted_rows": "0",
            "replay_submitted_rows": "0",
            "hash_manifest_submitted_rows": "0",
            "firewall_attestation_submitted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_remediation_packet_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PACKET_SHELL_DECLARED_NOT_MATERIALIZED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_v01_packet_shell_only_submission_remediation_packet_not_materialized_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "remediation packet shell" in note
    assert "evidence payload scoring input payload submission remediation packet is" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_rejects_unmaterialized_packet() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["packet_audit_status"] for row in rows} == {
        "SUBMISSION_REMEDIATION_PACKET_AUDIT_REJECTED_NOT_MATERIALIZED"
    }
    assert {row["packet_declared"] for row in rows} == {"true"}
    assert {row["packet_materialized"] for row in rows} == {"false"}
    assert {row["packet_submitted"] for row in rows} == {"false"}
    assert {row["packet_audit_passed"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_audit_passed"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_packet_slot"] for row in rows)
    assert all(row["required_payload_evidence"] for row in rows)
    assert all(row["required_completion_evidence"] for row in rows)
    assert all(row["required_provenance_evidence"] for row in rows)
    assert all(row["required_replay_evidence"] for row in rows)
    assert all(row["required_hash_evidence"] for row in rows)
    assert all(row["required_firewall_evidence"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PACKET_AUDIT_V01",
            "payload_submission_remediation_packet_audit_rows_declared": "7",
            "packet_declared_rows": "7",
            "packet_materialized_rows": "0",
            "packet_submitted_rows": "0",
            "packet_audit_passed_rows": "0",
            "remediation_completed_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_audit_passed_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_remediation_packet_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_REMEDIATION_PACKET_AUDIT_REJECTED_NOT_MATERIALIZED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_remediation_packet_audit_v01_audit_only_submission_remediation_packet_audit_rejected_not_materialized_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "packet audit rejected" in note
    assert "evidence payload scoring input payload submission remediation packet audit" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_is_unfulfilled() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["request_status"] for row in rows} == {
        "SUBMISSION_MATERIALIZATION_REQUEST_DECLARED_NOT_FULFILLED"
    }
    assert {row["materialization_requested"] for row in rows} == {"true"}
    assert {row["packet_materialized"] for row in rows} == {"false"}
    assert {row["packet_submitted"] for row in rows} == {"false"}
    assert {row["packet_audit_passed"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_packet_slot"] for row in rows)
    assert all(row["required_payload_file"] for row in rows)
    assert all(row["required_completion_evidence_file"] for row in rows)
    assert all(row["required_provenance_file"] for row in rows)
    assert all(row["required_replay_command_file"] for row in rows)
    assert all(row["required_hash_manifest_file"] for row in rows)
    assert all(row["required_firewall_attestation_file"] for row in rows)
    assert all(row["endpoint_blind_requirement"] for row in rows)
    assert all(row["known_limit_requirement"] for row in rows)
    assert all(row["dimension_requirement"] for row in rows)
    assert all(row["acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_REQUEST_V01",
            "payload_submission_materialization_request_rows_declared": "7",
            "materialization_requested_rows": "7",
            "packet_materialized_rows": "0",
            "packet_submitted_rows": "0",
            "packet_audit_passed_rows": "0",
            "remediation_completed_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_materialization_request_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_REQUEST_DECLARED_NOT_FULFILLED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_v01_request_only_submission_materialization_not_fulfilled_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "materialization request declared but not fulfilled" in note
    assert "evidence payload scoring input payload submission materialization request" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_is_not_fulfilled() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["request_audit_status"] for row in rows} == {
        "SUBMISSION_MATERIALIZATION_REQUEST_AUDITED_NOT_FULFILLED"
    }
    assert {row["materialization_requested"] for row in rows} == {"true"}
    assert {row["request_audited"] for row in rows} == {"true"}
    assert {row["request_audit_passed"] for row in rows} == {"false"}
    assert {row["packet_materialized"] for row in rows} == {"false"}
    assert {row["packet_submitted"] for row in rows} == {"false"}
    assert {row["packet_audit_passed"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_packet_slot"] for row in rows)
    assert all(row["required_payload_file"] for row in rows)
    assert all(row["required_completion_evidence_file"] for row in rows)
    assert all(row["required_provenance_file"] for row in rows)
    assert all(row["required_replay_command_file"] for row in rows)
    assert all(row["required_hash_manifest_file"] for row in rows)
    assert all(row["required_firewall_attestation_file"] for row in rows)
    assert all(row["endpoint_blind_requirement"] for row in rows)
    assert all(row["known_limit_requirement"] for row in rows)
    assert all(row["dimension_requirement"] for row in rows)
    assert all(row["acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_REQUEST_AUDIT_V01",
            "payload_submission_materialization_request_audit_rows_declared": "7",
            "materialization_requested_rows": "7",
            "request_audited_rows": "7",
            "request_audit_passed_rows": "0",
            "packet_materialized_rows": "0",
            "packet_submitted_rows": "0",
            "packet_audit_passed_rows": "0",
            "remediation_completed_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_materialization_request_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_REQUEST_AUDIT_NOT_FULFILLED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_request_audit_v01_audit_only_submission_materialization_request_unfulfilled_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "materialization request audited but not fulfilled" in note
    assert "evidence payload scoring input payload submission materialization request audit" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_is_shell_only() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["packet_status"] for row in rows} == {
        "SUBMISSION_MATERIALIZATION_PACKET_SHELL_DECLARED_ACTUAL_PAYLOAD_ABSENT"
    }
    assert {row["packet_shell_declared"] for row in rows} == {"true"}
    assert {row["actual_payload_present"] for row in rows} == {"false"}
    assert {row["actual_completion_evidence_present"] for row in rows} == {"false"}
    assert {row["actual_provenance_present"] for row in rows} == {"false"}
    assert {row["actual_replay_command_present"] for row in rows} == {"false"}
    assert {row["actual_hash_manifest_present"] for row in rows} == {"false"}
    assert {row["actual_firewall_attestation_present"] for row in rows} == {"false"}
    assert {row["packet_materialized"] for row in rows} == {"false"}
    assert {row["packet_submitted"] for row in rows} == {"false"}
    assert {row["packet_audit_passed"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["packet_shell_slot"] for row in rows)
    assert all(row["expected_payload_file"] for row in rows)
    assert all(row["expected_completion_evidence_file"] for row in rows)
    assert all(row["expected_provenance_file"] for row in rows)
    assert all(row["expected_replay_command_file"] for row in rows)
    assert all(row["expected_hash_manifest_file"] for row in rows)
    assert all(row["expected_firewall_attestation_file"] for row in rows)
    assert all(row["endpoint_blind_requirement"] for row in rows)
    assert all(row["known_limit_requirement"] for row in rows)
    assert all(row["dimension_requirement"] for row in rows)
    assert all(row["acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_PACKET_V01",
            "payload_submission_materialization_packet_rows_declared": "7",
            "packet_shell_declared_rows": "7",
            "actual_payload_present_rows": "0",
            "actual_completion_evidence_present_rows": "0",
            "actual_provenance_present_rows": "0",
            "actual_replay_command_present_rows": "0",
            "actual_hash_manifest_present_rows": "0",
            "actual_firewall_attestation_present_rows": "0",
            "packet_materialized_rows": "0",
            "packet_submitted_rows": "0",
            "packet_audit_passed_rows": "0",
            "remediation_completed_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_materialization_packet_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_PACKET_SHELL_DECLARED_ACTUAL_PAYLOAD_ABSENT",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_v01_packet_shell_only_submission_actual_payload_absent_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "materialization packet shell declared but actual payload absent" in note
    assert "evidence payload scoring input payload submission materialization packet" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_is_not_satisfied() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["packet_audit_status"] for row in rows} == {
        "SUBMISSION_MATERIALIZATION_PACKET_AUDITED_ACTUAL_PAYLOAD_ABSENT"
    }
    assert {row["packet_shell_declared"] for row in rows} == {"true"}
    assert {row["packet_shell_audited"] for row in rows} == {"true"}
    assert {row["actual_payload_present"] for row in rows} == {"false"}
    assert {row["actual_completion_evidence_present"] for row in rows} == {"false"}
    assert {row["actual_provenance_present"] for row in rows} == {"false"}
    assert {row["actual_replay_command_present"] for row in rows} == {"false"}
    assert {row["actual_hash_manifest_present"] for row in rows} == {"false"}
    assert {row["actual_firewall_attestation_present"] for row in rows} == {"false"}
    assert {row["packet_materialized"] for row in rows} == {"false"}
    assert {row["packet_submitted"] for row in rows} == {"false"}
    assert {row["packet_audit_passed"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["acceptance_allowed"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["packet_shell_slot"] for row in rows)
    assert all(row["expected_payload_file"] for row in rows)
    assert all(row["expected_completion_evidence_file"] for row in rows)
    assert all(row["expected_provenance_file"] for row in rows)
    assert all(row["expected_replay_command_file"] for row in rows)
    assert all(row["expected_hash_manifest_file"] for row in rows)
    assert all(row["expected_firewall_attestation_file"] for row in rows)
    assert all(row["endpoint_blind_requirement"] for row in rows)
    assert all(row["known_limit_requirement"] for row in rows)
    assert all(row["dimension_requirement"] for row in rows)
    assert all(row["acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_PACKET_AUDIT_V01",
            "payload_submission_materialization_packet_audit_rows_declared": "7",
            "packet_shell_declared_rows": "7",
            "packet_shell_audited_rows": "7",
            "actual_payload_present_rows": "0",
            "actual_completion_evidence_present_rows": "0",
            "actual_provenance_present_rows": "0",
            "actual_replay_command_present_rows": "0",
            "actual_hash_manifest_present_rows": "0",
            "actual_firewall_attestation_present_rows": "0",
            "packet_materialized_rows": "0",
            "packet_submitted_rows": "0",
            "packet_audit_passed_rows": "0",
            "remediation_completed_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_materialization_packet_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_MATERIALIZATION_PACKET_AUDITED_ACTUAL_PAYLOAD_ABSENT",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_materialization_packet_audit_v01_audit_only_submission_packet_shell_audited_actual_payload_absent_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "packet shell audited but actual payload absent" in note
    assert "evidence payload scoring input payload submission materialization packet audit" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_is_not_supplied() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["fulfillment_request_status"] for row in rows} == {
        "SUBMISSION_PAYLOAD_FULFILLMENT_REQUEST_DECLARED_NOT_SUPPLIED"
    }
    assert {row["fulfillment_requested"] for row in rows} == {"true"}
    assert {row["payload_supplied"] for row in rows} == {"false"}
    assert {row["completion_evidence_supplied"] for row in rows} == {"false"}
    assert {row["provenance_supplied"] for row in rows} == {"false"}
    assert {row["replay_supplied"] for row in rows} == {"false"}
    assert {row["hash_manifest_supplied"] for row in rows} == {"false"}
    assert {row["firewall_attestation_supplied"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_payload_file"] for row in rows)
    assert all(row["required_payload_content"] for row in rows)
    assert all(row["required_schema_or_units"] for row in rows)
    assert all(row["required_completion_evidence_file"] for row in rows)
    assert all(row["required_provenance_file"] for row in rows)
    assert all(row["required_replay_command_file"] for row in rows)
    assert all(row["required_hash_manifest_file"] for row in rows)
    assert all(row["required_firewall_attestation_file"] for row in rows)
    assert all(row["endpoint_blind_requirement"] for row in rows)
    assert all(row["known_limit_requirement"] for row in rows)
    assert all(row["dimension_requirement"] for row in rows)
    assert all(row["acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_FULFILLMENT_REQUEST_V01",
            "payload_submission_fulfillment_request_rows_declared": "7",
            "fulfillment_requested_rows": "7",
            "payload_supplied_rows": "0",
            "completion_evidence_supplied_rows": "0",
            "provenance_supplied_rows": "0",
            "replay_supplied_rows": "0",
            "hash_manifest_supplied_rows": "0",
            "firewall_attestation_supplied_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_fulfillment_request_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_FULFILLMENT_REQUEST_DECLARED_NOT_SUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_v01_request_only_submission_payload_fulfillment_not_supplied_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission fulfillment request" in note
    assert "evidence payload scoring input payload submission fulfillment request" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_is_not_supplied() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["request_audit_status"] for row in rows} == {
        "SUBMISSION_PAYLOAD_FULFILLMENT_REQUEST_AUDITED_NOT_SUPPLIED"
    }
    assert {row["fulfillment_requested"] for row in rows} == {"true"}
    assert {row["request_audited"] for row in rows} == {"true"}
    assert {row["request_audit_passed"] for row in rows} == {"false"}
    assert {row["payload_supplied"] for row in rows} == {"false"}
    assert {row["completion_evidence_supplied"] for row in rows} == {"false"}
    assert {row["provenance_supplied"] for row in rows} == {"false"}
    assert {row["replay_supplied"] for row in rows} == {"false"}
    assert {row["hash_manifest_supplied"] for row in rows} == {"false"}
    assert {row["firewall_attestation_supplied"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_payload_file"] for row in rows)
    assert all(row["required_payload_content"] for row in rows)
    assert all(row["required_schema_or_units"] for row in rows)
    assert all(row["required_completion_evidence_file"] for row in rows)
    assert all(row["required_provenance_file"] for row in rows)
    assert all(row["required_replay_command_file"] for row in rows)
    assert all(row["required_hash_manifest_file"] for row in rows)
    assert all(row["required_firewall_attestation_file"] for row in rows)
    assert all(row["endpoint_blind_requirement"] for row in rows)
    assert all(row["known_limit_requirement"] for row in rows)
    assert all(row["dimension_requirement"] for row in rows)
    assert all(row["acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_FULFILLMENT_REQUEST_AUDIT_V01",
            "payload_submission_fulfillment_request_audit_rows_declared": "7",
            "fulfillment_requested_rows": "7",
            "request_audited_rows": "7",
            "request_audit_passed_rows": "0",
            "payload_supplied_rows": "0",
            "completion_evidence_supplied_rows": "0",
            "provenance_supplied_rows": "0",
            "replay_supplied_rows": "0",
            "hash_manifest_supplied_rows": "0",
            "firewall_attestation_supplied_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_FULFILLMENT_REQUEST_AUDITED_NOT_SUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_fulfillment_request_audit_v01_audit_only_submission_payload_fulfillment_request_audited_not_supplied_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission fulfillment request audit" in note
    assert "evidence payload scoring input payload submission fulfillment request audit" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_is_blocked() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["execution_packet_status"] for row in rows} == {
        "SUBMISSION_EXECUTION_PACKET_DECLARED_BLOCKED_PAYLOAD_NOT_SUPPLIED"
    }
    assert {row["execution_packet_declared"] for row in rows} == {"true"}
    assert {row["can_execute"] for row in rows} == {"false"}
    assert {row["execution_attempted"] for row in rows} == {"false"}
    assert {row["execution_succeeded"] for row in rows} == {"false"}
    assert {row["payload_supplied"] for row in rows} == {"false"}
    assert {row["completion_evidence_supplied"] for row in rows} == {"false"}
    assert {row["provenance_supplied"] for row in rows} == {"false"}
    assert {row["replay_supplied"] for row in rows} == {"false"}
    assert {row["hash_manifest_supplied"] for row in rows} == {"false"}
    assert {row["firewall_attestation_supplied"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["execution_command_template"] for row in rows)
    assert all(row["execution_prerequisite_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_PACKET_V01",
            "payload_submission_execution_packet_rows_declared": "7",
            "execution_packet_declared_rows": "7",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "payload_supplied_rows": "0",
            "completion_evidence_supplied_rows": "0",
            "provenance_supplied_rows": "0",
            "replay_supplied_rows": "0",
            "hash_manifest_supplied_rows": "0",
            "firewall_attestation_supplied_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_execution_packet_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_PACKET_DECLARED_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_v01_execution_packet_declared_blocked_payload_not_supplied_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission execution packet" in note
    assert "evidence payload scoring input payload submission execution packet" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_is_blocked() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["execution_packet_audit_status"] for row in rows} == {
        "SUBMISSION_EXECUTION_PACKET_AUDITED_BLOCKED_PAYLOAD_NOT_SUPPLIED"
    }
    assert {row["execution_packet_declared"] for row in rows} == {"true"}
    assert {row["execution_packet_audited"] for row in rows} == {"true"}
    assert {row["execution_packet_audit_passed"] for row in rows} == {"false"}
    assert {row["can_execute"] for row in rows} == {"false"}
    assert {row["execution_attempted"] for row in rows} == {"false"}
    assert {row["execution_succeeded"] for row in rows} == {"false"}
    assert {row["payload_supplied"] for row in rows} == {"false"}
    assert {row["completion_evidence_supplied"] for row in rows} == {"false"}
    assert {row["provenance_supplied"] for row in rows} == {"false"}
    assert {row["replay_supplied"] for row in rows} == {"false"}
    assert {row["hash_manifest_supplied"] for row in rows} == {"false"}
    assert {row["firewall_attestation_supplied"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["execution_command_template"] for row in rows)
    assert all(row["execution_prerequisite_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_PACKET_AUDIT_V01",
            "payload_submission_execution_packet_audit_rows_declared": "7",
            "execution_packet_declared_rows": "7",
            "execution_packet_audited_rows": "7",
            "execution_packet_audit_passed_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "payload_supplied_rows": "0",
            "completion_evidence_supplied_rows": "0",
            "provenance_supplied_rows": "0",
            "replay_supplied_rows": "0",
            "hash_manifest_supplied_rows": "0",
            "firewall_attestation_supplied_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_execution_packet_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_PACKET_AUDITED_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_packet_audit_v01_audit_only_execution_packet_audited_blocked_payload_not_supplied_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission execution packet audit" in note
    assert "evidence payload scoring input payload submission execution packet audit" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_is_open() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["unblock_status"] for row in rows} == {"EXECUTION_UNBLOCK_DECLARED_NOT_COMPLETED"}
    assert {row["execution_packet_audited"] for row in rows} == {"true"}
    assert {row["unblock_completed"] for row in rows} == {"false"}
    assert {row["can_execute"] for row in rows} == {"false"}
    assert {row["execution_attempted"] for row in rows} == {"false"}
    assert {row["execution_succeeded"] for row in rows} == {"false"}
    assert {row["payload_supplied"] for row in rows} == {"false"}
    assert {row["completion_evidence_supplied"] for row in rows} == {"false"}
    assert {row["provenance_supplied"] for row in rows} == {"false"}
    assert {row["replay_supplied"] for row in rows} == {"false"}
    assert {row["hash_manifest_supplied"] for row in rows} == {"false"}
    assert {row["firewall_attestation_supplied"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_unblock_action"] for row in rows)
    assert all(row["required_evidence_object"] for row in rows)
    assert all(row["required_exit_condition"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_UNBLOCK_PLAN_V01",
            "unblock_rows_declared": "7",
            "execution_packet_audited_rows": "7",
            "unblock_completed_rows": "0",
            "payload_supplied_rows": "0",
            "completion_evidence_supplied_rows": "0",
            "provenance_supplied_rows": "0",
            "replay_supplied_rows": "0",
            "hash_manifest_supplied_rows": "0",
            "firewall_attestation_supplied_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_execution_unblock_plan_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_v01_unblock_plan_only_no_unblock_completed_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission execution unblock plan" in note
    assert "evidence payload scoring input payload submission execution unblock plan" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_is_open() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["unblock_plan_audit_status"] for row in rows} == {
        "EXECUTION_UNBLOCK_PLAN_AUDITED_NOT_COMPLETED"
    }
    assert {row["execution_packet_audited"] for row in rows} == {"true"}
    assert {row["unblock_plan_audited"] for row in rows} == {"true"}
    assert {row["unblock_plan_audit_passed"] for row in rows} == {"false"}
    assert {row["unblock_completed"] for row in rows} == {"false"}
    assert {row["can_execute"] for row in rows} == {"false"}
    assert {row["execution_attempted"] for row in rows} == {"false"}
    assert {row["execution_succeeded"] for row in rows} == {"false"}
    assert {row["payload_supplied"] for row in rows} == {"false"}
    assert {row["completion_evidence_supplied"] for row in rows} == {"false"}
    assert {row["provenance_supplied"] for row in rows} == {"false"}
    assert {row["replay_supplied"] for row in rows} == {"false"}
    assert {row["hash_manifest_supplied"] for row in rows} == {"false"}
    assert {row["firewall_attestation_supplied"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_unblock_action"] for row in rows)
    assert all(row["required_evidence_object"] for row in rows)
    assert all(row["required_exit_condition"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_UNBLOCK_PLAN_AUDIT_V01",
            "unblock_plan_audit_rows_declared": "7",
            "execution_packet_audited_rows": "7",
            "unblock_plan_audited_rows": "7",
            "unblock_plan_audit_passed_rows": "0",
            "unblock_completed_rows": "0",
            "payload_supplied_rows": "0",
            "completion_evidence_supplied_rows": "0",
            "provenance_supplied_rows": "0",
            "replay_supplied_rows": "0",
            "hash_manifest_supplied_rows": "0",
            "firewall_attestation_supplied_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EXECUTION_UNBLOCK_PLAN_AUDITED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_execution_unblock_plan_audit_v01_audit_only_unblock_plan_audited_not_completed_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission execution unblock plan audit" in note
    assert "evidence payload scoring input payload submission execution unblock plan audit" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_is_not_supplied() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["request_status"] for row in rows} == {"EVIDENCE_OBJECT_REQUESTED_NOT_SUPPLIED"}
    assert {row["evidence_requested"] for row in rows} == {"true"}
    assert {row["evidence_supplied"] for row in rows} == {"false"}
    assert {row["evidence_audited"] for row in rows} == {"false"}
    assert {row["evidence_accepted"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["can_execute"] for row in rows} == {"false"}
    assert {row["execution_attempted"] for row in rows} == {"false"}
    assert {row["execution_succeeded"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_evidence_file"] for row in rows)
    assert all(row["required_evidence_content"] for row in rows)
    assert all(row["required_schema_or_units"] for row in rows)
    assert all(row["required_acceptance_check"] for row in rows)
    assert all(row["required_firewall_check"] for row in rows)
    assert all(row["required_replay_check"] for row in rows)
    assert all(row["required_hash_check"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_REQUEST_V01",
            "evidence_object_request_rows_declared": "7",
            "evidence_requested_rows": "7",
            "evidence_supplied_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_request_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_REQUESTED_NOT_SUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_v01_request_only_evidence_objects_not_supplied_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission evidence object request" in note
    assert "evidence payload scoring input payload submission evidence object request" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_is_not_supplied() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["request_audit_status"] for row in rows} == {"EVIDENCE_OBJECT_REQUEST_AUDITED_NOT_SUPPLIED"}
    assert {row["evidence_requested"] for row in rows} == {"true"}
    assert {row["request_audited"] for row in rows} == {"true"}
    assert {row["request_audit_passed"] for row in rows} == {"false"}
    assert {row["evidence_supplied"] for row in rows} == {"false"}
    assert {row["evidence_audited"] for row in rows} == {"false"}
    assert {row["evidence_accepted"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["can_execute"] for row in rows} == {"false"}
    assert {row["execution_attempted"] for row in rows} == {"false"}
    assert {row["execution_succeeded"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_evidence_file"] for row in rows)
    assert all(row["required_evidence_content"] for row in rows)
    assert all(row["required_schema_or_units"] for row in rows)
    assert all(row["required_acceptance_check"] for row in rows)
    assert all(row["required_firewall_check"] for row in rows)
    assert all(row["required_replay_check"] for row in rows)
    assert all(row["required_hash_check"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_REQUEST_AUDIT_V01",
            "evidence_object_request_audit_rows_declared": "7",
            "evidence_requested_rows": "7",
            "request_audited_rows": "7",
            "request_audit_passed_rows": "0",
            "evidence_supplied_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_REQUEST_AUDITED_NOT_SUPPLIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_request_audit_v01_audit_only_evidence_object_request_audited_not_supplied_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission evidence object request audit" in note
    assert "evidence payload scoring input payload submission evidence object request audit" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_is_not_received() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["receipt_gate_status"] for row in rows} == {"EVIDENCE_OBJECT_RECEIPT_GATE_OPEN_NOT_RECEIVED"}
    assert {row["receipt_gate_open"] for row in rows} == {"true"}
    assert {row["evidence_received"] for row in rows} == {"false"}
    assert {row["receipt_validated"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["evidence_audited"] for row in rows} == {"false"}
    assert {row["evidence_accepted"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["can_execute"] for row in rows} == {"false"}
    assert {row["execution_attempted"] for row in rows} == {"false"}
    assert {row["execution_succeeded"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_evidence_file"] for row in rows)
    assert all(row["receipt_requirement"] for row in rows)
    assert all(row["receipt_validation_rule"] for row in rows)
    assert all(row["receipt_acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_GATE_V01",
            "evidence_object_receipt_gate_rows_declared": "7",
            "receipt_gate_open_rows": "7",
            "evidence_received_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_GATE_OPEN_NOT_RECEIVED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_v01_receipt_gate_only_evidence_not_received_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission evidence object receipt gate" in note
    assert "evidence payload scoring input payload submission evidence object receipt gate" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_is_not_received() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["receipt_gate_audit_status"] for row in rows} == {"EVIDENCE_OBJECT_RECEIPT_GATE_AUDITED_NOT_RECEIVED"}
    assert {row["receipt_gate_open"] for row in rows} == {"true"}
    assert {row["receipt_gate_audited"] for row in rows} == {"true"}
    assert {row["receipt_gate_audit_passed"] for row in rows} == {"false"}
    assert {row["evidence_received"] for row in rows} == {"false"}
    assert {row["receipt_validated"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["evidence_audited"] for row in rows} == {"false"}
    assert {row["evidence_accepted"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["can_execute"] for row in rows} == {"false"}
    assert {row["execution_attempted"] for row in rows} == {"false"}
    assert {row["execution_succeeded"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_evidence_file"] for row in rows)
    assert all(row["receipt_requirement"] for row in rows)
    assert all(row["receipt_validation_rule"] for row in rows)
    assert all(row["receipt_acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_GATE_AUDIT_V01",
            "evidence_object_receipt_gate_audit_rows_declared": "7",
            "receipt_gate_open_rows": "7",
            "receipt_gate_audited_rows": "7",
            "receipt_gate_audit_passed_rows": "0",
            "evidence_received_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_GATE_AUDITED_NOT_RECEIVED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_gate_audit_v01_audit_only_receipt_gate_audited_evidence_not_received_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission evidence object receipt gate audit" in note
    assert "evidence payload scoring input payload submission evidence object receipt gate audit" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_is_not_received() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["receipt_candidate_status"] for row in rows} == {
        "EVIDENCE_OBJECT_RECEIPT_CANDIDATE_DECLARED_NOT_RECEIVED"
    }
    assert {row["receipt_candidate_declared"] for row in rows} == {"true"}
    assert {row["receipt_gate_open"] for row in rows} == {"true"}
    assert {row["receipt_gate_audited"] for row in rows} == {"true"}
    assert {row["receipt_gate_audit_passed"] for row in rows} == {"false"}
    assert {row["evidence_received"] for row in rows} == {"false"}
    assert {row["receipt_validated"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["evidence_audited"] for row in rows} == {"false"}
    assert {row["evidence_accepted"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["can_execute"] for row in rows} == {"false"}
    assert {row["execution_attempted"] for row in rows} == {"false"}
    assert {row["execution_succeeded"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["expected_evidence_file"] for row in rows)
    assert all(row["expected_receipt_object"] for row in rows)
    assert all(row["receipt_candidate_rule"] for row in rows)
    assert all(row["receipt_validation_rule"] for row in rows)
    assert all(row["receipt_acceptance_rule"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_CANDIDATE_V01",
            "evidence_object_receipt_candidate_rows_declared": "7",
            "receipt_candidate_declared_rows": "7",
            "receipt_gate_open_rows": "7",
            "receipt_gate_audited_rows": "7",
            "receipt_gate_audit_passed_rows": "0",
            "evidence_received_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_CANDIDATE_DECLARED_NOT_RECEIVED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_v01_receipt_candidate_only_evidence_not_received_no_receipt_validated_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission evidence object receipt candidate" in note
    assert "evidence payload scoring input payload submission evidence object receipt candidate" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_is_not_received() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["receipt_candidate_audit_status"] for row in rows} == {
        "EVIDENCE_OBJECT_RECEIPT_CANDIDATE_AUDITED_NOT_RECEIVED"
    }
    assert {row["receipt_candidate_declared"] for row in rows} == {"true"}
    assert {row["receipt_candidate_audited"] for row in rows} == {"true"}
    assert {row["receipt_candidate_audit_passed"] for row in rows} == {"false"}
    assert {row["receipt_gate_open"] for row in rows} == {"true"}
    assert {row["receipt_gate_audited"] for row in rows} == {"true"}
    assert {row["receipt_gate_audit_passed"] for row in rows} == {"false"}
    assert {row["evidence_received"] for row in rows} == {"false"}
    assert {row["receipt_validated"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["evidence_audited"] for row in rows} == {"false"}
    assert {row["evidence_accepted"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["can_execute"] for row in rows} == {"false"}
    assert {row["execution_attempted"] for row in rows} == {"false"}
    assert {row["execution_succeeded"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["expected_evidence_file"] for row in rows)
    assert all(row["expected_receipt_object"] for row in rows)
    assert all(row["candidate_audit_rule"] for row in rows)
    assert all(
        row["audit_failure_reason"] == "receipt candidate is declared, but no evidence object or receipt object is received"
        for row in rows
    )
    assert all(row["audit_decision"] == "failed_until_evidence_object_and_receipt_are_supplied" for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_CANDIDATE_AUDIT_V01",
            "evidence_object_receipt_candidate_audit_rows_declared": "7",
            "receipt_candidate_declared_rows": "7",
            "receipt_candidate_audited_rows": "7",
            "receipt_candidate_audit_passed_rows": "0",
            "receipt_gate_open_rows": "7",
            "receipt_gate_audited_rows": "7",
            "receipt_gate_audit_passed_rows": "0",
            "evidence_received_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_CANDIDATE_AUDITED_NOT_RECEIVED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_audit_v01_audit_only_receipt_candidate_audited_evidence_not_received_no_receipt_validated_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission evidence object receipt candidate audit" in note
    assert "evidence payload scoring input payload submission evidence object receipt candidate audit" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_is_not_completed() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["remediation_status"] for row in rows} == {
        "RECEIPT_CANDIDATE_REMEDIATION_DECLARED_NOT_COMPLETED"
    }
    assert {row["receipt_candidate_declared"] for row in rows} == {"true"}
    assert {row["receipt_candidate_audited"] for row in rows} == {"true"}
    assert {row["receipt_candidate_audit_passed"] for row in rows} == {"false"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["evidence_received"] for row in rows} == {"false"}
    assert {row["receipt_validated"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["evidence_audited"] for row in rows} == {"false"}
    assert {row["evidence_accepted"] for row in rows} == {"false"}
    assert {row["payload_accepted"] for row in rows} == {"false"}
    assert {row["scoring_input_accepted"] for row in rows} == {"false"}
    assert {row["can_execute"] for row in rows} == {"false"}
    assert {row["execution_attempted"] for row in rows} == {"false"}
    assert {row["execution_succeeded"] for row in rows} == {"false"}
    assert {row["evidence_package_passed"] for row in rows} == {"false"}
    assert {row["certificate_passed"] for row in rows} == {"false"}
    assert {row["phi_tau_eff_derived"] for row in rows} == {"false"}
    assert {row["scores_computed"] for row in rows} == {"false"}
    assert {row["cmb_likelihood_available"] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["missing_evidence_object"] for row in rows)
    assert all(row["missing_receipt_object"] for row in rows)
    assert all(row["required_remediation_action"] for row in rows)
    assert all(row["required_receipt_binding"] for row in rows)
    assert all(row["required_evidence_bundle"] for row in rows)
    assert all(
        row["acceptance_exit_gate"]
        == "may exit only after evidence object and receipt are supplied, validated, and audit-passed without endpoint leakage"
        for row in rows
    )
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_CANDIDATE_REMEDIATION_PLAN_V01",
            "evidence_object_receipt_candidate_remediation_rows_declared": "7",
            "receipt_candidate_declared_rows": "7",
            "receipt_candidate_audited_rows": "7",
            "receipt_candidate_audit_passed_rows": "0",
            "remediation_completed_rows": "0",
            "evidence_received_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_CANDIDATE_REMEDIATION_DECLARED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_candidate_remediation_plan_v01_plan_only_receipt_candidate_remediation_not_completed_no_evidence_received_no_receipt_validated_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission evidence object receipt candidate remediation plan" in note
    assert "evidence payload scoring input payload submission evidence object receipt candidate remediation plan" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_is_not_materialized() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["materialization_status"] for row in rows} == {
        "EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_PACKET_DECLARED_NO_EVIDENCE_MATERIALIZED"
    }
    assert {row["packet_declared"] for row in rows} == {"true"}
    for field in [
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
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert all(row["required_evidence_file"] for row in rows)
    assert all(row["required_receipt_file"] for row in rows)
    assert all(row["allows_tau_response_claim"] == "false" for row in rows)
    assert all(row["allows_dark_sector_verdict"] == "false" for row in rows)
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_PACKET_V01",
            "evidence_object_receipt_materialization_packet_rows_declared": "7",
            "packet_declared_rows": "7",
            "evidence_materialized_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_PACKET_DECLARED_NO_EVIDENCE_MATERIALIZED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_packet_v01_packet_schema_only_no_evidence_materialized_no_receipt_validated_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission evidence object receipt materialization packet" in note
    assert "evidence payload scoring input payload submission evidence object receipt materialization packet" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_fails_without_evidence() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["materialization_audit_status"] for row in rows} == {
        "EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_AUDIT_FAILED_NO_EVIDENCE_MATERIALIZED"
    }
    assert {row["packet_declared"] for row in rows} == {"true"}
    for field in [
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
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert all(
        row["audit_failure_reason"] == "no materialized evidence object or receipt object is available for audit"
        for row in rows
    )
    assert all(row["audit_decision"] == "failed_until_evidence_object_and_receipt_are_materialized" for row in rows)
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_AUDIT_V01",
            "evidence_object_receipt_materialization_audit_rows_declared": "7",
            "packet_declared_rows": "7",
            "evidence_materialized_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_MATERIALIZATION_AUDIT_FAILED_NO_EVIDENCE_MATERIALIZED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_materialization_audit_v01_audit_only_no_evidence_materialized_no_receipt_validated_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission evidence object receipt materialization audit" in note
    assert "evidence payload scoring input payload submission evidence object receipt materialization audit" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_blocks_acceptance() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["acceptance_precheck_status"] for row in rows} == {
        "EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_SATISFIED"
    }
    assert {row["packet_declared"] for row in rows} == {"true"}
    for field in [
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
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert all(
        row["acceptance_blocker"] == "materialization audit failed because no evidence object is materialized"
        for row in rows
    )
    assert all(
        row["precheck_decision"] == "blocked_until_materialization_receipt_provenance_replay_and_firewall_gates_pass"
        for row in rows
    )
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_PRECHECK_V01",
            "evidence_object_receipt_acceptance_precheck_rows_declared": "7",
            "packet_declared_rows": "7",
            "evidence_materialized_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "acceptance_precheck_passed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_satisfied": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_SATISFIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_precheck_v01_precheck_only_no_evidence_materialized_no_receipt_validated_no_receipt_accepted_no_acceptance_pass_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission evidence object receipt acceptance precheck" in note
    assert "acceptance precheck is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_is_not_completed() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["unblock_status"] for row in rows} == {
        "EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_UNBLOCK_DECLARED_NOT_COMPLETED"
    }
    assert {row["packet_declared"] for row in rows} == {"true"}
    for field in [
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
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert all(row["required_unblock_action"] for row in rows)
    assert all(row["required_exit_condition"] for row in rows)
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_V01",
            "evidence_object_receipt_acceptance_unblock_plan_rows_declared": "7",
            "packet_declared_rows": "7",
            "unblock_completed_rows": "0",
            "evidence_materialized_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "provenance_bound_rows": "0",
            "replay_bound_rows": "0",
            "firewall_passed_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "acceptance_precheck_passed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_v01_unblock_plan_only_no_unblock_completed_no_evidence_materialized_no_receipt_validated_no_receipt_accepted_no_acceptance_pass_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission evidence object receipt acceptance unblock plan" in note
    assert "acceptance unblock plan is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_is_not_passed() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["unblock_plan_audit_status"] for row in rows} == {
        "EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_AUDITED_NOT_COMPLETED"
    }
    assert {row["unblock_plan_audited"] for row in rows} == {"true"}
    assert {row["packet_declared"] for row in rows} == {"true"}
    for field in [
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
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert all(row["unblock_plan_audit_rule"] for row in rows)
    assert all(row["unblock_plan_audit_finding"] for row in rows)
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_AUDIT_V01",
            "evidence_object_receipt_acceptance_unblock_plan_audit_rows_declared": "7",
            "unblock_plan_audited_rows": "7",
            "unblock_plan_audit_passed_rows": "0",
            "packet_declared_rows": "7",
            "unblock_completed_rows": "0",
            "evidence_materialized_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "provenance_bound_rows": "0",
            "replay_bound_rows": "0",
            "firewall_passed_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "acceptance_precheck_passed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_AUDITED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_unblock_plan_audit_v01_audit_only_unblock_plan_audited_not_completed_no_evidence_materialized_no_receipt_validated_no_receipt_accepted_no_acceptance_pass_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload submission evidence object receipt acceptance unblock plan audit" in note
    assert "acceptance unblock plan audit is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_is_closed() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["decision_gate_status"] for row in rows} == {
        "ACCEPTANCE_DECISION_CLOSED_UNBLOCK_AUDIT_NOT_PASSED"
    }
    assert {row["decision_output"] for row in rows} == {"acceptance_closed"}
    assert {row["packet_declared"] for row in rows} == {"true"}
    assert {row["unblock_plan_audited"] for row in rows} == {"true"}
    for field in [
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
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert all(row["target_gate"] for row in rows)
    assert all(row["required_prior_pass"] for row in rows)
    assert all(
        row["decision_rule"]
        == "acceptance may open only if receipt unblock plan audit passes and all upstream evidence gates are completed"
        for row in rows
    )
    assert all(row["decision_reason"] == "receipt acceptance unblock plan audit is not satisfied" for row in rows)
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_DECISION_GATE_V01",
            "evidence_object_receipt_acceptance_decision_gate_rows_declared": "7",
            "packet_declared_rows": "7",
            "unblock_plan_audited_rows": "7",
            "unblock_plan_audit_passed_rows": "0",
            "acceptance_allowed_rows": "0",
            "unblock_completed_rows": "0",
            "evidence_materialized_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "provenance_bound_rows": "0",
            "replay_bound_rows": "0",
            "firewall_passed_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "acceptance_precheck_passed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_DECISION_GATE_CLOSED_UNBLOCK_AUDIT_NOT_PASSED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_v01_decision_gate_only_no_acceptance_allowed_no_evidence_materialized_no_receipt_validated_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "acceptance remains closed" in note
    assert "acceptance decision gate is not satisfied" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_passes_closed_gate_only() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["decision_gate_audit_status"] for row in rows} == {
        "ACCEPTANCE_DECISION_GATE_AUDITED_ACCEPTANCE_CLOSED"
    }
    assert {row["decision_output"] for row in rows} == {"acceptance_closed"}
    assert {row["packet_declared"] for row in rows} == {"true"}
    assert {row["decision_gate_audited"] for row in rows} == {"true"}
    assert {row["decision_gate_audit_passed"] for row in rows} == {"true"}
    assert {row["unblock_plan_audited"] for row in rows} == {"true"}
    for field in [
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
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert all(row["decision_gate_audit_rule"] for row in rows)
    assert all(row["decision_gate_audit_finding"] for row in rows)
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_DECISION_GATE_AUDIT_V01",
            "evidence_object_receipt_acceptance_decision_gate_audit_rows_declared": "7",
            "packet_declared_rows": "7",
            "decision_gate_audited_rows": "7",
            "decision_gate_audit_passed_rows": "7",
            "unblock_plan_audited_rows": "7",
            "unblock_plan_audit_passed_rows": "0",
            "acceptance_allowed_rows": "0",
            "unblock_completed_rows": "0",
            "evidence_materialized_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "provenance_bound_rows": "0",
            "replay_bound_rows": "0",
            "firewall_passed_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "acceptance_precheck_passed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_DECISION_GATE_AUDITED_ACCEPTANCE_CLOSED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_decision_gate_audit_v01_audit_only_decision_gate_audited_acceptance_closed_no_evidence_materialized_no_receipt_validated_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "decision gate audit is satisfied as an audit of a closed gate" in note
    assert "permits no no-dark or dark-sector verdict" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_records_closed_gate_only() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["acceptance_record_status"] for row in rows} == {"ACCEPTANCE_RECORD_WRITTEN_ACCEPTANCE_CLOSED"}
    assert {row["record_output"] for row in rows} == {"acceptance_closed_recorded"}
    for field in ["packet_declared", "decision_gate_audited", "decision_gate_audit_passed", "acceptance_recorded"]:
        assert {row[field] for row in rows} == {"true"}
    for field in [
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
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert all(row["record_rule"] for row in rows)
    assert all(row["record_finding"] for row in rows)
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_RECORD_V01",
            "evidence_object_receipt_acceptance_record_rows_declared": "7",
            "packet_declared_rows": "7",
            "decision_gate_audited_rows": "7",
            "decision_gate_audit_passed_rows": "7",
            "acceptance_recorded_rows": "7",
            "acceptance_allowed_rows": "0",
            "unblock_plan_audit_passed_rows": "0",
            "unblock_completed_rows": "0",
            "evidence_materialized_rows": "0",
            "receipt_validated_rows": "0",
            "receipt_accepted_rows": "0",
            "provenance_bound_rows": "0",
            "replay_bound_rows": "0",
            "firewall_passed_rows": "0",
            "evidence_audited_rows": "0",
            "evidence_accepted_rows": "0",
            "acceptance_precheck_passed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_ACCEPTANCE_RECORD_WRITTEN_ACCEPTANCE_CLOSED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_acceptance_record_v01_record_only_acceptance_closed_no_evidence_materialized_no_receipt_validated_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "acceptance record is satisfied as a record of a closed gate" in note
    assert "accepts no evidence object or receipt" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_is_closed() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["scoring_handoff_precheck_status"] for row in rows} == {
        "SCORING_HANDOFF_PRECHECK_CLOSED_ACCEPTANCE_NOT_ALLOWED"
    }
    assert {row["handoff_output"] for row in rows} == {"handoff_closed"}
    assert {row["acceptance_recorded"] for row in rows} == {"true"}
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
        assert {row[field] for row in rows} == {"false"}
    assert all(row["handoff_rule"] for row in rows)
    assert all(row["handoff_blocker"] for row in rows)
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_PRECHECK_V01",
            "evidence_object_receipt_scoring_handoff_precheck_rows_declared": "7",
            "acceptance_recorded_rows": "7",
            "acceptance_allowed_rows": "0",
            "evidence_accepted_rows": "0",
            "receipt_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "can_handoff_to_scoring_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_PRECHECK_CLOSED_ACCEPTANCE_NOT_ALLOWED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_precheck_v01_precheck_only_handoff_closed_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "handoff precheck" in note
    assert "no evidence object, receipt, payload, or scoring input is" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_is_not_completed() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["scoring_handoff_unblock_status"] for row in rows} == {
        "SCORING_HANDOFF_UNBLOCK_DECLARED_NOT_COMPLETED"
    }
    assert {row["acceptance_recorded"] for row in rows} == {"true"}
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
        assert {row[field] for row in rows} == {"false"}
    assert all(row["required_unblock_action"] for row in rows)
    assert all(row["required_exit_condition"] for row in rows)
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_PLAN_V01",
            "evidence_object_receipt_scoring_handoff_unblock_plan_rows_declared": "7",
            "acceptance_recorded_rows": "7",
            "acceptance_allowed_rows": "0",
            "evidence_accepted_rows": "0",
            "receipt_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_handoff_to_scoring_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_v01_unblock_plan_only_no_handoff_unblocked_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "unblock plan" in note
    assert "unblocks no handoff" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_passes_but_handoff_remains_blocked() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["scoring_handoff_unblock_plan_audit_status"] for row in rows} == {
        "SCORING_HANDOFF_UNBLOCK_PLAN_AUDIT_PASSED_HANDOFF_STILL_BLOCKED"
    }
    assert {row["audit_passed"] for row in rows} == {"true"}
    assert {row["acceptance_recorded"] for row in rows} == {"true"}
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
        assert {row[field] for row in rows} == {"false"}
    assert all(row["audited_condition"] for row in rows)
    assert {row["audit_result"] for row in rows} == {"plan_condition_declared_and_handoff_remains_blocked"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_PLAN_AUDIT_V01",
            "evidence_object_receipt_scoring_handoff_unblock_plan_audit_rows_declared": "7",
            "audit_passed_rows": "7",
            "acceptance_recorded_rows": "7",
            "acceptance_allowed_rows": "0",
            "evidence_accepted_rows": "0",
            "receipt_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_handoff_to_scoring_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_PLAN_AUDIT_PASSED_HANDOFF_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_plan_audit_v01_audit_only_plan_consistent_handoff_still_blocked_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "unblock plan audit" in note
    assert "scoring handoff remains blocked" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_is_closed() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["scoring_handoff_decision_gate_status"] for row in rows} == {
        "SCORING_HANDOFF_DECISION_GATE_CLOSED_ACCEPTANCE_NOT_SATISFIED"
    }
    assert {row["decision_result"] for row in rows} == {"handoff_closed"}
    assert {row["audit_passed"] for row in rows} == {"true"}
    assert {row["acceptance_recorded"] for row in rows} == {"true"}
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
        assert {row[field] for row in rows} == {"false"}
    assert all(row["decision_rule"] for row in rows)
    assert all(row["decision_reason"] for row in rows)
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_DECISION_GATE_V01",
            "evidence_object_receipt_scoring_handoff_decision_gate_rows_declared": "7",
            "audit_passed_rows": "7",
            "closed_decision_rows": "7",
            "open_decision_rows": "0",
            "acceptance_recorded_rows": "7",
            "acceptance_allowed_rows": "0",
            "evidence_accepted_rows": "0",
            "receipt_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_handoff_to_scoring_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_DECISION_GATE_CLOSED_ACCEPTANCE_NOT_SATISFIED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_v01_decision_gate_only_handoff_closed_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "decision gate" in note
    assert "decision_result=handoff_closed" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_passes_closed_decision() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["scoring_handoff_decision_gate_audit_status"] for row in rows} == {
        "SCORING_HANDOFF_DECISION_GATE_AUDIT_PASSED_CLOSED_DECISION_CONSISTENT"
    }
    assert {row["audit_passed"] for row in rows} == {"true"}
    assert {row["audited_decision"] for row in rows} == {"handoff_closed"}
    assert {row["decision_result"] for row in rows} == {"handoff_closed"}
    assert {row["acceptance_recorded"] for row in rows} == {"true"}
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
        assert {row[field] for row in rows} == {"false"}
    assert {row["audit_result"] for row in rows} == {
        "closed_decision_consistent_with_missing_acceptance_conditions"
    }
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_DECISION_GATE_AUDIT_V01",
            "evidence_object_receipt_scoring_handoff_decision_gate_audit_rows_declared": "7",
            "audit_passed_rows": "7",
            "closed_decision_rows": "7",
            "open_decision_rows": "0",
            "acceptance_recorded_rows": "7",
            "acceptance_allowed_rows": "0",
            "evidence_accepted_rows": "0",
            "receipt_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_handoff_to_scoring_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_DECISION_GATE_AUDIT_PASSED_CLOSED_DECISION_CONSISTENT",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_decision_gate_audit_v01_audit_only_closed_decision_consistent_no_handoff_opened_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "decision gate audit" in note
    assert "decision_result=handoff_closed" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_passes_closed_handoff_only() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["scoring_handoff_acceptance_record_status"] for row in rows} == {
        "SCORING_HANDOFF_ACCEPTANCE_RECORD_PASSED_CLOSED_HANDOFF_RECORDED"
    }
    assert {row["record_passed"] for row in rows} == {"true"}
    assert {row["decision_audit_passed"] for row in rows} == {"true"}
    assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
    assert {row["record_result"] for row in rows} == {"closed_handoff_recorded"}
    assert {row["acceptance_recorded"] for row in rows} == {"true"}
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
        assert {row[field] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_ACCEPTANCE_RECORD_V01",
            "evidence_object_receipt_scoring_handoff_acceptance_record_rows_declared": "7",
            "record_passed_rows": "7",
            "decision_audit_passed_rows": "7",
            "closed_handoff_record_rows": "7",
            "open_handoff_record_rows": "0",
            "acceptance_recorded_rows": "7",
            "acceptance_allowed_rows": "0",
            "evidence_accepted_rows": "0",
            "receipt_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_handoff_to_scoring_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_ACCEPTANCE_RECORD_PASSED_CLOSED_HANDOFF_RECORDED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_v01_record_only_closed_handoff_recorded_no_handoff_opened_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "acceptance record" in note
    assert "recorded_decision=handoff_closed" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_passes_closed_record_only() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["scoring_handoff_acceptance_record_audit_status"] for row in rows} == {
        "SCORING_HANDOFF_ACCEPTANCE_RECORD_AUDIT_PASSED_CLOSED_HANDOFF_RECORD_CONSISTENT"
    }
    assert {row["audit_passed"] for row in rows} == {"true"}
    assert {row["record_passed"] for row in rows} == {"true"}
    assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
    assert {row["audited_record"] for row in rows} == {"closed_handoff_recorded"}
    assert {row["audit_result"] for row in rows} == {
        "closed_handoff_record_consistent_with_missing_acceptance_conditions"
    }
    assert {row["acceptance_recorded"] for row in rows} == {"true"}
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
        assert {row[field] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_ACCEPTANCE_RECORD_AUDIT_V01",
            "evidence_object_receipt_scoring_handoff_acceptance_record_audit_rows_declared": "7",
            "audit_passed_rows": "7",
            "record_passed_rows": "7",
            "closed_handoff_record_rows": "7",
            "open_handoff_record_rows": "0",
            "acceptance_recorded_rows": "7",
            "acceptance_allowed_rows": "0",
            "evidence_accepted_rows": "0",
            "receipt_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_handoff_to_scoring_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_ACCEPTANCE_RECORD_AUDIT_PASSED_CLOSED_HANDOFF_RECORD_CONSISTENT",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_acceptance_record_audit_v01_audit_only_closed_handoff_record_consistent_no_handoff_opened_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "acceptance record audit" in note
    assert "recorded_decision=handoff_closed" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_blocks_scoring() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["final_pre_score_lock_status"] for row in rows} == {
        "FINAL_PRE_SCORE_LOCK_PASSED_SCORING_STILL_BLOCKED"
    }
    assert {row["lock_result"] for row in rows} == {"pre_score_locked"}
    assert {row["lock_passed"] for row in rows} == {"true"}
    assert {row["acceptance_record_audit_passed"] for row in rows} == {"true"}
    assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
    assert {row["acceptance_recorded"] for row in rows} == {"true"}
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
        assert {row[field] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_FINAL_PRE_SCORE_LOCK_V01",
            "evidence_object_receipt_scoring_handoff_final_pre_score_lock_rows_declared": "7",
            "lock_passed_rows": "7",
            "acceptance_record_audit_passed_rows": "7",
            "closed_handoff_rows": "7",
            "open_handoff_rows": "0",
            "acceptance_recorded_rows": "7",
            "acceptance_allowed_rows": "0",
            "evidence_accepted_rows": "0",
            "receipt_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_handoff_to_scoring_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_FINAL_PRE_SCORE_LOCK_PASSED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_v01_lock_only_pre_score_closed_no_handoff_opened_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "final pre-score lock" in note
    assert "lock_result=pre_score_locked" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_blocks_scoring() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["final_pre_score_lock_audit_status"] for row in rows} == {
        "FINAL_PRE_SCORE_LOCK_AUDIT_PASSED_SCORING_STILL_BLOCKED"
    }
    assert {row["audited_lock"] for row in rows} == {"pre_score_locked"}
    assert {row["audit_result"] for row in rows} == {
        "pre_score_lock_consistent_with_missing_acceptance_conditions"
    }
    assert {row["audit_passed"] for row in rows} == {"true"}
    assert {row["lock_passed"] for row in rows} == {"true"}
    assert {row["lock_result"] for row in rows} == {"pre_score_locked"}
    assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
    assert {row["acceptance_recorded"] for row in rows} == {"true"}
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
        assert {row[field] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_FINAL_PRE_SCORE_LOCK_AUDIT_V01",
            "evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_rows_declared": "7",
            "audit_passed_rows": "7",
            "lock_passed_rows": "7",
            "pre_score_locked_rows": "7",
            "scoring_unlocked_rows": "0",
            "closed_handoff_rows": "7",
            "open_handoff_rows": "0",
            "acceptance_recorded_rows": "7",
            "acceptance_allowed_rows": "0",
            "evidence_accepted_rows": "0",
            "receipt_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_handoff_to_scoring_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_FINAL_PRE_SCORE_LOCK_AUDIT_PASSED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_final_pre_score_lock_audit_v01_audit_only_pre_score_lock_consistent_no_handoff_opened_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "final pre-score lock audit" in note
    assert "audit_result=pre_score_lock_consistent_with_missing_acceptance_conditions" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_blocks_scoring() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["score_attempt_blocker_certificate_status"] for row in rows} == {
        "SCORE_ATTEMPT_BLOCKER_CERTIFICATE_PASSED_SCORING_STILL_BLOCKED"
    }
    assert {row["certified_blocker"] for row in rows} == {
        "score_attempt_blocked_by_missing_acceptance_conditions"
    }
    assert {row["certificate_passed"] for row in rows} == {"true"}
    assert {row["final_pre_score_lock_audit_passed"] for row in rows} == {"true"}
    assert {row["lock_result"] for row in rows} == {"pre_score_locked"}
    assert {row["score_attempt_allowed"] for row in rows} == {"false"}
    assert {row["score_attempt_blocked"] for row in rows} == {"true"}
    assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
    assert {row["acceptance_recorded"] for row in rows} == {"true"}
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
        assert {row[field] for row in rows} == {"false"}
    assert sum(row["hard_failure_triggered"] == "true" for row in rows) == 0
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_SCORE_ATTEMPT_BLOCKER_CERTIFICATE_V01",
            "evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_rows_declared": "7",
            "certificate_passed_rows": "7",
            "final_pre_score_lock_audit_passed_rows": "7",
            "pre_score_locked_rows": "7",
            "score_attempt_allowed_rows": "0",
            "score_attempt_blocked_rows": "7",
            "closed_handoff_rows": "7",
            "open_handoff_rows": "0",
            "acceptance_recorded_rows": "7",
            "acceptance_allowed_rows": "0",
            "evidence_accepted_rows": "0",
            "receipt_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_handoff_to_scoring_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "input_certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "hard_failures_triggered": "0",
            "evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_SCORE_ATTEMPT_BLOCKER_CERTIFICATE_PASSED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_blocker_certificate_v01_certificate_only_score_attempt_blocked_no_handoff_opened_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "score attempt is currently blocked" in note
    assert "score_attempt_allowed=false" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_keep_scoring_blocked() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["score_attempt_unblock_condition_status"] for row in rows} == {
        "SCORE_ATTEMPT_UNBLOCK_CONDITION_DECLARED_NOT_SATISFIED"
    }
    assert {row["condition_required"] for row in rows} == {"true"}
    assert {row["condition_satisfied"] for row in rows} == {"false"}
    assert {row["condition_gap"] for row in rows} == {"missing_accepted_record"}
    assert {row["score_attempt_allowed_if_satisfied"] for row in rows} == {"true"}
    assert {row["score_attempt_allowed_now"] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["blocker_certificate_passed"] for row in rows} == {"true"}
    assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
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
        assert {row[field] for row in rows} == {"false"}
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_SCORE_ATTEMPT_UNBLOCK_CONDITIONS_V01",
            "score_attempt_unblock_condition_rows_declared": "7",
            "condition_required_rows": "7",
            "condition_satisfied_rows": "0",
            "condition_gap_rows": "7",
            "score_attempt_allowed_if_satisfied_rows": "7",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "blocker_certificate_passed_rows": "7",
            "open_handoff_rows": "0",
            "acceptance_allowed_rows": "0",
            "evidence_accepted_rows": "0",
            "receipt_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "input_certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "score_attempt_unblock_conditions_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORE_ATTEMPT_UNBLOCK_CONDITIONS_DECLARED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_score_attempt_unblock_conditions_v01_conditions_only_score_attempt_still_blocked_no_handoff_opened_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "score_attempt_unblock_conditions_satisfied=false" in note
    assert "score_attempt_blocked_now=true" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_keeps_scoring_blocked() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["evidence_request_status"] for row in rows} == {
        "UNBLOCK_CONDITION_EVIDENCE_REQUEST_OPEN_SCORING_STILL_BLOCKED"
    }
    assert {row["request_open"] for row in rows} == {"true"}
    assert {row["evidence_requested"] for row in rows} == {"true"}
    assert {row["evidence_received"] for row in rows} == {"false"}
    assert {row["evidence_accepted"] for row in rows} == {"false"}
    assert {row["condition_satisfied"] for row in rows} == {"false"}
    assert {row["score_attempt_allowed_now"] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
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
        assert {row[field] for row in rows} == {"false"}
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_REQUEST_V01",
            "unblock_condition_evidence_request_rows_declared": "7",
            "request_open_rows": "7",
            "evidence_requested_rows": "7",
            "evidence_received_rows": "0",
            "evidence_accepted_rows": "0",
            "condition_satisfied_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "open_handoff_rows": "0",
            "acceptance_allowed_rows": "0",
            "receipt_accepted_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "input_certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "unblock_condition_evidence_request_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "UNBLOCK_CONDITION_EVIDENCE_REQUEST_OPEN_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_request_v01_request_only_missing_unblock_evidence_requested_no_handoff_opened_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "evidence_requested_rows=7" in note
    assert "evidence_accepted_rows=0" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_keeps_scoring_blocked() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["receipt_candidate_status"] for row in rows} == {
        "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_CANDIDATE_PREPARED_SCORING_STILL_BLOCKED"
    }
    assert {row["request_open"] for row in rows} == {"true"}
    assert {row["evidence_requested"] for row in rows} == {"true"}
    assert {row["receipt_candidate_prepared"] for row in rows} == {"true"}
    assert {row["evidence_received"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["evidence_accepted"] for row in rows} == {"false"}
    assert {row["condition_satisfied"] for row in rows} == {"false"}
    assert {row["score_attempt_allowed_now"] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
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
        assert {row[field] for row in rows} == {"false"}
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_CANDIDATE_V01",
            "unblock_condition_evidence_receipt_candidate_rows_declared": "7",
            "request_open_rows": "7",
            "evidence_requested_rows": "7",
            "receipt_candidate_prepared_rows": "7",
            "evidence_received_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_accepted_rows": "0",
            "condition_satisfied_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "open_handoff_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "input_certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "unblock_condition_evidence_receipt_candidate_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_CANDIDATE_PREPARED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_v01_candidate_only_missing_unblock_evidence_receipt_candidate_prepared_no_handoff_opened_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "receipt_candidate_prepared_rows=7" in note
    assert "receipt_accepted_rows=0" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_keeps_scoring_blocked() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["receipt_candidate_audit_status"] for row in rows} == {
        "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_CANDIDATE_AUDIT_PASSED_SCORING_STILL_BLOCKED"
    }
    assert {row["audit_result"] for row in rows} == {
        "receipt_candidate_consistent_with_no_received_or_accepted_evidence"
    }
    assert {row["audit_passed"] for row in rows} == {"true"}
    assert {row["request_open"] for row in rows} == {"true"}
    assert {row["evidence_requested"] for row in rows} == {"true"}
    assert {row["receipt_candidate_prepared"] for row in rows} == {"true"}
    assert {row["evidence_received"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["evidence_accepted"] for row in rows} == {"false"}
    assert {row["condition_satisfied"] for row in rows} == {"false"}
    assert {row["score_attempt_allowed_now"] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
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
        assert {row[field] for row in rows} == {"false"}
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_CANDIDATE_AUDIT_V01",
            "unblock_condition_evidence_receipt_candidate_audit_rows_declared": "7",
            "audit_passed_rows": "7",
            "request_open_rows": "7",
            "evidence_requested_rows": "7",
            "receipt_candidate_prepared_rows": "7",
            "evidence_received_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_accepted_rows": "0",
            "condition_satisfied_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "open_handoff_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "input_certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "unblock_condition_evidence_receipt_candidate_audit_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_CANDIDATE_AUDIT_PASSED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_candidate_audit_v01_audit_only_receipt_candidates_consistent_no_handoff_opened_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "audit_passed_rows=7" in note
    assert "evidence_accepted_rows=0" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_keeps_scoring_blocked() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["remediation_status"] for row in rows} == {
        "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_REMEDIATION_DECLARED_NOT_COMPLETED"
    }
    assert {row["request_open"] for row in rows} == {"true"}
    assert {row["evidence_requested"] for row in rows} == {"true"}
    assert {row["receipt_candidate_prepared"] for row in rows} == {"true"}
    assert {row["receipt_candidate_audited"] for row in rows} == {"true"}
    assert {row["receipt_candidate_audit_passed"] for row in rows} == {"true"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["evidence_received"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["evidence_accepted"] for row in rows} == {"false"}
    assert {row["condition_satisfied"] for row in rows} == {"false"}
    assert {row["score_attempt_allowed_now"] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
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
        assert {row[field] for row in rows} == {"false"}
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_REMEDIATION_PLAN_V01",
            "unblock_condition_evidence_receipt_remediation_rows_declared": "7",
            "request_open_rows": "7",
            "evidence_requested_rows": "7",
            "receipt_candidate_prepared_rows": "7",
            "receipt_candidate_audited_rows": "7",
            "receipt_candidate_audit_passed_rows": "7",
            "remediation_completed_rows": "0",
            "evidence_received_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_accepted_rows": "0",
            "condition_satisfied_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "open_handoff_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "input_certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "unblock_condition_evidence_receipt_remediation_plan_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_REMEDIATION_DECLARED_NOT_COMPLETED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_remediation_plan_v01_plan_only_remediation_not_completed_no_handoff_opened_no_evidence_received_no_evidence_accepted_no_receipt_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "remediation_completed_rows=0" in note
    assert "score_attempt_blocked_now=true" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_keeps_scoring_blocked() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["materialization_status"] for row in rows} == {
        "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_PACKET_DECLARED_NO_EVIDENCE_MATERIALIZED"
    }
    for field in [
        "request_open",
        "evidence_requested",
        "receipt_candidate_prepared",
        "receipt_candidate_audited",
        "receipt_candidate_audit_passed",
        "remediation_declared",
        "packet_declared",
    ]:
        assert {row[field] for row in rows} == {"true"}
    assert {row["remediation_completed"] for row in rows} == {"false"}
    assert {row["evidence_materialized"] for row in rows} == {"false"}
    assert {row["evidence_received"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["evidence_accepted"] for row in rows} == {"false"}
    assert {row["condition_satisfied"] for row in rows} == {"false"}
    assert {row["score_attempt_allowed_now"] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
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
        assert {row[field] for row in rows} == {"false"}
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_PACKET_V01",
            "unblock_condition_evidence_receipt_materialization_packet_rows_declared": "7",
            "request_open_rows": "7",
            "evidence_requested_rows": "7",
            "receipt_candidate_prepared_rows": "7",
            "receipt_candidate_audited_rows": "7",
            "receipt_candidate_audit_passed_rows": "7",
            "remediation_declared_rows": "7",
            "remediation_completed_rows": "0",
            "packet_declared_rows": "7",
            "evidence_materialized_rows": "0",
            "evidence_received_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_accepted_rows": "0",
            "condition_satisfied_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "open_handoff_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "input_certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "unblock_condition_evidence_receipt_materialization_packet_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_PACKET_DECLARED_NO_EVIDENCE_MATERIALIZED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_packet_v01_packet_schema_only_no_evidence_materialized_no_handoff_opened_no_receipt_accepted_no_evidence_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "packet_declared_rows=7" in note
    assert "evidence_materialized_rows=0" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_keeps_scoring_blocked() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["materialization_audit_status"] for row in rows} == {
        "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_AUDIT_FAILED_NO_EVIDENCE_MATERIALIZED"
    }
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
        assert {row[field] for row in rows} == {"true"}
    assert {row["materialization_audit_passed"] for row in rows} == {"false"}
    assert {row["evidence_materialized"] for row in rows} == {"false"}
    assert {row["evidence_received"] for row in rows} == {"false"}
    assert {row["receipt_accepted"] for row in rows} == {"false"}
    assert {row["evidence_accepted"] for row in rows} == {"false"}
    assert {row["condition_satisfied"] for row in rows} == {"false"}
    assert {row["score_attempt_allowed_now"] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
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
        assert {row[field] for row in rows} == {"false"}
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_AUDIT_V01",
            "unblock_condition_evidence_receipt_materialization_audit_rows_declared": "7",
            "request_open_rows": "7",
            "evidence_requested_rows": "7",
            "receipt_candidate_prepared_rows": "7",
            "receipt_candidate_audited_rows": "7",
            "receipt_candidate_audit_passed_rows": "7",
            "remediation_declared_rows": "7",
            "packet_declared_rows": "7",
            "packet_audited_rows": "7",
            "materialization_audit_passed_rows": "0",
            "evidence_materialized_rows": "0",
            "evidence_received_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_accepted_rows": "0",
            "condition_satisfied_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "open_handoff_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "input_certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "unblock_condition_evidence_receipt_materialization_audit_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_MATERIALIZATION_AUDIT_FAILED_NO_EVIDENCE_MATERIALIZED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_materialization_audit_v01_audit_only_no_evidence_materialized_no_handoff_opened_no_receipt_accepted_no_evidence_accepted_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "packet_audited_rows=7" in note
    assert "materialization_audit_passed_rows=0" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_keeps_scoring_blocked() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["acceptance_precheck_status"] for row in rows} == {
        "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_PASSED"
    }
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
        assert {row[field] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_INPUT_EVIDENCE_PAYLOAD_SCORING_INPUT_PAYLOAD_SUBMISSION_EVIDENCE_OBJECT_RECEIPT_SCORING_HANDOFF_UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_PRECHECK_V01",
            "unblock_condition_evidence_receipt_acceptance_precheck_rows_declared": "7",
            "materialization_audit_passed_rows": "0",
            "evidence_materialized_rows": "0",
            "evidence_received_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_accepted_rows": "0",
            "acceptance_precheck_passed_rows": "0",
            "condition_satisfied_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "open_handoff_rows": "0",
            "acceptance_allowed_rows": "0",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "handoff_unblocked_rows": "0",
            "can_execute_rows": "0",
            "execution_attempted_rows": "0",
            "execution_succeeded_rows": "0",
            "evidence_package_passed_rows": "0",
            "input_certificate_passed_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "unblock_condition_evidence_receipt_acceptance_precheck_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_PRECHECK_FAILED_MATERIALIZATION_AUDIT_NOT_PASSED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_v01",
            "claim_boundary": "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_precheck_v01_precheck_only_no_materialization_audit_pass_no_evidence_accepted_no_receipt_accepted_no_handoff_opened_no_execution_allowed_no_scoring_input_accepted_no_payload_accepted_no_package_pass_no_certificate_pass_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "acceptance_precheck_passed_rows=0" in note
    assert "score_attempt_blocked_now_rows=7" in note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_and_audit_keep_scoring_blocked() -> None:
    plan_rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_v01.csv"
            ).open()
        )
    )
    plan_summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_summary_v01.csv"
            ).open()
        )
    )
    audit_rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_v01.csv"
            ).open()
        )
    )
    audit_summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_summary_v01.csv"
            ).open()
        )
    )
    plan_note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_v01.md"
    ).read_text()
    audit_note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_v01.md"
    ).read_text()

    assert len(plan_rows) == 7
    assert len(audit_rows) == 7
    assert {row["unblock_plan_status"] for row in plan_rows} == {
        "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED"
    }
    assert {row["unblock_plan_audit_status"] for row in audit_rows} == {
        "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_AUDITED_NOT_COMPLETED"
    }
    for rows in [plan_rows, audit_rows]:
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
            assert {row[field] for row in rows} == {"false"}
        assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
        assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
        assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert {row["unblock_plan_audited"] for row in audit_rows} == {"true"}
    assert {row["unblock_plan_audit_passed"] for row in audit_rows} == {"false"}

    assert plan_summary[0]["unblock_condition_evidence_receipt_acceptance_unblock_plan_rows_declared"] == "7"
    assert plan_summary[0]["materialization_audit_required_rows"] == "7"
    assert plan_summary[0]["receipt_acceptance_required_rows"] == "7"
    assert plan_summary[0]["evidence_acceptance_required_rows"] == "7"
    assert plan_summary[0]["handoff_open_required_rows"] == "7"
    assert plan_summary[0]["unblock_completed_rows"] == "0"
    assert plan_summary[0]["score_attempt_blocked_now_rows"] == "7"
    assert plan_summary[0]["overall_status"] == (
        "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_DECLARED_NOT_COMPLETED_SCORING_STILL_BLOCKED"
    )
    assert plan_summary[0]["next_required_artifact"] == (
        "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_v01"
    )

    assert audit_summary[0]["unblock_condition_evidence_receipt_acceptance_unblock_plan_audit_rows_declared"] == "7"
    assert audit_summary[0]["unblock_plan_audited_rows"] == "7"
    assert audit_summary[0]["unblock_plan_audit_passed_rows"] == "0"
    assert audit_summary[0]["score_attempt_blocked_now_rows"] == "7"
    assert audit_summary[0]["overall_status"] == (
        "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_UNBLOCK_PLAN_AUDITED_NOT_COMPLETED_SCORING_STILL_BLOCKED"
    )
    assert audit_summary[0]["next_required_artifact"] == (
        "tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_v01"
    )
    assert "unblock_completed_rows=0" in plan_note
    assert "unblock_plan_audit_passed_rows=0" in audit_note


def test_tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_closes_scoring() -> None:
    gate_rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_v01.csv"
            ).open()
        )
    )
    gate_summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_summary_v01.csv"
            ).open()
        )
    )
    audit_rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit_v01.csv"
            ).open()
        )
    )
    audit_summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit_summary_v01.csv"
            ).open()
        )
    )
    gate_note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_v01.md"
    ).read_text()
    audit_note = (
        ROOT
        / "docs/tau_cmb_phi_tau_parent_input_evidence_payload_scoring_input_payload_submission_evidence_object_receipt_scoring_handoff_unblock_condition_evidence_receipt_acceptance_decision_gate_audit_v01.md"
    ).read_text()

    assert len(gate_rows) == 7
    assert len(audit_rows) == 7
    assert {row["decision_gate_status"] for row in gate_rows} == {
        "ACCEPTANCE_DECISION_GATE_CLOSED_UNBLOCK_PLAN_AUDIT_NOT_PASSED"
    }
    assert {row["decision_gate_audit_status"] for row in audit_rows} == {
        "ACCEPTANCE_DECISION_GATE_AUDITED_CLOSED_SCORING_BLOCKED"
    }
    assert {row["decision_output"] for row in gate_rows} == {"acceptance_closed"}
    assert {row["decision_output"] for row in audit_rows} == {"acceptance_closed"}
    assert {row["decision_gate_audited"] for row in audit_rows} == {"true"}
    assert {row["decision_gate_audit_passed"] for row in audit_rows} == {"true"}
    for rows in [gate_rows, audit_rows]:
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
            assert {row[field] for row in rows} == {"false"}
        assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
        assert {row["recorded_decision"] for row in rows} == {"handoff_closed"}
        assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7

    assert gate_summary[0]["unblock_condition_evidence_receipt_acceptance_decision_gate_rows_declared"] == "7"
    assert gate_summary[0]["decision_gate_closed_rows"] == "7"
    assert gate_summary[0]["unblock_plan_audit_passed_rows"] == "0"
    assert gate_summary[0]["score_attempt_blocked_now_rows"] == "7"
    assert gate_summary[0]["unblock_condition_evidence_receipt_acceptance_decision_gate_satisfied"] == "false"
    assert gate_summary[0]["overall_status"] == (
        "UNBLOCK_CONDITION_EVIDENCE_RECEIPT_ACCEPTANCE_DECISION_GATE_CLOSED_SCORING_STILL_BLOCKED"
    )
    assert audit_summary[0]["unblock_condition_evidence_receipt_acceptance_decision_gate_audit_rows_declared"] == "7"
    assert audit_summary[0]["decision_gate_audited_rows"] == "7"
    assert audit_summary[0]["decision_gate_audit_passed_rows"] == "7"
    assert audit_summary[0]["decision_gate_closed_rows"] == "7"
    assert audit_summary[0]["scores_computed_rows"] == "0"
    assert audit_summary[0]["cmb_likelihood_available_rows"] == "0"
    assert audit_summary[0]["unblock_condition_evidence_receipt_acceptance_decision_gate_audit_satisfied"] == "true"
    assert "decision_gate_closed_rows=7" in gate_note
    assert "decision_gate_audit_passed_rows=7" in audit_note


def test_tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_declares_required_materials_without_scoring() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_v01.md").read_text()

    assert len(rows) == 7
    assert {row["fulfillment_status"] for row in rows} == {
        "ACCEPTANCE_EVIDENCE_FULFILLMENT_PACKAGE_DECLARED_NOT_MATERIALIZED"
    }
    assert {row["requirements_declared"] for row in rows} == {"true"}
    assert {row["required_material_count"] for row in rows} == {"7"}
    for row in rows:
        assert row["required_materials"].split(";") == [
            "materialized_evidence_object",
            "hash_manifest",
            "provenance_record",
            "replay_record",
            "firewall_record",
            "acceptance_record",
            "scoring_handoff_record",
        ]
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
        assert {row[field] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert sum(row["blocks_no_dark_claim"] == "true" for row in rows) == 7
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_FULFILLMENT_PACKAGE_V01",
            "acceptance_evidence_fulfillment_package_rows_declared": "7",
            "requirements_declared_rows": "7",
            "required_material_count_total": "49",
            "evidence_materialized_rows": "0",
            "hash_manifest_present_rows": "0",
            "provenance_record_present_rows": "0",
            "replay_record_present_rows": "0",
            "firewall_record_present_rows": "0",
            "acceptance_record_present_rows": "0",
            "scoring_handoff_record_present_rows": "0",
            "receipt_accepted_rows": "0",
            "evidence_accepted_rows": "0",
            "decision_gate_reopen_allowed_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "acceptance_evidence_fulfillment_package_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACCEPTANCE_EVIDENCE_FULFILLMENT_PACKAGE_DECLARED_NOT_MATERIALIZED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "materialize_acceptance_evidence_objects_and_replay_acceptance_checks",
            "claim_boundary": "tau_cmb_phi_tau_parent_acceptance_evidence_fulfillment_package_v01_fulfillment_package_only_requirements_declared_no_evidence_materialized_no_receipt_accepted_no_handoff_reopened_no_payload_accepted_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "required_material_count_total=49" in note
    assert "decision_gate_reopen_allowed_rows=0" in note


def test_tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_creates_hashed_materials_without_acceptance() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_v01.csv"
            ).open()
        )
    )
    manifest = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_v01_manifest.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_v01.md").read_text()

    assert len(rows) == 7
    assert len(manifest) == 49
    assert {row["materialization_status"] for row in rows} == {
        "ACCEPTANCE_EVIDENCE_MATERIALS_CREATED_HASHED_NOT_ACCEPTED"
    }
    for field in [
        "materialized_evidence_object_present",
        "hash_manifest_present",
        "provenance_record_present",
        "replay_record_present",
        "firewall_record_present",
        "acceptance_record_present",
        "scoring_handoff_record_present",
    ]:
        assert {row[field] for row in rows} == {"true"}
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
        assert {row[field] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["material_records_created"] for row in rows} == {"7"}
    assert {row["material_records_hashed"] for row in rows} == {"7"}

    assert {row["material_present"] for row in manifest} == {"true"}
    assert {row["endpoint_blind"] for row in manifest} == {"true"}
    for manifest_row in manifest:
        material_path = ROOT / manifest_row["material_path"]
        payload = material_path.read_bytes()
        assert hashlib.sha256(payload).hexdigest() == manifest_row["sha256"]
        assert len(payload) == int(manifest_row["byte_size"])
        material = json.loads(payload.decode("utf-8"))
        assert material["endpoint_blind"] == "true"
        assert material["score_status"] == "not_scored"

    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_MATERIALIZATION_PACKAGE_V01",
            "acceptance_evidence_materialization_package_rows_declared": "7",
            "material_records_required": "49",
            "material_records_created": "49",
            "material_records_hashed": "49",
            "materialized_evidence_object_present_rows": "7",
            "hash_manifest_present_rows": "7",
            "provenance_record_present_rows": "7",
            "replay_record_present_rows": "7",
            "firewall_record_present_rows": "7",
            "acceptance_record_present_rows": "7",
            "scoring_handoff_record_present_rows": "7",
            "receipt_accepted_rows": "0",
            "evidence_accepted_rows": "0",
            "decision_gate_reopen_allowed_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "acceptance_evidence_materialization_package_satisfied": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ACCEPTANCE_EVIDENCE_MATERIALS_CREATED_HASHED_NOT_ACCEPTED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "audit_acceptance_evidence_materialization_and_accept_receipts",
            "claim_boundary": "tau_cmb_phi_tau_parent_acceptance_evidence_materialization_package_v01_materialization_only_records_created_and_hashed_no_receipt_accepted_no_evidence_accepted_no_decision_gate_reopen_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "material_records_created=49" in note
    assert "receipt_accepted_rows=0" in note


def test_tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_passes_without_scoring() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["materialization_audit_status"] for row in rows} == {
        "MATERIALIZATION_AUDIT_PASSED_HASHED_ENDPOINT_BLIND_MATERIALS_PRESENT"
    }
    assert {row["materialization_audit_passed"] for row in rows} == {"true"}
    assert {row["receipt_acceptance_precheck_passed"] for row in rows} == {"true"}
    assert {row["evidence_acceptance_precheck_passed"] for row in rows} == {"true"}
    assert {row["material_records_expected"] for row in rows} == {"7"}
    assert {row["material_records_found"] for row in rows} == {"7"}
    assert {row["material_hashes_verified"] for row in rows} == {"7"}
    assert {row["endpoint_blind_materials"] for row in rows} == {"true"}
    assert {row["all_required_material_types_present"] for row in rows} == {"true"}
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
        assert {row[field] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_MATERIALIZATION_AUDIT_ACCEPTANCE_PRECHECK_V01",
            "materialization_audit_acceptance_precheck_rows_declared": "7",
            "materialization_audit_passed_rows": "7",
            "receipt_acceptance_precheck_passed_rows": "7",
            "evidence_acceptance_precheck_passed_rows": "7",
            "material_records_expected_total": "49",
            "material_records_found_total": "49",
            "material_hashes_verified_total": "49",
            "endpoint_blind_material_rows": "7",
            "all_required_material_types_present_rows": "7",
            "receipt_accepted_rows": "0",
            "evidence_accepted_rows": "0",
            "decision_gate_reopen_allowed_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "materialization_audit_acceptance_precheck_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "MATERIALIZATION_AUDIT_AND_ACCEPTANCE_PRECHECK_PASSED_RECEIPTS_NOT_YET_ACCEPTED_SCORING_STILL_BLOCKED",
            "next_required_artifact": "accept_receipts_and_evidence_objects_then_reopen_decision_gate",
            "claim_boundary": "tau_cmb_phi_tau_parent_acceptance_evidence_materialization_audit_acceptance_precheck_v01_audit_and_precheck_only_materialization_audit_passed_receipt_and_evidence_precheck_passed_no_receipt_accepted_no_evidence_accepted_no_decision_gate_reopen_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "materialization_audit_passed_rows=7" in note
    assert "evidence_acceptance_precheck_passed_rows=7" in note


def test_tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_still_blocks_scoring() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["acceptance_status"] for row in rows} == {
        "RECEIPT_AND_EVIDENCE_ACCEPTED_DECISION_GATE_REOPEN_ALLOWED"
    }
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
        assert {row[field] for row in rows} == {"true"}
    assert {row["material_records_expected"] for row in rows} == {"7"}
    assert {row["material_records_found"] for row in rows} == {"7"}
    assert {row["material_hashes_verified"] for row in rows} == {"7"}
    for field in [
        "score_attempt_allowed_now",
        "payload_accepted",
        "scoring_input_accepted",
        "scoring_handoff_opened",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_RECEIPT_EVIDENCE_ACCEPTANCE_REOPEN_GATE_V01",
            "receipt_evidence_acceptance_reopen_gate_rows_declared": "7",
            "materialization_audit_passed_rows": "7",
            "receipt_acceptance_precheck_passed_rows": "7",
            "evidence_acceptance_precheck_passed_rows": "7",
            "material_records_expected_total": "49",
            "material_records_found_total": "49",
            "material_hashes_verified_total": "49",
            "endpoint_blind_material_rows": "7",
            "all_required_material_types_present_rows": "7",
            "receipt_accepted_rows": "7",
            "evidence_accepted_rows": "7",
            "acceptance_record_created_rows": "7",
            "decision_gate_reopen_allowed_rows": "7",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "scoring_handoff_opened_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "receipt_evidence_acceptance_reopen_gate_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "RECEIPT_AND_EVIDENCE_ACCEPTED_DECISION_GATE_REOPEN_ALLOWED_SCORING_INPUT_STILL_BLOCKED",
            "next_required_artifact": "build_scoring_handoff_package_from_accepted_evidence",
            "claim_boundary": "tau_cmb_phi_tau_parent_acceptance_evidence_receipt_evidence_acceptance_reopen_gate_v01_receipt_and_evidence_accepted_decision_gate_reopen_allowed_no_payload_accepted_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "receipt_accepted_rows=7" in note
    assert "score_attempt_blocked_now_rows=7" in note


def test_tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_opens_handoff_without_scoring() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_v01.md").read_text()

    assert len(rows) == 7
    assert {row["handoff_status"] for row in rows} == {
        "SCORING_HANDOFF_PACKAGE_OPENED_FROM_ACCEPTED_EVIDENCE"
    }
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
        assert {row[field] for row in rows} == {"true"}
    for field in [
        "score_attempt_allowed_now",
        "payload_accepted",
        "scoring_input_accepted",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["next_gate"] for row in rows} == {"scoring_input_acceptance_gate"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_SCORING_HANDOFF_PACKAGE_V01",
            "scoring_handoff_package_rows_declared": "7",
            "receipt_accepted_rows": "7",
            "evidence_accepted_rows": "7",
            "acceptance_record_created_rows": "7",
            "decision_gate_reopen_allowed_rows": "7",
            "endpoint_blind_handoff_rows": "7",
            "scoring_handoff_package_created_rows": "7",
            "scoring_handoff_opened_rows": "7",
            "scoring_input_candidate_created_rows": "7",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "payload_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "scoring_handoff_package_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORING_HANDOFF_PACKAGE_OPENED_FROM_ACCEPTED_EVIDENCE_SCORING_INPUT_STILL_BLOCKED",
            "next_required_artifact": "accept_scoring_input_from_handoff_or_route_explicit_null_response",
            "claim_boundary": "tau_cmb_phi_tau_parent_acceptance_evidence_scoring_handoff_package_v01_scoring_handoff_package_opened_from_accepted_evidence_scoring_input_candidate_created_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "scoring_handoff_opened_rows=7" in note
    assert "scoring_input_accepted_rows=0" in note


def test_tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_routes_null_response() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["decision_status"] for row in rows} == {
        "SCORING_INPUT_DECISION_CLOSED_BY_EXPLICIT_NULL_RESPONSE"
    }
    for field in [
        "scoring_handoff_opened",
        "scoring_input_candidate_created",
        "scoring_input_acceptance_decision_closed",
        "explicit_null_response_routed",
    ]:
        assert {row[field] for row in rows} == {"true"}
    for field in [
        "scoring_input_accepted",
        "score_ready_input_available",
        "score_attempt_allowed_now",
        "payload_accepted",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["next_gate"] for row in rows} == {"score_attempt_guard_or_wait_for_real_score_ready_input"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_SCORING_INPUT_DECISION_PACKAGE_V01",
            "scoring_input_decision_package_rows_declared": "7",
            "scoring_handoff_opened_rows": "7",
            "scoring_input_candidate_created_rows": "7",
            "scoring_input_acceptance_decision_closed_rows": "7",
            "scoring_input_accepted_rows": "0",
            "explicit_null_response_routed_rows": "7",
            "score_ready_input_available_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "payload_accepted_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "scoring_input_decision_package_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORING_INPUT_DECISION_CLOSED_BY_EXPLICIT_NULL_RESPONSE_SCORE_STILL_BLOCKED",
            "next_required_artifact": "score_attempt_guard_or_real_score_ready_input_supply",
            "claim_boundary": "tau_cmb_phi_tau_parent_acceptance_evidence_scoring_input_decision_package_v01_scoring_input_decision_closed_by_explicit_null_response_handoff_opened_but_no_score_ready_input_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "explicit_null_response_routed_rows=7" in note
    assert "score_ready_input_available_rows=0" in note


def test_tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_denies_score() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_v01.md").read_text()

    assert len(rows) == 7
    assert {row["guard_status"] for row in rows} == {
        "SCORE_ATTEMPT_GUARD_EXECUTED_DENIED_NO_SCORE_READY_INPUT"
    }
    for field in [
        "score_attempt_guard_executed",
        "scoring_input_acceptance_decision_closed",
        "explicit_null_response_routed",
        "score_attempt_denied",
    ]:
        assert {row[field] for row in rows} == {"true"}
    for field in [
        "score_ready_input_available",
        "scoring_input_accepted",
        "score_attempt_allowed_now",
        "payload_accepted",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["required_unblock_condition"] for row in rows} == {
        "supply_real_score_ready_input_with_accepted_scoring_input"
    }
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_SCORE_ATTEMPT_GUARD_V01",
            "score_attempt_guard_rows_declared": "7",
            "score_attempt_guard_executed_rows": "7",
            "scoring_input_acceptance_decision_closed_rows": "7",
            "explicit_null_response_routed_rows": "7",
            "score_ready_input_available_rows": "0",
            "scoring_input_accepted_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_denied_rows": "7",
            "score_attempt_blocked_now_rows": "7",
            "payload_accepted_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "score_attempt_guard_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "SCORE_ATTEMPT_GUARD_EXECUTED_DENIED_NO_SCORE_READY_INPUT",
            "next_required_artifact": "real_score_ready_input_supply_or_keep_null_response_locked",
            "claim_boundary": "tau_cmb_phi_tau_parent_acceptance_evidence_score_attempt_guard_v01_score_attempt_guard_executed_and_denied_no_score_ready_input_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "score_attempt_guard_executed_rows=7" in note
    assert "score_attempt_denied_rows=7" in note


def test_tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_closes_route() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_v01.md").read_text()

    assert len(rows) == 7
    assert {row["lock_status"] for row in rows} == {"NULL_RESPONSE_LOCKED_AFTER_SCORE_GUARD_DENIAL"}
    for field in [
        "score_attempt_guard_executed",
        "score_attempt_denied",
        "explicit_null_response_routed",
        "null_response_locked",
    ]:
        assert {row[field] for row in rows} == {"true"}
    for field in [
        "score_ready_input_available",
        "scoring_input_accepted",
        "score_attempt_allowed_now",
        "payload_accepted",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["required_unlock_condition"] for row in rows} == {
        "replace_null_response_with_real_score_ready_input_and_accepted_scoring_input"
    }
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_NULL_RESPONSE_LOCK_V01",
            "null_response_lock_rows_declared": "7",
            "score_attempt_guard_executed_rows": "7",
            "score_attempt_denied_rows": "7",
            "explicit_null_response_routed_rows": "7",
            "null_response_locked_rows": "7",
            "score_ready_input_available_rows": "0",
            "scoring_input_accepted_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "payload_accepted_rows": "0",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "null_response_lock_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "NULL_RESPONSE_LOCKED_AFTER_SCORE_GUARD_DENIAL",
            "next_required_artifact": "real_score_ready_input_supply_to_unlock_null_response",
            "claim_boundary": "tau_cmb_phi_tau_parent_acceptance_evidence_null_response_lock_v01_null_response_locked_after_score_guard_denial_no_score_ready_input_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "null_response_locked_rows=7" in note
    assert "score_ready_input_available_rows=0" in note


def test_tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_terminal_state() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_summary_v01.csv"
            ).open()
        )
    )
    note = (
        ROOT / "docs/tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_v01.md"
    ).read_text()

    assert len(rows) == 7
    assert {row["certificate_status"] for row in rows} == {
        "ROUTE_COMPLETED_TO_NULL_RESPONSE_LOCKED_TERMINAL_STATE"
    }
    for field in [
        "route_completed",
        "terminal_state_reached",
        "null_response_locked",
        "score_attempt_guard_executed",
        "score_attempt_denied",
    ]:
        assert {row[field] for row in rows} == {"true"}
    for field in [
        "score_ready_input_available",
        "scoring_input_accepted",
        "score_attempt_allowed_now",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert {row["terminal_state"] for row in rows} == {"null_response_locked"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert {row["required_unlock_condition"] for row in rows} == {
        "real_score_ready_input_with_accepted_scoring_input"
    }
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_ACCEPTANCE_EVIDENCE_ROUTE_COMPLETION_CERTIFICATE_V01",
            "route_completion_certificate_rows_declared": "7",
            "route_completed_rows": "7",
            "terminal_state_reached_rows": "7",
            "null_response_locked_rows": "7",
            "score_attempt_guard_executed_rows": "7",
            "score_attempt_denied_rows": "7",
            "score_ready_input_available_rows": "0",
            "scoring_input_accepted_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "route_completion_certificate_satisfied": "true",
            "terminal_state": "null_response_locked",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "ROUTE_COMPLETED_TO_NULL_RESPONSE_LOCKED_TERMINAL_STATE",
            "next_required_artifact": "real_score_ready_input_supply_to_reopen_scoring_route",
            "claim_boundary": "tau_cmb_phi_tau_parent_acceptance_evidence_route_completion_certificate_v01_route_completed_to_null_response_locked_terminal_state_no_score_ready_input_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "route_completed_rows=7" in note
    assert "terminal_state=null_response_locked" in note


def test_tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_keeps_route_locked() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT / "data/derived/tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_v01.md").read_text()

    assert len(rows) == 7
    assert {row["contract_status"] for row in rows} == {
        "REAL_SCORE_READY_INPUT_REQUIRED_TO_UNLOCK_NULL_RESPONSE"
    }
    assert {row["terminal_state"] for row in rows} == {"null_response_locked"}
    assert {row["route_completed"] for row in rows} == {"true"}
    assert {row["null_response_locked"] for row in rows} == {"true"}
    for field in [
        "requires_phi_tau_eff_source",
        "requires_dimension_replay",
        "requires_normalization_binding",
        "requires_endpoint_blind_provenance",
        "requires_cmb_readout_mapping",
        "requires_likelihood_adapter",
        "requires_acceptance_replay",
    ]:
        assert {row[field] for row in rows} == {"true"}
    assert {row["required_materials_count"] for row in rows} == {"7"}
    assert {row["supplied_materials_count"] for row in rows} == {"0"}
    for field in [
        "real_score_ready_input_supplied",
        "scoring_input_accepted",
        "reopen_scoring_route_allowed_now",
        "score_attempt_allowed_now",
        "phi_tau_eff_derived",
        "scores_computed",
        "cmb_likelihood_available",
    ]:
        assert {row[field] for row in rows} == {"false"}
    assert {row["score_attempt_blocked_now"] for row in rows} == {"true"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_REAL_SCORE_READY_INPUT_SUPPLY_CONTRACT_V01",
            "real_score_ready_input_supply_contract_rows_declared": "7",
            "route_completed_rows": "7",
            "null_response_locked_rows": "7",
            "required_materials_total": "49",
            "supplied_materials_total": "0",
            "real_score_ready_input_supplied_rows": "0",
            "scoring_input_accepted_rows": "0",
            "reopen_scoring_route_allowed_now_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "7",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "real_score_ready_input_supply_contract_satisfied": "true",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "7",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "REAL_SCORE_READY_INPUT_SUPPLY_CONTRACT_DECLARED_INPUT_NOT_SUPPLIED_ROUTE_REMAINS_LOCKED",
            "next_required_artifact": "supply_all_real_score_ready_input_materials_or_keep_route_locked",
            "claim_boundary": "tau_cmb_phi_tau_parent_real_score_ready_input_supply_contract_v01_unlock_contract_only_real_score_ready_input_required_no_input_supplied_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "required_materials_total=49" in note
    assert "supplied_materials_total=0" in note


def test_tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_is_actionable_but_unfilled() -> None:
    rows = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_v01.csv").open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT / "data/derived/tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_v01.md").read_text()

    assert len(rows) == 49
    assert len({row["contract_row_id"] for row in rows}) == 7
    assert {row["material_class"] for row in rows} == {
        "phi_tau_eff_source",
        "dimension_replay",
        "normalization_binding",
        "endpoint_blind_provenance",
        "cmb_readout_mapping",
        "likelihood_adapter",
        "acceptance_replay",
    }
    assert {row["slot_status"] for row in rows} == {"PAYLOAD_SLOT_DECLARED_INPUT_NOT_MATERIALIZED"}
    assert all(row["expected_artifact_path"].startswith("data/score_ready_input/") for row in rows)
    assert all(row["required_schema_fields"] for row in rows)
    assert all(row["validation_rule"] for row in rows)
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
        assert {row[field] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_REAL_SCORE_READY_PAYLOAD_SLOT_SPEC_V01",
            "contract_rows": "7",
            "payload_slot_rows_declared": "49",
            "material_classes_per_contract_row": "7",
            "expected_artifact_paths_declared": "49",
            "payload_materialized_rows": "0",
            "payload_hash_bound_rows": "0",
            "dimension_replay_passed_rows": "0",
            "endpoint_blind_firewall_passed_rows": "0",
            "slot_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "reopen_scoring_route_allowed_now_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "49",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "payload_slot_spec_satisfied": "true",
            "all_required_slots_materialized": "false",
            "all_required_slots_accepted": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "49",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PAYLOAD_SLOT_SPEC_DECLARED_INPUT_NOT_MATERIALIZED_ROUTE_REMAINS_LOCKED",
            "next_required_artifact": "materialize_all_payload_slots_with_hash_bound_endpoint_blind_replay",
            "claim_boundary": "tau_cmb_phi_tau_parent_real_score_ready_payload_slot_spec_v01_slot_spec_only_no_payload_materialized_no_slot_accepted_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "payload_slot_rows_declared=49" in note
    assert "payload_materialized_rows=0" in note


def test_tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_is_bound_but_empty() -> None:
    rows = list(
        csv.DictReader(
            (
                ROOT / "data/derived/tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_v01.csv"
            ).open()
        )
    )
    summary = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_summary_v01.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_v01.md").read_text()

    assert len(rows) == 49
    assert len({row["contract_row_id"] for row in rows}) == 7
    assert len({row["template_path"] for row in rows}) == 7
    assert {row["template_file_exists"] for row in rows} == {"true"}
    assert {row["template_status"] for row in rows} == {"TEMPLATE_BOUND_REAL_PAYLOAD_NOT_MATERIALIZED"}
    for row in rows:
        assert (ROOT / row["template_path"]).exists()
        assert row["expected_artifact_path"].startswith("data/score_ready_input/")
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
        assert {row[field] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_REAL_SCORE_READY_PAYLOAD_TEMPLATE_MANIFEST_V01",
            "slot_rows_consumed": "49",
            "template_bindings_declared": "49",
            "template_files_declared": "7",
            "template_files_written": "7",
            "real_payload_materialized_rows": "0",
            "payload_hash_bound_rows": "0",
            "slot_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "reopen_scoring_route_allowed_now_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "49",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "payload_template_manifest_satisfied": "true",
            "all_real_payloads_materialized": "false",
            "all_slots_accepted": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "49",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "PAYLOAD_TEMPLATE_MANIFEST_DECLARED_REAL_PAYLOAD_NOT_MATERIALIZED_ROUTE_REMAINS_LOCKED",
            "next_required_artifact": "populate_template_files_with_endpoint_blind_real_payloads_and_hash_receipts",
            "claim_boundary": "tau_cmb_phi_tau_parent_real_score_ready_payload_template_manifest_v01_template_manifest_only_no_real_payload_no_hash_binding_no_slot_accepted_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "template_files_written=7" in note
    assert "real_payload_materialized_rows=0" in note


def test_tau_cmb_phi_tau_parent_real_payload_import_precheck_fails_missing_payloads() -> None:
    rows = list(
        csv.DictReader((ROOT / "data/derived/tau_cmb_phi_tau_parent_real_payload_import_precheck_v01.csv").open())
    )
    summary = list(
        csv.DictReader(
            (ROOT / "data/derived/tau_cmb_phi_tau_parent_real_payload_import_precheck_summary_v01.csv").open()
        )
    )
    note = (ROOT / "docs/tau_cmb_phi_tau_parent_real_payload_import_precheck_v01.md").read_text()

    assert len(rows) == 49
    assert len({row["contract_row_id"] for row in rows}) == 7
    assert {row["real_payload_path_exists"] for row in rows} == {"false"}
    assert {row["real_payload_readable"] for row in rows} == {"false"}
    assert {row["real_payload_nonempty"] for row in rows} == {"false"}
    assert {row["payload_sha256"] for row in rows} == {""}
    assert {row["schema_check_status"] for row in rows} == {"SCHEMA_NOT_CHECKED_MISSING_REAL_PAYLOAD"}
    assert {row["import_precheck_status"] for row in rows} == {"IMPORT_PRECHECK_FAIL_MISSING_REAL_PAYLOAD"}
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
        assert {row[field] for row in rows} == {"false"}
    assert summary == [
        {
            "summary_id": "TAU_CMB_PHI_TAU_PARENT_REAL_PAYLOAD_IMPORT_PRECHECK_V01",
            "template_bindings_consumed": "49",
            "import_precheck_rows_declared": "49",
            "real_payload_paths_expected": "49",
            "real_payload_paths_present": "0",
            "real_payload_paths_missing": "49",
            "real_payload_readable_rows": "0",
            "real_payload_nonempty_rows": "0",
            "payload_hash_bound_rows": "0",
            "schema_pass_rows": "0",
            "payload_import_accepted_rows": "0",
            "slot_accepted_rows": "0",
            "scoring_input_accepted_rows": "0",
            "reopen_scoring_route_allowed_now_rows": "0",
            "score_attempt_allowed_now_rows": "0",
            "score_attempt_blocked_now_rows": "49",
            "phi_tau_eff_derived_rows": "0",
            "scores_computed_rows": "0",
            "cmb_likelihood_available_rows": "0",
            "real_payload_import_precheck_satisfied": "true",
            "all_real_payloads_present": "false",
            "all_payload_imports_accepted": "false",
            "scores_computed": "false",
            "cmb_likelihood_available": "false",
            "no_dark_blockers": "49",
            "no_dark_cmb_verdict_allowed": "false",
            "tau_response_claim_allowed": "false",
            "dark_sector_verdict_allowed": "false",
            "overall_status": "REAL_PAYLOAD_IMPORT_PRECHECK_FAILS_MISSING_REAL_PAYLOADS_ROUTE_REMAINS_LOCKED",
            "next_required_artifact": "populate_data_score_ready_input_with_real_endpoint_blind_payloads",
            "claim_boundary": "tau_cmb_phi_tau_parent_real_payload_import_precheck_v01_import_precheck_only_missing_real_payloads_no_hash_binding_no_slot_accepted_no_scoring_input_accepted_no_phi_derivation_no_score_no_likelihood_no_verdict",
        }
    ]
    assert "real_payload_paths_missing=49" in note
    assert "payload_import_accepted_rows=0" in note


def test_planck_lensing_cross_readout_holdout_for_tau_candidate() -> None:
    summary = json.loads(
        (ROOT / "data/derived/cmb_planck_lensing_cross_readout_holdout_for_tau_candidate_v01_summary.json").read_text()
    )
    rows = list(
        csv.DictReader((ROOT / "data/derived/cmb_planck_lensing_cross_readout_holdout_for_tau_candidate_v01.csv").open())
    )
    scoreboard = list(
        csv.DictReader(
            (ROOT / "data/derived/cmb_planck_lensing_cross_readout_holdout_for_tau_candidate_v01_scoreboard.csv").open()
        )
    )
    note = (ROOT / "docs/cmb_planck_lensing_cross_readout_holdout_for_tau_candidate_v01.md").read_text()

    assert summary["summary_id"] == "CMB_PLANCK_LENSING_CROSS_READOUT_HOLDOUT_FOR_TAU_CANDIDATE_V01"
    assert summary["planck_rows"] == 9
    assert summary["planck_covariance_positive_definite"] is True
    assert summary["candidate_transferred_without_planck_refit"] is True
    assert summary["physical_tau_response_claim_allowed"] is False
    assert summary["dark_sector_verdict_allowed"] is False
    assert len(rows) == 9
    assert len(scoreboard) == 2
    assert float(summary["candidate_chi2"]) < float(summary["null_chi2"])
    assert float(summary["candidate_fractional_chi2_improvement_vs_null"]) > 0.8
    assert summary["obligation_NZRESP_OBL_004_status"].endswith("not_closed")
    assert "not a physical Tau prediction" in note
    assert "not a dark-sector verdict" in note


def test_tau_lensing_nonzero_candidate_derivation_status_audit() -> None:
    summary = json.loads(
        (ROOT / "data/derived/cmb_tau_lensing_nonzero_candidate_derivation_status_audit_v01_summary.json").read_text()
    )
    rows = list(
        csv.DictReader((ROOT / "data/derived/cmb_tau_lensing_nonzero_candidate_derivation_status_audit_v01.csv").open())
    )
    formula = list(
        csv.DictReader(
            (ROOT / "data/derived/cmb_tau_lensing_nonzero_candidate_derivation_status_audit_v01_formula_spec.csv").open()
        )
    )
    note = (ROOT / "docs/cmb_tau_lensing_nonzero_candidate_derivation_status_audit_v01.md").read_text()

    assert summary["summary_id"] == "CMB_TAU_LENSING_NONZERO_CANDIDATE_DERIVATION_STATUS_AUDIT_V01"
    assert summary["obligations_total"] == 4
    assert summary["closed_formula_level"] == 1
    assert summary["partially_addressed"] == 1
    assert summary["open_tau_derivation"] == 2
    assert summary["zero_limit_closed_for_formula_family"] is True
    assert summary["cross_readout_holdout_support_present"] is True
    assert summary["shape_tau_derivation_present"] is False
    assert summary["amplitude_tau_derivation_present"] is False
    assert summary["physical_tau_response_claim_allowed"] is False
    assert summary["dark_sector_verdict_allowed"] is False
    assert len(rows) == 4
    assert len(formula) == 4
    statuses = {row["obligation_id"]: row["status_after_audit"] for row in rows}
    assert statuses["NZRESP_OBL_003"] == "closed_formula_level_only"
    assert statuses["NZRESP_OBL_004"] == "partially_addressed_not_closed"
    assert statuses["NZRESP_OBL_001"] == "open_tau_derivation_required"
    assert statuses["NZRESP_OBL_002"] == "open_tau_derivation_required"
    assert "diagnostic candidate" in note
    assert "physical\nTau response" in note


def test_tau_lensing_response_origin_route_audit() -> None:
    summary = json.loads(
        (ROOT / "data/derived/cmb_tau_lensing_response_origin_route_audit_v01_summary.json").read_text()
    )
    routes = list(csv.DictReader((ROOT / "data/derived/cmb_tau_lensing_response_origin_route_audit_v01.csv").open()))
    requirements = list(
        csv.DictReader((ROOT / "data/derived/cmb_tau_lensing_response_origin_route_audit_v01_requirements.csv").open())
    )
    note = (ROOT / "docs/cmb_tau_lensing_response_origin_route_audit_v01.md").read_text()

    assert summary["summary_id"] == "CMB_TAU_LENSING_RESPONSE_ORIGIN_ROUTE_AUDIT_V01"
    assert summary["routes_declared"] == 4
    assert summary["route_selected_now"] is False
    assert summary["seed_only_route_status"] == "open_viable_but_unproved"
    assert summary["base_field_route_status"] == "open_viable_but_unproved"
    assert summary["hybrid_route_status"] == "open_high_burden_route"
    assert summary["requirements_total"] == 6
    assert summary["requirements_open"] == 4
    assert summary["requirements_partial"] == 1
    assert summary["requirements_closed_formula_level"] == 1
    assert summary["physical_tau_response_claim_allowed"] is False
    assert summary["dark_sector_verdict_allowed"] is False
    assert {row["route_id"] for row in routes} == {
        "ROUTE_00_NULL",
        "ROUTE_01_SEED_ONLY",
        "ROUTE_02_BASE_FIELD",
        "ROUTE_03_HYBRID",
    }
    assert {row["requirement_id"] for row in requirements} >= {
        "REQ_SHAPE_ELL_C",
        "REQ_SHAPE_RISE",
        "REQ_SHAPE_FALL",
        "REQ_AMPLITUDE",
    }
    assert "No route is selected" in note


def test_tau_lensing_base_field_route_prederivation_packet() -> None:
    summary = json.loads(
        (ROOT / "data/derived/cmb_tau_lensing_base_field_route_prederivation_packet_v01_summary.json").read_text()
    )
    decisions = list(
        csv.DictReader((ROOT / "data/derived/cmb_tau_lensing_base_field_route_prederivation_packet_v01.csv").open())
    )
    operators = list(
        csv.DictReader(
            (ROOT / "data/derived/cmb_tau_lensing_base_field_route_prederivation_packet_v01_operator_targets.csv").open()
        )
    )
    tests = list(
        csv.DictReader(
            (ROOT / "data/derived/cmb_tau_lensing_base_field_route_prederivation_packet_v01_acceptance_tests.csv").open()
        )
    )
    note = (ROOT / "docs/cmb_tau_lensing_base_field_route_prederivation_packet_v01.md").read_text()

    assert summary["summary_id"] == "CMB_TAU_LENSING_BASE_FIELD_ROUTE_PREDERIVATION_PACKET_V01"
    assert summary["selected_next_work_route"] == "ROUTE_02_BASE_FIELD"
    assert summary["route_selected_as_physical"] is False
    assert summary["seed_only_route_rejected"] is False
    assert summary["hybrid_route_rejected"] is False
    assert summary["operator_targets_total"] == 5
    assert summary["acceptance_tests_total"] == 5
    assert summary["acceptance_tests_open"] == 5
    assert summary["physical_tau_response_claim_allowed"] is False
    assert summary["dark_sector_verdict_allowed"] is False
    assert len(decisions) == 4
    assert any(row["route_id"] == "ROUTE_02_BASE_FIELD" and row["decision_for_next_work"] == "selected_as_next_derivation_work_route" for row in decisions)
    assert {row["operator_object"] for row in operators} >= {
        "seed_to_effective_tau_response",
        "lensing_projection_kernel",
        "minimal_broad_low_L_response_kernel",
        "amplitude_normalization",
    }
    assert {row["test_name"] for row in tests} >= {
        "endpoint_blind_shape_derivation",
        "endpoint_blind_amplitude_derivation",
        "zero_limit_recovery",
    }
    assert "not as a physical truth claim" in note


def test_tau_lensing_base_field_operator_ansatz_packet() -> None:
    summary = json.loads(
        (ROOT / "data/derived/cmb_tau_lensing_base_field_operator_ansatz_packet_v01_summary.json").read_text()
    )
    ansatz = list(csv.DictReader((ROOT / "data/derived/cmb_tau_lensing_base_field_operator_ansatz_packet_v01.csv").open()))
    properties = list(
        csv.DictReader((ROOT / "data/derived/cmb_tau_lensing_base_field_operator_ansatz_packet_v01_properties.csv").open())
    )
    gaps = list(
        csv.DictReader((ROOT / "data/derived/cmb_tau_lensing_base_field_operator_ansatz_packet_v01_open_gaps.csv").open())
    )
    note = (ROOT / "docs/cmb_tau_lensing_base_field_operator_ansatz_packet_v01.md").read_text()

    assert summary["summary_id"] == "CMB_TAU_LENSING_BASE_FIELD_OPERATOR_ANSATZ_PACKET_V01"
    assert summary["shape_ansatz_materialized"] is True
    assert summary["properties_total"] == 6
    assert summary["properties_pass_formula_level"] == 5
    assert summary["open_physical_derivation_gaps"] == 4
    assert summary["D_tau_derived"] is False
    assert summary["Pi_lens_derived"] is False
    assert summary["shape_parameters_derived"] is False
    assert summary["amplitude_derived"] is False
    assert summary["physical_tau_response_claim_allowed"] is False
    assert summary["dark_sector_verdict_allowed"] is False
    assert len(ansatz) == 4
    assert len(properties) == 6
    assert len(gaps) == 4
    assert {row["property_name"] for row in properties} >= {
        "dimensionless_shape_kernel",
        "normalization",
        "low_L_activation",
        "high_L_suppression",
        "zero_response_limit",
    }
    assert any(row["status"] == "open_physical_derivation_gap" for row in properties)
    assert "does not derive the ansatz from Tau Core" in note


def test_tau_lensing_factorized_response_derivation_attempt() -> None:
    summary = json.loads(
        (ROOT / "data/derived/cmb_tau_lensing_factorized_response_derivation_attempt_v01_summary.json").read_text()
    )
    factors = list(
        csv.DictReader((ROOT / "data/derived/cmb_tau_lensing_factorized_response_derivation_attempt_v01.csv").open())
    )
    assessment = list(
        csv.DictReader(
            (ROOT / "data/derived/cmb_tau_lensing_factorized_response_derivation_attempt_v01_assessment.csv").open()
        )
    )
    next_steps = list(
        csv.DictReader(
            (ROOT / "data/derived/cmb_tau_lensing_factorized_response_derivation_attempt_v01_next_steps.csv").open()
        )
    )
    note = (ROOT / "docs/cmb_tau_lensing_factorized_response_derivation_attempt_v01.md").read_text()

    assert summary["summary_id"] == "CMB_TAU_LENSING_FACTORIZED_RESPONSE_DERIVATION_ATTEMPT_V01"
    assert summary["formula_factorization_exact"] is True
    assert summary["factors_total"] == 5
    assert summary["formula_level_assessments_pass"] == 4
    assert summary["open_tau_side_factor_derivations"] == 4
    assert summary["seed_activation_derived"] is False
    assert summary["base_field_screening_derived"] is False
    assert summary["transition_scale_derived"] is False
    assert summary["amplitude_derived"] is False
    assert summary["physical_tau_response_claim_allowed"] is False
    assert summary["dark_sector_verdict_allowed"] is False
    assert {row["factor_name"] for row in factors} >= {
        "seed_activation_factor",
        "base_field_screening_factor",
        "readout_normalization_factor",
        "amplitude_slot",
    }
    assert any(row["status"] == "open_physical_derivation_gap" for row in assessment)
    assert len(next_steps) == 4
    assert "does not derive the factors from Tau Core" in note


def test_tau_lensing_seed_screening_minimal_closure_attempt() -> None:
    summary = json.loads(
        (
            ROOT
            / "data/derived/cmb_tau_lensing_seed_screening_minimal_closure_attempt_v01_summary.json"
        ).read_text()
    )
    assumptions = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/cmb_tau_lensing_seed_screening_minimal_closure_attempt_v01_assumptions.csv"
            ).open()
        )
    )
    closures = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/cmb_tau_lensing_seed_screening_minimal_closure_attempt_v01_closures.csv"
            ).open()
        )
    )
    next_steps = list(
        csv.DictReader(
            (
                ROOT
                / "data/derived/cmb_tau_lensing_seed_screening_minimal_closure_attempt_v01_next_steps.csv"
            ).open()
        )
    )
    note = (ROOT / "docs/cmb_tau_lensing_seed_screening_minimal_closure_attempt_v01.md").read_text()

    assert summary["summary_id"] == "CMB_TAU_LENSING_SEED_SCREENING_MINIMAL_CLOSURE_ATTEMPT_V01"
    assert summary["conditional_factor_closures"] == 2
    assert summary["unconditional_tau_derivations"] == 0
    assert summary["reconstructs_factorized_kernel"] is True
    assert summary["seed_activation_conditionally_closed"] is True
    assert summary["base_field_screening_conditionally_closed"] is True
    assert summary["score_readiness_unlocked"] is False
    assert summary["physical_tau_response_claim_allowed"] is False
    assert summary["dark_sector_verdict_allowed"] is False
    assert {row["target_factor"] for row in assumptions} >= {
        "seed_activation_factor",
        "base_field_screening_factor",
    }
    assert {row["factor"] for row in closures} >= {
        "seed_activation_factor",
        "base_field_screening_factor",
        "combined_shape_kernel",
    }
    assert len(next_steps) == 4
    assert "does not prove the physical Tau response" in note


def test_manuscript_scope_and_no_overclaim() -> None:
    text = (ROOT / "paper13_submission_source/main.tex").read_text()
    assert "CMB Constraint Mapping" in text
    assert "Effective Source Equation Target" in text
    assert "Known-Limit and Dimension Audit" in text
    assert "Minimal Source-Term Candidate" in text
    assert "Source-Term Dimensional Precheck" in text
    assert "LCDM Role Scoring Rubric" in text
    assert "Role Scorecard Template" in text
    assert "Score Input Unblock Plan" in text
    assert "Known-Limit Failure Map" in text
    assert "Density Amplitude Derivation" in text
    assert "Acoustic Role Reduced Benchmark" in text
    assert "Lensing Transfer Benchmark" in text
    assert "Growth Transfer Kernel" in text
    assert "Radiation Guard Bound Check" in text
    assert "Scorecard Readiness Audit" in text
    assert "Scorecard Blocker Closure Plan" in text
    assert "Density Amplitude Closure" in text
    assert "Acoustic Reduced Evaluation" in text
    assert "Lensing Transfer Reduced Evaluation" in text
    assert "Growth Transfer Kernel Closure" in text
    assert "Radiation Guard Evaluation" in text
    assert "Known-Limit Decision Update" in text
    assert "Scorecard Prescore Blocker Summary" in text
    assert "Minimal Scoring Input Contract" in text
    assert "Scoring Execution Gate" in text
    assert "Scoring Input Fulfillment Plan" in text
    assert "Effective Potential Source Handoff" in text
    assert "Endpoint-Blind Phi Tau Derivation Contract" in text
    assert "Phi Tau Parent Input Provenance" in text
    assert "Phi Tau Parent Input Candidate Manifest" in text
    assert "Phi Tau Parent Input Firewall Audit" in text
    assert "Phi Tau Parent Input Payload Stub" in text
    assert "Phi Tau Parent Input Firewall Execution" in text
    assert "Phi Tau Parent Input Concrete Payload Requirements" in text
    assert "Phi Tau Parent Input Concrete Payload Candidate" in text
    assert "Phi Tau Parent Input Payload Firewall Audit" in text
    assert "Phi Tau Parent Input Dimension Replay Certificate" in text
    assert "Phi Tau Parent Input Certificate Candidate" in text
    assert "Phi Tau Parent Input Certificate Audit" in text
    assert "Phi Tau Parent Input Certificate Evidence Request" in text
    assert "Phi Tau Parent Input Certificate Evidence Package Candidate" in text
    assert "Phi Tau Parent Input Certificate Evidence Package Audit" in text
    assert "Phi Tau Parent Input Scoring Acceptance Precheck" in text
    assert "Phi Tau Parent Input Scoring Acceptance Unblock Plan" in text
    assert "Phi Tau Parent Input Populated Evidence Package Candidate" in text
    assert "Phi Tau Parent Input Populated Evidence Package Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Submission Gate" in text
    assert "Phi Tau Parent Input Evidence Payload Receipt Candidate" in text
    assert "Phi Tau Parent Input Evidence Payload Receipt Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Receipt Remediation Plan" in text
    assert "Phi Tau Parent Input Evidence Payload Materialization Packet" in text
    assert "Phi Tau Parent Input Evidence Payload Materialization Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Acceptance Precheck" in text
    assert "Phi Tau Parent Input Evidence Payload Acceptance Unblock Plan" in text
    assert "Phi Tau Parent Input Evidence Payload Acceptance Decision Gate" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Candidate" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Remediation Plan" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Remediation Packet" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Remediation Packet Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Materialization Request" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Materialization Request Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Materialization Packet" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Materialization Packet Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Fulfillment Request" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Fulfillment Request Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Packet" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Packet Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Remediation Plan" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Remediation Packet" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Remediation Packet Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Materialization Request" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Materialization Request Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Materialization Packet" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Materialization Packet Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Fulfillment Request" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Fulfillment Request Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Execution Packet" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Execution Packet Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Execution Unblock Plan" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Execution Unblock Plan Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Request" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Request Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Gate" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Gate Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Candidate" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Candidate Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Candidate Remediation Plan" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Materialization Packet" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Materialization Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Acceptance Precheck" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Acceptance Unblock Plan" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Acceptance Unblock Plan Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Acceptance Decision Gate" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Acceptance Decision Gate Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Acceptance Record" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Precheck" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Plan" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Plan Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Decision Gate" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Decision Gate Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Acceptance Record" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Acceptance Record Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Final Pre-Score Lock" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Final Pre-Score Lock Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Score Attempt Blocker Certificate" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Score Attempt Unblock Conditions" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Request" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Receipt Candidate" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Receipt Candidate Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Receipt Remediation Plan" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Receipt Materialization Packet" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Receipt Materialization Audit" in text
    assert "Phi Tau Parent Input Evidence Payload Scoring Input Payload Submission Evidence Object Receipt Scoring Handoff Unblock Condition Evidence Receipt Acceptance Precheck" in text
    assert "Evidence Receipt Acceptance Unblock Plan" in text
    assert "Evidence Receipt Acceptance Unblock Plan Audit" in text
    assert "Evidence Receipt Acceptance Decision Gate" in text
    assert "Evidence Receipt Decision Gate Audit" in text
    assert "Acceptance Evidence Fulfillment Package" in text
    assert "Acceptance Evidence Materialization Package" in text
    assert "Materialization Audit and Acceptance Precheck" in text
    assert "Receipt and Evidence Acceptance Reopen Gate" in text
    assert "Acceptance Evidence Scoring Handoff Package" in text
    assert "Acceptance Evidence Scoring Input Decision Package" in text
    assert "Acceptance Evidence Score Attempt Guard" in text
    assert "Acceptance Evidence Null-Response Lock" in text
    assert "Acceptance Evidence Route Completion Certificate" in text
    assert "Real Score-Ready Input Supply Contract" in text
    assert "Planck Lensing Cross-Readout Holdout" in text
    assert "Nonzero Candidate Derivation Status Audit" in text
    assert "Tau Lensing Response-Origin Routes" in text
    assert "Base-Field Route Prederivation Target" in text
    assert "Base-Field Operator Ansatz" in text
    assert "Factorized Lensing Response Attempt" in text
    assert "Seed-Screening Minimal Closure Attempt" in text
    assert "Real Score-Ready Payload Slot Specification" in text
    assert "Real Score-Ready Payload Template Manifest" in text
    assert "Real Payload Import Precheck" in text
    assert "does not claim that Tau Core explains the CMB" in text
    forbidden_absent = [
        "We show that Tau Core explains the CMB",
        "We show that dark matter does not exist",
        "we detect a Tau dark-sector field",
    ]
    for phrase in forbidden_absent:
        assert phrase not in text


def test_arxiv_zip_is_source_only() -> None:
    with zipfile.ZipFile(ROOT / "arxiv_submission_source.zip") as archive:
        names = set(archive.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "main.pdf" not in names
    assert not any(name.endswith(".aux") or name.endswith(".log") for name in names)
