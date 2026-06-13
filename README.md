# Tau Core CMB Dark-Sector Necessity Paper 13

Private scaffold for Paper 13:

**CMB constraint mapping for dark-sector necessity in Tau Core**

This repository starts a narrow CMB-facing protocol for deciding what a Tau Core
cosmology must reproduce before any dark-sector necessity claim can be made.

## Main Claim

The paper defines a reproducible constraint map from CMB observables to Tau Core
requirements. It distinguishes three claim levels:

```text
TC0: no effective dark-sector response required
TC1: effective Tau base-field response required
TC2: standard CDM/Lambda-like benchmark still required
```

The first version does not fit CMB spectra. It identifies which CMB features
make a completely no-dark Tau Core cosmology difficult to defend, and which
features a Tau base-field response layer would have to reproduce.

## Does Not Claim

- It does not claim that Tau Core has explained the CMB.
- It does not claim that dark matter does not exist.
- It does not claim a physical Tau dark-sector field has been detected.
- It does not claim a Boltzmann solver, perturbation solver, or CMB likelihood.
- It does not claim Planck, ACT, SPT, BAO, lensing, or supernova validation.
- It does not claim a final dark-sector verdict.

## Included Data

Only compact source-backed manifests and derived protocol tables are included:

```text
data/source_manifest/cmb_external_reference_manifest_v01.csv
data/source_manifest/tau_core_cmb_decision_ladder_v01.csv
data/derived/cmb_constraint_map_v01.csv
data/derived/tau_core_dark_sector_requirement_map_v01.csv
data/derived/paper13_readiness_summary_v01.csv
```

## Reproduce

```bash
python scripts/reproduce.py
```

The reproduction script builds the compact derived tables, validates protocol
claim boundaries, compiles the manuscript when `tectonic` is available, builds
the arXiv source ZIP, and runs the public tests.

## Scope

Paper 13 is intentionally not a galaxy-rotation continuation of Paper 11. It
uses the CMB as a stronger global test of whether Tau Core can remain no-dark,
or whether a Tau base-field response/effective dark-sector layer is required.
