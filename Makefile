.PHONY: intake intake-report evidence-check route-submission-audit payload-checklist score-fulfillment skeleton-direct skeleton-delta skeleton-failure tau-grid-formula-template tau-grid-upstream-table-template tau-grid-upstream-metadata-template tau-grid-production-status tau-grid-derivation-intake-audit tau-grid-derivation-intake-smoke tau-grid-route-b-template tau-grid-route-b-parent-request tau-grid-route-b-parent-formula-template tau-grid-route-b-parent-formula-candidate tau-grid-route-b-parent-formula-audit tau-grid-route-b-parent-from-formula-dry-run tau-grid-route-b-parent-from-formula-write-staging tau-grid-route-b-parent-table-template tau-grid-route-b-parent-table-precheck tau-grid-route-b-parent-template tau-grid-route-b-parent-dry-run tau-grid-route-b-parent-write-staging tau-grid-route-b-parent-smoke tau-grid-physical-candidate-request tau-grid-physical-candidate-scaffold tau-grid-nonzero-probe tau-grid-nonzero-precheck tau-grid-physical-candidate-precheck tau-grid-nonzero-probe-package tau-grid-physical-candidate-package tau-grid-zero-control tau-grid-zero-control-package tau-grid-zero-control-activate tau-grid-upstream-table-spec tau-grid-handoff-dry-run tau-grid-handoff-write-staging tau-grid-spec-candidate tau-grid-equation-packet tau-grid-from-formula tau-grid-scale-diagnostic tau-grid-normalization-gap-derivation tau-grid-endpoint-blind-normalization-gate tau-grid-adapter-convention-lock tau-grid-tau-side-normalization-obligation tau-grid-parent-projection-packet-skeleton tau-grid-projection-normalization-split tau-grid-physical-projection-domain-lock tau-grid-physical-projection-firewall-certificate tau-grid-projection-post-population-firewall-spec-scaffold tau-grid-projection-formula-spec-acceptance-matrix tau-grid-projection-operator-rule-requirement tau-grid-projection-operator-formula-spec-scaffold tau-grid-projection-equation-spec-scaffold tau-grid-projection-kernel-measure-spec-scaffold tau-grid-projection-normalization-spec-scaffold tau-grid-projection-output-replay-spec-scaffold tau-grid-projection-dimension-sign-audit-scaffold tau-grid-projection-zero-source-limit-obligation tau-grid-projection-operator-explicit-failure tau-grid-projection-normalization-requirement tau-grid-physical-projection-replay-requirement tau-grid-projection-operator-decision-gate tau-grid-physical-projection-operator-packet tau-grid-physical-projection-operator-audit staging-precheck-direct staging-precheck-delta staging-precheck-failure staging-promote-direct-dry-run staging-promote-delta-dry-run staging-promote-delta-replace-dry-run staging-promote-failure-dry-run staging-promote-direct staging-promote-delta staging-promote-delta-replace staging-promote-failure payload-replacement-packet env-check materialize-replay preflight score score-report score-todo score-readiness route-pack score-unblock score-gate score-attempt-guard score-output-audit scoring-status scoring-smoke scoring-positive-smoke scoring-firewall-smoke scoring-good-route-smoke scoring-guarded-entrypoint-smoke scoring-guarded-positive-smoke scoring-stale-receipt-smoke scoring-matching-receipt-smoke staging-positive-smoke staging-promotion-guard-smoke staging-promotion-copy-smoke scoring-regression-all prepare-direct-hash prepare-delta-hash validate-direct-grid validate-delta-grid

intake:
	@python3 scripts/intake_tau_lensing_route_evidence.py

intake-report:
	@python3 scripts/intake_tau_lensing_route_evidence.py --write-report

evidence-check:
	@python3 scripts/check_tau_lensing_route_evidence_firewall.py --write-report

route-submission-audit:
	@python3 scripts/audit_tau_lensing_route_submission.py --write-audit

payload-checklist:
	@python3 scripts/build_tau_lensing_payload_acceptance_checklist.py --write-checklist

score-fulfillment:
	@python3 scripts/build_tau_lensing_scoring_input_fulfillment_packet.py --write-packet

tau-grid-production-status:
	@python3 scripts/build_tau_lensing_grid_production_status.py --write-status

tau-grid-derivation-intake-audit:
	@python3 scripts/audit_tau_lensing_physical_derivation_intake.py --write-audit

tau-grid-derivation-intake-smoke:
	@python3 scripts/smoke_tau_lensing_derivation_intake_audit.py --write-report

tau-grid-route-b-template:
	@python3 scripts/build_tau_lensing_route_b_metadata_template.py --write-report

tau-grid-route-b-parent-request:
	@python3 scripts/build_tau_lensing_route_b_parent_source_request.py --write-packet --write-doc

tau-grid-route-b-parent-formula-template:
	@python3 scripts/materialize_tau_lensing_route_b_parent_source_from_formula_spec.py --write-template

tau-grid-route-b-parent-formula-candidate:
	@python3 scripts/build_tau_lensing_route_b_parent_source_formula_spec_candidate.py --write-spec --write-report

tau-grid-route-b-parent-formula-audit:
	@python3 scripts/audit_tau_lensing_route_b_parent_source_formula_spec.py --write-report

tau-grid-route-b-parent-from-formula-dry-run:
	@python3 scripts/materialize_tau_lensing_route_b_parent_source_from_formula_spec.py payload_staging/tau_lensing_route_b_parent_source_formula_spec_v01.json --write-report

tau-grid-route-b-parent-from-formula-write-staging:
	@python3 scripts/materialize_tau_lensing_route_b_parent_source_from_formula_spec.py payload_staging/tau_lensing_route_b_parent_source_formula_spec_v01.json --write-staging --write-report

tau-grid-route-b-parent-table-template:
	@python3 scripts/precheck_tau_lensing_route_b_parent_source_table.py --write-template payload_templates/tau_lensing_route_b_parent_source_TABLE_TEMPLATE_v01.csv

tau-grid-route-b-parent-table-precheck:
	@python3 scripts/precheck_tau_lensing_route_b_parent_source_table.py --write-report

