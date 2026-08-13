# Tau CMB SHR Seed-Covariance and QED Import v01

**Doc class:** theory-import refinement
**Status:** conditional source form imported; numerical source packet open
**Canonical parent:** [SHR common-operator import](tau_cmb_shr_common_operator_import_v01.md)

The SHR theory now supplies the conditional initial-covariance law

\[
\Sigma_{\rm seed}^{\rm CMB}(k)
=
L_{\rm CMB}(k)
\frac{\hbar}{2}
\begin{pmatrix}
\Omega_s(k)^{-1}&0\\
0&\Omega_s(k)
\end{pmatrix}
L_{\rm CMB}(k)^\dagger .
\]

It also fixes the weakest common photon--baryon--polarization interaction as
Maxwell plus minimally coupled charged matter on the same body metric.
Temperature opacity and polarization use the same Thomson collision operator;
Paper 13 must not introduce an independent polarization gain.

Numerical evaluation remains blocked until the source packet freezes

```text
Omega_s(k)
L_CMB(k)
q_e and m_e
baryon effective action and ionization inputs
physical occupation of the required matter bundles
```

Measured Standard Model constants may be used for a known-limit control, but
must not be reported as Tau-derived constants.

## Primary spectral candidate

The direct identity map from seed coordinate to primordial curvature is
rejected: with \(\Omega_s(k)\sim k\), it gives
\(\Delta_{\mathcal R}^2\sim k^2\).

The primary endpoint-blind candidate is instead the body Riesz descent

\[
L_{\mathcal R}=\zeta_{\mathcal R}\Omega_s^{-1},
\qquad
\mathcal P_{\mathcal R}^{\rm dimensional}
=\frac{\hbar\zeta_{\mathcal R}^2}{2}\Omega_s^{-3}.
\]

Its linear-dispersion limit is scale invariant. Paper 13 must keep the
amplitude and tilt blocked until \(\zeta_{\mathcal R}\) and the finite-body
dispersion correction are derived from the source packet. A rank-one
adiabatic handoff is the primary minimal branch; isocurvature requires an
independently occupied seed perturbation direction.

The bare finite-cycle correction is rejected as the origin of the observed
red tilt: its leading correction is blue,
\(\Delta_{\mathcal R}^2=1+(kL_B)^2/8+\cdots\). The Planck central value
\(n_s=0.9649\) instead defines the inverse target
\(p=(4-n_s)/3=1.0117\) for an effective
\(\Omega_{\rm eff}\propto k^p\) Riesz branch. Likewise
\(\ln(10^{10}A_s)=3.044\) fixes only
\(\sqrt{\hbar/c^3}\zeta_{\mathcal R,*}\simeq2.88\times10^{-4}\).
Neither value is promoted to a parent derivation.

The existing homogeneous SHR action supplies the nontrivial pump candidate:

\[
P_K(Y)=Z_\Phi Y+\beta_KY^2-V_{\rm eff},
\qquad
c_s^2=\frac{Z_\Phi+2\beta_KY}{Z_\Phi+6\beta_KY}.
\]

Its source-frozen prediction must satisfy

\[
A_s^{\rm SHR}
=\frac{\hbar H_*^2}
{8\pi^2M_{\rm SHR}^2\epsilon_{M,*}c_{s,*}},
\qquad
n_s^{\rm SHR}-1
=-2\epsilon_{M,*}-\eta_{M,*}-s_{M,*}.
\]

Paper 13 may evaluate these only after the parent-side background point,
potential and \(\beta_K\) are frozen. Planck values define acceptance targets,
not the background selection.

The primary finite potential candidate is now the morphology squared-defect
pump

\[
V_{\rm MSDP}
=\Lambda_M^4
\left[\frac14(\chi^2-1)^2+\frac12I_K\chi^2\right]+V_B.
\]

For \(0<I_K<1\), it has stable occupied branches
\(\chi_*^2=1-I_K\) with positive morphology contribution
\(\Lambda_M^4(I_K/2-I_K^2/4)\). This is an endpoint-blind conditional
completion. Paper 13 must not select \(\Lambda_M\), \(V_B\), \(I_K\) or the
pivot point from Planck residuals.

For the current CHDF reference \(I_K=0.0610078751933\), the forward MSDP
values are

