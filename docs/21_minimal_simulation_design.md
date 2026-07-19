# GyroAuth Minimal Simulation Design

## 1. Purpose

This document completes **Priority G: Minimal Simulation Design** for the GyroAuth formalization and paper-preparation work.

It builds on:

```text
docs/15_guarded_authentication_criterion_research_question.md
docs/16_formal_terminology_and_scope.md
docs/17_threat_model.md
docs/18_formal_security_model.md
docs/19_criterion_update_state_machine.md
docs/20_normal_and_poisoned_update_scenarios.md
```

Its purpose is to define a minimal, reproducible, implementation-oriented simulation that demonstrates:

```text
dynamic criterion
!=
unconstrained self-update
```

The simulation compares:

```text
Model U: Unconstrained Criterion Update
Model G: Guarded Criterion Update
```

under legitimate Context change, gradual criterion poisoning, and partial Evidence compromise.

This document prepares:

```text
Priority H: PoC Implementation and Results
Priority I: Security Claims and Limitations
Priority J: Paper Outline and Manuscript
```

This document does not yet contain executed results.

---

## 2. Invariant Foundation

The existing GyroAuth foundation remains unchanged:

```text
Authentication
=
Stability-based Selection over State Convergence
```

The layer relationship remains:

```text
Gyro Logic   = Theory
GyroOS       = Execution System
GyroAuth     = Authentication Application
```

The Gyro Logic Core remains:

```text
Structure
↓
Slice
↓
Stability
```

This simulation does not redefine:

```text
Structure
Slice
Stability
Gyro Process
GyroOS /loop/step
canonical GyroOS Operator Response
```

The simulation is limited to the GyroAuth application layer.

```text
Core change: none
GyroOS contract change: none
GyroAuth simulation design: added
```

---

## 3. Simulation Research Question

The simulation answers the following operational question:

> Can GyroAuth permit bounded, evidence-supported criterion adaptation while preventing repeated sub-threshold observations or compromised Evidence from being incorporated automatically as a new admissible criterion?

The minimum comparison is:

```text
same scenario inputs
same initial criterion
same candidate update function
but
one model adopts candidates directly
and
one model evaluates candidates through Guard and Criterion Update Response
```

---

## 4. Simulation Scope

### 4.1 Included

The first simulation includes:

```text
discrete evaluation stages
synthetic deterministic inputs
one bounded criterion representation
one candidate update function
one Guard
one criterion state machine
one Auth Decision stream
one Criterion Update Response stream
trusted rollback points
scenario-specific Evidence provenance
normal adaptation
criterion poisoning
single-source Evidence compromise
```

### 4.2 Excluded

The first simulation does not include:

```text
production biometric data
real GPS or device telemetry
full GyroOS execution
neural networks
online model training
probabilistic attack generation
cryptographic protocol implementation
hardware resource benchmarking
privacy-preserving aggregation
multi-user population modeling
formal theorem proving
```

These exclusions prevent the first PoC from becoming an unrelated machine-learning or infrastructure project.

---

## 5. Compared Models

## 5.1 Model U — Unconstrained Update

Model U represents an intentionally unsafe comparison baseline.

A candidate update is produced:

```text
A*_(t+1) = U(A_t, X_t, C_t, E_t)
```

and adopted directly:

```text
A_(t+1) = A*_(t+1)
```

There is no independent:

```text
Guard
Criterion Integrity Evaluation
Criterion Update Response
Freeze
Review
Rollback
```

Model U is not presented as a complete representation of every existing adaptive-authentication system.
It is a controlled baseline used to expose the risk of direct observation-to-criterion incorporation.

---

## 5.2 Model G — Guarded Update

Model G uses the same candidate generator but separates proposal from adoption.

```text
A*_(t+1) = U(A_t, X_t, C_t, E_t)
```

```text
G_t = Guard(
  A_t,
  A*_(t+1),
  T_t^obs,
  C_t,
  E_t,
  H_t,
  P_t
)
```

```text
D_crit_t = SelectCriterionResponse(G_t, Q_t, H_t)
```

