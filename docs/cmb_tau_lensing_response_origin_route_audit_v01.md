# Tau Lensing Response Origin Route Audit v01

**Doc class:** response-origin route audit
**Status:** seed-only, base-field, and hybrid Tau-origin routes declared; no route selected
**Canonical parent:** Paper 13 ACT/Planck lensing scoring route

This artifact turns the nonzero lensing candidate into an origin problem. The
ACT and Planck reduced diagnostics show that a nonzero broad low-\(L\) response
is much better than the null response, but they do not say where that response
comes from. This audit therefore separates the viable Tau-origin routes.

Candidate target:

```text
candidate_id=tau_shape_control_morph_lensing_broad_lowL_A1e-07
R_tau^kk(L) = A*S(L; L_c,p,q)
A=1e-07
L_c=120.0
p=0.5
q=1.0
ACT_delta_chi2_vs_null=1727.675704446904
Planck_delta_chi2_vs_null=1667.2063883803967
```

Route status:

```text
routes_declared=4
route_selected_now=False
seed_only_route_status=open_viable_but_unproved
base_field_route_status=open_viable_but_unproved
hybrid_route_status=open_high_burden_route
physical_tau_response_claim_allowed=False
dark_sector_verdict_allowed=False
```

## Interpretation

The seed-only route would make the morphology seed itself carry the scale and
amplitude of the lensing response. The base-field route would make the seed act
as an excitation/source for a Tau base-substrate response, with the response
operator producing the broad lensing shape. The hybrid route allows direct seed
projection plus base-field response, but it has the highest proof burden.

No route is selected by this artifact. The next successful step must derive or
reject at least one route by producing the candidate \(L_c,p,q,A\) without
endpoint selection.
