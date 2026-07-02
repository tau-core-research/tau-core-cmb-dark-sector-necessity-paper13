# Tau Lensing Base-Field Route Prederivation Packet v01

**Doc class:** base-field route prederivation target
**Status:** ROUTE_02 selected as next derivation work route, not as a physical truth claim
**Canonical parent:** Paper 13 ACT/Planck lensing scoring route

This artifact takes the origin-route audit and chooses the seed-induced Tau
base-field response route as the next derivation target. This is not a
selection of the true physical route. It is a work-priority decision: the broad
low-\(L\) shape and independent amplitude burden are more naturally expressed
as a response operator than as a direct seed-only projection.

Target chain:

```text
M_seed + B_tau
-> M_tau = F_tau(M_seed, B_tau, constraints)
-> Phi_tau_eff = D_tau[M_tau; B_tau]
-> R_tau^kk(L) = Pi_lens[Phi_tau_eff](L)
-> A*S(L; L_c,p,q)
```

Candidate values to derive or reject:

```text
A=1e-07
L_c=120.0
p=0.5
q=1.0
```

Prederivation status:

```text
selected_next_work_route=ROUTE_02_BASE_FIELD
physical_tau_response_claim_allowed=False
dark_sector_verdict_allowed=False
acceptance_tests_total=5
acceptance_tests_open=5
```

## Claim Boundary

The packet only defines the next derivation target. It does not prove the Tau
base field, does not derive \(D_\tau\), does not derive \(\Pi_\mathrm{lens}\),
does not establish the amplitude, and does not decide dark-sector necessity.
