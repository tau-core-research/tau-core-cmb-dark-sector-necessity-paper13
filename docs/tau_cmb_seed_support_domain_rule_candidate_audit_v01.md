# Tau CMB Seed Support Domain Rule Candidate Audit v01

**Doc class:** support-domain rule candidate audit
**Status:** SEED_SUPPORT_DOMAIN_RULE_CANDIDATE_AUDITED_BLOCKED_NOT_CERTIFIED

## Claim Boundary

```text
tau_cmb_seed_support_domain_rule_candidate_audit_v01_audit_only_support_not_certified_no_payload_acceptance_no_domain_certificate_no_readout_no_score_no_verdict
```

## Purpose

This audit checks whether the support-domain rule candidate is well-formed and
endpoint-blind as a candidate. It does not certify support, accept the payload,
certify `seed_tau_CMB in Dom(R_CMB)`, evaluate readout survival, assign
`A_tau(a,k)`, enter scoring, or decide the dark-sector question.

## Audit Rows

- `rule_table_shape`: PASS_RULE_ROWS_PRESENT | components=['parent_domain_symbol', 'support_coordinate_basis', 'membership_rule', 'forbidden_endpoint_dependence', 'normalization_dependency', 'zero_control_dependency']
- `parent_domain_symbol`: PASS_SYMBOL_DECLARED_AS_SECTOR_LABEL | parent-domain symbol is declared as CMB morphology/readout sector label
- `support_tuple_well_formed_candidate`: PASS_TUPLE_FIELDS_PRESENT_NOT_NORMALIZED | payload provides morphology_class, readout_sector, and scale_label candidate fields
- `endpoint_blindness_candidate`: PASS_ENDPOINT_BLIND_CANDIDATE_EVIDENCE | firewall records endpoint_inputs_used=[] and provenance keeps score closed
- `support_certification`: BLOCKED_SCALE_LABEL_NOT_NORMALIZED | scale label remains candidate_not_normalized
- `domain_membership_promotion`: BLOCKED_DOMAIN_CERTIFICATE_PERMISSION_CLOSED | payload explicitly keeps domain_certificate permission closed
- `zero_control_dependency`: BLOCKED_ZERO_CONTROL_NOT_DEFINED | support rule correctly requires later zero-control over the same convention

## Status

```text
SEED_SUPPORT_DOMAIN_RULE_CANDIDATE_AUDITED_BLOCKED_NOT_CERTIFIED
```

The support-domain rule is now audited as a candidate, but certification is
blocked because the scale label is not normalized, domain-certificate
permission remains closed, and the zero-control object is not defined.

## Next Minimal Unblock

```text
tau_cmb_seed_normalization_replay_candidate_v01
```
