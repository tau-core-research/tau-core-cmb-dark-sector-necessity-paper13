# Data Notice

This repository does not redistribute CMB maps, likelihoods, chains, or spectra.
It contains only compact manifests, source-data receipts, and derived protocol
tables used for theory-scaffold testing.

Any later numerical CMB likelihood work must cite and obtain the relevant
collaboration data products from their official release channels.

Local working copies may be downloaded under `data/external/` for private
reproducibility checks, but that directory is ignored by git and is not part of
the redistributable repository package. Source-data receipt files may record
official URLs, byte sizes, hashes, retrieval dates, and claim boundaries for
those local working copies.

The source-data acquisition status artifact verifies the receipt-listed local
working copies. In the current local workspace, six official CMB source entries
are present and hash/size matched: four Planck PR3 products and two ACT DR6
lensing products. This is source acquisition only; it does not run a likelihood,
construct a Tau prediction, compute a score, or decide dark-sector necessity.

The ACT DR6 lensing observable-payload artifact extracts a compact 18-row
observed lensing convergence bandpower table from the locally acquired ACT DR6
lensing package, together with source hashes, covariance dimensions, and
binning-matrix dimensions. It does not redistribute the raw ACT likelihood
package, does not run the ACT likelihood, does not construct a Tau-side
prediction, does not compute a score, and does not decide dark-sector
necessity.

The ACT DR6 lensing observed-score-adapter artifact records the observed-side
reduced score expression, vector slots, and inverse-covariance diagnostic for
that 18-bin payload. It is still not a likelihood run and not a score. It only
states that a later Tau-side prediction vector must be supplied in the same
ACT DR6 18-bin readout basis before the reduced score can execute.

The ACT DR6 Tau-prediction score-preflight artifact creates the exact 18-row
Tau prediction template expected at
`data/score_ready_input/act_dr6_lensing_tau_prediction_vector_v01.csv`. The
repository also includes that expected path as a Tau Core-specific null-response
control vector with all Tau-predicted ACT lensing values set to zero. This is a
control baseline, not a fitted physical Tau response. It permits a reduced
null-control score while preserving the claim boundary: no ACT likelihood is
run, no dark-sector verdict is allowed, and any nonzero Tau response must still
come from an endpoint-blind Tau-side derivation.

The ACT DR6 Tau-shape response-controls artifact screens a small predeclared
family of nonzero Tau Core-style morphology response controls. These controls
are not endpoint-fitted physical predictions; they are diagnostic probes showing
whether nonzero Tau-like response shapes can improve on the null-response
baseline. The current best control substantially improves the reduced
chi-square relative to null, but it still does not run the ACT likelihood,
validate Tau Core, or decide dark-sector necessity.

The ACT DR6 Tau nonzero-response candidate packet materializes the best screened
shape-control vector as a candidate input for follow-up derivation work. It
also records four open obligations: derive the shape parameters from Tau-side
morphology, derive or bound the amplitude from Tau-side normalization, prove the
zero-response known limit, and test the same candidate on an independent
readout or holdout. Until those obligations are closed, the vector remains a
diagnostic candidate rather than a physical Tau prediction.

The Planck lensing cross-readout holdout artifact transfers that ACT-selected
candidate unchanged to the Planck 9-bin lensing block distributed in the same
ACT DR6 lensing package. It uses the bottom-right Planck block of the combined
ACT+Planck covariance as a reduced diagnostic covariance. This partially
addresses the holdout obligation by showing that the same nonzero shape can be
evaluated outside the ACT-only adapter without Planck refitting, but it still
does not run a Planck likelihood, derive the Tau response from first
principles, validate Tau Core, or decide dark-sector necessity.

The Tau lensing nonzero-candidate derivation-status audit records the current
state of the four candidate obligations after the ACT+Planck diagnostics. It
closes only the formula-level zero-source limit for the diagnostic family
`R_tau^kk(L)=A*S(L)`, partially addresses the cross-readout obligation through
the Planck holdout, and leaves the Tau-side shape and amplitude derivations
open. It is an obligation audit, not a physical response derivation.

The Tau lensing response-origin route audit separates the nonzero candidate's
possible origin into seed-only projection, seed-induced Tau base-field response,
and hybrid routes. It does not select a route and does not promote the
candidate to a physical response. It records that the remaining target is to
derive or reject the candidate shape and amplitude from one route without
endpoint fitting.

The Tau lensing base-field route prederivation packet selects the seed-induced
Tau base-field response route as the next work route only. It does not select
the physical origin of the response. It records operator targets for
`M_tau=F_tau(M_seed,B_tau,constraints)`, `D_tau[M_tau;B_tau]`,
`Pi_lens[Phi_tau_eff]`, the broad low-L response kernel, and amplitude
normalization, all with open acceptance tests.

The Tau lensing base-field operator ansatz packet materializes the minimal
operator form for that work route and checks formula-level compatibility only.
It verifies that the candidate kernel is dimensionless, normalized, low-L
activated, high-L suppressed, and zero-limit preserving. It does not derive the
Tau response operator, the lensing projection, the shape parameters, or the
amplitude.

