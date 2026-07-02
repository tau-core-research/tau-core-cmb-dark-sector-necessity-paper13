# CMB Tau Lensing Adapter Convention Normalization Lock v01

**Doc class:** source-side adapter convention lock
**Reader role:** Paper 13 Tau-grid implementer
**Status:** package-unit convention candidate, not Tau-side normalization
**Canonical parent:** `docs/cmb_tau_lensing_endpoint_blind_normalization_gate_v01.md`

## Claim Boundary

```text
adapter_convention_lock_only_no_tau_normalization_no_score_no_dark_sector_verdict
```

## Lock

For the reduced local ACT lensing adapter, the source-side convention is:

```text
m_ACT = B_ACT @ PP_grid
N_PP_or_clkk_convention = 1
```

This means that no extra Tau-side amplitude is hidden in the adapter. The
adapter accepts a package-style `PP_grid` and uses the package binning matrix to
produce the 18-vector comparison object.

## Source-Side Scale Check

Using the ACT package fiduciary `PP` column over L=10..3009:

```text
PP min..max = 1.069900e-09 .. 1.430900e-07
B_ACT @ PP min..max = 2.476505e-09 .. 1.414775e-07
```

This is a package-unit sanity check. It is not a Tau amplitude derivation and
does not use a Tau model score.

## Consequence

After this convention lock, the remaining Tau-side normalization obligation is:

```text
N_tau_remaining = N_parent_source * N_projection
```

The next physical retry must derive those two factors before materialization.

The Tau-side obligation is decomposed at:

```text
docs/cmb_tau_lensing_tau_side_normalization_obligation_v01.md
data/derived/cmb_tau_lensing_tau_side_normalization_obligation_v01.json
```

## Non-Claims

```text
does not prove that CAMB/ACT PP is identical to a fundamental Tau readout variable
does not derive N_parent_source
does not derive N_projection
does not run a score
does not support a dark-sector verdict
```
