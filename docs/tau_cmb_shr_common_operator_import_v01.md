# Tau CMB SHR Common-Operator Import v01

**Doc class:** theory-import and prediction-contract refinement
**Status:** conditional operator imported; numerical source state unavailable
**Canonical parent:** Paper 13 CMB scoring input fulfillment chain

## Imported result

The current Tau Core SHR branch replaces independently open acoustic,
lensing and growth response symbols by one source-frozen evolution:

\[
\partial_\eta X_\tau
=\mathcal A_{\rm CMB}^{\rm SHR}X_\tau,
\qquad
X_\tau=
(\delta_\gamma,\theta_\gamma,\delta_b,\theta_b,
\Phi,\Psi,\delta\rho_{M,O},q_{M,O})^{\mathsf T}.
\]

The morphology source and current are

\[
\delta\rho_{M,O}
=u_Ou_O\,\mathcal D_O[(I-P_0)P_M\mathbb T],
\qquad
J_{M,O}=\mathcal D_O[A\,dI_K],
\]

and the metric potentials use the same \(G_{\rm SHR}\) as the gravity
terminal. Consequently the Paper 13 prediction has the fixed form

\[
Y_\tau^{\rm CMB}
=\Pi_{\rm P13}\!\left[
\left\{
4\pi\int d\ln k\,\mathcal P_{\rm seed}(k)
\Delta_{\ell,\tau}^{A}(k)
\Delta_{\ell,\tau}^{B}(k)^*
\right\}_{AB}
\right].
\]

This imports an operator identity, not numerical values.

## Blocker reduction

The previous free slots

```text
Phi_tau_eff, A_tau, Theta_tau_ac, T_tau_CMB
```

must no longer be populated independently. They are components or projections
of the same common solution.

Numerical population now requires exactly:

1. a parent-selected initial seed covariance
   \(\Sigma_{\rm seed}(k)\);
2. a parent-selected universal photon/baryon/polarization coupling block.

Neither may be inferred from Planck residuals or tuned separately by readout.

## Status

```text
COMMON_SHR_CMB_OPERATOR_IMPORTED
NUMERICAL_Y_TAU_CMB_BLOCKED_BY_TWO_SOURCE_INPUTS
NO_SCORE_NO_LIKELIHOOD_NO_DARK_SECTOR_VERDICT
```

Theory source:
`tau-core-theory/docs/tau_core_shr_to_paper13_cmb_prediction_handoff_001.md`.
