# Tau CMB Growth Transfer Kernel v01

**Doc class:** transfer-kernel specification scaffold
**Status:** kernel requirements declared; no operator rule, no score, no likelihood, no verdict

Script:

```text
scripts/build_tau_cmb_growth_transfer_kernel.py
```

Derived outputs:

```text
data/derived/tau_cmb_growth_transfer_kernel_v01.csv
data/derived/tau_cmb_growth_transfer_kernel_summary_v01.csv
```

This artifact declares what a Tau CMB growth-transfer kernel must specify:

```text
domain
codomain
time/scale convention
operator rule
cross-role consistency
explicit failure branch
```

Every row remains:

```text
DECLARED_NOT_SPECIFIED
```

The artifact does not provide a transfer operator and does not compare against
growth, lensing, or structure data. It only prevents the project from treating
an unspecified propagation step as an available Tau response.

## Claim Boundary

This artifact declares transfer-kernel requirements only. It supplies no operator rule, evaluates no growth data, computes no score, supplies no CMB likelihood, validates no Tau-response source, and permits no no-dark or dark-sector verdict.