\[
\chi_{\min}=0.9690160601,
\qquad
\frac{V_{\min}-V_B}{\Lambda_M^4}=0.02957344739.
\]

The pivot cannot be this stable minimum because there \(Y=0\) and
\(\epsilon_M=0\). It must be a source-selected rolling section. The
no-new-scale candidate \(\Lambda_M^4=\mathcal A_*/L_H^4\) and zero-offset
control \(V_B=0\) may be evaluated as conditional controls, but neither is
currently a physical Tau-parent theorem.

The constant-\(I_K\), zero-offset control also fails the graceful-exit test.
Using the hilltop Planck-tilt diagnostic gives
\(f_M/M_{\rm SHR}=14.6293\), but the maximum slow-roll parameter on the
complete occupied branch is only

\[
\max\epsilon_M=0.0499220<1.
\]

It therefore settles into the positive-energy minimum instead of ending
acceleration. Paper 13 must not repair this with a fitted endpoint switch.
The primary theory-side completion is the already sourced ordered morphology
exchange

\[
Q_{\phi\leftarrow K}
=-\dot\beta_KY^2
+\frac{Z_\Phi\phi^2}{2\ell_H^2}\dot I_K,
\]

with exit at
\(V_{\rm eff}=2Z_\Phi Y+3\beta_KY^2\). A prediction remains blocked until
the parent body law fixes a nonconstant \(I_K\) ordering and its handoff to
the radiation branch.

The current scalar-conformal body
\(K_{\rm leaf}=e^{2z}K_0\) cannot provide this ordering because its normalized
shape and \(I_K\) are constant. The minimal active completion requires a
trace-free shape mode \(d\), giving

\[
j_I
=\frac{\partial I_K}{\partial d}\mathcal L_{u_O}d,
\qquad
\left.\frac{\partial I_K}{\partial d}\right|_{\rm CHDF}
=-1.06341377025.
\]

This coefficient is source-forward. The occupation and ordered first jet of
\(d\) remain open and may not be fitted from Planck.

The theory-side body solve further reduces that jet to

\[
\mathcal L_{u_O}d_*
=
\left\langle S_{\rm CHDF},
H_{\rm TF}^{-1}
\left[
\mathcal L_{u_O}J_{\rm TF}
-(\mathcal L_{u_O}H_{\rm TF})D_*
\right]\right\rangle .
\]

The remaining morphology-exit input is therefore the occupied trace-free
seed-load packet \((J_{\rm TF},\mathcal L_{u_O}J_{\rm TF},H_{\rm TF})\), not
an independent fitted \(j_I\).

The tetrahedral seed carrier fixes the direction of \(J_{\rm TF}\) through

\[
\sum_e w_e^{(i)}t_et_e^{\mathsf T}
=3\left(n_in_i^{\mathsf T}-\frac13I_3\right).
\]

Paper 13 therefore needs only the source-owned ordered variation of this
specific edge-incidence contrast and its trace-free susceptibility. A static
contrast produces anisotropy but no exit jet.

For a Hodge-compatible occurrence response,

\[
j_{I,*}
=
\left.\frac{\partial I_K}{\partial d}\right|_*
\left\langle \widehat D_*,
\iota_{u_O}H_1^{-1}d_{\rm occ}J_{\rm TF}\right\rangle .
\]

Paper 13 must therefore receive the global seed cocycle
\(d_{\rm occ}J_{\rm TF}\) from the frozen parent source packet and project
its radial component for the scalar pump. It may not choose this cocycle from
CMB spectra.

The finite source parametrization is

\[
J_{\rm TF}(x)=a(x)T_{\omega(x)},
\qquad
\omega(x)\in S_4/S_3.
\]

Both amplitude variation and tetrahedral-role variation can produce the
tensor cocycle. Only amplitude variation changes the scalar invariant:

\[
j_I=2a\,\mathcal L_{u_O}a.
\]

Pure role variation preserves \(I_K\) and belongs to tensor/polarization
tests, not to the scalar pump. Constant \(a\) and constant \(\omega\) give
the exact full null control. The local CHDF orbit fixes neither global field.

The scalar amplitude is jointly sourced:

\[
\mathcal L_{u_O}a
=
\left\langle\widehat D_*,
H_{\rm TF}^{-1}
\left[
\mathcal L_{u_O}J_{\rm TF}
-(\mathcal L_{u_O}H_{\rm TF})D_*
\right]\right\rangle .
\]