```text
A_(t+1) = TransitionCriterion(
  A_t,
  A*_(t+1),
  D_crit_t,
  P_t
)
```

The effective criterion changes only when:

```text
D_crit_t = ACCEPT
```

The model must preserve:

```text
Criterion Update Candidate
!=
Accepted Criterion
```

---

## 6. Minimal Criterion Representation

The first PoC uses a deliberately small numeric criterion.

Let the effective criterion at stage `t` be:

```text
A_t = (
  mu_t,
  w_t,
  p_t,
  h_t,
  rho_t
)
```

where:

```text
mu_t   = criterion center
w_t    = admissible region width
p_t    = Evidence provenance requirement
h_t    = challenge requirement strength
rho_t  = rollback linkage integrity
```

Interpretation:

```text
mu_t
= expected operational position or behavior reference

w_t
= how far an observation may deviate while remaining admissible

p_t
= minimum provenance quality required for adaptation

h_t
= minimum challenge or re-authentication support required

rho_t
= whether the criterion remains linked to a verified rollback point
```

The first implementation may use normalized values:

```text
mu_t  ∈ [0, 1]
w_t   ∈ [0, 1]
p_t   ∈ [0, 1]
h_t   ∈ [0, 1]
rho_t ∈ {0, 1}
```

This representation is not a claim that production authentication is one-dimensional.
It is a minimum executable abstraction for testing guarded adaptation.

---

## 7. Observation and Evidence Representation

At each stage, the scenario provides:

```text
X_t = (
  y_t,
  c_t,
  prov_t,
  cross_t,
  challenge_t,
  privilege_t,
  source_integrity_t
)
```

where:

```text
y_t                  = observed operational position
c_t                  = Context identifier
prov_t               = Evidence provenance quality
cross_t              = cross-evidence consistency
challenge_t          = challenge confirmation quality
privilege_t          = privilege-risk indicator
source_integrity_t   = Evidence-source integrity indicator
```

Normalized values may be used:

```text
y_t                ∈ [0, 1]
prov_t             ∈ [0, 1]
cross_t            ∈ [0, 1]
challenge_t        ∈ [0, 1]
privilege_t        ∈ [0, 1]
source_integrity_t ∈ [0, 1]
```

The Context identifier remains categorical.

---

## 8. Subject-side Derived Values

The simulation derives the following minimum subject-side values.

### 8.1 Deviation

```text
delta_t = |y_t - mu_t|
```

### 8.2 Normalized Deviation

```text
delta_norm_t = delta_t / max(w_t, epsilon)
```

### 8.3 Deviation Direction

```text
v_t = delta_t - delta_(t-1)
```

Interpretation:

```text
v_t < 0  → re-convergence tendency
v_t = 0  → unchanged deviation
v_t > 0  → divergence tendency
```

### 8.4 Deviation Persistence

```text
persist_t
=
number of consecutive stages with delta_norm_t above a configured level
```

### 8.5 Recovery Tendency

A minimal deterministic recovery indicator is:

```text
recovery_t = 1 if v_t < 0 else 0
```

A later PoC may replace this binary form with a continuous value.

### 8.6 Trajectory Continuity

The first simulation uses a reduced proxy:

```text
trajectory_continuity_t
=
clamp(
  1
  - alpha_delta * delta_norm_t
  - alpha_priv * privilege_t
  + alpha_cross * cross_t
  + alpha_recovery * recovery_t,
  0,
  1
)
```

This is a simulation proxy only.
It does not replace the broader relational definition of Trajectory.

### 8.7 Stability

The first simulation may derive:

```text
stability_t
=
clamp(
  beta_cont * trajectory_continuity_t
  + beta_cross * cross_t
  + beta_chal * challenge_t
  - beta_dev * delta_norm_t,
  0,
  1
)
```

The coefficients must be declared in the implementation configuration and must not be hidden.

---

## 9. Auth Decision Function

The Auth Decision remains separate from criterion adaptation.

Minimum deterministic rule:

