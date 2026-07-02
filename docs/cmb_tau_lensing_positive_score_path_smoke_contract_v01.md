# CMB Tau Lensing Positive Score Path Smoke Contract v01

**Doc class:** positive score-path smoke contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, synthetic plumbing check only
**Canonical parent:** `docs/cmb_tau_lensing_reduced_score_runner_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_positive_score_path_smoke_contract_v01.csv`

This contract adds a positive-path plumbing smoke test using a synthetic zero
grid. It proves that the validator, projection replay, reduced score runner, and
score-output validator can execute end to end once a valid replay exists.

It is not Tau evidence, not a physical Tau score, not a likelihood run, and not
a dark-sector verdict.

## Command

```text
make scoring-positive-smoke
```

## Claim Boundary

```text
positive_score_path_smoke_contract_synthetic_grid_only_no_tau_evidence_no_dark_sector_verdict
```
