# CMB Tau Lensing Response Vector Requirement v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** Tau response requirement gate, not a score
**Canonical parent:** `docs/cmb_lensing_reduced_score_adapter_contract_v01.md`

This gate states exactly what must exist before the ACT DR6 reduced lensing
adapter may produce a Tau Core diagnostic score.

## Required Object

At least one of these must be supplied before scoring:

```text
tau_theory_lenspotential_PP_grid: shape (3000,)
```

or:

```text
delta_PP_tau: shape (3000,)
tau_PP_grid = PP_fiducial + delta_PP_tau
```

The grid must be defined before the ACT bandpower residual is used. It cannot
be fitted after looking at the residual unless the fitting parameterization and
priors were declared in advance.

## Source Requirement

The Tau response vector must come from Tau Core theory-side material, for
example:

```text
Phi_tau_eff
-> T_tau_CMB
-> lensing-era potential response
-> tau_PP_grid or delta_PP_tau
```

It is not enough to choose a shape that improves the ACT residual.

## Parameter Policy

For a Tau score, no free post-hoc scale is allowed. Any amplitude, tilt, phase,
smoothing, or morphology parameter must be recorded before scoring with:

```text
parameter_name
fixed_or_free
prior_or_allowed_range
source_derivation
units_or_dimension_status
```

Otherwise the adapter would test fitting freedom, not Tau Core content.

## Minimal Acceptance Tests

Before a score attempt, the candidate must pass:

- shape `(3000,)`;
- finite numeric values;
- declared units or dimensionless convention;
- declared alignment with `B_ACT`;
- projected vector shape `(18,)`;
- no data-derived post-hoc tuning unless explicitly modeled as a parameter;
- claim boundary stating reduced diagnostic only.

## Still Blocked

No Tau response vector is currently accepted. The adapter sanity check exists,
but Tau Core has not yet supplied the theory object needed for a Tau score.

## Claim Boundary

```text
tau_response_requirement_only_no_tau_score_no_dark_sector_verdict
```

The candidate slot declaration is tracked at:

```text
data/source_manifest/cmb_tau_lensing_response_vector_candidate_v01.csv
docs/cmb_tau_lensing_response_vector_candidate_v01.md
```
