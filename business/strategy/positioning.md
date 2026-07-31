# GyroAuth Commercial Positioning

## Status

Draft for validation. These statements are commercial hypotheses, not established market claims.

## Core Technical Definition

```text
Authentication = Stability-based Selection over State Convergence
```

GyroAuth evaluates whether an authentication relation remains viable under change. It separates:

```text
Current access decision
!=
Future authentication-criterion update decision
```

## Initial Business Position

GyroAuth should initially be positioned as an evaluation and update-control layer that complements existing authentication systems rather than replacing credentials, MFA, IdP, IAM, VPN, or ZTNA products.

Preferred initial form:

```text
Existing authentication and access logs
+ GyroAuth trajectory evaluation
+ guarded criterion-update decision
→ offline report or Shadow Mode evaluation
```

## Audience-Specific One-Sentence Drafts

### Non-technical stakeholder

GyroAuth evaluates not only whether an access looks normal now, but also whether that behavior should be allowed to reshape what the system considers normal in the future.

### CISO / Security Manager

GyroAuth separates current access authorization from adaptive-criterion updates, enabling potentially legitimate access to continue while suspicious learning or baseline expansion is frozen for review.

### Authentication or Security Vendor

GyroAuth is a complementary trajectory-evaluation and criterion-update guard that can sit above existing authentication, IAM, UEBA, or access-control telemetry without requiring immediate replacement of the underlying platform.

### New Business / Innovation Team

GyroAuth provides a testable approach to continuous authentication and adaptive-model governance, starting with low-risk offline log evaluation and progressing to Shadow Mode or step-up authentication integration.

### Researcher

GyroAuth models authentication as stability-based selection over state convergence and explicitly separates subject evaluation from criterion-integrity evaluation.

## Candidate Value Propositions

These require third-party validation:

- prevent unchecked expansion of adaptive authentication criteria;
- distinguish current access continuity from permission to learn from the event;
- identify gradual poisoning or compromised evidence sources;
- reduce unnecessary hard authentication failures by separating re-authentication from relation collapse;
- produce an audit trace explaining both access and criterion-update decisions.

## What GyroAuth Is Not Yet

- a production identity provider;
- a replacement for MFA or credentials;
- a certified security product;
- a statistically validated fraud or intrusion detector;
- a service with production SLA or 24-hour support;
- a general guarantee against account takeover or criterion poisoning.

## Messaging Rule

Always distinguish:

```text
Demonstrated in deterministic research scenarios
```

from:

```text
Validated in real enterprise environments
```

The first is currently supported. The second is a target for PoC and external evaluation.
