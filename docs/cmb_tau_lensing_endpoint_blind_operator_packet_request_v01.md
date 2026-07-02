# CMB Tau Lensing Endpoint-Blind Operator Packet Request v01

**Doc class:** endpoint-blind operator packet request
**Reader role:** Paper 13 Tau-grid implementer
**Status:** request open; no operator accepted; not a grid; not a score
**Canonical parent:** `docs/cmb_tau_lensing_projection_formula_spec_acceptance_matrix_v01.md`

## Claim Boundary

```text
endpoint_blind_operator_packet_request_only_no_operator_acceptance_no_grid_no_score_no_dark_sector_verdict
```

## Target

```text
minimum supplied packet needed to test Projection_PP[Phi_lens_tau](L) for acceptance
```

## Submission Template

```text
payload_templates/cmb_tau_lensing_endpoint_blind_operator_packet_submission_TEMPLATE_v01.csv
```

## Intended Submission Path

```text
payloads/cmb_tau_lensing_endpoint_blind_operator_packet_submission_v01.csv
```

## Requested Packet Slots

- `TCMBEBOPR01_001` `source_domain`: REQUESTED_NOT_SUPPLIED | object: Phi_lens_tau(a,k) domain declaration | fills: `TCMBPFSAM01_001;TCMBPFSAM01_002`
- `TCMBEBOPR01_002` `projection_equation`: REQUESTED_NOT_SUPPLIED | object: Projection_PP[Phi_lens_tau](L) equation | fills: `TCMBPFSAM01_001;TCMBPFSAM01_005`
- `TCMBEBOPR01_003` `kernel_measure`: REQUESTED_NOT_SUPPLIED | object: K_tau_PP(L; a,k)dmu(a,k) | fills: `TCMBPFSAM01_002;TCMBPFSAM01_006`
- `TCMBEBOPR01_004` `normalization`: REQUESTED_NOT_SUPPLIED | object: N_projection_physical | fills: `TCMBPFSAM01_003;TCMBPFSAM01_006`
- `TCMBEBOPR01_005` `output_replay`: REQUESTED_NOT_SUPPLIED | object: 3000-row projected Tau-grid | fills: `TCMBPFSAM01_004`
- `TCMBEBOPR01_006` `zero_source_limit`: REQUESTED_NOT_SUPPLIED | object: zero-source proof or replay | fills: `TCMBPFSAM01_005`
- `TCMBEBOPR01_007` `dimension_sign_audit`: REQUESTED_NOT_SUPPLIED | object: dimension/sign audit table | fills: `TCMBPFSAM01_006`
- `TCMBEBOPR01_008` `post_population_firewall`: REQUESTED_NOT_SUPPLIED | object: post-population endpoint firewall certificate | fills: `TCMBPFSAM01_007`

## Submission Rule

The packet can only be considered after all requested slots are supplied with
endpoint-blind provenance. Supplying this packet does not itself allow a score:
it must first pass an operator-packet receipt audit, dimension/sign audit,
zero-source audit, replay audit, and post-population firewall.
