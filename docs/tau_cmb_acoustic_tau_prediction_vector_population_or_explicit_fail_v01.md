# Tau CMB Acoustic Tau Prediction Vector Population Or Explicit Fail v01

**Doc class:** Tau-side acoustic prediction-vector population decision
**Reader role:** closes the first Paper13 acoustic diagnostic route attempt after the `Y_tau^ac` spec
**Status:** explicit fail; no endpoint-blind Tau acoustic prediction vector values supplied; acoustic diagnostic score not run
**Canonical parent:** [`tau_cmb_acoustic_diagnostic_route_theory_import_v01.md`](tau_cmb_acoustic_diagnostic_route_theory_import_v01.md)

## Purpose

The previous theory import made the acoustic diagnostic route finite:

```text
frozen Planck PR3 O_CMB^peak source vector
  -> diagnostic pre-score policy
  -> required endpoint-blind Tau-side prediction vector Y_tau^ac.
```

This artifact answers the next focused question:

```text
Can Paper 13 currently populate Y_tau^ac without endpoint leakage?
```

The answer in v01 is no. The route fails explicitly at Tau-side population, not
at the observed Planck source side.

## Required Vector

The required object is:

```text
Y_tau^ac =
  (
    theta_peak_tau,
    P_pos_tau,
    P_height_tau,
    P_phase_tau,
    P_damp_tau,
    E_peak_tau
  ).
```

It must be derived through an endpoint-blind route:

```text
B_tau^base, M_seed^CMB, C_CMB
  -> F_tau
  -> D_tau
  -> P_CMB
  -> R_ac
  -> Y_tau^ac.
```

## Population Decision

```text
tau_side_prediction_vector_spec_declared = true
tau_side_prediction_values_supplied = false
endpoint_blind_derivation_trace_supplied = false
channel_map_supplied = false
null_control_supplied = false
wrong_family_control_supplied = false
diagnostic_score_allowed = false
diagnostic_score_run = false
```

Therefore:

```text
Y_TAU_AC_POPULATION_EXPLICIT_FAIL
```

## Failure Reasons

| Required field | Status | Reason |
| --- | --- | --- |
| `theta_peak_tau` | missing | no endpoint-blind Tau first-peak prediction |
| `P_pos_tau` | missing | no TT/EE peak-position prediction sequence |
| `P_height_tau` | missing | no normalized TT/EE peak-height prediction sequence |
| `P_phase_tau` | missing | no signed TE phase-extremum prediction sequence |
| `P_damp_tau` | missing | no Tau damping proxy compatible with the diagnostic source vector |
| `E_peak_tau` | missing | no EE peak-survival/readout prediction |
| channel map | missing | no accepted TT/TE/EE Tau response routing |
| null control | missing | no accepted null acoustic prediction vector |
| wrong-family control | missing | no accepted wrong-family acoustic control vector |

## Consequence

Allowed conclusion:

```text
The observed Planck PR3 acoustic source vector and diagnostic policy are ready,
but Paper 13 currently lacks the endpoint-blind Tau-side prediction vector
needed to run the acoustic diagnostic score.
```

Forbidden conclusions:

```text
Tau Core fails the CMB;
Tau Core matches the acoustic peaks;
dark sector is required;
dark sector is not required;
TC0/TC1/TC2 is decided;
Planck likelihood has been evaluated.
```

## Next Artifact

The next honest artifact is:

```text
tau_cmb_acoustic_operator_population_work_order_v01
```

It must fill, or explicitly fail, the upstream pieces that could produce
`Y_tau^ac`:

```text
Phi_tau,eff acoustic input
A_tau activation/amplitude input
oscillator/kernel rule
baryon-loading coupling
projection-to-peak map
uncertainty/null policy
TT/TE/EE channel map
```

## Machine Summary

The compact machine-readable summary is:

```text
data/derived/tau_cmb_acoustic_tau_prediction_vector_population_or_explicit_fail_summary_v01.csv
```

## Claim Boundary

```text
tau_cmb_acoustic_tau_prediction_vector_population_or_explicit_fail_v01_explicit_tau_side_population_fail_no_acoustic_score_no_likelihood_no_dark_sector_verdict
```

This artifact is an explicit failure to populate the Tau-side acoustic
prediction vector. It is not a physical CMB failure, not a Tau Core falsification,
not a CMB likelihood, and not a dark-sector decision.
