# Tau CMB Phi Tau Parent Input Payload Stub v01

**Doc class:** parent-input payload stub
**Status:** payload schema declared but concrete values absent; no firewall pass, no accepted inputs, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_payload_stub.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_payload_stub_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_payload_stub_summary_v01.csv
```

This artifact declares a minimal payload-stub schema for the parent-input
candidate manifest. It does not supply concrete parent-input values. It does
not pass the endpoint firewall. It does not derive `Phi_tau_eff`.

The payload stub is not satisfied:

```text
payload_stub_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_firewall_execution_v01
```

## Claim Boundary

This artifact declares payload schema only. It supplies no concrete parent-side
Tau values, provides no payload-level firewall pass, accepts no parent-side Tau
inputs, derives no `Phi_tau_eff`, computes no score, supplies no CMB likelihood,
declares no reproduction or failure, validates no Tau-response source, and
permits no no-dark or dark-sector verdict.
