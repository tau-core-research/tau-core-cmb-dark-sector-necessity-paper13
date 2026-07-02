# CMB Tau Lensing Response Vector Candidate v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** candidate slot declaration, payload missing
**Canonical parent:** `docs/cmb_tau_lensing_response_vector_requirement_v01.md`

This candidate declares the minimal admissible slots for a future Tau Core
lensing response vector. It does not supply the vector.

## Candidate Forms

Two forms are admissible:

```text
tau_theory_lenspotential_PP_grid: shape (3000,)
```

or:

```text
delta_PP_tau: shape (3000,)
tau_PP_grid = PP_fiducial + delta_PP_tau
```

Both must be constructed from Tau Core theory-side material before any ACT
lensing score is used.

## Required Payload

A payload must include:

```text
values: 3000 numeric entries
units_or_dimensionless_convention
L_alignment
source_derivation
provenance_hash
firewall_statement
parameter_policy_reference
```

The source chain must be compatible with:

```text
Phi_tau_eff
-> T_tau_CMB
-> lensing-era potential response
-> tau_PP_grid or delta_PP_tau
```

## Firewall

The candidate must not be constructed from:

- ACT bandpower residuals;
- a previous Tau score;
- posterior tuning to minimize `chi2`;
- dark-sector verdict preference.

The adapter may later evaluate the supplied vector, but the vector must not be
derived from the evaluation target.

## Current Status

No Tau response payload is accepted. The candidate slots are declared only to
make the next work item exact.

```text
CANDIDATE_SLOT_DECLARED_PAYLOAD_MISSING
```

## Claim Boundary

```text
tau_response_candidate_slot_only_no_payload_no_tau_score_no_dark_sector_verdict
```

The concrete payload submission packet is tracked at:

```text
data/source_manifest/cmb_tau_lensing_response_payload_submission_packet_v01.csv
docs/cmb_tau_lensing_response_payload_submission_packet_v01.md
```
