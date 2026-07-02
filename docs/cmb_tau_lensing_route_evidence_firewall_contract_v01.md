# CMB Tau Lensing Route Evidence Firewall Contract v01

**Doc class:** route-evidence firewall contract
**Reader role:** Paper 13 scoring implementer
**Status:** implemented, currently blocked by intake
**Canonical parent:** `docs/cmb_tau_lensing_route_evidence_intake_contract_v01.md`
**Canonical data:** `data/source_manifest/cmb_tau_lensing_route_evidence_firewall_contract_v01.csv`

This contract adds a content firewall between route intake and projection replay
materialization. It does not validate numeric grid values and does not compute a
score. It only rejects template markers, route-declaration mismatches, and
unparseable JSON evidence files before the materializer can run. For direct and
delta numeric routes, it also requires the route declaration to name the exact
payload paths expected by the scoring gates. For JSON sidecars, it requires a
minimal set of provenance/fiducial keys, and those required values must be
non-empty before projection replay materialization. For the explicit failure
route, it requires the failure statement to name the missing parent input,
derivation rule, numeric kernel, normalization, and next theoretical blocker.
The provenance and fiducial sidecars must also match the selected route and
expected payload path values. Numeric route provenance must include
`numeric_grid_sha256`, matching the actual submitted grid payload file.

## Command

```text
make evidence-check
```

Default generated report:

```text
data/derived/cmb_tau_lensing_route_evidence_firewall_report_v01.json
```

## Claim Boundary

```text
route_evidence_firewall_contract_only_no_grid_validation_no_score_no_dark_sector_verdict
```
