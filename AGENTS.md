# API Registry maintenance

- Treat each owner repository as the source of truth; pin immutable commits and file SHA-256 values.
- Do not copy API source files, application credentials, runtime grants, deployed endpoints or bot profile instances into this repository.
- Keep contract parsing, source tests, implementation conformance and live endpoint checks as separate evidence states.
- Regenerate `index.json` with `python3 scripts/build-index.py`; use `--check` and the registry tests before publishing.
- Run `scripts/verify-local-sources.py` when the owner repositories are present in a neighboring `kotoba-lang` checkout.
- Preserve existing repository work and review source ownership and license before registering new assets.