tau-grid-route-b-parent-template:
	@python3 scripts/materialize_tau_lensing_route_b_from_parent_source.py --write-template

tau-grid-route-b-parent-dry-run:
	@python3 scripts/materialize_tau_lensing_route_b_from_parent_source.py payload_staging/tau_lensing_route_b_parent_source_config_v01.json --write-report

tau-grid-route-b-parent-write-staging:
	@python3 scripts/materialize_tau_lensing_route_b_from_parent_source.py payload_staging/tau_lensing_route_b_parent_source_config_v01.json --write-staging --write-report

tau-grid-route-b-parent-smoke:
	@python3 scripts/smoke_tau_lensing_route_b_parent_source_materializer.py --write-report

skeleton-direct:
	@python3 scripts/build_tau_lensing_submission_skeleton.py --route direct_tau_PP_grid --write-report

skeleton-delta:
	@python3 scripts/build_tau_lensing_submission_skeleton.py --route delta_PP_tau_against_named_fiducial_PP --write-report

skeleton-failure:
	@python3 scripts/build_tau_lensing_submission_skeleton.py --route explicit_failure_no_endpoint_blind_grid --write-report

tau-grid-formula-template:
	@python3 scripts/materialize_tau_lensing_grid_from_formula_spec.py --write-template

tau-grid-upstream-table-template:
	@python3 scripts/build_tau_lensing_upstream_table_formula_spec.py --write-template

tau-grid-upstream-metadata-template:
	@python3 scripts/build_tau_lensing_upstream_table_formula_spec.py --write-metadata-template

tau-grid-physical-candidate-request:
	@python3 scripts/build_tau_lensing_physical_candidate_upstream_request.py --write-packet --write-doc

tau-grid-physical-candidate-scaffold:
	@python3 scripts/build_tau_lensing_physical_candidate_upstream_scaffold.py --write-report

tau-grid-nonzero-probe:
	@python3 scripts/build_tau_lensing_nonzero_probe_response.py --write-report

tau-grid-nonzero-precheck:
	@python3 scripts/precheck_tau_lensing_nonzero_upstream_table.py --write-report

tau-grid-physical-candidate-precheck:
	@python3 scripts/precheck_tau_lensing_physical_candidate_upstream_table.py --write-report

tau-grid-nonzero-probe-package:
	@python3 scripts/build_tau_lensing_nonzero_probe_delta_route_package.py --write-report

tau-grid-physical-candidate-package:
	@python3 scripts/build_tau_lensing_physical_candidate_delta_route_package.py --write-report

tau-grid-zero-control:
	@python3 scripts/build_tau_lensing_zero_response_control.py --write-report

tau-grid-zero-control-package:
	@python3 scripts/build_tau_lensing_zero_control_delta_route_package.py --write-report

tau-grid-zero-control-activate:
	@python3 scripts/activate_tau_lensing_zero_control_delta_route.py --write-report

tau-grid-upstream-table-spec:
	@python3 scripts/build_tau_lensing_upstream_table_formula_spec.py --table payload_staging/tau_lensing_upstream_l_response_v01.csv --metadata payload_staging/tau_lensing_upstream_l_response_metadata_v01.json --write-spec --write-report

tau-grid-handoff-dry-run:
	@python3 scripts/run_tau_lensing_upstream_grid_handoff_dry_run.py --write-report

tau-grid-handoff-write-staging:
	@python3 scripts/run_tau_lensing_upstream_grid_handoff_dry_run.py --write-staging --write-report

tau-grid-spec-candidate:
	@python3 scripts/build_tau_lensing_grid_formula_spec_candidate.py --write-candidate --write-audit

tau-grid-equation-packet:
	@python3 scripts/build_tau_lensing_grid_equation_packet.py --write-packet

tau-grid-from-formula:
	@python3 scripts/materialize_tau_lensing_grid_from_formula_spec.py payload_staging/tau_lensing_grid_formula_spec_v01.json --write-staging --write-report

tau-grid-scale-diagnostic:
	@python3 scripts/fit_tau_lensing_route_b_candidate_scale_diagnostic.py --write-report

tau-grid-normalization-gap-derivation:
	@python3 scripts/derive_tau_lensing_route_b_normalization_gap.py --write-report --write-doc

tau-grid-endpoint-blind-normalization-gate:
	@python3 scripts/build_tau_lensing_endpoint_blind_normalization_gate.py --write-report --write-doc

tau-grid-adapter-convention-lock:
	@python3 scripts/build_tau_lensing_adapter_convention_normalization_lock.py --write-report --write-doc

tau-grid-tau-side-normalization-obligation:
	@python3 scripts/build_tau_lensing_tau_side_normalization_obligation.py --write-report --write-doc

tau-grid-parent-projection-packet-skeleton:
	@python3 scripts/build_tau_lensing_parent_projection_packet_skeleton.py --write-packet --write-summary --write-doc

tau-grid-projection-normalization-split:
	@python3 scripts/build_tau_lensing_projection_normalization_split.py --write-report --write-doc

tau-grid-physical-projection-domain-lock:
	@python3 scripts/build_tau_lensing_physical_projection_domain_lock.py --write-report --write-doc

tau-grid-physical-projection-firewall-certificate:
	@python3 scripts/build_tau_lensing_physical_projection_firewall_certificate.py --write-report --write-doc

tau-grid-projection-post-population-firewall-spec-scaffold:
	@python3 scripts/build_tau_lensing_projection_post_population_firewall_spec_scaffold.py --write-table --write-summary --write-doc

tau-grid-projection-formula-spec-acceptance-matrix:
	@python3 scripts/build_tau_lensing_projection_formula_spec_acceptance_matrix.py --write-table --write-summary --write-doc

tau-grid-endpoint-blind-operator-packet-request:
	@python3 scripts/build_tau_lensing_endpoint_blind_operator_packet_request.py --write-table --write-summary --write-doc

tau-grid-endpoint-blind-operator-packet-submission-template:
	@python3 scripts/build_tau_lensing_endpoint_blind_operator_packet_submission_template.py --write-template --write-summary --write-doc

