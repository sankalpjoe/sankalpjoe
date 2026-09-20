"""Read public GitHub data. Standard library only; no third-party stats service."""
import json
import os
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

API = "https://api.github.com"
USER = "sankalpjoe"


def request(path, *, raw=False):
    headers = {"User-Agent": "sankalpjoe-profile", "Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    if raw:
        headers["Accept"] = "application/vnd.github.raw+json"
    for attempt in range(3):
        try:
            with urlopen(Request(API + path, headers=headers), timeout=30) as response:
                result = response.read().decode("utf-8")
                return result if raw else json.loads(result)
        except HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
        except (URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(2 ** attempt)


def collect():
    user = request(f"/users/{USER}")
    repos, page = [], 1
    while True:
        batch = request(f"/users/{USER}/repos?type=owner&sort=full_name&per_page=100&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    fields = ("name", "html_url", "description", "fork", "archived", "language", "size",
              "stargazers_count", "forks_count", "pushed_at", "default_branch", "topics")
    cleaned = []
    for repo in repos:
        if (repo.get("private") is not False
                or repo.get("visibility", "public") != "public"
                or repo["owner"]["login"].lower() != USER.lower()):
            continue
        item = {field: repo.get(field) for field in fields}
        item.update(private=False, visibility="public")
        # Exclude the profile itself from language totals: generated art isn't project code.
        try:
            item["languages"] = (request(f"/repos/{USER}/{quote(repo['name'])}/languages")
                                 if repo["name"].lower() != USER.lower() else {})
        except HTTPError as error:
            # Visibility can change after the listing. An inaccessible repo must
            # not keep its old card on the homepage by failing the whole refresh.
            if error.code == 404:
                continue
            raise
        cleaned.append(item)
    cleaned.sort(key=lambda r: r["name"].casefold())
    return {"schema_version": 1, "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source": f"{API}/users/{USER}/repos", "username": USER,
            "followers": user["followers"], "repos": cleaned}


if __name__ == "__main__":
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    data = collect()
    (root / "data").mkdir(exist_ok=True)
    (root / "data/public-repos.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    research = {}
    for repo in data["repos"]:
        if repo["name"] == USER:
            continue
        try:
            research[repo["name"]] = request(f"/repos/{USER}/{quote(repo['name'])}/readme", raw=True)[:24000]
        except HTTPError as error:
            if error.code != 404:
                raise
            research[repo["name"]] = "No README available."
    (root / ".preview").mkdir(exist_ok=True)
    (root / ".preview/research.json").write_text(json.dumps(research, indent=2), encoding="utf-8")
    print(f"Read {len(data['repos'])} public repositories and their language data.")
