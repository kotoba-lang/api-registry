#!/usr/bin/env python3
import argparse, json, sys
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load_entries():
 entries=[]
 for path in sorted((ROOT/"entries").glob("*.json")):
  entry=json.loads(path.read_text())
  if path.stem != entry.get("id"):
   raise ValueError(f"{path}: filename must match id")
  entries.append(entry)
 ids=[e["id"] for e in entries]
 if len(ids)!=len(set(ids)): raise ValueError("duplicate entry id")
 allowed_kinds={"api-contract-library","protocol-spec","service-api-spec","api-client","api-implementation"}
 required={"name","kind","description","source","contract","verification"}
 for e in entries:
  if not required.issubset(e): raise ValueError(f"{e.get('id')}: missing required fields")
  if e["kind"] not in allowed_kinds: raise ValueError(f"{e['id']}: unsupported kind {e['kind']}")
  if not e["name"].strip() or not e["description"].strip(): raise ValueError(f"{e['id']}: name and description must not be empty")
  if not all(e["contract"].get(k) for k in ("format","version","maturity","license")): raise ValueError(f"{e['id']}: incomplete contract metadata")
  if not all(k in e["verification"] for k in ("remoteDefaultBranch","remoteHeadMatchedPinnedCommit","sourceFilesHashCheckedAgainstLocalCheckout","contractParse","tests","implementationConformance","liveEndpoint")): raise ValueError(f"{e['id']}: incomplete verification metadata")
  if not re.fullmatch(r"[0-9a-f]{40}", e.get("source",{}).get("commit", "")): raise ValueError(f"{e['id']}: source commit must be pinned")
  if not e["source"].get("files"): raise ValueError(f"{e['id']}: source files required")
  for f in e["source"]["files"]:
   if not re.fullmatch(r"[0-9a-f]{64}", f.get("sha256", "")): raise ValueError(f"{e['id']}: invalid source digest for {f.get('path')}")
   if f.get("url") != f"https://github.com/{e['source']['repository']}/blob/{e['source']['commit']}/{f.get('path')}": raise ValueError(f"{e['id']}: source URL must point to the pinned owner file")
 ids=set(e["id"] for e in entries)
 for e in entries:
  for related in e.get("relatedEntries", []):
   if related not in ids: raise ValueError(f"{e['id']}: unknown related entry {related}")
 return entries

def main():
 p=argparse.ArgumentParser(); p.add_argument("--check",action="store_true"); a=p.parse_args()
 try:
  index={"schemaVersion":"kotoba-api-registry/1.0","entries":load_entries()}
  out=(json.dumps(index,indent=2,ensure_ascii=False)+"\n")
  target=ROOT/"index.json"
  if a.check:
   if not target.exists() or target.read_text()!=out: raise ValueError("index.json is stale; run scripts/build-index.py")
   print(f"valid: {len(index['entries'])} entries")
  else:
   target.write_text(out); print(f"wrote {target} ({len(index['entries'])} entries)")
 except Exception as e:
  print(e,file=sys.stderr); return 1
 return 0
if __name__=="__main__": raise SystemExit(main())
