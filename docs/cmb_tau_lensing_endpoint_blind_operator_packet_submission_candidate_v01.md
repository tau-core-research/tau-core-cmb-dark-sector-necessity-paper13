# CMB Tau Lensing Endpoint-Blind Operator Packet Submission Candidate v01

**Doc class:** endpoint-blind operator packet submission candidate
**Reader role:** Paper 13 Tau-grid implementer
**Status:** supplied for audit; not accepted; not score eligible
**Canonical parent:** `docs/cmb_tau_lensing_endpoint_blind_operator_packet_submission_template_v01.md`

## Claim Boundary

```text
endpoint_blind_operator_packet_submission_candidate_only_no_operator_acceptance_no_physical_score_no_dark_sector_verdict
```

## Submission Path

```text
payloads/cmb_tau_lensing_endpoint_blind_operator_packet_submission_v01.csv
```

## Candidate Rows

- `source_domain`
- `projection_equation`
- `output_replay`
- `zero_source_limit`

## Blocking Rows

- `dimension_sign_audit`
- `kernel_measure`
- `normalization`
- `output_replay`
- `post_population_firewall`

## Interpretation

This candidate packages existing endpoint-blind-looking artifacts so the receipt
and content-audit path can run. It intentionally preserves blockers for the
missing full `K_tau_PP(L; a,k)dmu(a,k)` projection kernel, physical projection
normalization, dimension/sign audit, and post-population firewall. It does not
accept the physical Tau-route and does not allow scoring.
