# Initial API registry candidate review — 2026-10-13

| Candidate | Decision | Rationale |
|---|---|---|
| `kotoba-lang/openapi` | registered: `openapi-cljk-model` | Generic portable OpenAPI 3 model, validator, JSON converter and pure request builder; does not own any service endpoint.
| `kotoba-lang/mail-a2a` | registered: `mail-a2a-v1` | Versioned normative document and machine schema; status remains experimental and non-official.
| `kotoba-lang/kotobase-sdk/spec/openapi.yaml` | registered: `kotobase-query-api-v0_2` | Explicit language-neutral read-only query contract.
| `kotoba-lang/kotobase-sdk/spec/graphdb-openapi.yaml` | registered: `kotobase-graphdb-compat-api-v0_1` | Separately versioned read-only compatibility surface; not merged into the unified query entry.
| `kotoba-lang/kotobase-sdk` clients | registered: `kotobase-sdk` | Four language clients share the query envelope and remain owned by the SDK repository.
| 243 owner-published actor API surfaces | registered as source references | 240 were found in the local org snapshot; three more were net-new findings from public GitHub code search (one other result was already in the local snapshot). All are public, unarchived, use `main` and have GitHub Apache-2.0 metadata. Each pinned `openapi.json` parsed as OpenAPI 3.1.0, and each `main` head was rechecked after file retrieval. Compatibility and runtime remain unverified.
| `kotoba-lang/org.worldbank.api` | source-only / separate data product | Preserves API response snapshots in a DataLad dataset; not a live API contract or endpoint. Keep distinct from the `com-worldbank` actor family.
| `kotoba-lang/vault`, `tasks` application APIs/components | source-only | Application-specific routes/components; no independent reusable contract selected in this first cohort.

The first five entries pin three distinct source repositories and were checked against GitHub public `main` on 2026-10-13. For the additional 243 actor entries, public repository metadata, the `main` commit before and after retrieval, and the exact `openapi.json` bytes were checked through GitHub. All pinned heads remained unchanged during the audit, all files parsed, titles identified their subjects as clean-room APIs, and each file received SHA-256 plus Git blob identity. This does not establish upstream equivalence, implementation conformance or live endpoint behavior.

The earlier local-only report found apparent license and Git metadata gaps because many symlinked checkouts were unavailable. Current GitHub owner metadata supersedes those local observations for these entries; no source tree was copied into this registry. A GitHub code search query returned six API files, three net-new to the first inventory and three overlapping. Code search coverage is not assumed exhaustive, so this review does not claim that all API-shaped assets across the entire organization have been found.