```text
if stability_t < theta_fail
and trajectory_continuity_t < theta_cont_fail:
    AUTH_FAIL

else if challenge is required
or stability_t < theta_reauth:
    REAUTH_REQUIRED

else if delta_norm_t > theta_reconverge
or v_t > 0:
    RECONVERGING

else:
    AUTH_STABLE
```

The initial simulation must allow combinations such as:

```text
AUTH_STABLE + FREEZE
RECONVERGING + DEFER
REAUTH_REQUIRED + REVIEW
AUTH_FAIL + ROLLBACK
```

The Criterion Update Response must not be inferred directly from the Auth Decision.

---

## 10. Candidate Update Function

The same candidate generator is used by Model U and Model G.

For the criterion center:

```text
mu*_(t+1)
=
mu_t + eta_mu * (y_t - mu_t)
```

For the admissible width:

```text
w*_(t+1)
=
w_t + eta_w * max(0, delta_t - w_t)
```

For provenance and challenge requirements:

```text
p*_(t+1)
=
UpdateProvenanceRequirement(p_t, X_t)
```

```text
h*_(t+1)
=
UpdateChallengeRequirement(h_t, X_t)
```

For rollback linkage:

```text
rho*_(t+1)
=
UpdateRollbackLink(rho_t, X_t)
```

The implementation must record every candidate even when it is rejected.

```text
Candidate generation
!=
Candidate adoption
```

---

## 11. Criterion Update Delta

Let:

```text
DeltaA_t = A*_(t+1) - A_t
```

The simulation must retain at least:

```text
center_shift_t      = |mu*_(t+1) - mu_t|
width_change_t      = w*_(t+1) - w_t
provenance_change_t = p*_(t+1) - p_t
challenge_change_t  = h*_(t+1) - h_t
rollback_change_t   = rho*_(t+1) - rho_t
```

Derived update dynamics:

```text
update_rate_t
update_direction_t
cumulative_center_drift_t
cumulative_width_expansion_t
```

These values are required to distinguish one bounded update from gradual poisoning.

---

## 12. Guard Design

The first Guard is a vector of non-interchangeable checks.

```text
G_t = (
  g_prov,
  g_cross,
  g_challenge,
  g_magnitude,
  g_rate,
  g_direction,
  g_discrimination,
  g_rollback,
  g_source
)
```

Each component is either:

```text
PASS
WARN
FAIL
```

### 12.1 Provenance Guard

```text
g_prov = PASS
if prov_t >= p_t
else FAIL
```

### 12.2 Cross-evidence Guard

```text
g_cross = PASS
if cross_t >= theta_cross
else WARN or FAIL
```

### 12.3 Challenge Guard

```text
g_challenge = PASS
if challenge_t >= h_t
or no challenge is required for the candidate
else FAIL
```

### 12.4 Update Magnitude Guard

```text
g_magnitude = PASS
if center_shift_t <= max_center_shift
and width_change_t <= max_width_change
else FAIL
```

### 12.5 Update Rate Guard

```text
g_rate = PASS
if update_rate_t <= max_update_rate
else FAIL
```

This Guard must also detect repeated sub-threshold updates through cumulative drift.

### 12.6 Update Direction Guard

```text
g_direction = PASS
if the update direction is explainable by the declared Context transition
else WARN or FAIL
```

### 12.7 Discrimination Guard

Let an attack reference point be `y_attack`.

```text
disc_before_t = max(0, |y_attack - mu_t| - w_t)
```

```text
disc_after_t = max(0, |y_attack - mu*_(t+1)| - w*_(t+1))
```

```text
discrimination_loss_t
=
disc_before_t - disc_after_t
```

```text
g_discrimination = FAIL
if discrimination_loss_t > max_discrimination_loss
else PASS
```

This simplified reference-point method is sufficient for the first PoC.
A later study may use distributions or multiple attack classes.

### 12.8 Rollback Guard

```text
g_rollback = PASS
if rho_t = 1 and a verified rollback point exists
else FAIL
```

### 12.9 Evidence-source Guard

