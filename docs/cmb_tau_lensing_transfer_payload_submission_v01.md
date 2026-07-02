# CMB Tau Lensing Transfer Payload Submission v01

**Doc class:** data-frontier protocol
**Reader role:** Paper 13 scoring implementer
**Status:** submission packet, payload not submitted
**Canonical parent:** `docs/cmb_tau_lensing_score_unblock_plan_v01.md`

This packet defines the concrete files required to close the second unblock
step: the `T_tau_CMB(k,a)` transfer payload.

## Required Files

```text
tau_lensing_transfer_domain_v01.md
tau_lensing_transfer_codomain_v01.md
tau_lensing_transfer_time_scale_convention_v01.csv
tau_lensing_transfer_operator_rule_v01.md
tau_lensing_transfer_normalization_v01.md
tau_lensing_transfer_cross_role_consistency_v01.md
```

## Acceptance Rule

The files must establish an endpoint-blind transfer from the accepted
`Phi_tau_eff` source to a lensing-era potential response. They must declare
domain, codomain, time/scale convention, normalization, and an operator rule,
reduced evolution equation, kernel table, or explicit failure.

They must not choose a transfer rule from ACT residual behavior, previous score
outputs, or a desired dark-sector verdict.

## Current Status

```text
PAYLOAD_NOT_SUBMITTED
```

No `T_tau_CMB` payload is accepted and no Tau score is allowed.

## Claim Boundary

```text
transfer_submission_packet_only_no_transfer_payload_no_tau_score_no_dark_sector_verdict
```

## Partial Submission Update

All six transfer components have now been submitted for review at:

```text
payloads/tau_lensing_transfer_domain_v01.md
payloads/tau_lensing_transfer_codomain_v01.md
payloads/tau_lensing_transfer_time_scale_convention_v01.csv
payloads/tau_lensing_transfer_operator_rule_v01.md
payloads/tau_lensing_transfer_normalization_v01.md
payloads/tau_lensing_transfer_cross_role_consistency_v01.md
```

This completes the transfer submission packet for review. It does not accept
the transfer payload for scoring. The operator rule is a signature-only
scaffold, not a numeric transfer kernel, and the normalization file does not set
a fitted amplitude.
