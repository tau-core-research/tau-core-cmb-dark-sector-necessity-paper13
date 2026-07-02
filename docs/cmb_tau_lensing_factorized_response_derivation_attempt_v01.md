# Tau Lensing Factorized Response Derivation Attempt v01

**Doc class:** formula-level factorized derivation attempt
**Status:** candidate lensing kernel split into seed activation, base-field screening, readout normalization, and amplitude slots
**Canonical parent:** Paper 13 ACT/Planck lensing scoring route

This artifact factors the current base-field lensing ansatz into smaller
derivation targets. It does not derive the factors from Tau Core. It records a
minimal decomposition that a later Tau-side proof must justify or reject.

Candidate response:

```text
R_tau^kk(L) = A * K_lens(L)
x = L/L_c
K_lens(L) = x^p / (1 + x^(p+q)) / N
N = max_x[x^p/(1+x^(p+q))]
```

Factorized route:

```text
seed activation:        x^p
base-field screening:  1/(1+x^(p+q))
readout normalization: 1/N
amplitude slot:        A
```

Candidate values:

```text
A=1e-07
L_c=120.0
p=0.5
q=1.0
```

Formula-level status:

```text
factors_total=5
formula_factorization_exact=True
open_tau_side_factor_derivations=4
physical_tau_response_claim_allowed=False
```

## Claim Boundary

This is only a factorization of the diagnostic kernel. It does not prove that
the Tau seed produces \(x^p\), that the Tau base field produces
\(1/(1+x^{p+q})\), that the readout normalization is physically fixed, or
that the amplitude \(A\) follows from Tau normalization.