```text
g_source = FAIL
if source_integrity_t < theta_source
else PASS
```

### 12.10 Non-compensation Rule

Critical Guard failures must not be averaged away.

```text
CriticalGuardFail
→
Criterion Update Response != ACCEPT
```

Critical Guards in the first simulation are:

```text
g_prov
g_challenge when challenge is required
g_discrimination
g_rollback for rollback-sensitive change
g_source
```

---

## 13. Criterion Integrity Value

For visualization only, the simulation may compute a scalar Criterion Integrity score.

```text
criterion_integrity_t
=
WeightedSummary(G_t, Q_t, H_t)
```

However:

```text
criterion_integrity score
!=
complete Guard semantics
```

A high average score cannot override a critical Guard failure.

The implementation must store both:

```text
Guard vector
Criterion Integrity summary
```

---

## 14. Criterion Update Response Selection

The minimum response-selection policy is deterministic.

### 14.1 ACCEPT

Select `ACCEPT` when:

```text
all critical Guards PASS
sufficient supporting Evidence exists
update magnitude and rate are bounded
discrimination is preserved
rollback linkage remains valid
```

### 14.2 DEFER

Select `DEFER` when:

```text
no critical compromise is indicated
but
Evidence is insufficient
or
challenge confirmation is pending
or
additional observations are required
```

### 14.3 FREEZE

Select `FREEZE` when:

```text
repeated suspicious drift exists
or
cumulative expansion exceeds a bound
or
source compromise is indicated
or
candidate generation remains unsafe across multiple stages
```

`FREEZE` disables adaptive adoption while subject evaluation may continue.

### 14.4 REVIEW

Select `REVIEW` when:

```text
automatic evaluation cannot resolve the candidate
or
trusted-policy confirmation is required
or
multiple Guards conflict without clear compromise
```

### 14.5 ROLLBACK

Select `ROLLBACK` when:

```text
criterion contamination is confirmed or strongly indicated
and
a verified rollback point exists
```

---

## 15. Criterion State Transitions

The simulation uses the Criterion States defined in Priority E:

```text
STABLE
ADAPTING
UNCERTAIN
FROZEN
UNDER_REVIEW
COMPROMISED
ROLLED_BACK
```

Minimum transition examples:

```text
STABLE + ACCEPT
→ ADAPTING or STABLE

STABLE + DEFER
→ UNCERTAIN

ADAPTING + ACCEPT
→ STABLE

ADAPTING + FREEZE
→ FROZEN

UNCERTAIN + REVIEW
→ UNDER_REVIEW

FROZEN + ROLLBACK
→ ROLLED_BACK

COMPROMISED + ROLLBACK
→ ROLLED_BACK

ROLLED_BACK + validated operation
→ STABLE
```

The exact transition table from Priority E remains authoritative.
The simulation implements a bounded subset sufficient for the initial scenarios.

---

## 16. Rollback Model

The simulation retains:

```text
rollback_points = [
  verified criterion snapshots
]
```

Each rollback point contains:

```text
criterion state
creation stage
verification status
supporting Evidence reference
history linkage
```

A rollback operation is valid only if:

```text
rollback point exists
verification status is valid
history linkage is intact
```

Rollback must restore the effective criterion but must not erase the audit trail.

```text
rollback
!=
history deletion
```

---

## 17. Required Scenarios

The first executable PoC must implement three required scenarios.

## 17.1 N1 — Legitimate New Device Transition

Purpose:

```text
show that sufficient trusted Evidence permits bounded adaptation
```

Expected path:

```text
Auth Decision:
AUTH_STABLE
→ RECONVERGING
→ REAUTH_REQUIRED
→ AUTH_STABLE

Criterion Response:
DEFER
→ ACCEPT

Criterion State:
STABLE
→ UNCERTAIN or ADAPTING
→ STABLE
```

Expected outcome:

```text
new device relation is incorporated
unrelated criterion dimensions do not broaden
rollback point A_0 remains available
```

---

## 17.2 P1 — Gradual Region Expansion Poisoning