tau-grid-endpoint-blind-operator-packet-submission-candidate:
	@python3 scripts/build_tau_lensing_endpoint_blind_operator_packet_submission_candidate.py --write-submission --write-summary --write-doc

tau-grid-endpoint-blind-operator-packet-receipt-audit:
	@python3 scripts/audit_tau_lensing_endpoint_blind_operator_packet_receipt.py --write-report --write-doc

tau-grid-endpoint-blind-operator-packet-content-audit-router:
	@python3 scripts/build_tau_lensing_endpoint_blind_operator_packet_content_audit_router.py --write-table --write-summary --write-doc

tau-grid-endpoint-blind-operator-packet-content-audit:
	@python3 scripts/audit_tau_lensing_endpoint_blind_operator_packet_content.py --write-table --write-summary --write-doc

tau-grid-endpoint-blind-operator-prescore-lock:
	@python3 scripts/build_tau_lensing_endpoint_blind_operator_prescore_lock.py --write-report --write-doc

tau-cmb-cosmology-derivation-spine:
	@python3 scripts/build_tau_cmb_cosmology_derivation_spine.py --write-table --write-summary --write-doc

tau-cmb-single-pass-derivation-spine:
	@python3 scripts/build_tau_cmb_single_pass_derivation_spine.py --write-table --write-summary --write-doc

tau-cmb-source-grounding-gate:
	@python3 scripts/build_tau_cmb_source_grounding_gate.py --write-table --write-summary --write-doc

tau-cmb-parent-source-freeze-packet:
	@python3 scripts/build_tau_cmb_parent_source_freeze_packet.py --write-table --write-summary --write-doc

tau-cmb-parent-source-freeze-packet-submission-template:
	@python3 scripts/build_tau_cmb_parent_source_freeze_packet_submission_template.py --write-template --write-summary --write-doc

tau-cmb-parent-source-freeze-packet-submission-candidate:
	@python3 scripts/build_tau_cmb_parent_source_freeze_packet_submission_candidate.py --write-candidate --write-summary --write-doc

tau-cmb-parent-source-freeze-packet-submission-candidate-audit:
	@python3 scripts/audit_tau_cmb_parent_source_freeze_packet_submission_candidate.py --write-report --write-doc

tau-cmb-parent-source-unavailability-record:
	@python3 scripts/build_tau_cmb_parent_source_unavailability_record.py --write-report --write-doc

tau-cmb-parent-source-component-unblock-plan:
	@python3 scripts/build_tau_cmb_parent_source_component_unblock_plan.py --write-table --write-summary --write-doc

tau-cmb-morphological-seed-descriptor-candidate:
	@python3 scripts/build_tau_cmb_morphological_seed_descriptor_candidate.py --write-table --write-summary --write-doc

tau-cmb-morphological-seed-descriptor-candidate-audit:
	@python3 scripts/audit_tau_cmb_morphological_seed_descriptor_candidate.py --write-report --write-doc

tau-cmb-morphological-seed-activation-quotient-audit:
	@python3 scripts/build_tau_cmb_morphological_seed_activation_quotient_audit.py --write-table --write-summary --write-doc

tau-cmb-morphological-seed-activation-rule-candidate:
	@python3 scripts/build_tau_cmb_morphological_seed_activation_rule_candidate.py --write-table --write-summary --write-doc

tau-cmb-morphological-seed-activation-rule-candidate-audit:
	@python3 scripts/audit_tau_cmb_morphological_seed_activation_rule_candidate.py --write-report --write-doc

tau-cmb-morphological-seed-quotient-survival-test:
	@python3 scripts/build_tau_cmb_morphological_seed_quotient_survival_test.py --write-table --write-summary --write-doc

tau-cmb-seed-readout-interface-candidate:
	@python3 scripts/build_tau_cmb_seed_readout_interface_candidate.py --write-table --write-summary --write-doc

tau-cmb-seed-readout-domain-certificate:
	@python3 scripts/build_tau_cmb_seed_readout_domain_certificate.py --write-table --write-summary --write-doc

tau-cmb-seed-tau-payload-materialization-packet:
	@python3 scripts/build_tau_cmb_seed_tau_payload_materialization_packet.py --write-table --write-summary --write-doc --write-template

tau-cmb-seed-tau-payload-candidate:
	@python3 scripts/build_tau_cmb_seed_tau_payload_candidate.py --write-all

tau-cmb-seed-tau-payload-candidate-audit:
	@python3 scripts/audit_tau_cmb_seed_tau_payload_candidate.py --write-report --write-doc

tau-cmb-seed-payload-unblock-triad:
	@python3 scripts/build_tau_cmb_seed_payload_unblock_triad.py --write-table --write-summary --write-doc

tau-cmb-seed-support-domain-rule-candidate:
	@python3 scripts/build_tau_cmb_seed_support_domain_rule_candidate.py --write-table --write-summary --write-doc

tau-cmb-seed-support-domain-rule-candidate-audit:
	@python3 scripts/audit_tau_cmb_seed_support_domain_rule_candidate.py --write-report --write-doc

tau-cmb-seed-normalization-replay-candidate:
	@python3 scripts/build_tau_cmb_seed_normalization_replay_candidate.py --write-table --write-summary --write-replay --write-doc

tau-cmb-seed-normalization-replay-candidate-audit:
	@python3 scripts/audit_tau_cmb_seed_normalization_replay_candidate.py --write-report --write-doc

tau-cmb-seed-zero-control:
	@python3 scripts/build_tau_cmb_seed_zero_control.py --write-table --write-summary --write-replay --write-doc

tau-cmb-seed-zero-control-audit:
	@python3 scripts/audit_tau_cmb_seed_zero_control.py --write-report --write-doc

tau-cmb-seed-chain-pre-acceptance-gate:
	@python3 scripts/build_tau_cmb_seed_chain_pre_acceptance_gate.py --write-table --write-summary --write-doc

tau-cmb-seed-readout-quotient-relation-candidate:
	@python3 scripts/build_tau_cmb_seed_readout_quotient_relation_candidate.py --write-table --write-summary --write-doc

