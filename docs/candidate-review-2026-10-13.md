# Initial API registry candidate review — 2026-10-13

| Candidate | Decision | Rationale |
|---|---|---|
| `kotoba-lang/openapi` | registered: `openapi-cljk-model` | Generic portable OpenAPI 3 model, validator, JSON converter and pure request builder; does not own any service endpoint.
| `kotoba-lang/mail-a2a` | registered: `mail-a2a-v1` | Versioned normative document and machine schema; status remains experimental and non-official.
| `kotoba-lang/kotobase-sdk/spec/openapi.yaml` | registered: `kotobase-query-api-v0_2` | Explicit language-neutral read-only query contract.
| `kotoba-lang/kotobase-sdk/spec/graphdb-openapi.yaml` | registered: `kotobase-graphdb-compat-api-v0_1` | Separately versioned read-only compatibility surface; not merged into the unified query entry.
| `kotoba-lang/kotobase-sdk` clients | registered: `kotobase-sdk` | Four language clients share the query envelope and remain owned by the SDK repository.
| 240 local root-level `openapi.json` actor candidates | deferred/source-only | Candidate index is in the review workspace. Local scan found 56 directories without Git metadata and 35 with neither LICENSE nor NOTICE. Public default-branch equality, provenance and compatibility conformance require per-repo review. No actor was copied or registered as a verified provider.
| `kotoba-lang/org.worldbank.api` | source-only / separate data product | Preserves API response snapshots in a DataLad dataset; not a live API contract or endpoint. Keep distinct from the `com-worldbank` actor family.
| `kotoba-lang/vault`, `tasks` application APIs/components | source-only | Application-specific routes/components; no independent reusable contract selected in this first cohort.

The three distinct source commits pinned by the five entries were checked against GitHub public `main` on 2026-10-13 and matched the local selected source commits. Source file digests were computed from clean tracked files at those commits. This does not establish implementation conformance or live endpoint behavior.
