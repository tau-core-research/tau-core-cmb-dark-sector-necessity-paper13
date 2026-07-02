# Tau CMB Concrete R_CMB Candidate Gate v01

**Doc class:** concrete readout candidate gate
**Reader role:** Paper 13 / CMB readout route implementer
**Status:** CONCRETE_R_CMB_STRUCTURAL_CANDIDATE_GATE_DECLARED_NOT_PHYSICAL
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
tau_cmb_concrete_R_CMB_candidate_gate_v01_structural_candidate_shell_only_not_physical_R_CMB_no_codomain_pass_no_checker_execution_no_score_no_likelihood_no_verdict
```

## Purpose

This artifact declares a structural `R_CMB` candidate shell for codomain
prechecking. It is not a physical or numerical CMB readout. It does not certify
the carrier/domain, pass the codomain checker, execute checkers, materialize
physical `R_CMB`, open score entry, compute a likelihood, or decide the
dark-sector question.

## Candidate Rows

- `readout_signature`: PASS_STRUCTURAL_SIGNATURE_DECLARED | formal R_CMB candidate signature is declared without numeric values
- `role_vector_slots`: PASS_ROLE_VECTOR_SLOTS_ENUMERATED | e_acoustic, e_density, e_lensing, e_growth, e_radiation, e_null
- `carrier_domain_certification`: BLOCKED_CARRIER_DOMAIN_NOT_CERTIFIED | carrier/domain certificate requirements remain blocked
- `physical_materialization`: BLOCKED_PHYSICAL_R_CMB_NOT_MATERIALIZED | candidate shell has no physical/numeric readout values
- `promotion_firewall`: PASS_NO_SCORE_OR_VERDICT_OPENED | score, likelihood, and dark-sector verdict remain closed

## Status

```text
CONCRETE_R_CMB_STRUCTURAL_CANDIDATE_GATE_DECLARED_NOT_PHYSICAL
```

The gate gives the codomain route a structural readout target, while preserving
the physical materialization and carrier/domain certification blockers.

## Next Minimal Unblock

```text
tau_cmb_concrete_R_CMB_candidate_gate_audit_v01
```
