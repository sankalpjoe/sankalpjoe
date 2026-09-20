"""Refresh public data and generate profile assets; --offline uses the saved snapshot."""
import argparse
import json
import os
from pathlib import Path
from github_data import collect
from render_profile import render

ROOT=Path(__file__).resolve().parents[1]


def validate(data):
    if data.get("username") != "sankalpjoe" or not isinstance(data.get("repos"),list):
        raise ValueError("Unexpected snapshot schema or account")
    names=set()
    for repo in data["repos"]:
        if repo.get("private", False) or repo.get("visibility", "public") != "public":
            raise ValueError("Snapshot contains a non-public repository")
        name=repo["name"]
        if name in names or not name or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_." for c in name):
            raise ValueError("Invalid or duplicate repository name")
        names.add(name)
        if repo["html_url"] != f"https://github.com/sankalpjoe/{name}":
            raise ValueError("Unexpected repository URL")
        if any(not isinstance(v,int) or v<0 for v in repo["languages"].values()):
            raise ValueError("Invalid language totals")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline",action="store_true")
    args=parser.parse_args()
    snapshot=ROOT/"data/public-repos.json"
    previous=json.loads(snapshot.read_text(encoding="utf-8")) if snapshot.exists() else None
    if previous is not None:
        validate(previous)
    # Finish all requests and rendering before replacing any good assets.
    if args.offline and previous is None:
        raise ValueError("Offline rendering requires an existing snapshot")
    data=previous if args.offline else collect()
    validate(data)
    outputs=render(data)
    outputs["data/public-repos.json"]=json.dumps(data,indent=2)+"\n"
    for name,content in outputs.items():
        target=ROOT/name
        target.parent.mkdir(parents=True,exist_ok=True)
        temp=target.with_name(target.name+".tmp")
        temp.write_text(content,encoding="utf-8",newline="\n")
        os.replace(temp,target)
    # Remove only the exact card filenames belonging to previously known repos.
    # Never sweep the asset folder: unrelated or hand-authored art is preserved.
    removed=0
    for repo in previous["repos"] if previous else []:
        for suffix in ("", "-mobile"):
            name=f"assets/project-{repo['name']}{suffix}.svg"
            target=ROOT/name
            if name not in outputs and target.is_file():
                target.unlink()
                removed+=1
    print(f"Rendered {len(outputs)-2} SVGs and {len(data['repos'])} public repository entries.")
    if removed:
        print(f"Removed {removed} obsolete project graphics.")


if __name__=="__main__":
    main()