The Tau lensing factorized response derivation-attempt artifact splits the
operator ansatz into seed activation, base-field screening, readout
normalization, transition-scale, and amplitude factors. The split is exact at
the formula level, but it remains a derivation attempt: the Tau-side origin of
each factor is still open.

The Tau lensing seed-screening minimal-closure artifact conditionally closes
the two central shape factors by explicit assumptions about co-determination:
the morphological seed is an initial morphology/constraint state, while Tau
base-field properties help shape the stabilized response morphology. The
resulting conditional factors are a seed-conditioned activation and a
saturating base-field screening transfer. This is useful because it separates
the candidate shape into interpretable Tau-side roles, but it is still not an
unconditional derivation. The transition scale, amplitude, and exponent origins
remain open, and the score route remains locked.

The same artifact records an inverse-constraint reading: morphology and 4D
readout behavior may restrict compatible Tau base-field response-family
candidates only under declared null/gauge, wrong-family, and holdout controls.
It does not identify `B_tau`, choose a unique response equation, or promote a
physical dark-sector verdict.

The Planck PR3 peak source-freeze packet records official IRSA ancillary-data
URLs for selected TT/TE/EE binned spectra and a baseline minimum-theory
reference curve. The public package records only the selected source locations
and claim boundary at the source-freeze layer; raw Planck bytes are not
redistributed.

The Planck PR3 peak extraction artifact may download the selected public source
files into the gitignored `data/external/planck_pr3/` cache during reproduction.
Only compact receipts, SHA256 hashes, parser rules, and the derived
peak-observable table are stored in the public package. The extracted table is
an observed-feature input artifact only; it is not a Tau prediction, CMB
likelihood, score, or dark-sector verdict.

The Planck PR3 peak Tau-prediction materialization artifact is likewise not a
physical prediction table. It records the endpoint-blind Tau-side payload fields
that must be supplied before any peak score can be attempted, while keeping the
current score blocked until such a payload or accepted null-response control
exists.

The subsequent Tau-prediction payload-supply artifact is an explicit empty
supply record: it stores no predicted peak positions, amplitudes, likelihoods,
or fitted parameters. Its purpose is to make the absent Tau-side prediction
auditable and to route the next step to an actual Tau acoustic source
derivation rather than to a premature score.

The acoustic Tau-prediction source-derivation artifact declares only a formal
source target and dependency spine. It does not store a solved acoustic source,
peak prediction, likelihood value, fitted parameter, or accepted physical
readout.

The acoustic source-operator payload artifact is a contract for the still
missing `P_ac` operator payload. It records required rows and rejection status
only; it stores no operator solution, spectra, peak predictions, or fitted
parameters.

The acoustic source-operator payload-supply artifact records an explicit empty
supply attempt against that contract. It stores no acoustic operator solution,
spectra, peak predictions, likelihoods, or fitted parameters, and its only
scoring effect is to preserve the score firewall until a minimal operator model
attempt is available.

The acoustic minimal operator model attempt stores a formula scaffold and
acceptance audit only. It records no executable acoustic operator, no Planck
peak prediction, no CMB likelihood, and no fitted parameter values.

The acoustic operator dependency-unblock plan stores only an ordered list of
required follow-up artifacts and acceptance requirements. It records no
completed dependency, no executable operator, no spectra, no CMB likelihood,
and no fitted parameter values.

The acoustic domain/basis lock acceptance artifact stores only convention rows
for the reduced acoustic operator domain. It records no executable Tau source,
no Planck peak prediction, no spectra, no CMB likelihood, and no fitted
parameter values.

The Phi_tau_eff acoustic input acceptance artifact stores an acceptance audit
for the effective-potential input slot. It accepts only the source-slot
identity and records no accepted effective-potential construction, no spectra,
no CMB likelihood, and no fitted parameter values.

The Phi_tau_eff endpoint-blind provenance acceptance artifact stores a
policy/provenance audit only. It accepts the endpoint-exclusion policy but
records no supplied parent-input manifest, no accepted parent-side content, no
derivation rule, no replay package, no score-ready source, no CMB likelihood,
and no dark-sector verdict.

The acceptance-evidence receipt/evidence acceptance reopen-gate artifact
accepts the seven endpoint-blind receipt/evidence objects and allows the
decision gate to reopen. It still records no accepted scoring payload, no
accepted scoring input, no opened scoring handoff, no derived `Phi_tau_eff`, no
score, no CMB likelihood, and no no-dark or dark-sector verdict.

The acceptance-evidence scoring-handoff package consumes those accepted
receipt/evidence objects and opens an endpoint-blind scoring-handoff candidate
route. It still records no accepted scoring input, no derived `Phi_tau_eff`, no
score, no CMB likelihood, and no no-dark or dark-sector verdict.

The acceptance-evidence scoring-input decision package closes the handoff route
by explicit null response because no score-ready input is available. It records
no accepted scoring input, no derived `Phi_tau_eff`, no score, no CMB
likelihood, and no no-dark or dark-sector verdict.

