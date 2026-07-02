# Tau CMB Phi Tau Parent Input Concrete Payload Candidate v01

**Doc class:** concrete parent-input payload candidate
**Status:** candidate payload declared but unaccepted; no payload firewall pass, no Phi derivation, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_phi_tau_parent_input_concrete_payload_candidate.py
```

Derived outputs:

```text
data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_candidate_v01.csv
data/derived/tau_cmb_phi_tau_parent_input_concrete_payload_candidate_summary_v01.csv
```

This artifact declares a concrete payload candidate package for the parent-side
Tau inputs. It does not accept any candidate payload. It does not pass the
payload-level endpoint firewall. It does not derive `Phi_tau_eff`.

The concrete payload candidate is not satisfied:

```text
concrete_payload_candidate_satisfied=false
```

The next focused artifact is:

```text
tau_cmb_phi_tau_parent_input_payload_firewall_audit_v01
```

## Claim Boundary

This artifact declares candidate parent-side payload rows only. It accepts no
parent-side Tau inputs, provides no payload-level firewall pass, derives no
`Phi_tau_eff`, computes no score, supplies no CMB likelihood, declares no
reproduction or failure, validates no Tau-response source, and permits no
no-dark or dark-sector verdict.
