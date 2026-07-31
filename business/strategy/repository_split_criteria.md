# Repository Split Criteria

## Current Decision

Keep the business workspace in this repository under `business/` during the exploratory phase.

## Keep It Here While

- materials can remain public;
- documents depend directly on GyroAuth research artifacts;
- commercialization is exploratory;
- there is no independent product release cycle;
- no customer-confidential information is included.

## Consider a Separate Repository When

- a product prototype or integration has its own release lifecycle;
- a different license or access policy is required;
- external collaborators require restricted access;
- customer-specific or NDA-controlled material is created;
- product operations become separate from research development.

## Storage Boundary

Do not place secrets, credentials, raw customer logs, personal data, confidential pricing, contracts, or restricted security information in this public repository.

## Review Milestones

Review this decision when the project reaches:

1. the first external interview;
2. the first formal PoC proposal;
3. the first confidential dataset or NDA;
4. the first commercial integration component;
5. the first paid engagement;
6. an independent release or support process.

## Split Decision Record

Document the reason, visibility, ownership, license, source-of-truth rule, release policy, and artifacts affected by any future split.
