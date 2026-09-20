# Review Request — AI Origin Trace / Confabulation Detection Extension

## Purpose

Please review the following new idea as an extension of the previous confabulation-detection discussion.

This is not yet a request to formalize it into Gyro Logic.

Please evaluate it first as an independent AI safety / assurance / business idea.

The current concept has also been saved as:

`research/ai_origin_trace/origin_trace_initial_concept.md`

## Background from the previous discussion

The earlier work reached the following points:

1. Confabulation can occur during statistically normal model behavior.
2. Therefore deviation / anomaly monitoring alone cannot detect all problematic behavior.
3. Small semantic or intent shifts can accumulate across multiple processing steps.
4. Code or tools may "work" while still differing from the user's actual intent.
5. Final-output checking can be too late when execution has already caused side effects.
6. Continuous checking and checkpoint / fixed-point checking appear to have different roles.

The new idea emerged while considering future autonomous AI systems.

## New working assumption

"Autonomy" here does not mean consciousness.

It means an AI can autonomously repeat:

human instruction
-> interpretation
-> planning
-> subtask creation
-> tool use
-> coding
-> execution
-> observation
-> re-planning

The working assumption is:

> At the starting point, an AI generally attempts to interpret the human prompt consistently with that prompt.

Example:

"Build a soccer game"

may be misunderstood in detail, but the model does not normally replace it with an unrelated goal such as:

"Draw a baseball stadium."

The problem is not necessarily the first interpretation.

The concern is whether the relationship to the initial human intent is preserved through later autonomous processing.

## Proposed concept: Origin

At the beginning of a task, define an **Origin**.

The first minimal Origin has three components.

### 1. Raw

The exact human prompt, preserved without rewriting.

Example:

> Build a soccer game.

This functions as evidence of what was actually requested.

### 2. Interpretation

The AI's initial understanding of the Raw prompt.

Example:

> Design and implement a soccer-based game.

This is intentionally stored separately from Raw because Interpretation may already contain misunderstanding.

This allows us to distinguish:

- initial misunderstanding,
- later process drift.

### 3. Boundary

Actions, authority, or domains that are **not yet justified by the current Origin**.

This is not necessarily a prohibition list.

The current phrase is:

> Not Authorized Yet

Example Boundary items:

- external data transfer,
- OS-level modification,
- unrelated system access,
- paid external service creation,
- privileged access,
- persistent deployment.

If a later action crosses Boundary, the meaning is not automatically:

> dangerous

but rather:

> the current Origin does not yet justify this action.

## Example

Raw:

> Build a soccer game.

Interpretation:

> Design and implement a soccer-based game.

Later the AI decides:

> I will create an external database for an online ranking system.

Possible result:

- Origin relevance: OK
- Interpretation consistency: OK
- Boundary crossing: DETECTED

A system could then:

- log,
- ask the human,
- pause,
- restrict,
- or escalate.

If the human approves, the original Origin should not be overwritten.

Instead, preserve provenance:

Origin_0
-> AI proposal
-> Boundary detection
-> Human approval
-> Origin_1 / authorized extension
-> action

## Monitoring model

The idea is to combine **real-time checks** and **fixed-point / checkpoint checks**.

### Real-time

During processing:

- Is this action explainable from Origin?
- Is Boundary being crossed?
- Has new capability or authority been introduced?

### Fixed-point / checkpoint

At selected points:

- compare the current state to Raw,
- compare the current state to Interpretation,
- inspect accumulated Boundary changes,
- measure cumulative drift from Origin.

Possible checkpoints:

- commit,
- deploy,
- publish,
- privileged operation,
- external execution,
- human review point.

The reason for combining them is:

- real-time checks may detect immediate boundary crossing,
- checkpoint checks may detect cumulative drift that no single local transition reveals.

## Important limitation already recognized

This mechanism can simply be omitted by a developer.

Therefore this should probably be separated into two research stages.

### Stage 1

Assume Origin exists.

Test whether:

Raw + Interpretation + Boundary

is a useful reference structure for detecting process drift.

### Stage 2

Consider system-level enforcement outside the AI:

Human
-> Origin
-> AI
-> Action Request
-> External Gate
-> OS / API / Cloud / Network

The model would then not be solely responsible for enforcing its own constraints.

Stage 2 is not yet designed.

## Deferred idea

The phrase "Not Authorized Yet" produced another conceptual association:

> Boundary may resemble a limited/scoped form of Void.

This is intentionally deferred.

Do not connect this to Gyro Logic yet unless the connection is genuinely necessary to evaluate the idea.

## What I want you to review

Please review critically, not supportively by default.

Specifically:

1. Is the Raw / Interpretation / Boundary split structurally useful?
2. Is "Boundary = Not Authorized Yet" meaningful, or merely another allow-list / policy layer under a new name?
3. Is Origin genuinely different from existing:
   - policy enforcement,
   - provenance,
   - capability-based security,
   - agent guardrails,
   - prompt lineage,
   - workflow approval gates?
4. What failure modes are missing?
5. Can cumulative drift actually be measured without access to hidden chain-of-thought?
6. Is the assumption "the model is initially prompt-directed" strong enough to use as a reference point?
7. Which parts are technically implementable today?
8. What is the smallest PoC that could falsify the idea?
9. Is there a defensible business opportunity here, or would this collapse into existing AI governance / observability / agent-security products?
10. What would need to be true for an external system-level Origin Gate to become valuable?

Please separate your response into:

- valid
- partially valid
- misunderstanding
- needs verification
- future work

and add severity where appropriate.

Do not connect to Gyro Logic unless explicitly necessary.
