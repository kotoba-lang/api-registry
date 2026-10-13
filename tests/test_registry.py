import json
from collections import Counter
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RegistryTests(unittest.TestCase):
    def test_schema_and_index_are_valid_json(self):
        schema = json.loads((ROOT / "schemas/entry.schema.json").read_text())
        index_schema = json.loads((ROOT / "schemas/index.schema.json").read_text())
        index = json.loads((ROOT / "index.json").read_text())
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(index_schema["properties"]["schemaVersion"]["const"], index["schemaVersion"])
        self.assertEqual(index["schemaVersion"], "kotoba-api-registry/1.0")
        self.assertGreater(len(index["entries"]), 0)

    def test_pinned_sources_have_valid_digests_and_links(self):
        index = json.loads((ROOT / "index.json").read_text())
        ids = [entry["id"] for entry in index["entries"]]
        self.assertEqual(len(ids), len(set(ids)))
        for entry in index["entries"]:
            self.assertIn(entry["kind"], {"api-contract-library", "protocol-spec", "service-api-spec", "api-client", "api-implementation"})
            self.assertTrue(entry["name"].strip())
            self.assertTrue(entry["description"].strip())
            self.assertTrue(entry["contract"]["license"])
            source = entry["source"]
            self.assertRegex(source["commit"], r"^[0-9a-f]{40}$")
            self.assertTrue(source["repository"].startswith("kotoba-lang/"))
            for source_file in source["files"]:
                self.assertRegex(source_file["sha256"], r"^[0-9a-f]{64}$")
                if "gitBlobSha" in source_file:
                    self.assertRegex(source_file["gitBlobSha"], r"^[0-9a-f]{40}$")
                expected = f"https://github.com/{source['repository']}/blob/{source['commit']}/{source_file['path']}"
                self.assertEqual(source_file["url"], expected)
            self.assertRegex(entry["verification"]["checkedAt"], r"^2026-10-13$")
            self.assertTrue(all(key in entry["verification"] for key in ("sourceFileHashesVerified", "sourceHashMethod", "tests", "implementationConformance", "liveEndpoint")))
            for related in entry.get("relatedEntries", []):
                self.assertIn(related, ids)

    def test_profile_and_secret_fields_are_not_part_of_entries(self):
        index = json.loads((ROOT / "index.json").read_text())
        forbidden = {"profile", "credentials", "token", "secret", "authorizationGrant"}
        for entry in index["entries"]:
            self.assertTrue(forbidden.isdisjoint(entry))
            self.assertNotIn("endpoint", entry)

    def test_actor_family_has_remote_source_only_evidence(self):
        index = json.loads((ROOT / "index.json").read_text())
        actors = [entry for entry in index["entries"] if entry["id"].startswith("api-actor-")]
        self.assertEqual(len(actors), 240)
        self.assertTrue(all(entry["kind"] == "api-implementation" for entry in actors))
        self.assertTrue(all(entry["contract"]["license"] == "Apache-2.0" for entry in actors))
        self.assertTrue(all(entry["operationCount"] > 0 for entry in actors))
        self.assertTrue(all("operation-effects-unclassified" in entry["effects"] for entry in actors))
        self.assertTrue(all(entry["verification"]["sourceHashMethod"] == "github-content-read-at-pinned-commit" for entry in actors))
        self.assertTrue(all(entry["verification"]["implementationConformance"] == "owner-described-only-not-verified" for entry in actors))
        self.assertTrue(all(entry["verification"]["liveEndpoint"] == "not-verified" for entry in actors))
        self.assertEqual(Counter(entry["operationCount"] for entry in actors), Counter({13: 214, 11: 11, 12: 6, 9: 4, 7: 2, 15: 2, 17: 1}))


if __name__ == "__main__":
    unittest.main()
