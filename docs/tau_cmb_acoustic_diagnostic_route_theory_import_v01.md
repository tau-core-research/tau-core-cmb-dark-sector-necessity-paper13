# Tau CMB Acoustic Diagnostic Route Theory Import v01

**Doc class:** Paper13 theory-import / acoustic diagnostic route update
**Reader role:** records the Tau Core theory import that turns the Planck PR3 acoustic chain into a bounded diagnostic pre-score route
**Status:** diagnostic route contract only; no Tau prediction values, no physical CMB score, no likelihood, no dark-sector verdict
**Canonical parent:** Paper 13 Planck PR3 peak observed-side input chain

## Purpose

This artifact imports the latest Tau Core theory-side CMB acoustic route into
Paper 13 without promoting it to an empirical result.

The imported theory status is:

```text
official Planck PR3 acoustic source vector
  -> deterministic binned O_CMB^peak extraction
  -> diagnostic pre-score policy
  -> endpoint-blind Tau-side prediction-vector spec Y_tau^ac
  -> score still blocked until Y_tau^ac is populated.
```

## Imported Source-Side Status

The observed side is now treated as source-frozen for the reduced acoustic
diagnostic route:

```text
Planck PR3 TT/TE/EE binned spectra selected
best-fit theory file retained as control only
artifact hashes recorded in the Tau Core theory repo
deterministic binned TT/TE/EE peak/extremum extraction declared
O_CMB^peak source-value candidate filled
```

This does not mean the full Planck likelihood is available. It means Paper 13
has a reproducible acoustic diagnostic target.

## Diagnostic Pre-Score Policy

The imported pre-score policy is:

```text
ACOUSTIC_DIAGNOSTIC_PRE_SCORE_INPUT_READY
```

Allowed use:

```text
debug a future Tau-side acoustic prediction vector against a frozen source
vector using a binned diagonal error envelope.
```

Forbidden use:

```text
physical CMB score
full Planck likelihood
Tau CMB validation
TC0 / TC1 / TC2 verdict
dark-sector necessity decision
```

The cross-role rule is explicit:

```text
an acoustic-only diagnostic pass may not be promoted to lensing, growth,
damping, or global dark-sector success.
```

## Tau-Side Prediction Vector Spec

The required Tau-side object is:

```text
Y_tau^ac =
  R_ac(P_CMB(D_tau[F_tau(M_seed^CMB, B_tau^base, C_CMB); B_tau^base])).
```

Paper 13 may compare against the frozen acoustic source vector only after an
endpoint-blind `Y_tau^ac` is supplied with:

```text
predicted TT peak positions
predicted TT relative heights
predicted TE signed phase extrema
predicted EE peak positions
predicted EE relative heights
predicted damping proxy
null and wrong-family controls
channel-map declaration
```

No component may be tuned to Planck peak residuals after the source vector is
frozen.

## Paper13 Status Update

```text
observed_acoustic_source_vector: READY_FOR_DIAGNOSTIC_USE
diagnostic_error_envelope: BINNED_DIAGONAL_ONLY
cross_role_fail_policy: DECLARED
tau_side_prediction_vector_spec: DECLARED
tau_side_prediction_values: UNFILLED
channel_map: UNFILLED
full_likelihood: UNFILLED
physical_score: NOT_READY
dark_sector_verdict: NOT_READY
next_required_artifact: tau_cmb_acoustic_tau_prediction_vector_population_or_explicit_fail_v01
```

## Claim Boundary

```text
tau_cmb_acoustic_diagnostic_route_theory_import_v01_imports_diagnostic_route_only_no_tau_prediction_values_no_physical_cmb_score_no_likelihood_no_dark_sector_verdict
```

This is a paper-level route update. It is not a Tau acoustic prediction, not a
CMB fit, not a likelihood result, and not a decision about whether a dark sector
is needed.
