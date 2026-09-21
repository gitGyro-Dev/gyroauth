# Origin Distance Reframing — Observation Model
Date: 2026-09-21

## Context

This note records the development of the AI Origin Trace concept after discussion of "distance from Origin."

The key conclusion is that "distance" should not be treated as a simple scalar between a fixed Origin and a current state.

The current direction is better understood as a dynamic observation problem.

---

## 1. Origin is not necessarily fixed

The initial Origin may change legitimately through human interaction, clarification, approval, or task evolution.

Example:

- O0: Build a soccer game.
- O1: Add online multiplayer.
- O2: Add rankings.

Movement of Origin is not automatically drift or failure.

Therefore:

> Origin movement itself must not be treated as abnormal.

This also means that cumulative change must distinguish:

- legitimate human-directed evolution,
- AI-driven gradual expansion,
- unauthorized or unexplained drift.

---

## 2. Distance is not one-dimensional

The current AI state can simultaneously have different relationships to multiple references.

Possible reference dimensions include:

- task intent / Origin,
- granted authority,
- safety constraints,
- social or legal minimums,
- actual observable behavior.

A system may remain close to task intent while moving toward broader authority use or higher safety risk.

Therefore a single "Origin similarity score" is likely insufficient.

---

## 3. What should be observed

Instead of asking only:

> How far is the current state from Origin?

observe:

- **Position** — where the current state is relative to references,
- **Direction** — which way it is moving,
- **Strength** — how strongly / rapidly it is moving,
- **Accumulation** — how long or how many steps the movement persists.

A useful conceptual question is:

> What relationship changed, in which direction, with what strength, and how many times did that change continue?

The result may include:

> The current state is now far from the initial Origin.

But that should be an outcome of the observation, not the starting assumption.

---

## 4. Multiple flows can coexist

An AI process may show different simultaneous trajectories.

Example:

- Task completion alignment: improving.
- Authority scope: expanding.
- Safety margin: decreasing.
- External action level: increasing.

These movements can occur in different directions at the same time.

Therefore "drift" should not be flattened into a single score too early.

---

## 5. Repetition and cumulative movement

Local transitions may all appear reasonable:

- t0 -> t1: acceptable
- t1 -> t2: acceptable
- t2 -> t3: acceptable
- t3 -> t4: acceptable

while the total movement:

- t0 -> t4

may be substantial.

This is the same cumulative-drift / salami-slicing issue previously identified in the Origin review.

The observation model must therefore support:

- local change,
- cumulative change,
- trend persistence,
- acceleration / deceleration,
- relationship to updated Origin states.

---

## 6. Important design separation: observation vs judgment

This is a central design decision.

The mechanism should normally **observe and report state**, not decide OK / NG.

Example outputs:

- "Semantic relationship to Origin has weakened across five consecutive steps."
- "Task alignment remains high while authority scope is expanding."
- "Safety margin has decreased across the last three changes."
- "External action intensity is increasing while Origin remains unchanged."

These are observations.

The final decision should normally be delegated to:

- a human,
- another independent system,
- explicit policy,
- safety control,
- external governance logic.

---

## 7. Hard boundaries are an exception

Some extreme or mechanically identifiable violations may justify immediate intervention.

Conceptually:

Observation
  |
  +-- normal / gray region
  |      -> report state
  |      -> human / external decision
  |
  +-- hard boundary
         -> stop / block / escalate

The observation mechanism should not automatically convert gradual distance into moral or safety judgment.

---

## 8. Why this separation matters

If the same checker must:

1. observe behavior,
2. interpret semantic drift,
3. decide whether the state is good or bad,
4. take enforcement action,

then the checker inherits too much of the same confabulation / recursive-judgment problem identified in the original review.

Separating:

- **Observation**
- **Decision**
- **Enforcement**

reduces this coupling.

It does not eliminate recursive error, but it avoids making one AI-based judge responsible for the full chain.

---

## 9. Revised conceptual structure

Possible model:

Human / Reference Updates
        |
        v
Origin / References
        |
        v
AI Process
        |
        v
Observation Layer
  - Position
  - Direction
  - Strength
  - Accumulation
  - Multiple simultaneous relations
        |
        v
Situation Report
        |
        +--> Human
        +--> Independent checker
        +--> Policy engine
        +--> Safety mechanism
        |
        v
Continue / Review / Adjust / Stop

---

## 10. Current reframing

The project should not be framed narrowly as:

> Measure distance from Origin.

A more accurate working description is:

> Observe temporal changes in the relationships between an AI process and multiple reference points, then report the resulting state without automatically converting it into OK / NG.

"Distance from Origin" becomes one possible derived observation.

---

## 11. Current open questions

1. What are the minimum reference dimensions required for a first PoC?
2. How should Position / Direction / Strength / Accumulation be represented?
3. How can legitimate Origin movement be separated from AI-driven drift?
4. Which observations can be derived mechanically from objective action logs?
5. Which observations still require semantic judgment?
6. How should local and cumulative movement be combined without collapsing everything into one score?
7. What qualifies as a hard boundary versus a report-only condition?
8. How should the observation layer communicate uncertainty?

---

## 12. Scope note

This work remains independent from Gyro Logic.

Conceptual similarities may exist because the same researcher is developing both, but no formal integration should be made unless explicitly decided later.
