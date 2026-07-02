# Tau CMB Effective Source Equation v01

**Doc class:** equation-target scaffold
**Status:** target declared; no CMB source equation filled

Script:

```text
scripts/build_tau_cmb_effective_source_equation.py
```

Derived outputs:

```text
data/derived/tau_cmb_effective_source_equation_v01.csv
data/derived/tau_cmb_effective_source_equation_summary_v01.csv
```

This artifact converts the CMB constraint map into an equation-level target.
It does not solve the target.

The intended skeleton is:

```text
B_tau_base_CMB, delta_M_CMB, OI, ell, h
  -> Response_tau_CMB
  -> rho_tau_eff(a,k), Phi_tau_eff(a,k), T_tau_CMB(k,a)
  -> acoustic, lensing, damping, and growth role checks
```

The target is deliberately split into carrier, source, response-operator,
effective-density, effective-potential, transfer, radiation-guard, and
known-limit rows so that a future derivation cannot hide the standard CDM role
inside a fitted residual.

## Claim Boundary

This artifact declares required fields and dimensional roles only. It provides
no Boltzmann solver, no CMB likelihood, no fitted parameters, no Tau Core CMB
validation, no physical Tau dark-sector field, and no dark-sector verdict.
