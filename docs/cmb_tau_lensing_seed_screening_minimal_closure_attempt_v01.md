# Tau Lensing Seed-Screening Minimal Closure Attempt v01

**Doc class:** conditional formula-closure attempt
**Status:** seed activation and base-field screening are conditionally closed at formula level
**Canonical parent:** Paper 13 ACT/Planck lensing route

This artifact takes the factorized response kernel and asks whether the two
central shape factors can be expressed as a minimal interaction between an
initial morphological seed condition and the Tau base-field response medium.

It does not prove the physical Tau response. It records a conditional closure:
if the initial seed condition is read through an admissible response coordinate,
and if the Tau base field supplies a saturating screening transfer, then the
two factors of the current diagnostic kernel follow. The seed is not the whole
source; it is the initial morphology/constraint state that co-determines the
later response together with the base-field properties.

Conditional route:

```text
x = L/L_c
M_seed = initial morphological/constraint state
B_tau  = Tau base-field response medium
M_tau  = F_tau(M_seed, B_tau, constraints)
seed-conditioned activation:       alpha(M_tau,B_tau;x) = x^0.5
base-field screening transfer:     S_B(M_tau,B_tau;x) = 1/(1+x^1.5)
conditional response shape:        alpha(M_tau,B_tau;x) * S_B(M_tau,B_tau;x)
```

Inverse-constraint reading:

```text
source-frozen morphology/readout evidence
+ 4D residual/readout behavior
+ null, gauge, and wrong-family controls
-> compatible B_tau response-family candidates.
```

This is not an identification of the Tau base field. It says only that
morphology and 4D readout data can constrain which base-field response families
remain viable.

Formula-level status:

```text
assumptions_total=4
conditional_factor_closures=2
unconditional_tau_derivations=0
reconstructs_factorized_kernel=True
score_readiness_unlocked=False
```

## Claim Boundary

This artifact is useful but deliberately limited. It turns two open factors
into explicit conditional assumptions about seed--base-field co-determination.
It does not derive \(p=0.5\), \(p+q=1.5\), \(L_c=120\), or \(A=10^-7\)
from Tau Core, and it does not decide whether a dark-sector-like Tau
base-field response is physically required.
