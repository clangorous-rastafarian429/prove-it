# Verification profiles

Choose the smallest profile that adequately covers the consequence of being wrong. Upgrade a profile whenever uncertainty or impact is higher than normal.

## Quick

Use for a localized, low-risk change with an obvious execution path, such as copy, styling, a small pure function, or narrow configuration.

Required evidence:

- inspect the final diff;
- run one focused behavioral or regression check;
- run the cheapest relevant syntax, formatting, compile, or type check when available;
- identify any unverified user-visible behavior.

Quick is not appropriate for security boundaries, data changes, releases, public contracts, or cross-service behavior.

## Standard

Use by default for ordinary features, bug fixes, refactors, dependency changes, and non-trivial configuration.

Required evidence:

- inspect the final diff and working-tree state;
- run focused tests for changed behavior;
- run relevant lint, type, schema, or compile checks;
- run the normal project test or build command when reasonably bounded;
- exercise the primary runtime path when feasible;
- test one important negative or boundary case;
- disclose environmental or coverage gaps.

## Strict

Use for authentication, authorization, payments, privacy, secrets, migrations, destructive operations, concurrency, public APIs, release artifacts, production configuration, or any change with a high cost of failure.

Required evidence:

- satisfy the Standard profile;
- test success, rejection, boundary, and failure paths;
- verify authorization and data isolation where applicable;
- verify migration, rollback, compatibility, or recovery behavior where applicable;
- run the broadest safe project-native suite available;
- verify release or production-shaped artifacts rather than development-only behavior;
- inspect logs and outputs for secret or personal-data exposure;
- obtain real integration evidence when mocks cannot establish the material claim;
- mark the result partially verified if an essential environment or integration is unavailable.

Strict does not authorize production access, real payments, destructive migrations, or external changes. Ask for the needed authority or use a safe test environment.

## Profile adjustments

Increase depth when:

- the code has weak or absent tests;
- the change spans several packages or services;
- generated code, schemas, or lockfiles changed;
- behavior varies by operating system, browser, locale, clock, or network;
- the original bug was intermittent;
- the project has a history of regressions in the affected area.

Reduce breadth only when a check is unavailable, unsafe, excessively expensive, or explicitly excluded by the user. Record the omission and its consequence.
