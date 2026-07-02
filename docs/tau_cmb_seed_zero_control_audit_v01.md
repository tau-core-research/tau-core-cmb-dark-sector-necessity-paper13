# Tau CMB Seed Zero Control Audit v01

**Doc class:** zero-control audit
**Status:** SEED_ZERO_CONTROL_AUDITED_BLOCKED_NOT_ACCEPTED

## Claim Boundary

```text
tau_cmb_seed_zero_control_audit_v01_audit_only_zero_control_not_accepted_no_physical_response_no_domain_certificate_no_readout_no_score_no_verdict
```

## Purpose

This audit checks whether the zero-control candidate is a same-convention,
inactive, null-readout control object and whether physical/scoring promotion is
forbidden. It does not accept zero-control, certify domain membership, evaluate
readout survival, assign `A_tau(a,k)`, enter scoring, or decide the dark-sector
question.

## Audit Rows

- `zero_table_shape`: PASS_ZERO_ROWS_PRESENT | components=['null_seed_definition', 'same_domain_convention', 'inactive_activation', 'null_readout_role', 'forbidden_promotion', 'quotient_survival_dependency']
- `null_seed_tuple`: PASS_NULL_SEED_TUPLE_DECLARED | null seed uses null morphology, CMB readout sector, and canonical scale
- `normalization_dependency`: PASS_NORMALIZATION_AUDITED_AS_CANDIDATE | normalization replay audit has zero failures and remains non-accepted
- `inactive_activation`: PASS_INACTIVE_ACTIVATION_DECLARED | null seed activation is declared zero or inactive
- `null_readout_role`: PASS_NULL_READOUT_DECLARED | null seed readout role is declared as null_readout
- `forbidden_promotion`: PASS_PROMOTION_FORBIDDEN | zero-control cannot be promoted to physical response, dark-sector claim, or score input
- `quotient_survival_dependency`: BLOCKED_QUOTIENT_RELATION_NOT_DEFINED | zero-control supplies null side, but concrete R_CMB and equivalence relation are missing
- `zero_control_acceptance`: BLOCKED_ZERO_CONTROL_ACCEPTANCE_CLOSED | zero-control candidate keeps acceptance permissions closed

## Status

```text
SEED_ZERO_CONTROL_AUDITED_BLOCKED_NOT_ACCEPTED
```

The zero-control side is now audited as a candidate. Acceptance remains closed
because quotient survival still needs concrete `R_CMB`, an equivalence relation,
and a separate pre-acceptance gate.

## Next Minimal Unblock

```text
tau_cmb_seed_chain_pre_acceptance_gate_v01
```
