# Tau CMB Phi Tau Parent Input Concrete Payload Requirements v01

**Doc class:** concrete parent-input payload requirements
**Status:** requirements declared but unsatisfied; no concrete payload, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_concrete_payload_requirements.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_requirements_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_requirements_summary_v01.csv
```

This artifact declares the concrete parent-side payload requirements needed
before the payload-level firewall can pass.
It does not supply concrete parent-input values. It does not derive `Phi_tau_eff`.

The concrete payload requirements are not satisfied:

```text
concrete_payload_requirements_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01
```

## Claim Boundary

This artifact declares concrete payload requirements only. It supplies no
concrete parent-side Tau values, provides no payload-level firewall pass,
accepts no parent-side Tau inputs, derives no `Phi_tau_eff`, computes no score,
supplies no CMB likelihood, declares no reproduction or failure, validates no
Tau-response source, and permits no no-dark or dark-sector verdict.