Accordingly, a constant seed contrast can still produce a scalar morphology
jet through a nonhomogeneous base susceptibility. Paper 13 must freeze both
terms from the parent packet.

Their covariance is not an independent sum. Define

\[
C_D=A_J-\mathcal B_D,
\qquad
R_a=P_{\widehat D_*}H_{\rm TF}^{-1}C_D.
\]

The scalar morphology source supplied to the common CMB operator is

\[
\boxed{
\Sigma_I(k)
=4a_*^2R_a(k)\Sigma_s(k)R_a(k)^\dagger.
}
\]

For MCUS,

\[
C_D^{\rm MCUS}(\delta x,\delta y)
=F_B\mathsf D^*\delta x
+\frac{F_B}{L_B}
\mathsf D^*\operatorname{diag}(\delta y)\mathsf Dp_*.
\]

The two seed grades must therefore be propagated jointly, including their
cross covariance. Independent loading/susceptibility gains are forbidden.

With the gapped body response

\[
H_{\rm TF}(k)=m_{\rm TF}^2+\kappa_{\rm TF}\lambda(k),
\]

the infrared linear-dispersion/local-Jacobian limit predicts

\[
n_s-1=-\frac{4q_*}{1+q_*},
\qquad
q_*=\frac{\kappa_{\rm TF}\lambda(k_*)}{m_{\rm TF}^2}.
\]

The Planck central value corresponds to
\(q_*=0.008852682287\), or \(k_*\ell_{\rm TF}=0.09408869\) in the continuum
approximation. This is a frozen-source acceptance target. It must not be
used to choose the body gap or stiffness.

An identical trace-free lift of the current global nonlinear CHDF witness
would give \(q=\lambda\). Its nearest lowest finite-mode inverse targets are
cycle \(n=67\) and path \(m=33\). These values are not predictions and may
not be adopted unless independently selected by the parent source packet.

The explicit quartic trace-free lift changes the occupied radial ratio to

\[
\frac{\kappa_{\rm TF}}{m_\parallel^2}
=\frac{1}{1+3k_RI_K}
=0.875420854231.
\]

Its inverse target is \(\lambda_*=0.010112487319\), with nearest cycle
\(n=62\) and path \(m=31\). This lift is positive and coefficient-free
relative to the current CHDF units, but \(S_4\) symmetry alone does not
select it uniquely.

The coefficient-free shape now has an explicit conditional squared-Hodge
source. If `SRMT-P1` supplies the unrescaled STF Hilbert--Schmidt module, let

\[
\mathcal H_Q=\Gamma+\sqrt{k_R}c(Q),
\qquad
\mathcal H_Q^2=(1+k_R\|Q\|^2)I.
\]

Its normalized vacuum-subtracted spectral excess is

\[
\frac14\left(
\overline{\operatorname{Tr}}\mathcal H_Q^4-1
\right)
=\frac{k_R}{2}\|Q\|^2+\frac{k_R^2}{4}\|Q\|^4.
\]

Thus `ESH-STF1` reproduces exactly the local potential of the explicit lift.
`SRMT-P1` alone fixes only the STF metric; it does not prohibit distinct
\(E_2/E_3\) mass operators. The physical parent must additionally own the
displayed Euclidean STF Hodge operator slot. Paper 13 may not infer that
incidence from Planck agreement or from the separately typed EACER
orientation-lock construction.

The primary `SHR-ACT1` already owns the STF body coordinate \(Q\), its common
metric and stiffness, so `ESH-STF1` needs no new carrier. The current
SHR/PCSA/GCHD/JVCT/BRDC source inventory does not, however, select the
normalized Clifford-spectral excess on that coordinate. Conditional
`SRMT-P1` supplies the canonical unrescaled Clifford map; the remaining
physical choice is the spectral functional itself. Existing Clifford
carriers have different stages and domains and cannot be retyped as its
proof. Numerical scoring remains blocked pending that enriched-parent
selection.

The spectral law has the exact source split

\[
\frac14(\overline{\operatorname{Tr}}\mathcal H_Q^4-1)
=\frac{k_R}{2}\|Q\|^2
+\frac14\|\mathcal H_Q^2-I\|_{\rm nHS}^2.
\]

