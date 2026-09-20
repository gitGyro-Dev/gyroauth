# AI Origin Trace — Initial Concept

## Positioning

This note records an early-stage AI safety / assurance idea.

It is intentionally kept separate from Gyro Logic formalization for now.

The idea emerged from prior confabulation-detection work:
- deviation monitoring can miss behavior that is statistically normal for the model,
- small interpretation shifts can accumulate,
- output-only inspection can be too late,
- continuous checks and checkpoint reviews may need to be combined.

## Problem

Future AI systems may increasingly:
- receive a human instruction,
- interpret the goal,
- plan,
- create subtasks,
- call tools,
- write code,
- execute actions,
- observe results,
- re-plan,
- continue without human confirmation at every step.

This does not require human-like consciousness.

The safety problem is that each local step may look reasonable while the total process gradually moves away from the original human intent.

A final output check is necessary, but may be too late after code execution, external access, data transfer, configuration changes, persistent resource creation, or other side effects.

## Working assumption

At the starting point, an AI generally attempts to interpret and respond consistently with the human prompt.

Example:

Raw prompt:

> Build a soccer game.

The model may misunderstand details or over-interpret, but the working assumption is that it does not normally replace the task with an unrelated objective such as:

> Draw a baseball stadium.

The important question is:

> Can the relationship between the initial human intent and later AI actions be preserved and checked throughout the process?

## Origin

The current minimal proposal is to define an Origin at the beginning of an AI task.

Origin is not a complete safety policy.
It is a reference point for later comparison.

### Raw

The exact human input, preserved without AI rewriting.

Example:

> Build a soccer game.

Role:
- evidence of what the human actually requested,
- stable reference for later comparison,
- protection against retrospective reinterpretation.

### Interpretation

The AI's initial interpretation of Raw.

Example:

> Design and implement a game based on soccer.

Role:
- record the first machine-side understanding,
- compare Raw and the initial interpretation,
- distinguish initial misunderstanding from later drift.

Interpretation is itself AI-generated and may be wrong.

### Boundary

Actions, authority, or domains that are not yet justified by the Origin.

Boundary is not necessarily a prohibition list.

Current meaning:

> Not Authorized Yet

Examples:
- external data transfer,
- external account creation,
- charging money,
- OS configuration changes,
- unrelated system access,
- persistent external deployment,
- privileged access.

Crossing Boundary does not automatically mean dangerous.

It means:

> The current Origin alone does not yet justify this action.

## Example

Raw:

> Build a soccer game.

Interpretation:

> Design and implement a soccer-based game.

Later:

> Create an external database for an online ranking system.

Possible check result:
- Origin relevance: OK
- Interpretation consistency: OK
- Boundary crossing: DETECTED

Possible responses:
- log,
- request human approval,
- pause,
- restrict,
- escalate.

If approved, do not overwrite the original Origin.

Preserve provenance:

Origin_0
-> AI proposal
-> Boundary detection
-> Human approval
-> Origin_1 / authorized extension
-> action

## Real-time check and checkpoint check

### Real-time check

Lightweight, continuous checking during the AI process.

Possible questions:
- Is the current action still explainable from Origin?
- Has Boundary been crossed?
- Has a new capability or external dependency been introduced?
- Is the current action still connected to the initial Interpretation?

### Checkpoint check

At selected points, review the accumulated trajectory from Origin to the current state.

Possible triggers:
- commit,
- deploy,
- publication,
- external execution,
- privilege escalation,
- resource creation,
- scheduled interval,
- explicit human checkpoint.

Purpose:
- detect cumulative drift,
- inspect chains where each local step looked reasonable,
- compare current state with Raw + Interpretation + Boundary.

## Why both may be necessary

Real-time checks alone can miss cumulative drift.

Origin -> P1 -> P2 -> P3 -> P4

Each adjacent transition may look reasonable, while Origin -> P4 may no longer fit the initial task.

Checkpoint review provides a longer-range comparison.

Conversely, checkpoint review alone may be too late for irreversible actions.

Current direction:

> Real-time monitoring + periodic origin-based cumulative review

## Current limits

This concept is not yet:
- a complete alignment method,
- a complete authorization framework,
- a replacement for output inspection,
- a replacement for laws, regulation, model evaluation, or sandboxing,
- a guarantee against malicious developers,
- a guarantee against systems that omit Origin.

## System-level follow-up

A developer can simply choose not to implement Origin.

Therefore a later research direction is external enforcement:

Human
-> Origin
-> AI
-> Action Request
-> External Gate
-> OS / API / Cloud / Network / Infrastructure

In such a structure, the AI would not be solely responsible for enforcing its own constraints.

This is future work and not part of the first PoC.

## Minimal next step

Start with:
1. Raw
2. Interpretation
3. Boundary
4. process event log
5. real-time comparison
6. checkpoint comparison

First experiment:

> Can this minimal Origin structure detect meaningful drift that ordinary output checks or local step checks miss?

## Open questions

- How should Interpretation be generated?
- Should another model verify Raw <-> Interpretation?
- How should Boundary be derived?
- Which Boundary items should be universal versus task-specific?
- How should approvals extend Origin without destroying provenance?
- How should cumulative drift be measured?
- Which events require blocking versus logging?
- What is the smallest useful event schema?
- How much internal reasoning is actually observable or necessary?
- How should the approach work with closed models versus local/open models?
- How should external enforcement work when Origin support is absent?

## Deferred note

"Not Authorized Yet" may have an interesting conceptual relationship with a limited/scoped form of "Void".

This is intentionally deferred.
It should not be merged into the present Origin design until the Origin mechanism is independently clarified and tested.