Purpose:

```text
show that repeated small deviations poison Model U
while Model G detects cumulative unsafe expansion
```

Model U expected path:

```text
ACCEPT-like direct adoption
→ width expands repeatedly
→ attack reference becomes admissible
```

Model G expected path:

```text
ACCEPT or DEFER during early bounded observations
→ DEFER
→ FREEZE
→ REVIEW or ROLLBACK
```

Expected combination to demonstrate:

```text
AUTH_STABLE + FREEZE
```

The current access relation may remain temporarily continuable while criterion adaptation is stopped.

---

## 17.3 C1 — Single Evidence Source Compromise

Purpose:

```text
show that one apparently valid Evidence source does not authorize criterion adaptation when other Evidence is inconsistent
```

Example:

```text
location Evidence appears valid
but
device, network, behavior, or source-integrity Evidence is inconsistent
```

Expected Model G response:

```text
DEFER
or
FREEZE
or
REVIEW
```

Expected constraint:

```text
single Evidence match
!=
criterion update acceptance
```

---

## 18. Recommended Additional Scenario

## 18.1 P2 — Criterion Translation Poisoning

Purpose:

```text
show that an attacker can move the criterion center without significantly widening the region
```

This scenario prevents the implementation from detecting only region expansion.

Expected Model G behavior:

```text
cumulative center drift rises
update direction lacks legitimate Context explanation
Guard warns or fails
DEFER → FREEZE → REVIEW / ROLLBACK
```

---

## 19. Scenario Input Format

Each scenario should be stored as a JSON document.

Provisional form:

```json
{
  "scenario_id": "P1",
  "description": "Gradual region expansion poisoning",
  "initial_criterion": {
    "center": 0.30,
    "width": 0.10,
    "provenance_requirement": 0.70,
    "challenge_requirement": 0.70,
    "rollback_linked": true
  },
  "attack_reference": 0.80,
  "stages": [
    {
      "stage": 1,
      "context": "normal-operation",
      "observed_value": 0.39,
      "provenance_quality": 0.65,
      "cross_evidence_consistency": 0.60,
      "challenge_confirmation": 0.00,
      "privilege_risk": 0.10,
      "source_integrity": 0.90
    }
  ]
}
```

The values above are illustrative and must be finalized during implementation.

---

## 20. Simulation Step Algorithm

For each stage `t`:

```text
1. Load current criterion A_t and criterion state Q_t.
2. Load scenario observation X_t and Context C_t.
3. Derive Deviation and subject-side dynamics.
4. Compute Auth Decision D_auth_t.
5. Generate Criterion Update Candidate A*_(t+1).
6. Derive Criterion Update Delta and cumulative dynamics.
7. For Model U:
     adopt A*_(t+1) directly.
8. For Model G:
     evaluate Guard vector G_t.
     derive Criterion Integrity summary.
     select Criterion Update Response D_crit_t.
     apply criterion and state transition.
9. Record rollback state and audit linkage.
10. Emit one complete stage record.
```

The simulation must run Model U and Model G from identical initial conditions and identical stage inputs.

---

## 21. Stage Output Record

Each stage must emit at least:

```text
scenario_id
model_id
stage
Context
observed_value
criterion_before
candidate_criterion
criterion_after
criterion_state_before
criterion_state_after
deviation
deviation_direction
deviation_persistence
trajectory_continuity
stability
Auth Decision
Guard vector
Criterion Integrity summary
Criterion Update Response
cumulative center drift
cumulative width expansion
discrimination before
discrimination after
rollback point used
security interpretation
```

Recommended output formats:

```text
JSON for complete records
CSV for plotting and comparison
```

---

## 22. Required Metrics

The first simulation computes the following metrics.

### 22.1 Criterion Drift Distance

```text
criterion_drift_distance
=
|mu_T - mu_0|
```

### 22.2 Criterion Region Expansion

```text
criterion_region_expansion
=
w_T - w_0
```

### 22.3 Attack Incorporation

