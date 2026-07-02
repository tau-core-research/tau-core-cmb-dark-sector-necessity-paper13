# CMB Tau Lensing Response Payload Submission Packet v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** payload submission packet, payload not submitted
**Canonical parent:** `docs/cmb_tau_lensing_response_vector_candidate_v01.md`

This packet defines the concrete files required before a Tau lensing response
vector can be audited.

## Required Payload Files

At least one numeric response file is required:

```text
tau_lensing_response_pp_grid_v01.csv
```

or:

```text
tau_lensing_response_delta_pp_v01.csv
```

The numeric file must contain exactly 3000 finite values and enough alignment
metadata to project with `B_ACT`.

The supporting files are also required:

```text
tau_lensing_response_parameter_policy_v01.csv
tau_lensing_response_payload_provenance_v01.json
tau_lensing_response_payload_hashes_v01.json
tau_lensing_response_firewall_v01.md
tau_lensing_response_claim_boundary_v01.md
```

## Acceptance Checks

A payload cannot proceed to Tau scoring unless:

- the numeric vector has shape `(3000,)`;
- all values are finite;
- units or dimensionless convention are declared;
- `L`/index alignment is declared;
- parameters and priors are declared before scoring;
- provenance identifies theory-side sources;
- hashes match submitted files;
- the firewall statement excludes ACT residual fitting and posterior tuning;
- the claim boundary remains reduced diagnostic only.

## Current Status

No payload is submitted. Every row in the submission packet is intentionally:

```text
PAYLOAD_NOT_SUBMITTED
```

## Claim Boundary

```text
tau_response_payload_submission_packet_only_no_payload_no_tau_score_no_dark_sector_verdict
```

The payload acceptance audit is tracked at:

```text
data/source_manifest/cmb_tau_lensing_response_payload_acceptance_audit_v01.csv
docs/cmb_tau_lensing_response_payload_acceptance_audit_v01.md
```
