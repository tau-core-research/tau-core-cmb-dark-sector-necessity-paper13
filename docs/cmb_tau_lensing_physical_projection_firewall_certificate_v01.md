# CMB Tau Lensing Physical Projection Firewall Certificate v01

**Doc class:** endpoint firewall certificate
**Reader role:** Paper 13 Tau-grid implementer
**Status:** current-packet firewall certificate only
**Canonical parent:** `docs/cmb_tau_lensing_physical_projection_operator_packet_v01.md`

## Claim Boundary

```text
projection_firewall_certificate_for_current_packet_only_no_operator_no_score_no_dark_sector_verdict
```

## Status

```text
PASS_FOR_CURRENT_SKELETON_ONLY
```

This certificate covers only the current physical projection operator packet:

```text
data/derived/cmb_tau_lensing_physical_projection_operator_packet_v01.csv
```

It must be rerun after any projection operator, normalization, or replay value
is populated.

## Checks

- `packet_exists`: True
- `forbidden_endpoint_markers_absent`: True
- `no_endpoint_like_numeric_projection_values_populated`: True