tau-cmb-seed-readout-quotient-relation-candidate-audit:
	@python3 scripts/audit_tau_cmb_seed_readout_quotient_relation_candidate.py --write-report --write-doc

tau-cmb-seed-readout-equivalence-relation-audit:
	@python3 scripts/audit_tau_cmb_seed_readout_equivalence_relation.py --write-report --write-doc

tau-cmb-seed-readout-equivalence-axiom-proof-obligation:
	@python3 scripts/build_tau_cmb_seed_readout_equivalence_axiom_proof_obligation.py --write-table --write-summary --write-doc

tau-cmb-readout-role-space-basis:
	@python3 scripts/build_tau_cmb_readout_role_space_basis.py --write-table --write-summary --write-doc

tau-cmb-readout-role-space-basis-audit:
	@python3 scripts/audit_tau_cmb_readout_role_space_basis.py --write-report --write-doc

tau-cmb-readout-role-coordinate-acoustic:
	@python3 scripts/build_tau_cmb_readout_role_coordinate_acoustic.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-acoustic-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_acoustic.py --write-report --write-doc

tau-cmb-readout-role-coordinate-density:
	@python3 scripts/build_tau_cmb_readout_role_coordinate_density.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-density-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_density.py --write-report --write-doc

tau-cmb-readout-role-coordinate-lensing:
	@python3 scripts/build_tau_cmb_readout_role_coordinate_lensing.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-lensing-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_lensing.py --write-report --write-doc

tau-cmb-readout-role-coordinate-growth:
	@python3 scripts/build_tau_cmb_readout_role_coordinate_growth.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-growth-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_growth.py --write-report --write-doc

tau-cmb-readout-role-coordinate-radiation:
	@python3 scripts/build_tau_cmb_readout_role_coordinate_radiation.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-radiation-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_radiation.py --write-report --write-doc

tau-cmb-readout-role-coordinate-null:
	@python3 scripts/build_tau_cmb_readout_role_coordinate_null.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-null-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_null.py --write-report --write-doc

tau-cmb-readout-role-coordinate-bundle-closure:
	@python3 scripts/build_tau_cmb_readout_role_coordinate_bundle_closure.py --write-report --write-doc

tau-cmb-readout-role-coordinate-bundle-closure-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_bundle_closure.py --write-report --write-doc

tau-cmb-scoring-input-gap-matrix:
	@python3 scripts/build_tau_cmb_scoring_input_gap_matrix.py --write-table --write-summary --write-doc

tau-cmb-concrete-R-CMB-carrier-certificate:
	@python3 scripts/build_tau_cmb_concrete_R_CMB_carrier_certificate.py --write-table --write-summary --write-doc

tau-cmb-concrete-R-CMB-carrier-certificate-audit:
	@python3 scripts/audit_tau_cmb_concrete_R_CMB_carrier_certificate.py --write-report --write-doc

tau-cmb-carrier-domain-predicate-candidate:
	@python3 scripts/build_tau_cmb_carrier_domain_predicate_candidate.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-predicate-candidate-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_predicate_candidate.py --write-report --write-doc

tau-cmb-carrier-domain-certificate-requirements:
	@python3 scripts/build_tau_cmb_carrier_domain_certificate_requirements.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-certificate-requirements-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_certificate_requirements.py --write-report --write-doc

tau-cmb-carrier-domain-certificate-candidate:
	@python3 scripts/build_tau_cmb_carrier_domain_certificate_candidate.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-certificate-candidate-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_certificate_candidate.py --write-report --write-doc

tau-cmb-carrier-domain-proof-checker-payload-packet:
	@python3 scripts/build_tau_cmb_carrier_domain_proof_checker_payload_packet.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-proof-checker-payload-packet-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_proof_checker_payload_packet.py --write-report --write-doc

tau-cmb-carrier-domain-checker-execution-packet:
	@python3 scripts/build_tau_cmb_carrier_domain_checker_execution_packet.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-checker-execution-packet-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_execution_packet.py --write-report --write-doc

tau-cmb-carrier-domain-checker-input-payload-request:
	@python3 scripts/build_tau_cmb_carrier_domain_checker_input_payload_request.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-checker-input-payload-request-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_input_payload_request.py --write-report --write-doc

tau-cmb-carrier-domain-checker-input-payload-fulfillment-packet:
	@python3 scripts/build_tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-checker-input-payload-fulfillment-packet-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_input_payload_fulfillment_packet.py --write-report --write-doc

tau-cmb-carrier-domain-checker-input-payload-materialization-packet:
	@python3 scripts/build_tau_cmb_carrier_domain_checker_input_payload_materialization_packet.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-checker-input-payload-materialization-packet-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_input_payload_materialization_packet.py --write-report --write-doc

tau-cmb-carrier-domain-checker-input-payload-file-materialization:
	@python3 scripts/build_tau_cmb_carrier_domain_checker_input_payload_file_materialization.py --write-table --write-summary --write-doc --write-templates

tau-cmb-carrier-domain-checker-input-payload-file-materialization-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_input_payload_file_materialization.py --write-report --write-doc

tau-cmb-carrier-domain-checker-input-payload-staging-population-packet:
	@python3 scripts/build_tau_cmb_carrier_domain_checker_input_payload_staging_population_packet.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-checker-input-payload-staging-population-packet-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_input_payload_staging_population_packet.py --write-report --write-doc

tau-cmb-carrier-domain-checker-input-payload-staging-population-execution:
	@python3 scripts/populate_tau_cmb_carrier_domain_checker_input_payload_staging.py --write-staging --write-table --write-summary --write-doc

tau-cmb-carrier-domain-checker-input-payload-staging-population-execution-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_input_payload_staging_population_execution.py --write-report --write-doc

tau-cmb-carrier-domain-checker-input-payload-acceptance-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_input_payload_acceptance.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-checker-execution-packet-refresh:
	@python3 scripts/build_tau_cmb_carrier_domain_checker_execution_packet_refresh.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-checker-execution-packet-refresh-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_execution_packet_refresh.py --write-report --write-doc

tau-cmb-concrete-R-CMB-candidate-gate:
	@python3 scripts/build_tau_cmb_concrete_R_CMB_candidate_gate.py --write-candidate --write-doc

