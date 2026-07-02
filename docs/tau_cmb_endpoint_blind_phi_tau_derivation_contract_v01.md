# Tau CMB Endpoint-Blind Phi Tau Derivation Contract v01

**Doc class:** endpoint-blind source-derivation contract
**Status:** contract declared but unsatisfied; no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_endpoint_blind_phi_tau_derivation_contract.py
```

Derived outputs:

```text
data/derived/tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.csv
data/derived/tau_cmb_endpoint_blind_phi_tau_derivation_contract_summary_v01.csv
```

This artifact declares the minimum endpoint-blind derivation contract for:

```text
Phi_tau_eff(a,k)
```

It does not derive `Phi_tau_eff`. Instead, it states what must be true before
the source may enter acoustic, lensing, growth, or radiation scoring. CMB
endpoint residuals, likelihood residuals, and role-score labels are excluded
from the construction path.

The endpoint-blind contract is not satisfied:

```text
endpoint_blind_contract_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_provenance_v01
```

## Claim Boundary

This artifact is a derivation contract only. It derives no `Phi_tau_eff`,
computes no score, supplies no CMB likelihood, declares no reproduction or
failure, validates no Tau-response source, and permits no no-dark or
dark-sector verdict.
