#!/usr/bin/env python3
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument("--kotoba-root",type=Path,required=True);a=p.parse_args();root=a.kotoba_root.resolve();index=json.loads((ROOT/"index.json").read_text());errors=[];checked=0
 for e in index["entries"]:
  repo=e["source"]["repository"].split("/",1)[1]; checkout=root/repo
  if not checkout.is_dir(): errors.append(f"{repo}: checkout missing");continue
  head=subprocess.run(["git","-C",str(checkout),"rev-parse","HEAD"],capture_output=True,text=True)
  if head.returncode or head.stdout.strip()!=e["source"]["commit"]: errors.append(f"{repo}: local HEAD does not match pinned commit");continue
  for f in e["source"]["files"]:
   tracked=subprocess.run(["git","-C",str(checkout),"ls-files","--error-unmatch",f["path"]],capture_output=True,text=True)
   if tracked.returncode: errors.append(f"{repo}/{f['path']}: not tracked at pinned commit");continue
   status=subprocess.run(["git","-C",str(checkout),"status","--porcelain","--",f["path"]],capture_output=True,text=True)
   if status.stdout.strip(): errors.append(f"{repo}/{f['path']}: worktree differs from pinned commit");continue
   path=checkout/f["path"]
   if not path.is_file(): errors.append(f"{repo}/{f['path']}: missing");continue
   digest=hashlib.sha256(path.read_bytes()).hexdigest()
   if digest!=f["sha256"]: errors.append(f"{repo}/{f['path']}: SHA-256 mismatch")
   else: checked+=1
 if errors:
  print("\n".join(errors),file=sys.stderr);return 1
 print(f"verified {checked} files across {len(index['entries'])} entries at pinned local heads")
 return 0
if __name__=="__main__":raise SystemExit(main())