tau-cmb-concrete-R-CMB-candidate-gate-audit:
	@python3 scripts/audit_tau_cmb_concrete_R_CMB_candidate_gate.py --write-report --write-doc

tau-cmb-carrier-domain-checker-execution-packet-refresh-v02:
	@python3 scripts/build_tau_cmb_carrier_domain_checker_execution_packet_refresh_v02.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-checker-execution-packet-refresh-v02-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_execution_packet_refresh_v02.py --write-report --write-doc

tau-cmb-carrier-domain-checker-execution-attempt-packet:
	@python3 scripts/build_tau_cmb_carrier_domain_checker_execution_attempt_packet.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-checker-execution-attempt-packet-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_execution_attempt_packet.py --write-report --write-doc

tau-cmb-carrier-domain-checker-scaffold-execution:
	@python3 scripts/run_carrier_ok_checker.py
	@python3 scripts/run_dom_ok_checker.py
	@python3 scripts/run_seed_admissibility_checker.py
	@python3 scripts/run_null_control_checker.py
	@python3 scripts/run_source_object_checker.py
	@python3 scripts/run_quotient_survival_checker.py
	@python3 scripts/run_endpoint_firewall_checker.py

tau-cmb-carrier-domain-checker-implementation-scaffold:
	@python3 scripts/build_tau_cmb_carrier_domain_checker_implementation_scaffold.py --write-report --write-doc

tau-cmb-carrier-domain-checker-implementation-scaffold-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_implementation_scaffold.py --write-report --write-doc

tau-cmb-carrier-domain-checker-scaffold-output-acceptance:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_scaffold_output_acceptance.py --write-table --write-summary --write-doc

tau-cmb-certificate-level-checker-rule-implementation:
	@python3 scripts/build_tau_cmb_certificate_level_checker_rule_implementation.py --write-table --write-summary --write-doc

tau-cmb-certificate-level-checker-rule-implementation-audit:
	@python3 scripts/audit_tau_cmb_certificate_level_checker_rule_implementation.py --write-report --write-doc

tau-cmb-certificate-semantic-evidence-materialization:
	@python3 scripts/build_tau_cmb_certificate_semantic_evidence_materialization.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-artifact-supply:
	@python3 scripts/supply_tau_cmb_certificate_semantic_evidence_artifacts.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-artifact-supply-audit:
	@python3 scripts/audit_tau_cmb_certificate_semantic_evidence_artifact_supply.py --write-report --write-doc

tau-cmb-certificate-semantic-evidence-acceptance-audit:
	@python3 scripts/audit_tau_cmb_certificate_semantic_evidence_acceptance.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-replacement-request:
	@python3 scripts/build_tau_cmb_certificate_semantic_evidence_replacement_request.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-replacement-supply:
	@python3 scripts/supply_tau_cmb_certificate_semantic_evidence_replacements.py --write-replacements --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-replacement-supply-audit:
	@python3 scripts/audit_tau_cmb_certificate_semantic_evidence_replacement_supply.py --write-report --write-doc

tau-cmb-certificate-semantic-evidence-substantive-assertion-supply:
	@python3 scripts/supply_tau_cmb_certificate_semantic_evidence_substantive_assertions.py --write-assertions --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-positive-proof-trace-request:
	@python3 scripts/build_tau_cmb_certificate_semantic_evidence_positive_proof_trace_request.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-positive-proof-trace-supply:
	@python3 scripts/supply_tau_cmb_certificate_semantic_evidence_positive_proof_traces.py --write-traces --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-positive-proof-trace-supply-audit:
	@python3 scripts/audit_tau_cmb_certificate_semantic_evidence_positive_proof_trace_supply.py --write-report --write-doc

tau-cmb-certificate-semantic-evidence-positive-proof-trace-acceptance-audit:
	@python3 scripts/audit_tau_cmb_certificate_semantic_evidence_positive_proof_trace_acceptance.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-substantive-trace-component-supply:
	@python3 scripts/supply_tau_cmb_certificate_semantic_evidence_substantive_trace_components.py --write-components --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-substantive-trace-component-supply-audit:
	@python3 scripts/audit_tau_cmb_certificate_semantic_evidence_substantive_trace_component_supply.py --write-report --write-doc

