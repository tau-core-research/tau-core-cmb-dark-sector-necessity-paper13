# CMB Tau Lensing Physical Candidate Upstream Agent Prompt v01

**Doc class:** upstream agent prompt
**Status:** prompt only; no grid, no score, no verdict
**Canonical parent:** `docs/cmb_tau_lensing_physical_candidate_upstream_request_v01.md`

You are helping produce the upstream Tau-derived table needed for a Paper 13
CMB lensing Tau-grid candidate. Do not use endpoint residuals, reduced chi2,
score outputs, or dark-sector verdict preferences.

## Goal

Produce two files:

```text
payload_staging/tau_lensing_upstream_l_response_v01.csv
payload_staging/tau_lensing_upstream_l_response_metadata_v01.json
```

The CSV must have exactly 3000 rows:

```text
L,tau_response_value
10,<finite value>
...
3009,<finite value>
```

The values must be a Tau-derived endpoint-blind `delta_PP_tau(L)` or `tau_PP(L)`
response, not a diagnostic probe and not a zero-control.

## Allowed Routes

Route A, preferred:

```text
rho_tau_eff(a,k) = A_tau(a,k) * rho_ref(a)
k^2 Phi_tau_eff(a,k) = 4*pi*G*a^2*rho_tau_eff(a,k)*Delta_tau(a,k)
Phi_lens_tau(a,k) = T_tau_CMB(k,a)[Phi_tau_eff]
tau_PP(L) = Projection_PP[Phi_lens_tau](L)
```

Route B, allowed only if Tau-derived before endpoint scoring:

```text
delta_PP_tau(L) = F_tau_L(parent_tau_source, readout_profile, scale_profile; L)
```

## Metadata Requirements

The JSON metadata must include:

```text
selected_route
l_column
value_column
formula_role
endpoint_blind_statement
parameter_policy
source_chain
normalization_statement
known_limit_statement
derivation_script_or_formula
claim_boundary
```

The metadata must explain:

- what Tau-side parent source fixes the response;
- how parameters are fixed without endpoint fitting;
- the normalization and sign convention;
- the known zero/null/LCDM comparison limit;
- the replayable formula or script command that regenerates the table.

## Forbidden

Do not use:

- ACT residuals;
- Planck residuals;
- reduced chi2 tuning;
- score output tuning;
- dark-sector verdict preference;
- diagnostic probe parameters;
- zero-control definitions promoted as physical response;
- placeholder `FILL` fields.

## Acceptance Commands

After writing the files, the repo-side validator must pass:

```text
make tau-grid-physical-candidate-precheck
make tau-grid-handoff-write-staging
make tau-grid-physical-candidate-package
make staging-promote-delta-dry-run
```

If the derivation cannot supply the table honestly, report the missing object
instead of inventing a shape.

## Claim Boundary

```text
physical_candidate_upstream_agent_prompt_only_no_grid_no_score_no_dark_sector_verdict
```
