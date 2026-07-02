# Tau CMB Score Input Unblock Plan v01

**Doc class:** scoring input unblock plan
**Status:** ranked plan declared; no scores computed, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_score_input_unblock_plan.py
```

Derived outputs:

```text
data/derived/tau_cmb_score_input_unblock_plan_v01.csv
data/derived/tau_cmb_score_input_unblock_plan_summary_v01.csv
```

This artifact ranks the blocked scorecard inputs. It does not compute CMB
scores. Its purpose is to prevent the project from branching into every
possible missing proof at once.

The ranked unblock order is:

```text
1. tau_cmb_known_limit_failure_map_v01 - known_limit_or_explicit_failure
2. tau_cmb_density_amplitude_derivation_v01 - omega_c_h2_density_inference
3. tau_cmb_acoustic_role_reduced_benchmark_v01 - acoustic_peak_phase_and_height
4. tau_cmb_lensing_transfer_benchmark_v01 - cmb_lensing_potential
5. tau_cmb_growth_transfer_kernel_v01 - growth_seed_and_transfer_consistency
6. tau_cmb_radiation_guard_bound_check_v01 - damping_tail_and_radiation_guard
```

The immediate next artifact is therefore:

```text
tau_cmb_known_limit_failure_map_v01
```

This is chosen first because it gives the whole scorecard a disciplined
reproduce/approximate/fail map before the paper attempts detailed numerical
or reduced-benchmark scoring.

## Claim Boundary

This artifact is a plan only. It computes no scores, supplies no CMB likelihood,
validates no Tau-response source, and permits no no-dark or dark-sector verdict.
