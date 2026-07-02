# Tau Lensing Base-Field Operator Ansatz Packet v01

**Doc class:** operator ansatz and mathematical compatibility audit
**Status:** candidate broad low-L kernel materialized as a base-field response ansatz; Tau-side derivation still open
**Canonical parent:** Paper 13 ACT/Planck lensing scoring route

This artifact turns the selected base-field work route into a concrete
operator ansatz. It does not derive the ansatz from Tau Core. It only verifies
that the candidate kernel has the mathematical properties required of the next
Tau-side derivation target.

Minimal ansatz:

```text
M_tau = F_tau(M_seed, B_tau, constraints)
Phi_tau_eff = D_tau[M_tau; B_tau]
R_tau^kk(L) = A * K_lens(L)
K_lens(L) = x^p / (1+x^(p+q)) / max_x[x^p/(1+x^(p+q))]
x = L/L_c
```

Candidate values:

```text
A=1e-07
L_c=120.0
p=0.5
q=1.0
```

Compatibility audit:

```text
properties_total=6
properties_pass_formula_level=5
open_physical_derivation_gaps=4
shape_ansatz_materialized=True
physical_tau_response_claim_allowed=False
```

Formula-level result: the kernel is dimensionless, normalized, has low-\(L\)
activation exponent \(p\), high-\(L\) suppression exponent \(q\), and preserves
the zero-response limit through \(A=0\). The open problem is still to derive
\(D_\tau\), \(\Pi_\mathrm{lens}\), \(L_c,p,q\), and \(A\) from Tau-side
structure without endpoint selection.
