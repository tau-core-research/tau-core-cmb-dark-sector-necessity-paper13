# Tau Lensing Nonzero Candidate Derivation Status Audit v01

**Doc class:** derivation-status and obligation audit
**Status:** formula-level zero limit closed; Planck holdout partially addresses cross-readout; Tau-side shape and amplitude derivation remain open
**Canonical parent:** Paper 13 ACT/Planck lensing scoring route

This artifact audits the four obligations attached to the current nonzero
Tau-style lensing candidate. It does not promote the candidate to a physical
Tau prediction. It separates what is now closed at the formula/control level
from what still needs a Tau-side derivation.

Locked diagnostic response family:

```text
S(L; L_c,p,q) = ((L/L_c)^p)/(1+(L/L_c)^(p+q)) / max_L S_raw
R_tau^kk(L) = A S(L; L_c,p,q)
y_tau = R_tau^kk evaluated in the chosen lensing readout basis
```

Current candidate:

```text
candidate_id=tau_shape_control_morph_lensing_broad_lowL_A1e-07
A=1e-07
L_c=120.0
p=0.5
q=1.0
```

Audit result:

```text
obligations_total=4
closed_formula_level=1
partially_addressed=1
open_tau_derivation=2
physical_tau_response_claim_allowed=False
dark_sector_verdict_allowed=False
```

The zero-source known limit is closed only for this diagnostic formula family:
if the Tau response amplitude is absent or set to \(A=0\), then
\(R_\tau^{\kappa\kappa}(L)=0\) in every band. The Planck holdout partially
addresses the cross-readout obligation because the same ACT-selected candidate
was transferred unchanged and still improved over null in the Planck block.

## Remaining Blocker

The candidate still needs a Tau-side derivation or rejection of both:

1. the shape parameters \(L_c,p,q\) from morphology/readout structure;
2. the amplitude \(A\) from Tau-side normalization rather than endpoint
   selection.

Until those are supplied, this remains a diagnostic candidate, not a physical
Tau response.