tau-cmb-certificate-semantic-evidence-substantive-trace-component-acceptance-audit:
	@python3 scripts/audit_tau_cmb_certificate_semantic_evidence_substantive_trace_component_acceptance.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-substantive-trace-component-proof-content-request:
	@python3 scripts/build_tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_request.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-substantive-trace-component-proof-content-supply:
	@python3 scripts/supply_tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-substantive-trace-component-proof-content-acceptance-audit:
	@python3 scripts/audit_tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_acceptance.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-substantive-trace-component-proof-content-substantive-verification-supply:
	@python3 scripts/supply_tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-substantive-trace-component-proof-content-substantive-verification-acceptance-audit:
	@python3 scripts/audit_tau_cmb_certificate_semantic_evidence_substantive_trace_component_proof_content_substantive_verification_acceptance.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-substantive-trace-component-local-derivation-replay-body-supply:
	@python3 scripts/supply_tau_cmb_certificate_semantic_evidence_substantive_trace_component_local_derivation_replay_body.py --write-bodies --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-trace-acceptance-refresh:
	@python3 scripts/refresh_tau_cmb_certificate_semantic_evidence_trace_acceptance_from_component_acceptance.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-certificate-rule-execution-refresh:
	@python3 scripts/refresh_tau_cmb_certificate_semantic_evidence_certificate_rule_execution.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-checker-execution-replay-supply:
	@python3 scripts/supply_tau_cmb_certificate_semantic_evidence_checker_execution_replay.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-checker-execution-replay-acceptance-audit:
	@python3 scripts/audit_tau_cmb_certificate_semantic_evidence_checker_execution_replay_acceptance.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-certificate-level-checker-replay-supply:
	@python3 scripts/supply_tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-certificate-level-checker-replay-acceptance-audit:
	@python3 scripts/audit_tau_cmb_certificate_semantic_evidence_certificate_level_checker_replay_acceptance.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-domain-object-acceptance-refresh:
	@python3 scripts/refresh_tau_cmb_certificate_semantic_evidence_domain_object_acceptance.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-physical-r-cmb-materialization-request:
	@python3 scripts/build_tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_request.py --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-physical-r-cmb-materialization-supply:
	@python3 scripts/supply_tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-certificate-semantic-evidence-physical-r-cmb-materialization-acceptance-audit:
	@python3 scripts/audit_tau_cmb_certificate_semantic_evidence_physical_R_CMB_materialization_acceptance.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-materialization-supply:
	@python3 scripts/supply_tau_cmb_readout_role_coordinate_numeric_materialization.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-materialization-acceptance-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_numeric_materialization_acceptance.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-source-supply:
	@python3 scripts/supply_tau_cmb_readout_role_coordinate_numeric_value_source.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-source-acceptance-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_numeric_value_source_acceptance.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-population:
	@python3 scripts/build_tau_cmb_readout_role_coordinate_numeric_value_population.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-population-acceptance-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_numeric_value_population_acceptance.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-cell-supply:
	@python3 scripts/supply_tau_cmb_readout_role_coordinate_numeric_value_cell.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-cell-acceptance-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_numeric_value_cell_acceptance.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-import-packet:
	@python3 scripts/supply_tau_cmb_readout_role_coordinate_numeric_value_import_packet.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-import-packet-acceptance-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_numeric_value_import_packet_acceptance.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-import-execution:
	@python3 scripts/execute_tau_cmb_readout_role_coordinate_numeric_value_import.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-import-execution-acceptance-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_numeric_value_import_execution_acceptance.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-import-population-packet:
	@python3 scripts/build_tau_cmb_readout_role_coordinate_numeric_value_import_population_packet.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-import-population-packet-acceptance-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_numeric_value_import_population_packet_acceptance.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-population-value-payload:
	@python3 scripts/build_tau_cmb_readout_role_coordinate_numeric_value_population_value_payload.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-population-value-payload-acceptance-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_numeric_value_population_value_payload_acceptance.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-payload-value-source-acquisition:
	@python3 scripts/build_tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-payload-value-source-acquisition-acceptance-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_numeric_value_payload_value_source_acquisition_acceptance.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-score:
	@python3 scripts/build_tau_cmb_readout_role_coordinate_numeric_value_score.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-score-acceptance-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_numeric_value_score_acceptance.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-payload-source-ingest:
	@python3 scripts/ingest_tau_cmb_readout_role_coordinate_numeric_value_payload_sources.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-payload-source-ingest-acceptance-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_numeric_value_payload_source_ingest_acceptance.py --write-table --write-summary --write-doc

tau-cmb-readout-role-coordinate-numeric-value-protocol-saturation-audit:
	@python3 scripts/audit_tau_cmb_readout_role_coordinate_numeric_value_protocol_saturation.py --write-table --write-summary --write-doc

tau-cmb-endpoint-blind-physical-value-source-packet:
	@python3 scripts/build_tau_cmb_endpoint_blind_physical_value_source_packet.py --write-artifacts --write-table --write-summary --write-doc

tau-cmb-endpoint-blind-physical-value-source-packet-acceptance-audit:
	@python3 scripts/audit_tau_cmb_endpoint_blind_physical_value_source_packet_acceptance.py --write-table --write-summary --write-doc

tau-cmb-endpoint-blind-physical-value-source-frontier-collapse:
	@python3 scripts/build_tau_cmb_endpoint_blind_physical_value_source_frontier_collapse.py --write-table --write-summary --write-doc

tau-cmb-endpoint-blind-lensing-bridge-candidates-audit:
	@python3 scripts/audit_tau_cmb_endpoint_blind_lensing_bridge_candidates.py --write-table --write-summary --write-doc

tau-cmb-lensing-transfer-kernel-explicit-fail-supply:
	@python3 scripts/supply_tau_cmb_lensing_transfer_kernel_explicit_fail.py --write-artifact --write-summary --write-doc

tau-cmb-lensing-transfer-kernel-explicit-fail-acceptance-audit:
	@python3 scripts/audit_tau_cmb_lensing_transfer_kernel_explicit_fail_acceptance.py --write-summary --write-doc

tau-cmb-endpoint-blind-physical-value-source-frontier-recompute:
	@python3 scripts/build_tau_cmb_endpoint_blind_physical_value_source_frontier_recompute.py --write-table --write-summary --write-doc

tau-cmb-lensing-amplitude-shape-response-adapter-or-explicit-fail:
	@python3 scripts/audit_tau_cmb_lensing_amplitude_shape_response_adapter_or_explicit_fail.py --write-summary --write-doc

tau-cmb-lensing-amplitude-shape-response-explicit-fail-supply:
	@python3 scripts/supply_tau_cmb_lensing_amplitude_shape_response_explicit_fail.py --write-artifact --write-summary --write-doc

tau-cmb-lensing-amplitude-shape-response-explicit-fail-acceptance-audit:
	@python3 scripts/audit_tau_cmb_lensing_amplitude_shape_response_explicit_fail_acceptance.py --write-summary --write-doc

tau-cmb-endpoint-blind-physical-value-source-frontier-recompute-v02:
	@python3 scripts/build_tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_v02.py --write-table --write-summary --write-doc

tau-cmb-physical-source-dependency-unblock-plan:
	@python3 scripts/build_tau_cmb_physical_source_dependency_unblock_plan.py --write-table --write-summary --write-doc

tau-cmb-endpoint-blind-phi-tau-source-or-explicit-fail-supply:
	@python3 scripts/supply_tau_cmb_endpoint_blind_phi_tau_source_or_explicit_fail.py --write-artifact --write-summary --write-doc

tau-cmb-endpoint-blind-phi-tau-source-explicit-fail-acceptance-audit:
	@python3 scripts/audit_tau_cmb_endpoint_blind_phi_tau_source_explicit_fail_acceptance.py --write-summary --write-doc

tau-cmb-endpoint-blind-physical-value-source-frontier-recompute-v03:
	@python3 scripts/build_tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_v03.py --write-table --write-summary --write-doc