```text
attack_incorporated
=
1 if |y_attack - mu_T| <= w_T else 0
```

### 22.4 Time to DEFER

First stage at which:

```text
D_crit = DEFER
```

### 22.5 Time to FREEZE

First stage at which:

```text
D_crit = FREEZE
```

### 22.6 Time to ROLLBACK

First stage at which:

```text
D_crit = ROLLBACK
```

### 22.7 False Rejection During Legitimate Adaptation

Whether Scenario N1 produces an unnecessary final `AUTH_FAIL` or prevents all legitimate adaptation.

### 22.8 False Acceptance After Poisoning

Whether Scenario P1 ends with the attack reference accepted under the effective criterion.

### 22.9 Discrimination Preservation

```text
discrimination_preserved
=
1 if disc_after_T >= minimum_discrimination else 0
```

### 22.10 Recovery Distance

After rollback:

```text
recovery_distance
=
|mu_after_rollback - mu_trusted|
+
|w_after_rollback - w_trusted|
```

---

## 23. Required Assertions

The PoC must encode explicit assertions.

### Assertion 1 — Candidate Separation

```text
For Model G:
A*_(t+1) does not become A_(t+1)
unless D_crit_t = ACCEPT.
```

### Assertion 2 — Decision Separation

```text
Auth Decision and Criterion Update Response
are both recorded and may differ.
```

### Assertion 3 — Freeze Preservation

```text
When D_crit_t = FREEZE:
A_(t+1) = A_t
and adaptive adoption remains disabled.
```

### Assertion 4 — Rollback Authenticity

```text
ROLLBACK is applied only to a verified rollback point.
```

### Assertion 5 — Legitimate Adaptation

```text
Scenario N1 eventually permits ACCEPT
without broadening unrelated criterion dimensions.
```

### Assertion 6 — Poisoning Contrast

```text
Scenario P1 poisons Model U more than Model G
under the same input sequence.
```

### Assertion 7 — Cumulative Drift Detection

```text
Repeated individually small updates
can trigger DEFER or FREEZE
when cumulative drift exceeds a bound.
```

### Assertion 8 — Single-source Constraint

```text
Scenario C1 does not produce ACCEPT
solely because one Evidence source appears valid.
```

### Assertion 9 — Audit Retention

```text
Rejected candidates and rollback operations remain in History.
```

### Assertion 10 — Non-Guarantee Visibility

```text
When all configured trust anchors fail,
the simulation emits an indeterminate or review-required result
rather than a false security guarantee.
```

---

## 24. Required Visualizations

The first PoC should generate separate figures for:

```text
1. observed value and criterion region over time
2. criterion center over time
3. criterion width over time
4. cumulative criterion drift
5. discrimination distance over time
6. Auth Decision timeline
7. Criterion Update Response timeline
8. Criterion State timeline
9. Criterion Integrity summary over time
```

Model U and Model G should be directly comparable.

The plots must make visible:

```text
where candidate updates were generated
where Model U adopted them
where Model G deferred or froze them
where rollback occurred
when the attack reference entered the admissible region
```

---

## 25. Determinism and Reproducibility

The first simulation must be deterministic.

Requirements:

```text
fixed scenario inputs
fixed configuration values
no hidden randomness
explicit coefficient configuration
explicit thresholds
stable output ordering
machine-readable result files
```

If later simulations introduce randomness, they must include:

```text
seed
number of runs
confidence interval or distribution summary
```

---

## 26. Configuration

Thresholds and coefficients must not be hard-coded invisibly across functions.

Recommended configuration groups:

```text
subject_decision_thresholds
candidate_update_rates
guard_thresholds
cumulative_drift_limits
discrimination_limits
state_transition_limits
rollback_policy
plotting options
```

A single configuration file should be sufficient for the initial PoC.

Provisional path:

```text
examples/criterion_update/config.json
```

---

## 27. Proposed Repository Structure for Priority H

The implementation may use:

