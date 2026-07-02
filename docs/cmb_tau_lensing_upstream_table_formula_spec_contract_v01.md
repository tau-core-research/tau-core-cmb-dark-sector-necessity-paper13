# CMB Tau Lensing Upstream Table Formula Spec Contract v01

**Doc class:** upstream Tau-grid handoff contract
**Status:** executable handoff path; no score, no verdict
**Canonical script:** `scripts/build_tau_lensing_upstream_table_formula_spec.py`
**Canonical parent:** `docs/cmb_tau_lensing_grid_formula_materializer_contract_v01.md`

This contract defines the shortest clean handoff from a Tau-side derivation to
the Paper 13 grid materializer.

## Required Upstream Table

The upstream Tau derivation must emit a CSV table with exactly:

```text
3000 rows
L = 10..3009 exactly
one finite numeric Tau response value per L
```

Default columns:

```text
L,tau_response_value
```

The table may represent either:

```text
tau_PP(L)
```

or:

```text
delta_PP_tau(L)
```

depending on the selected route. The table must be generated before any
ACT/Planck residual score readout.

## Handoff

The builder validates the table and writes:

```text
payload_staging/tau_lensing_grid_formula_spec_v01.json
```

using:

```text
formula_family = tabulated_l_response_v01
```

The intended default handoff uses two upstream files:

```text
payload_staging/tau_lensing_upstream_l_response_v01.csv
payload_staging/tau_lensing_upstream_l_response_metadata_v01.json
```

The metadata sidecar supplies the endpoint-blind statement, source chain,
normalization statement, known-limit statement, and derivation reference. It
must not be marked `TEMPLATE_NOT_PAYLOAD`.

The repository keeps skeleton versions of these files in `payload_staging/`.
While they are still templates, `make tau-grid-handoff-dry-run` must report
`UPSTREAM_INPUTS_PRESENT_BUT_INVALID` rather than silently materializing a grid.

The downstream command is then:

```text
make tau-grid-from-formula
```

To generate the exact upstream request for a physical-candidate Tau response,
use:

```text
make tau-grid-physical-candidate-request
```

This writes the route A / route B deliverable contract that an upstream
Tau-side derivation must satisfy before the table can be treated as a physical
candidate.

To write a fillable physical-candidate upstream scaffold under
`payload_templates/`, use:

```text
make tau-grid-physical-candidate-scaffold
```

The scaffold is explicitly marked `TEMPLATE_NOT_PAYLOAD`; it must not be copied
into staging until all `FILL` fields and the full 3000-row table are replaced by
Tau-derived endpoint-blind content.

For an end-to-end handoff dry run, use:

```text
make tau-grid-handoff-dry-run
```

After reviewing the upstream table and metadata, the staging grid can be written
and validated without computing a score:

```text
make tau-grid-handoff-write-staging
```

For pipeline validation only, a null-control upstream response can be generated:

```text
make tau-grid-zero-control
```

This writes `delta_PP_tau(L)=0` for `L=10..3009`. It is a control object, not a
Tau-response success claim.

The matching delta route staging package can then be filled with:

```text
make tau-grid-zero-control-package
```

This writes the route declaration, provenance, and fiducial-reference metadata
needed for the guarded delta staging-promotion dry run.

To activate the zero-control route as the single active payload route, use:

```text
make tau-grid-zero-control-activate
```

This archives the previous active failure statement before promotion, then runs
the route intake and firewall checks. It does not compute a score.

Before replacing the control with a real Tau-derived response, run:

```text
make tau-grid-nonzero-precheck
```

This requires a non-template, non-control upstream table with at least one
nonzero finite value and endpoint-blind metadata. It does not promote a payload
or compute a score.

For a physical-candidate Tau response, run the stricter gate:

```text
make tau-grid-physical-candidate-precheck
```

This gate also rejects diagnostic probes. The metadata must declare a Tau-side
or Tau-derived basis, endpoint-blind status, normalization support, and a
known-limit statement before any staging promotion can be treated as a physical
Tau candidate.

After a physical-candidate table passes this gate and the staging grid is
written, the matching route package is:

```text
make tau-grid-physical-candidate-package
```

This command refuses to write a physical-candidate route package if the current
upstream metadata is still a control or diagnostic probe.

For handoff testing only, a nonzero diagnostic probe can be generated:

```text
make tau-grid-nonzero-probe
```

This is not a physical Tau response. It exists only to test the nonzero table
handoff path before a Tau-derived table is supplied.

After the probe grid is written to staging with
`make tau-grid-handoff-write-staging`, its matching diagnostic route package is:

```text
make tau-grid-nonzero-probe-package
```

This updates the staging declaration and provenance so the staging promotion
precheck can verify the grid hash. If this probe is ever scored, downstream
audit logic must classify the result as a diagnostic probe, not as a physical
Tau score.

## Claim Boundary

```text
tabulated_tau_response_to_grid_spec_only_no_score_no_dark_sector_verdict
```

This handoff proves only that the upstream table is shape-valid, finite,
hash-identified, and materializer-ready. It does not prove that the Tau response
is physically correct.