`SHR-ACT1` already supplies the first term. Because the prediction uses the
occupied body Hessian, the second term must be present before body
stabilization; a post-body PUSC/PRRC cost cannot modify it retroactively.
The correct nonlinear statement is `NGBD-STF1`: the enriched global body
action assigns the canonical squared-Hodge residual one positive normalized
defect cost. This fixes the quartic coefficient to \(k_R^2/4\); symmetry and
positivity alone would leave it free. It is compatible with PUSC6 because
that theorem is quadratic only on its protected abelian response fiber.
Until `NGBD-STF1` is physically selected, this coefficient remains
conditional.

The resulting prediction contract contains only two frozen branches:

\[
b=0\quad(\text{IPC/SGC-minimal}),\qquad
b=\frac14\quad(\text{NGBD-STF1}),
\]

with

\[
\frac{\kappa_{\rm TF}}{m_\parallel^2}
=\frac{1}{1+12b\,k_RI_K}.
\]

They correspond to the \(67/33\) and \(62/31\) inverse finite-mode
diagnostics respectively. Paper 13 may compare these two pre-registered
models, but it may not fit \(b\) continuously or infer parent truth from the
better CMB score.

Before any CMB projection, the two branches already have an amplitude-free
ordering. With common seed and terminal factors,

\[
\mathcal S_b(\lambda)=(1+r_b\lambda)^{-2},
\qquad
r_b=(1+12b\,k_RI_K)^{-1},
\]

so

\[
\frac{\mathcal S_{\rm NGBD}}{\mathcal S_{\rm minimal}}
=
\left(
\frac{1+\lambda}{1+0.875420854231\,\lambda}
\right)^2>1
\quad(\lambda>0).
\]

The ratio grows monotonically from one: `NGBD-STF1` gives less high-mode
morphology suppression after zero-mode normalization. This is a source-side
directional prediction, not a TT/TE/EE or lensing bandpower prediction.

Under the already declared rank-one adiabatic handoff and identical common
transfer functions, the auto-spectrum kernel is positive:

\[
C_\ell^{XX}[b]
=4\pi\int d\ln k\,
\mathcal P_0(k)\mathcal S_b(\lambda(k))
|\Delta_\ell^X(k)|^2.
\]

Therefore TT, EE and lensing auto power inherit the source ordering,
\(C_\ell^{XX}[\mathrm{NGBD}]\ge
C_\ell^{XX}[\mathrm{minimal}]\). TE does not: its transfer product is
sign-indefinite. These are conditional sign constraints, not populated
bandpowers.

Theory source:
`tau-core-theory/docs/tau_core_shr_cmb_seed_covariance_and_universal_coupling_001.md`.

```text
CONDITIONAL_SOURCE_FORM_IMPORTED
NO_INDEPENDENT_POLARIZATION_GAIN
CONSTANT_IK_GRACEFUL_EXIT_REJECTED
CONFORMAL_BODY_MORPHOLOGY_JET_REJECTED
TRACE_FREE_SHAPE_JET_REQUIRED
TETRAHEDRAL_SEED_STF_LINE_DERIVED
GLOBAL_SEED_STF_COCYCLE_OPEN
LOCAL_CHDF_TO_GLOBAL_COCYCLE_NON_ENTAILMENT
GAPPED_BODY_RED_TILT_MECHANISM_DERIVED
ESH_STF_QUARTIC_SOURCE_CONDITIONALLY_CONSTRUCTED
CURRENT_SOURCE_PACKET_DOES_NOT_ENTAIL_ESH_STF_SPECTRAL_LAW
ESH_STF_REQUIRES_NO_NEW_BODY_CARRIER
PHYSICAL_ESH_STF_SPECTRAL_LAW_OPEN
POST_BODY_PUSC_STF_HESSIAN_ROUTE_REJECTED
NGBD_STF_GLOBAL_BODY_DEFECT_SLOT_OPEN
IPC_MINIMAL_VS_NGBD_STF_TWO_BRANCH_TEST
CONTINUOUS_QUARTIC_COEFFICIENT_FIT_FORBIDDEN
AMPLITUDE_FREE_NGBD_HIGH_MODE_EXCESS_DERIVED
COMMON_TRANSFER_AUTO_SPECTRUM_ORDERING_CONDITIONAL
TE_CROSS_SPECTRUM_ORDERING_NOT_DERIVED
NUMERICAL_PLANCK_PREDICTION_STILL_BLOCKED
```