tau-cmb-density-source-amplitude-or-explicit-fail-supply:
	@python3 scripts/supply_tau_cmb_density_source_amplitude_or_explicit_fail.py --write-artifact --write-summary --write-doc

tau-cmb-density-source-amplitude-explicit-fail-acceptance-audit:
	@python3 scripts/audit_tau_cmb_density_source_amplitude_explicit_fail_acceptance.py --write-summary --write-doc

tau-cmb-endpoint-blind-physical-value-source-frontier-recompute-v04:
	@python3 scripts/build_tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_v04.py --write-table --write-summary --write-doc

tau-cmb-delta-neff-or-explicit-fail-supply:
	@python3 scripts/supply_tau_cmb_delta_neff_or_explicit_fail.py --write-artifact --write-summary --write-doc

tau-cmb-delta-neff-explicit-fail-acceptance-audit:
	@python3 scripts/audit_tau_cmb_delta_neff_explicit_fail_acceptance.py --write-summary --write-doc

tau-cmb-endpoint-blind-physical-value-source-frontier-recompute-v05:
	@python3 scripts/build_tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_v05.py --write-table --write-summary --write-doc

tau-cmb-acoustic-response-bundle-or-explicit-fail-supply:
	@python3 scripts/supply_tau_cmb_acoustic_response_bundle_or_explicit_fail.py --write-artifact --write-summary --write-doc

tau-cmb-acoustic-response-bundle-explicit-fail-acceptance-audit:
	@python3 scripts/audit_tau_cmb_acoustic_response_bundle_explicit_fail_acceptance.py --write-summary --write-doc

tau-cmb-endpoint-blind-physical-value-source-frontier-recompute-v06:
	@python3 scripts/build_tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_v06.py --write-table --write-summary --write-doc

tau-cmb-growth-transfer-operator-or-explicit-fail-supply:
	@python3 scripts/supply_tau_cmb_growth_transfer_operator_or_explicit_fail.py --write-artifact --write-summary --write-doc

tau-cmb-growth-transfer-operator-explicit-fail-acceptance-audit:
	@python3 scripts/audit_tau_cmb_growth_transfer_operator_explicit_fail_acceptance.py --write-summary --write-doc

tau-cmb-endpoint-blind-physical-value-source-frontier-recompute-v07:
	@python3 scripts/build_tau_cmb_endpoint_blind_physical_value_source_frontier_recompute_v07.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-checker-input-payload-endpoint-blind-source-artifact-request:
	@python3 scripts/build_tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-checker-input-payload-endpoint-blind-source-artifact-request-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_request.py --write-report --write-doc

tau-cmb-carrier-domain-checker-input-payload-endpoint-blind-source-artifact-supply-packet:
	@python3 scripts/build_tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet.py --write-table --write-summary --write-doc

tau-cmb-carrier-domain-checker-input-payload-endpoint-blind-source-artifact-supply-packet-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_supply_packet.py --write-report --write-doc

tau-cmb-carrier-domain-checker-input-payload-endpoint-blind-source-artifact-materialization-packet:
	@python3 scripts/materialize_tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifacts.py --write-sources --write-report --write-doc

tau-cmb-carrier-domain-checker-input-payload-endpoint-blind-source-artifact-materialization-packet-audit:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_materialization_packet.py --write-report --write-doc

tau-grid-projection-operator-rule-requirement:
	@python3 scripts/build_tau_lensing_projection_operator_rule_requirement.py --write-report --write-doc

tau-grid-projection-operator-formula-spec-scaffold:
	@python3 scripts/build_tau_lensing_projection_operator_formula_spec_scaffold.py --write-report --write-doc

tau-grid-projection-equation-spec-scaffold:
	@python3 scripts/build_tau_lensing_projection_equation_spec_scaffold.py --write-table --write-summary --write-doc

tau-grid-projection-kernel-measure-spec-scaffold:
	@python3 scripts/build_tau_lensing_projection_kernel_measure_spec_scaffold.py --write-table --write-summary --write-doc

tau-grid-projection-normalization-spec-scaffold:
	@python3 scripts/build_tau_lensing_projection_normalization_spec_scaffold.py --write-table --write-summary --write-doc

tau-grid-projection-output-replay-spec-scaffold:
	@python3 scripts/build_tau_lensing_projection_output_replay_spec_scaffold.py --write-table --write-summary --write-doc

tau-grid-projection-dimension-sign-audit-scaffold:
	@python3 scripts/build_tau_lensing_projection_dimension_sign_audit_scaffold.py --write-table --write-summary --write-doc

tau-grid-projection-zero-source-limit-obligation:
	@python3 scripts/build_tau_lensing_projection_zero_source_limit_obligation.py --write-report --write-doc

tau-grid-projection-operator-explicit-failure:
	@python3 scripts/build_tau_lensing_projection_operator_explicit_failure.py --write-report --write-doc

tau-grid-projection-normalization-requirement:
	@python3 scripts/build_tau_lensing_projection_normalization_requirement.py --write-report --write-doc

tau-grid-physical-projection-replay-requirement:
	@python3 scripts/build_tau_lensing_physical_projection_replay_requirement.py --write-report --write-doc

tau-grid-projection-operator-decision-gate:
	@python3 scripts/build_tau_lensing_projection_operator_decision_gate.py --write-report --write-doc

tau-grid-physical-projection-operator-packet:
	@python3 scripts/build_tau_lensing_physical_projection_operator_packet.py --write-packet --write-summary --write-doc

tau-grid-physical-projection-operator-audit:
	@python3 scripts/audit_tau_lensing_physical_projection_operator_packet.py --write-audit

staging-precheck-direct:
	@python3 scripts/precheck_tau_lensing_staging_promotion.py --route direct_tau_PP_grid --write-report

staging-precheck-delta:
	@python3 scripts/precheck_tau_lensing_staging_promotion.py --route delta_PP_tau_against_named_fiducial_PP --write-report

staging-precheck-failure:
	@python3 scripts/precheck_tau_lensing_staging_promotion.py --route explicit_failure_no_endpoint_blind_grid --write-report

