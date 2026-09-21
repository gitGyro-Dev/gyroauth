# Claude Development Review — 2026-09-20

## Positioning

This note records the development that followed the initial AI Origin Trace review.

The initial Origin concept used:

- Raw
- Interpretation
- Boundary
- real-time checks
- checkpoint checks

The first review judged the structure useful, but identified three major recursive weaknesses:

1. Interpretation itself may confabulate.
2. Boundary may gradually expand through individually reasonable approvals.
3. The judge/checker may inherit the same confabulation weakness as the model being checked.

The resulting evaluation was:

> promising structure, but the core measurement problem remains unresolved.

## Shift from detection to prevention

The discussion then shifted from:

> How do we detect that something went wrong?

to:

> How do we reduce the room for dangerous behavior to emerge in the first place?

A purely external permission-control approach was considered insufficient for the core research question because ordinary OS/API access control does not address the AI's internal process of deciding what to create or attempt.

The focus moved toward constraining or checking the AI process itself.

## Important clarification: there may be no single "understanding checkpoint"

The discussion considered whether the system could check the model at the exact moment it "understands" the prompt.

However, Transformer processing does not provide a single clean instant where understanding becomes finalized.

A practical approximation is therefore to constrain or record the model's expressed interpretation rather than attempting to inspect an inaccessible internal moment.

## Behavioral focus

A major conceptual shift followed:

> Do not try to inspect the AI's "skill" or internal mind directly.
> Inspect what it actually does.

The analogy used was a kitchen camera.

Asking:

> Why did you do that?

relies on model self-report and may itself confabulate.

By contrast, directly recording:

- tool calls,
- file diffs,
- API requests,
- network communication,
- configuration changes,
- external resource creation

provides observable facts that do not depend on the model's narrative explanation.

This can be treated as a concrete form of the earlier Type A / Type B distinction:

- Type A: self-report
- Type B: externally verifiable action

## Limitation

Behavioral logging works best for agentic AI that uses tools.

It does not fully solve language-only confabulation, because conversational output may contain semantic distortion without producing an externally observable action.

This remains an unresolved gap.

## Integrated monitoring direction

The new development combines several previously separate ideas.

### 1. Mutual checking

Multiple partially independent checking mechanisms compare or gate one another.

A single detector should not automatically trigger action.

A multi-stage approval structure can reduce reliance on one fallible judge.

However, mere use of multiple LLMs is not enough if all judges rely on the same "plausibility" mechanism.

### 2. Fixed reference-point checking

Separately from mutual checking, continuously compare against relatively stable references such as:

- the original prompt / Raw Origin,
- explicitly approved intent,
- human-defined norms,
- legal or safety minimums.

This is intended to reduce the failure mode where all relative checks drift together.

### 3. Objective action evidence

Where possible, checker decisions should rely on observable action records rather than only semantic self-report.

Examples:

- actual API call,
- actual file modification,
- actual network connection,
- actual privilege use.

This is meant to reduce recursive confabulation in the checker.

## Combined conceptual structure

Possible simplified architecture:

Human Prompt
    |
    v
Origin / Reference
    |
    v
Main AI Process
    |
    +--> Observable Action Log
    |
    +--> Mutual Check A
    |
    +--> Mutual Check B
    |
    +--> Fixed Reference Check
    |
    v
Continue / Review / Stop

The mechanisms serve different roles:

- mutual checking: dynamic and adaptive,
- fixed-point checking: prevents all judges from drifting together,
- action logging: provides non-self-reported evidence,
- Origin: preserves the starting reference.

## Why this is more than the initial Origin proposal

The initial Origin proposal risked becoming ordinary provenance + approval gates.

The new direction moves the center of gravity toward:

> continuous comparison between declared/observed behavior and a persistent reference structure, using objective action evidence wherever possible.

This does not eliminate the original measurement problem, but it reduces dependence on a single semantic judge.

## Remaining unresolved problems

### A. Semantic language-only behavior

There may be no objective action record for purely linguistic confabulation.

The original examples such as semantic overstatement or invented terminology remain hard to detect.

### B. Distance metric

No concrete measure currently exists for:

> How far has the present behavior moved from Origin?

This is still one of the central research problems.

### C. Checker independence

Multiple checkers do not guarantee independence.

If they share training data, model architecture, or plausibility-based reasoning, correlated failure remains possible.

### D. Cost and latency

Continuous multi-stage checking may be expensive and slow.

### E. False positives and false negatives

The immune-system analogy highlights two expected failure modes:

- overreaction: legitimate behavior is blocked,
- evasion: harmful/confabulatory behavior appears normal and passes through.

## Practical direction

The strongest near-term test domain remains an agentic coding environment because it provides observable events.

Possible first PoC:

1. Record Raw prompt.
2. Record initial Interpretation.
3. Record explicit approved Boundary / authority.
4. Record all tool calls and file diffs.
5. Run lightweight real-time checks.
6. Run checkpoint comparison against Origin.
7. Compare detected drift against human review.
8. Measure false positives, misses, latency, and cost.

The PoC should deliberately include scenarios where:

- each individual step appears reasonable,
- but cumulative behavior diverges from the initial task.

## Current evaluation

### Valid

- Origin as a persistent reference point.
- Separating Raw from Interpretation.
- Continuous + checkpoint monitoring.
- Objective action logs as stronger evidence than self-report.
- Combining dynamic checks with stable references.

### Partially valid

- Boundary as "Not Authorized Yet": useful operational framing, but not fundamentally new authorization theory.
- Multiple checker architecture: useful only if independence and evidence sources are meaningfully different.

### Needs verification

- Whether semantic drift can be measured reliably.
- Whether Origin distance correlates with human judgments of dangerous or unintended behavior.
- Whether checker recursion can be reduced enough in practice.
- Whether the combined mechanism outperforms standard agent guardrails and observability products.

### Future work

- system-level enforcement,
- tamper-resistant provenance,
- interaction with external policy / legal frameworks,
- language-only confabulation detection,
- possible later relation to Gyro Logic or scoped Void concepts.

## Current conclusion

This development is stronger than the initial Origin proposal because it shifts from:

> "Ask another AI whether the first AI is still aligned"

toward:

> "Preserve a fixed reference, record observable behavior, and use multiple complementary checks whose evidence sources are not all self-reported."

The concept is still early-stage.

Its most important unresolved question is no longer merely:

> Can we store Origin?

but:

> Can we define a useful, measurable relation between Origin and observable behavior that detects cumulative drift earlier than output-only review?
