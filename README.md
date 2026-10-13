# Kotoba API Registry

A curated discovery index for API contracts, protocols, client libraries and API implementations owned by `kotoba-lang`. It points to immutable owner-repository commits and selected source files; the owner repository remains the source of truth.

This is separate from [kotoba-registry](https://github.com/kotoba-lang/kotoba-registry), which distributes installable skills and MCP definitions, and from [cloud-itonami/itonami-registry](https://github.com/cloud-itonami/itonami-registry), which catalogs reusable bot templates, workflows, skills, MCP connections and tool references. This registry contains no bot profile instances, credentials, MCP grants, runtime approvals, copied API implementations or claims that an endpoint is live.

Start with [`llms.txt`](llms.txt), the generated [`index.json`](index.json), and the [ownership ADR](docs/adr/0001-api-registry-ownership.md). Each entry records type, maturity, effects, immutable commit, file SHA-256 and separate verification states. A declared OpenAPI `servers` URL is documentation only.

The current catalog has **248 entries**: five reusable contract, protocol and SDK assets plus 243 owner-published clean-room actor API surfaces. Actor entries are source references; they do not verify equivalence with an external provider or claim a deployed endpoint.

## Validate

```sh
python3 scripts/build-index.py
python3 scripts/build-index.py --check
python3 scripts/verify-local-sources.py --kotoba-root .. --entry openapi-cljk-model
```

The local source verifier is optional for standalone registry consumers. Pass `--entry` to select assets whose source repositories are present in a neighboring Kotoba checkout. It checks that pinned repositories and files match the recorded commit and SHA-256. It does not verify API behavior, compatibility, deployment, authentication success or authorization.

## Adding entries

Add one JSON file under `entries/`, following [`schemas/entry.schema.json`](schemas/entry.schema.json), then regenerate `index.json`. Prefer API contract and client assets with clear ownership and versioning. Keep effects and maturity explicit. Do not add secrets, environment-specific endpoints, profile configuration or copied source trees. Actor-family API entries are declarations from their owner repositories; they do not certify compatibility or runtime behavior.
