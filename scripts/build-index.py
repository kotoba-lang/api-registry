#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_KINDS = {
    "api-contract-library",
    "protocol-spec",
    "service-api-spec",
    "api-client",
    "api-implementation",
}
ENTRY_FIELDS = {
    "id",
    "name",
    "kind",
    "description",
    "source",
    "contract",
    "operationCount",
    "relatedEntries",
    "effects",
    "verification",
}


def load_entries():
    entries = []
    for path in sorted((ROOT / "entries").glob("*.json")):
        entry = json.loads(path.read_text())
        if path.stem != entry.get("id"):
            raise ValueError(f"{path}: filename must match id")
        if set(entry) - ENTRY_FIELDS:
            raise ValueError(f"{entry.get('id')}: unsupported fields {sorted(set(entry) - ENTRY_FIELDS)}")
        entries.append(entry)

    ids = [entry["id"] for entry in entries]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate entry id")

    for entry in entries:
        entry_id = entry["id"]
        if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", entry_id):
            raise ValueError(f"{entry_id}: invalid id")
        if entry.get("kind") not in ALLOWED_KINDS:
            raise ValueError(f"{entry_id}: unsupported kind {entry.get('kind')}")
        if not entry.get("name", "").strip() or not entry.get("description", "").strip():
            raise ValueError(f"{entry_id}: name and description must not be empty")

        contract = entry.get("contract", {})
        if not all(contract.get(key) for key in ("format", "version", "maturity", "license")):
            raise ValueError(f"{entry_id}: incomplete contract metadata")

        source = entry.get("source", {})
        if not re.fullmatch(r"kotoba-lang/[a-z0-9._-]+", source.get("repository", "")):
            raise ValueError(f"{entry_id}: source repository must be a Kotoba repo")
        if not re.fullmatch(r"[0-9a-f]{40}", source.get("commit", "")):
            raise ValueError(f"{entry_id}: source commit must be pinned")
        if not source.get("ref") or not source.get("files"):
            raise ValueError(f"{entry_id}: source ref and files are required")
        for source_file in source["files"]:
            required_file_fields = {"path", "role", "mediaType", "sha256", "url"}
            if not required_file_fields.issubset(source_file):
                raise ValueError(f"{entry_id}: incomplete source file metadata")
            if not re.fullmatch(r"[0-9a-f]{64}", source_file.get("sha256", "")):
                raise ValueError(f"{entry_id}: invalid source digest for {source_file.get('path')}")
            if "gitBlobSha" in source_file and not re.fullmatch(r"[0-9a-f]{40}", source_file["gitBlobSha"]):
                raise ValueError(f"{entry_id}: invalid Git blob SHA for {source_file.get('path')}")
            expected_url = f"https://github.com/{source['repository']}/blob/{source['commit']}/{source_file['path']}"
            if source_file.get("url") != expected_url:
                raise ValueError(f"{entry_id}: source URL must point to the pinned owner file")

        verification = entry.get("verification", {})
        required_verification = {
            "remoteDefaultBranch",
            "checkedAt",
            "remoteHeadMatchedPinnedCommit",
            "sourceFileHashesVerified",
            "sourceHashMethod",
            "contractParse",
            "tests",
            "implementationConformance",
            "liveEndpoint",
        }
        if not required_verification.issubset(verification):
            raise ValueError(f"{entry_id}: incomplete verification metadata")
        if not isinstance(verification["remoteHeadMatchedPinnedCommit"], bool):
            raise ValueError(f"{entry_id}: remote head check must be boolean")
        if not isinstance(verification["sourceFileHashesVerified"], bool):
            raise ValueError(f"{entry_id}: source hash check must be boolean")
        if verification["sourceHashMethod"] not in {
            "clean-tracked-local-checkout-at-pinned-commit",
            "github-content-read-at-pinned-commit",
        }:
            raise ValueError(f"{entry_id}: unsupported source hash method")

    id_set = set(ids)
    for entry in entries:
        for related in entry.get("relatedEntries", []):
            if related not in id_set:
                raise ValueError(f"{entry['id']}: unknown related entry {related}")
    return entries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        index = {"schemaVersion": "kotoba-api-registry/1.0", "entries": load_entries()}
        output = json.dumps(index, indent=2, ensure_ascii=False) + "\n"
        target = ROOT / "index.json"
        if args.check:
            if not target.exists() or target.read_text() != output:
                raise ValueError("index.json is stale; run scripts/build-index.py")
            print(f"valid: {len(index['entries'])} entries")
        else:
            target.write_text(output)
            print(f"wrote {target} ({len(index['entries'])} entries)")
    except Exception as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
