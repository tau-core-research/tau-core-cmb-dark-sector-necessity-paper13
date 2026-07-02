# CMB Tau Lensing Transfer Payload v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** transfer payload requirement, no operator
**Canonical parent:** `docs/cmb_tau_lensing_response_derivation_route_v01.md`

This packet states what the transfer payload must provide before
`Phi_tau_eff(a,k)` can be propagated into a lensing-era potential response.

## Required Transfer Object

The required object is:

```text
T_tau_CMB(k,a)
```

or an equivalent endpoint-blind transfer rule/operator.

## Required Payload Components

A valid transfer payload must provide:

- selected domain;
- selected codomain;
- `k` convention;
- scale-factor convention;
- initial and final epoch;
- normalization point;
- operator rule, reduced evolution equation, kernel table, or explicit failure;
- cross-role consistency statement.

## Current Status

The existing growth-transfer kernel scaffold declares the requirements but does
not supply an operator rule. This packet therefore remains blocked:

```text
BLOCKED_OPERATOR_RULE_NOT_DERIVED
```

## Claim Boundary

```text
transfer_payload_requirement_only_no_operator_no_tau_score_no_dark_sector_verdict
```

The transfer acceptance audit is tracked at:

```text
data/source_manifest/cmb_tau_lensing_transfer_acceptance_audit_v01.csv
docs/cmb_tau_lensing_transfer_acceptance_audit_v01.md
```
