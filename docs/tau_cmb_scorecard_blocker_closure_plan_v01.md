# Tau CMB Scorecard Blocker Closure Plan v01

**Doc class:** scorecard blocker closure plan
**Status:** closure plan declared; no closures completed, no scores, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_scorecard_blocker_closure_plan.py
```

Derived outputs:

```text
data/derived/tau_cmb_scorecard_blocker_closure_plan_v01.csv
data/derived/tau_cmb_scorecard_blocker_closure_plan_summary_v01.csv
```

This artifact turns the readiness audit into a closure plan. The ranked closure
order is:

```text
1. tau_cmb_density_amplitude_closure_v01 - omega_c_h2_density_inference
2. tau_cmb_acoustic_reduced_evaluation_v01 - acoustic_peak_phase_and_height
3. tau_cmb_lensing_transfer_reduced_evaluation_v01 - cmb_lensing_potential
4. tau_cmb_growth_transfer_kernel_closure_v01 - growth_seed_and_transfer_consistency
5. tau_cmb_radiation_guard_evaluation_v01 - damping_tail_and_radiation_guard
6. tau_cmb_known_limit_decision_update_v01 - known_limit_or_explicit_failure
```

Each row has a closure criterion and a stop rule. The purpose is to prevent the
scorecard from expanding into unrelated proof work before the named blockers
are closed or explicitly failed.

The immediate next artifact is:

```text
tau_cmb_density_amplitude_closure_v01
```

## Claim Boundary

This artifact is a closure plan only. It completes no closure, computes no
score, supplies no CMB likelihood, validates no Tau-response source, and permits
no no-dark or dark-sector verdict.
