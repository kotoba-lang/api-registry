# ADR-0001: Kotoba API discovery registry

Status: accepted for initial catalog draft, 2026-10-13.

## Context

The Kotoba repository forest contains reusable API contract tooling, protocol specifications, SDKs, service API specifications and many API-compatible actor repositories. `kotoba-registry` owns installable skills and MCP definitions in Hermes format. `cloud-itonami/itonami-registry` owns reusable Itonami agent templates, workflows, skills, MCP connections and tool references. Neither catalog models API contracts and their conformance lifecycle.

## Decision

`kotoba-lang/api-registry` owns discovery metadata for Kotoba API assets. Owner repositories remain authoritative for source specifications, implementation, SDK code, deployment and credentials. Entries link immutable commits and file digests; specifications are not copied into this repository.

| Surface | Authority |
|---|---|
| API contract discovery metadata | `kotoba-lang/api-registry` |
| Installable skill and MCP extension discovery | `kotoba-lang/kotoba-registry` |
| Itonami reusable agent templates, workflows, skills, connections and tool references | `cloud-itonami/itonami-registry` |
| API specification, implementation, SDK, release and deployment | Each source owner repository |
| Credentials, grants, runtime approvals and live service state | Existing application/service authority |

Entries distinguish `api-contract-library`, `protocol-spec`, `service-api-spec`, `api-client` and later `api-implementation` types. They record maturity, effects and separate source/spec/test/conformance/live verification. Registry inclusion does not authorize invocation or imply endpoint availability.

## Initial curation

The initial 245 entries cover one OpenAPI contract library, one experimental protocol binding, two Kotobase API specifications, the multi-language Kotobase SDK and 240 owner-published OpenAPI surfaces for clean-room compatibility actors. Every actor reference pins its public `main` commit and file digest. It records the owner's declaration only; no provider equivalence, runtime behavior, conformance, deployment or availability is asserted. The 240 sources were rechecked remotely on 2026-10-13 after the prior local inventory proved incomplete.
