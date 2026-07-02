# CMB Tau Lensing Tau-Side Normalization Obligation v01

**Doc class:** Tau-side normalization proof obligation
**Reader role:** Paper 13 Tau-grid implementer
**Status:** remaining normalization decomposition, no numeric Tau amplitude
**Canonical parent:** `docs/cmb_tau_lensing_endpoint_blind_normalization_gate_v01.md`

## Claim Boundary

```text
tau_side_normalization_obligation_only_no_numeric_tau_normalization_no_score_no_dark_sector_verdict
```

## Remaining Formula

After the ACT adapter convention lock, the unresolved Tau-side factor is:

```text
N_tau_remaining = N_parent_source * N_projection
```

This artifact does not assign a value to either factor. It defines what must be
proved before a new endpoint-blind physical score retry is allowed.

## Input Chain

- `normalization_gap`: `docs/cmb_tau_lensing_route_b_normalization_gap_derivation_v01.md` (exists)
- `normalization_gate`: `docs/cmb_tau_lensing_endpoint_blind_normalization_gate_v01.md` (exists)
- `adapter_lock`: `docs/cmb_tau_lensing_adapter_convention_normalization_lock_v01.md` (exists)
- `phi_contract`: `docs/tau_cmb_endpoint_blind_phi_tau_derivation_contract_v01.md` (exists)
- `potential_handoff`: `docs/tau_cmb_effective_potential_source_handoff_v01.md` (exists)
- `minimal_source_candidate`: `docs/tau_cmb_minimal_source_term_candidate_v01.md` (exists)

## Obligations

### N_parent_source

amplitude/units carried by the endpoint-blind Tau CMB source before lensing projection

```text
BLOCKED_PHI_TAU_EFF_NOT_DERIVED
```

Depends on:

  - endpoint-blind Phi_tau_eff(a,k) derivation
  - dimensionless or dimensionful A_tau(a,k) normalization
  - source sign and gauge convention
  - known-limit rule: parent response -> 0 implies delta_PP_tau -> 0

Forbidden shortcut:

```text
cannot be set from ACT/Planck bandpower residuals or post-score alpha
```

### N_projection

normalization of the map from Tau effective potential/readout source to L-space PP or delta_PP_tau grid

```text
EXPLICIT_NON_SCORE_FAILURE_PHYSICAL_PROJECTION_OPERATOR_NOT_SUPPLIED
```

Depends on:

  - resume from failure by supplying endpoint-blind Projection_PP operator
  - operator-implied N_projection_physical normalization
  - source-to-3000-grid physical replay certificate
  - post-population endpoint firewall certificate

Forbidden shortcut:

```text
cannot be inferred from the observed ACT amplitude after scoring
```


## Minimum Packet To Unblock A Physical Retry

```text
tau_cmb_lensing_N_parent_projection_packet_v01
```

It must contain:

- parent_source_normalization row/table for N_parent_source
- projection_operator_normalization row/table for N_projection
- dimension and unit audit
- gauge/sign convention audit
- endpoint firewall certificate
- materialization replay from source packet to tau_lensing_response_delta_pp_v01.csv
- formula-spec update that freezes N_tau before scoring

The packet skeleton is tracked at:

```text
docs/tau_cmb_lensing_N_parent_projection_packet_v01.md
data/derived/tau_cmb_lensing_N_parent_projection_packet_v01.csv
data/derived/tau_cmb_lensing_N_parent_projection_packet_summary_v01.json
```

## Decision

```text
The current evidence is sufficient to define the missing Tau-side objects. N_projection is explicitly failed for the current physical projection packet; N_parent_source remains blocked by missing endpoint-blind Phi_tau_eff derivation.
```
