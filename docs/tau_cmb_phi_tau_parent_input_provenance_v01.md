# Tau CMB Phi Tau Parent Input Provenance v01

**Doc class:** parent-input provenance manifest scaffold
**Status:** provenance slots declared but unsatisfied; no parent inputs, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_provenance.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_provenance_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_provenance_summary_v01.csv
```

This artifact declares the parent-side input provenance slots required before
`Phi_tau_eff(a,k)` can be derived endpoint-blind.
It does not supply parent inputs. It does not derive `Phi_tau_eff`.

The endpoint firewall is explicit: acoustic residuals, lensing residuals, score
labels, and CMB likelihood errors cannot enter the parent-input packet.

The parent-input provenance is not satisfied:

```text
parent_input_provenance_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_candidate_manifest_v01
```

## Claim Boundary

This artifact declares provenance slots only. It supplies no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
