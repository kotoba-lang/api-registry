import json
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
                expected = f"https://github.com/{source['repository']}/blob/{source['commit']}/{source_file['path']}"
                self.assertEqual(source_file["url"], expected)
            self.assertTrue(all(key in entry["verification"] for key in ("tests", "implementationConformance", "liveEndpoint")))
            for related in entry.get("relatedEntries", []):
                self.assertIn(related, ids)

    def test_profile_and_secret_fields_are_not_part_of_entries(self):
        index = json.loads((ROOT / "index.json").read_text())
        forbidden = {"profile", "credentials", "token", "secret", "authorizationGrant"}
        for entry in index["entries"]:
            self.assertTrue(forbidden.isdisjoint(entry))
            self.assertNotIn("endpoint", entry)


if __name__ == "__main__":
    unittest.main()
