# Tau CMB Single-Pass Derivation Spine v01

**Doc class:** single-pass derivation route spine
**Reader role:** Paper 13 / scoring-readiness reviewer
**Status:** SINGLE_PASS_DERIVATION_SPINE_DECLARED_ROUTE_BLOCKED_NOT_SCORE_READY
**Canonical parent:** `paper13_submission_source/main.tex`

## Claim Boundary

```text
tau_cmb_single_pass_derivation_spine_v01_route_spine_only_not_a_proof_no_concrete_R_CMB_no_score_no_likelihood_no_dark_sector_verdict
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

- `TCMBSPDS01_001` `seed_and_root_context`: CANDIDATE_CONTEXT / SEED_CONTEXT_DECLARED_NOT_ACCEPTED | `m_tau^seed, CMB readout context` | promote by: accepted seed descriptor, activation rule, quotient survival, and endpoint firewall
- `TCMBSPDS01_002` `carrier`: PREDICATE_CANDIDATE / CARRIER_PREDICATE_DECLARED_NOT_PROVED | `C_CMB^seed` | promote by: proof or executable checker for WellFormedRoleRepresentative_CMB
- `TCMBSPDS01_003` `domain`: PREDICATE_CANDIDATE / DOMAIN_RULE_DECLARED_NOT_CERTIFIED | `Dom(R_CMB)` | promote by: joint support-domain, normalization, evidence-payload, null-control, and firewall certificate
- `TCMBSPDS01_004` `concrete_readout`: REQUIRED_OBJECT_NOT_MATERIALIZED / CONCRETE_R_CMB_BLOCKED | `R_CMB: Dom(R_CMB) -> V_CMB^roles` | promote by: materialized map, codomain convention, dimension/gauge replay, and endpoint firewall rerun
- `TCMBSPDS01_005` `effective_source`: CONDITIONAL_ROLE_FORMULA / SOURCE_OBJECT_NOT_ACCEPTED | `rho_tau_eff(a,k) := A_tau(a,k) rho_ref(a)` | promote by: endpoint-blind A_tau/rho_tau_eff derivation plus normalization replay
- `TCMBSPDS01_006` `potential_constraint`: COMPARISON_SLOT_NOT_FIELD_EQUATION / PHI_TAU_EFF_NOT_DERIVED | `k^2 Phi_tau_eff = 4 pi G a^2 rho_tau_eff Delta_tau` | promote by: Tau-side perturbation equation, Delta_tau definition, known-limit and dimensional proof
- `TCMBSPDS01_007` `transfer`: TRANSFER_OPERATOR_REQUIRED / T_TAU_CMB_NOT_MATERIALIZED | `Phi_lens_tau = T_tau_CMB[Phi_tau_eff]` | promote by: analytic or executable T_tau_CMB with support, units, gauge convention, and zero-source behavior
- `TCMBSPDS01_008` `projection`: FORMULA_SCAFFOLD_NOT_ACCEPTED / KERNEL_MEASURE_NORMALIZATION_BLOCKED | `tau_PP(L) = N_proj int K_tau_PP Phi_lens_tau dmu` | promote by: K_tau_PP, dmu, N_projection_physical, codomain units, and zero-source proof
- `TCMBSPDS01_009` `role_bundle`: AUDITED_BUNDLE_BLOCKED / ROLE_BUNDLE_AUDITED_NOT_SCORE_READY | `acoustic, density, lensing, growth, radiation, null roles` | promote by: cross-role consistency matrix, role-specific numeric guards, and quotient survival proof
- `TCMBSPDS01_010` `firewall_and_provenance`: PROTOCOL_REQUIREMENT / FIREWALL_DECLARED_NOT_REPLAYABLE_OVER_ABSENT_VALUES | `endpoint-blind provenance path` | promote by: post-population endpoint firewall replay over concrete values
- `TCMBSPDS01_011` `scoring`: SCORING_GATE_CLOSED / NO_SCORE_ENTRY | `CMB role score / likelihood comparison` | promote by: all upstream blockers closed plus fixed scoring rubric, covariance/readout convention, and stale-output guard
- `TCMBSPDS01_012` `verdict`: VERDICT_FORBIDDEN / NO_DARK_SECTOR_VERDICT | `dark-sector necessity decision` | promote by: accepted score outputs, controls, uncertainty accounting, and reviewer-safe decision rule

## Input Chain

- `cosmology_spine`: DERIVATION_SPINE_DECLARED_PARTIAL_NOT_SCORE_ELIGIBLE
- `source_grounding`: SOURCE_GROUNDING_GATE_DECLARED_BLOCKED
- `bundle_closure_audit`: READOUT_ROLE_COORDINATE_BUNDLE_CLOSURE_AUDITED_BLOCKED_NOT_SCORE_READY
- `scoring_gap_matrix`: SCORING_INPUT_GAP_MATRIX_DECLARED_ALL_ROWS_BLOCKED_NO_SCORE
- `carrier_certificate_audit`: CONCRETE_R_CMB_CARRIER_CERTIFICATE_REQUIREMENTS_AUDITED_BLOCKED
- `carrier_domain_predicate_audit`: CARRIER_DOMAIN_PREDICATE_CANDIDATE_AUDITED_BLOCKED_NOT_SCORE_READY

## Status

```text
SINGLE_PASS_DERIVATION_SPINE_DECLARED_ROUTE_BLOCKED_NOT_SCORE_READY
```

The route can be viewed in one pass, but the route is still blocked. No concrete
`R_CMB`, no score entry, no likelihood, and no dark-sector verdict are opened.

## Next Minimal Unblock

```text
tau_cmb_carrier_domain_certificate_requirements_v01
```
