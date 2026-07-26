# 19. GyroOS Consumption Boundary Minimal PoC

---

## 1. Purpose

This document records the isolated implementation of integration gate D:

```text
D1 consumer-side public models and settings
D2 caller-supplied envelope adapter and consumer service
D3 optional read-only HTTP transport adapter
```

The dependency direction remains:

```text
Gyro Logic
↓
GyroOS
↓
GyroAuth
```

---

## 2. Added Components

```text
app/vnext/gyroos_consumption.py
app/vnext/gyroos_consumption_service.py
app/vnext/gyroos_http_transport.py
```

Tests:

```text
tests/vnext/test_gyroos_consumption_models.py
tests/vnext/test_gyroos_consumption_service.py
tests/vnext/test_gyroos_http_transport.py
```

Workflow:

```text
.github/workflows/gyroos-consumption-boundary.yml
```

---

## 3. D1 Models and Settings

Added:

```text
GyroOSConsumptionSettings
GyroOSExperimentalRecordReference
GyroOSExperimentalRecordSnapshot
GyroOSConsumptionRequest
GyroOSConsumptionResult
GyroOSHttpTransportSettings
```

The models represent consumer-side references, snapshots, and inspection results only.

They do not define authentication state, score, or action.

---

## 4. D2 Adapter and Consumer

Added:

```text
CallerSuppliedGyroOSEnvelopeAdapter
GyroOSExperimentalRecordConsumer
```

The adapter copies and validates a caller-supplied experimental record envelope.

The consumer checks explicit record identity, process scope, and record type expectations.

The result means:

```text
accepted_for_inspection
```

not authentication acceptance.

---

## 5. D3 HTTP Transport

Added:

```text
GyroOSReadOnlyHttpClient
GyroOSExperimentalRecordHttpAdapter
```

The adapter performs only:

```text
GET /vnext/experimental/records/{record_id}
```

It returns a consumer-side source snapshot.

It does not invoke `/auth/step`, compute scores, select states, or persist sessions.

---

## 6. Explicit Non-mapping Boundary

The implementation does not map:

```text
StabilityScene → AUTH_STABLE
ContinuityRelationRecord → identity continuity
TrajectoryGraph → authentication trajectory
RuntimeSnapshot → authentication context
DifferenceObject → deviation risk
BoundaryEvaluation → attack classification
OperatorResponse → next action
```

---

## 7. Error Boundary

Consumer errors and transport errors remain explicit boundary failures.

They do not automatically become:

```text
AUTH_FAIL
REAUTH_REQUIRED
attack detected
identity break
trajectory break
```

---

## 8. Existing GyroAuth Isolation

Unchanged:

```text
app/vnext/main.py
POST /auth/step
AuthStepRequest
AuthStepResponse
compute_auth_score
decide_auth_state
SESSIONS
VNEXT_HISTORY_CSV
```

---

## 9. Current Decision

```text
D1 models and settings
= IMPLEMENTED

D2 caller-supplied adapter and consumer
= IMPLEMENTED

D3 optional HTTP transport
= IMPLEMENTED

Automatic authentication mapping
= NOT IMPLEMENTED

Canonical GyroAuth persistence
= NOT IMPLEMENTED

Existing /auth/step behavior
= UNCHANGED

GitHub Actions verification
= PENDING
```