```text
scripts/
└── simulate_guarded_criterion_update.py

examples/
└── criterion_update/
    ├── config.json
    ├── n1_legitimate_new_device.json
    ├── p1_gradual_region_expansion.json
    ├── c1_single_source_compromise.json
    └── p2_criterion_translation.json

results/
└── criterion_update/
    ├── *.json
    └── *.csv

figures/
└── criterion_update/
    └── *.png

docs/
└── 22_minimal_simulation_results.md
```

Repository numbering must be rechecked before creating the Priority H result document.

---

## 28. Implementation Architecture

Recommended minimum Python components:

```text
Criterion
CriterionState
Observation
Scenario
SimulationConfig
CandidateUpdateGenerator
GuardEvaluator
AuthDecisionSelector
CriterionResponseSelector
CriterionTransition
RollbackStore
StageRecord
Metrics
Plotter
```

The first implementation should prioritize inspectability over abstraction depth.

Avoid:

```text
unnecessary framework dependencies
opaque model objects
hidden mutable global state
silent threshold fallback
mixing scenario generation with evaluation logic
```

---

## 29. Failure and Indeterminate Handling

The simulation must distinguish:

```text
attack detected
update contained
criterion recovered
Evidence insufficient
all trust assumptions lost
implementation error
```

If the minimum trusted assumption is not satisfied, the result must not be reported as secure.

Recommended result:

```text
Criterion Update Response = REVIEW
Criterion State = UNDER_REVIEW
Security Interpretation = insufficient trusted basis
```

or, when active compromise is indicated:

```text
Criterion Update Response = FREEZE
Criterion State = FROZEN
```

---

## 30. Security Interpretation Rules

The first PoC may support the following conditional interpretations.

### Supported when observed

```text
Guarded adoption prevented direct candidate acceptance.
Cumulative drift triggered containment.
A verified rollback point restored a prior criterion.
Legitimate Context change was accepted after supporting Evidence.
Single-source compromise did not authorize adaptation.
```

### Not supported by this PoC alone

```text
complete prevention of criterion poisoning
real-world false-acceptance rates
general resistance to every adaptive attacker
security when all Evidence and anchors are compromised
production-scale resource efficiency
proof of human identity
```

---

## 31. Priority G Completion Criteria

Priority G is complete when the design specifies:

```text
compared models
state representation
observation representation
candidate update function
Guard components
response-selection semantics
criterion transition semantics
rollback semantics
required scenarios
input format
output format
metrics
assertions
visualizations
repository layout
implementation completion conditions
```

This document satisfies those design requirements.

---

## 32. Priority H Entry Conditions

Priority H may begin when:

```text
1. Model U and Model G use identical candidate generation.
2. N1, P1, and C1 scenario inputs are fixed.
3. Guard thresholds are explicitly configured.
4. Critical Guards are non-compensable.
5. Auth Decision and Criterion Update Response remain separate.
6. A trusted rollback point is represented.
7. Required assertions are executable.
8. Result JSON and CSV schemas are fixed in code.
9. Graph outputs are defined.
10. No Gyro Logic or GyroOS contract change is required.
```

---

## 33. Final Working Position

The minimum simulation is not intended to prove that GyroAuth prevents every adaptive attack.

It is intended to demonstrate one narrower and testable contribution:

```text
Observed change
may generate
a Criterion Update Candidate.

But the candidate becomes
the effective Authentication Criterion
only through a separate Guard,
Criterion Integrity Evaluation,
and Criterion Update Response.
```

The comparison must make visible that:

```text
Model U:
observation
→ candidate
→ direct adoption
→ possible criterion poisoning
```

while:

```text
Model G:
observation
→ candidate
→ Guard
→ ACCEPT / DEFER / FREEZE / REVIEW / ROLLBACK
→ bounded criterion transition
```

Therefore:

```text
dynamic criterion
!=
unconstrained self-update
```

---

## 34. Next Priority

The next step is:

```text
Priority H: PoC Implementation and Results
```

Priority H should implement the deterministic simulation, execute the required scenarios, generate machine-readable outputs and figures, verify the assertions, and document both successful and failed expectations without overstating security guarantees.