The acceptance-evidence score-attempt guard executes the final pre-score guard
for the current accepted-evidence chain and denies all score attempts because
no score-ready input is available. It records no accepted scoring input, no
derived `Phi_tau_eff`, no score, no CMB likelihood, and no no-dark or
dark-sector verdict.

The acceptance-evidence null-response lock records the resulting closed route:
the explicit null response remains locked until replaced by a real score-ready
input with accepted scoring input. It records no derived `Phi_tau_eff`, no
score, no CMB likelihood, and no no-dark or dark-sector verdict.

The acceptance-evidence route-completion certificate certifies that the current
accepted-evidence route has reached its terminal state: null-response locked.
It records no accepted scoring input, no derived `Phi_tau_eff`, no score, no
CMB likelihood, and no no-dark or dark-sector verdict.

The real score-ready input supply contract declares the seven required material
classes per row needed to unlock that null-response state: Phi_tau_eff source,
dimension replay, normalization binding, endpoint-blind provenance, CMB readout
mapping, likelihood adapter, and acceptance replay. It supplies none of these
materials and keeps the route locked.

The real score-ready payload slot specification expands that contract into 49
concrete expected artifact paths and schemas. It is actionable as an import
shape for future score-ready material, but it materializes no payload, accepts
no slot, accepts no scoring input, and keeps the route locked.

The real score-ready payload template manifest binds those 49 slots to seven
reusable template files under `data/score_ready_input_templates/`. These files
are input shapes only. They contain no real Tau-side CMB payload values, bind no
hash receipt, accept no slot, and do not unlock scoring.

The real payload import precheck checks the expected `data/score_ready_input/`
payload paths produced by the slot specification. In this package all 49 real
payload paths are missing, no hash is bound, no schema passes, no payload import
is accepted, and the scoring route remains locked.

The Phi Tau parent-input candidate manifest acceptance artifact stores an
acceptance audit only. It accepts only the candidate packet identity and
records no accepted base-field state, no accepted morphological seed, no
accepted response operator, no locked gauge/normalization metadata, no executed
endpoint firewall, no provenance replay, no score-ready source, no CMB
likelihood, and no dark-sector verdict.

The Phi Tau parent-source-content closure decision artifact stores a closure
decision only. It records endpoint-clean candidate content, but no dimensional
or normalization pass, no payload-level firewall pass, no executable replay, no
accepted parent input, no Phi_tau_eff derivation, no CMB likelihood, and no
dark-sector verdict.

The Phi Tau parent-certificate closure decision artifact stores a certificate
closure decision only. It records declared requirements, declared candidates,
and audited candidates, but no supplied certificate evidence, no passed
dimension/replay/firewall audit, no accepted payload, no Phi_tau_eff
derivation, no CMB likelihood, and no dark-sector verdict.

The Phi Tau parent evidence-package closure decision artifact stores a
scoring-facing closure decision only. It records that evidence was requested,
package slots were declared, and the package was audited, but no dimension,
replay, or firewall evidence payload was supplied, no evidence package passed,
no certificate passed, no parent payload was accepted, no Phi_tau_eff was
derived, no CMB likelihood was computed, and no dark-sector verdict was
allowed.

The Phi Tau parent evidence-payload acquisition candidate and audit artifacts
store hash-bound local semantic replay payload candidates. They record concrete
source artifacts and hashes for the seven parent evidence rows, but the rows
remain candidate payloads only: no parent payload is accepted, no certificate
passes, no Phi_tau_eff is derived, no CMB likelihood is computed, and no
dark-sector verdict is allowed.

The Phi Tau parent evidence-payload intake bridge decision artifact stores the
bridge state between acquired candidate payloads and the canonical
submission/materialization route. It records that candidate payloads are
available and hash-bound, but canonical payload packets, receipt bindings, and
dimension/replay/firewall acceptance bindings are still absent; therefore no
parent payload is accepted and no score is allowed.

The Phi Tau parent canonical payload packet artifact stores the repackaged
candidate payload rows as canonical packet rows with source hashes and receipt
bindings. It records packet materialization only: binding coverage remains
incomplete for acceptance, no parent payload is accepted, no certificate
passes, no Phi_tau_eff is derived, no CMB likelihood is computed, and no
dark-sector verdict is allowed.

The scoring-handoff unblock-condition evidence receipt acceptance precheck,
unblock plan, unblock-plan audit, decision gate, decision-gate audit,
acceptance-evidence fulfillment package, acceptance-evidence materialization
package, and materialization-audit/acceptance-precheck artifacts record the
remaining pre-score exit requirements after materialization audit failure. They
require materialization-audit pass, accepted receipts, accepted evidence objects,
and an open handoff before scoring can be attempted. The materialization package
creates and hashes endpoint-blind evidence materials, and the audit/precheck
artifact verifies them and passes receipt/evidence acceptance prechecks, but
still accepts no receipt or evidence object; no score, likelihood, Tau-response
claim, or dark-sector verdict is allowed.
