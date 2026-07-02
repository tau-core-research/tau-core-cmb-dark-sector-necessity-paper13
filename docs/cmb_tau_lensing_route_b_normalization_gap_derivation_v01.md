# CMB Tau Lensing Route B Normalization Gap Derivation v01

**Doc class:** data-frontier diagnostic derivation
**Reader role:** Paper 13 Tau-grid implementer
**Status:** algebraic normalization-gap derivation, not physical Tau normalization
**Canonical parent:** `docs/cmb_lensing_reduced_score_adapter_contract_v01.md`

## Claim Boundary

```text
normalization_gap_derivation_diagnostic_only_not_endpoint_blind_no_dark_sector_verdict
```

This note derives the algebraic scale implied by the current reduced ACT
lensing adapter. It does not derive a Tau Core physical amplitude and it does
not support a dark-sector verdict.

## Locked Algebra

Let

```text
y = ACT DR6 clkk bandpower vector
C = ACT covariance
s = current Route B unit-normalized Tau-side grid
B = ACT binning matrix
m = B s
```

For a single global diagnostic scale, the covariance-weighted least-squares
solution is

```text
alpha_* = (m^T C^-1 y) / (m^T C^-1 m)
chi2(alpha_*) = (y - alpha_* m)^T C^-1 (y - alpha_* m)
```

This is an adapter diagnostic. Because `alpha_*` is computed after inspecting
the endpoint bandpowers, it is not endpoint-blind.

## Numerical Result

For the current Route B payload:

```text
alpha_* = 1.02522734044147962e-08
unscaled chi2 = 8.56114198481747840e+17
scaled chi2 = 2.03913332504383607e+03
scaled chi2 / 18 = 1.13285184724657555e+02
```

The active Tau grid has unit-shape scale:

```text
grid min..max = 9.999793e-03 .. 9.435402e-01
B @ grid min..max = 2.449672e-02 .. 9.411380e-01
```

The ACT bandpowers live at lensing amplitude scale:

```text
ACT clkk min..max = 2.737565e-09 .. 2.429987e-07
```

So the `~1e-8` factor is not mysterious: it is the amplitude conversion needed
to turn the present unit-normalized Route B shape into the ACT lensing
bandpower scale.

## Fiducial PP Context

The ACT source package also contains a fiducial lensing-potential table with a
`PP` column. In the same L=10..3009 range:

```text
fiducial PP min..max = 1.069900e-09 .. 1.430900e-07
B @ fiducial PP min..max = 2.476505e-09 .. 1.414775e-07
median(fiducial PP / Tau unit shape) = 3.79483539767772587e-09
median(B @ fiducial PP / B @ Tau unit shape) = 5.94143103063187498e-08
```

This shows the same order-of-magnitude gap from an independent source-side
reference in the ACT package. It still does not prove the Tau amplitude.

## What Remains To Derive

To turn this into an admissible endpoint-blind Tau score, the next payload must
derive and predeclare a normalization rule before scoring:

```text
N_tau = N_parent_source * N_projection * N_PP_or_clkk_convention
tau_grid(L) = N_tau * shape_tau(L)
```

Allowed promotion requires:

```text
Tau-side normalization derived before endpoint residual inspection
PP/clkk convention locked as an adapter rule
formula spec updated before materialization
new payload generated from the predeclared rule
new score run without post-score scale fitting
```