staging-promote-direct-dry-run:
	@python3 scripts/promote_tau_lensing_staging_payload.py --route direct_tau_PP_grid --dry-run --write-report

staging-promote-delta-dry-run:
	@python3 scripts/promote_tau_lensing_staging_payload.py --route delta_PP_tau_against_named_fiducial_PP --dry-run --write-report

staging-promote-delta-replace-dry-run:
	@python3 scripts/promote_tau_lensing_staging_payload.py --route delta_PP_tau_against_named_fiducial_PP --dry-run --allow-replace --write-report

staging-promote-failure-dry-run:
	@python3 scripts/promote_tau_lensing_staging_payload.py --route explicit_failure_no_endpoint_blind_grid --dry-run --write-report

staging-promote-direct:
	@python3 scripts/promote_tau_lensing_staging_payload.py --route direct_tau_PP_grid --write-report

staging-promote-delta:
	@python3 scripts/promote_tau_lensing_staging_payload.py --route delta_PP_tau_against_named_fiducial_PP --write-report

staging-promote-delta-replace:
	@python3 scripts/promote_tau_lensing_staging_payload.py --route delta_PP_tau_against_named_fiducial_PP --allow-replace --write-report

staging-promote-failure:
	@python3 scripts/promote_tau_lensing_staging_payload.py --route explicit_failure_no_endpoint_blind_grid --write-report

payload-replacement-packet:
	@python3 scripts/build_tau_lensing_payload_replacement_packet.py --write-packet

env-check:
	@python3 scripts/check_tau_lensing_scoring_environment.py --write-report

materialize-replay:
	@python3 scripts/materialize_tau_lensing_projection_replay.py

preflight:
	@python3 scripts/preflight_tau_lensing_reduced_score.py

score:
	@python3 scripts/run_tau_lensing_guarded_score_report.py --write-receipt

score-report:
	@python3 scripts/run_tau_lensing_guarded_score_report.py --write-report --write-receipt

score-todo:
	@python3 scripts/extract_tau_lensing_scoring_todo.py --write-todo

score-readiness:
	@python3 scripts/decide_tau_lensing_score_readiness.py --write-decision

route-pack:
	@python3 scripts/build_tau_lensing_route_evidence_pack.py --write-pack

score-unblock:
	@python3 scripts/build_tau_lensing_score_unblock_bundle.py --write-bundle

score-gate:
	@python3 scripts/run_tau_lensing_score_gate.py --write-gate

score-attempt-guard:
	@python3 scripts/guard_tau_lensing_score_attempt.py --write-guard

score-output-audit:
	@python3 scripts/audit_tau_lensing_score_output_status.py --write-audit

scoring-status:
	@python3 scripts/build_tau_lensing_scoring_status_summary.py --write-status

scoring-smoke:
	@python3 scripts/smoke_tau_lensing_scoring_gates.py

scoring-positive-smoke:
	@python3 scripts/smoke_tau_lensing_positive_score_path.py

scoring-firewall-smoke:
	@python3 scripts/smoke_tau_lensing_firewall_blocker_path.py

scoring-good-route-smoke:
	@python3 scripts/smoke_tau_lensing_good_route_submission_path.py

scoring-guarded-entrypoint-smoke:
	@python3 scripts/smoke_tau_lensing_guarded_score_entrypoint.py

scoring-guarded-positive-smoke:
	@python3 scripts/smoke_tau_lensing_guarded_positive_score_entrypoint.py

scoring-stale-receipt-smoke:
	@python3 scripts/smoke_tau_lensing_score_output_stale_receipt_guard.py

scoring-matching-receipt-smoke:
	@python3 scripts/smoke_tau_lensing_score_output_matching_receipt_acceptance.py

staging-positive-smoke:
	@python3 scripts/smoke_tau_lensing_staging_promotion_positive_path.py

staging-promotion-guard-smoke:
	@python3 scripts/smoke_tau_lensing_staging_promotion_guard.py

staging-promotion-copy-smoke:
	@python3 scripts/smoke_tau_lensing_staging_promotion_copy_path.py

scoring-regression-all:
	@python3 scripts/smoke_tau_lensing_scoring_gates.py
	@python3 scripts/smoke_tau_lensing_positive_score_path.py
	@python3 scripts/smoke_tau_lensing_firewall_blocker_path.py
	@python3 scripts/smoke_tau_lensing_good_route_submission_path.py
	@python3 scripts/smoke_tau_lensing_guarded_score_entrypoint.py
	@python3 scripts/smoke_tau_lensing_guarded_positive_score_entrypoint.py
	@python3 scripts/smoke_tau_lensing_score_output_stale_receipt_guard.py
	@python3 scripts/smoke_tau_lensing_score_output_matching_receipt_acceptance.py
	@python3 scripts/smoke_tau_lensing_staging_promotion_positive_path.py
	@python3 scripts/smoke_tau_lensing_staging_promotion_guard.py
	@python3 scripts/smoke_tau_lensing_staging_promotion_copy_path.py
	@python3 scripts/run_tau_lensing_score_gate.py --with-regression-smokes --write-gate
	@python3 scripts/guard_tau_lensing_score_attempt.py --write-guard
	@python3 scripts/audit_tau_lensing_score_output_status.py --write-audit

prepare-direct-hash:
	@python3 scripts/prepare_tau_lensing_payload_hashes.py --route direct_tau_PP_grid

prepare-delta-hash:
	@python3 scripts/prepare_tau_lensing_payload_hashes.py --route delta_PP_tau_against_named_fiducial_PP

validate-direct-grid:
	@python3 scripts/validate_tau_lensing_grid_payload.py payloads/tau_lensing_response_pp_grid_v01.csv --route direct_tau_PP_grid

validate-delta-grid:
	@python3 scripts/validate_tau_lensing_grid_payload.py payloads/tau_lensing_response_delta_pp_v01.csv --route delta_PP_tau

tau-cmb-carrier-domain-checker-input-payload-endpoint-blind-source-artifact-acceptance:
	@python3 scripts/audit_tau_cmb_carrier_domain_checker_input_payload_endpoint_blind_source_artifact_acceptance.py --write-table --write-summary --write-doc
