# 15. GyroOS vNext Consumption Boundary Design

---

## 1. Purpose

This document defines integration gate D:

```text
GyroOS public experimental record API
↓
GyroAuth read-only consumer boundary
```

The purpose is to allow GyroAuth to consume explicitly selected GyroOS vNext experimental records without collapsing GyroOS semantics into authentication decisions.

The layer direction remains:

```text
Gyro Logic
↓
GyroOS
↓
GyroAuth
```

GyroOS must not depend on GyroAuth.

---

## 2. Verified GyroOS Source Boundary

The initial source contract is the verified GyroOS public experimental API:

```text
GET /vnext/experimental/records/{record_id}
GET /vnext/experimental/records
```

The source returns opaque:

```text
ExperimentalRecordEnvelope
```

Initial GyroAuth consumption is read-only.

GyroAuth must not initially call:

```text
POST /vnext/experimental/records
DELETE /vnext/experimental/records/{record_id}
```

Decision:

```text
GyroOS source contract
= READ-ONLY EXPERIMENTAL RECORD RETRIEVAL
```

---

## 3. Consumer-side Separation

The following must remain distinct:

```text
GyroOS ExperimentalRecordEnvelope
≠ GyroAuth authentication request

GyroOS ExperimentalRecordEnvelope
≠ GyroAuth authentication result

GyroOS RuntimeSnapshot
≠ GyroAuth session state

GyroOS StabilityScene
≠ AUTH_STABLE

GyroOS ContinuityRelationRecord
≠ identity proof

GyroOS TrajectoryGraph
≠ authentication trajectory
```

A GyroOS record is source evidence or reference material only until GyroAuth applies an explicit consumer-owned mapping.

---

## 4. Initial Consumer Models

The first GyroAuth-side boundary should define:

```text
GyroOSExperimentalRecordReference
GyroOSExperimentalRecordSnapshot
GyroOSConsumptionRequest
GyroOSConsumptionResult
```

### GyroOSExperimentalRecordReference

Suggested fields:

```text
source_record_id
source_record_type
source_process_id
source_endpoint
```

### GyroOSExperimentalRecordSnapshot

Suggested fields:

```text
reference
payload
source_metadata
retrieved_at
provisional
```

The snapshot copies source content into a GyroAuth-owned immutable observation boundary.

It does not establish semantic equivalence.

### GyroOSConsumptionRequest

Suggested fields:

```text
source_record_id
expected_record_type
expected_process_id
consumer_context
```

`expected_record_type` and `expected_process_id` are caller-supplied checks only.

### GyroOSConsumptionResult

Suggested fields:

```text
snapshot
accepted
rejection_reason
warnings
```

`accepted` means accepted for consumer-side inspection, not authentication accepted.

---

## 5. Initial Consumer Service

Proposed service:

```text
GyroOSExperimentalRecordConsumer
```

Initial operation:

```text
consume(request)
→ GyroOSConsumptionResult
```

Responsibilities:

```text
retrieve one explicit record by ID
verify optional expected process ID
verify optional expected record type
copy payload and metadata
record retrieval warnings
return a consumer-owned snapshot
```

Non-responsibilities:

```text
calculate auth_score
select auth_state
select next_action
infer identity continuity
infer attack
infer recovery
infer reauthentication
infer trajectory continuity
persist into canonical GyroAuth state
```

---

## 6. Mapping Boundary

No automatic mapping is approved between GyroOS record types and GyroAuth meanings.

The following mappings are forbidden in the initial D scope:

```text
StabilityScene → AUTH_STABLE
ContinuityRelationRecord → identity continuity
TrajectoryGraph → observed_access_trajectory
RuntimeSnapshot → authentication context
DifferenceObject → deviation_risk
BoundaryEvaluation → attack classification
OperatorResponse → next_action
```

Future mappings must be explicit, versioned, testable, and owned by GyroAuth.

A future mapping should have the form:

```text
GyroOS source snapshot
+
GyroAuth mapping policy
+
GyroAuth risk context
→ GyroAuth interpretation
```

not:

```text
GyroOS source snapshot
→ authentication decision
```

---

## 7. Transport Boundary

Initial transport options:

```text
A. direct HTTP GET from GyroOS experimental API
B. caller-supplied ExperimentalRecordEnvelope payload
C. exported JSON artifact supplied out of band
```

Initial implementation should select one transport only.

Recommended first transport:

```text
caller-supplied envelope adapter
```

Reason:

```text
no network dependency in core tests
no endpoint configuration coupling
no retry/authentication complexity
mapping boundary can be tested independently
```

Direct HTTP transport should be a later adapter behind the same consumer contract.

---

## 8. Error Boundary

The consumer must distinguish:

```text
source record unavailable
source payload invalid
record type mismatch
process ID mismatch
unsupported source record type
consumer mapping absent
transport failure
```

These errors must not be converted automatically into:

```text
AUTH_FAIL
REAUTH_REQUIRED
attack detected
identity break
trajectory break
```

Initial failure behavior:

```text
consumption rejected
+
explicit reason
+
no authentication state mutation
```

---

## 9. Version and Compatibility Boundary

The initial source contract should record:

```text
source API namespace
source contract label
record type label
consumer contract version
```

The consumer must reject or warn on incompatible contract labels rather than silently reinterpret payloads.

No schema registry is required initially.

---

## 10. Authentication Boundary

GyroAuth may use its own credentials to access GyroOS in a future HTTP adapter.

However:

```text
transport authentication
≠ GyroAuth subject authentication
```

The bearer token protecting the GyroOS API is service-access authentication only.

It must not be treated as evidence about the end user being authenticated by GyroAuth.

---

## 11. Persistence Boundary

Initial D consumption remains in-memory and request-local.

Do not write consumed snapshots into:

```text
canonical authentication session state
identity reference
observed access trajectory
admissible trajectory set
existing persistent auth history
```

until a separate persistence and ownership review is completed.

---

## 12. Layer Consistency Check

```text
GyroOS depends on GyroAuth
= NO

GyroAuth consumes GyroOS source records
= YES

GyroOS semantics automatically become auth semantics
= NO

GyroOS OperatorResponse controls GyroAuth next_action
= NO

Continuity relation proves identity
= NO

Trajectory graph becomes authentication trajectory
= NO

Existing /auth/step behavior changed
= NO

Existing /loop/step behavior changed
= NO
```

---

## 13. Proposed Implementation Sequence

```text
D1. consumer-side public models and settings
↓
Review
↓
D2. caller-supplied envelope adapter and consumer service
↓
Review
↓
D3. optional read-only HTTP transport adapter
↓
Actions verification
↓
D Review
```

D3 should remain optional. D can be completed initially with D1-D2 if the consumer boundary is the primary objective and network integration is not yet required.

---

## 14. Final Design Decision

```text
D GyroAuth consumption boundary design
= COMPLETE

Initial source
= GYROOS EXPERIMENTAL RECORD ENVELOPE

Initial direction
= READ-ONLY

Initial transport
= CALLER-SUPPLIED ENVELOPE ADAPTER RECOMMENDED

Automatic authentication mapping
= NOT APPROVED

Canonical GyroAuth persistence
= NOT APPROVED

Direct HTTP integration
= DEFERRED TO OPTIONAL D3

Critical design blocker
= NONE IDENTIFIED
```

Proceed next to:

```text
D1. consumer-side public models and settings
```

Do not implement authentication-state mapping, identity continuity inference, next-action selection, or canonical persistence before a separate review explicitly approves them.