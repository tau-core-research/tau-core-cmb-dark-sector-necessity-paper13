# Tau CMB Phi Tau Parent Real Payload Import Precheck v01

**Doc class:** real payload import precheck
**Status:** executable import precheck declared; real payloads missing

This artifact checks whether the expected score-ready payload files exist under
`data/score_ready_input/`, whether they are readable and nonempty, whether a
hash can be bound, and whether their schema matches the template manifest. In
the current repository package no real payload files are present.

Summary:

```text
template_bindings_consumed=49
import_precheck_rows_declared=49
real_payload_paths_expected=49
real_payload_paths_present=0
real_payload_paths_missing=49
payload_hash_bound_rows=0
payload_import_accepted_rows=0
scoring_input_accepted_rows=0
score_attempt_blocked_now_rows=49
```

## Claim Boundary

This artifact is an import precheck only. It imports no real Tau-side CMB
payload, binds no payload hash, accepts no slot, accepts no scoring input,
derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood, and
permits no no-dark or dark-sector verdict.
