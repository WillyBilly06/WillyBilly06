"""Update the Recently Working On section of the profile README
with the most recently pushed repository (excluding the profile repo)."""
import json
import os
import re
import urllib.request

USER = "WillyBilly06"

req = urllib.request.Request(
    f"https://api.github.com/users/{USER}/repos?sort=pushed&per_page=10",
    headers={"Accept": "application/vnd.github+json"},
)
token = os.environ.get("GITHUB_TOKEN")
if token:
    req.add_header("Authorization", f"Bearer {token}")

repos = json.load(urllib.request.urlopen(req))
repo = next(r for r in repos if r["name"] != USER and not r["fork"])

desc = repo["description"] or "No description yet"
lang = repo["language"] or "—"
pushed = repo["pushed_at"][:10]

block = (
    f'🛠️ Most recently pushed to <a href="{repo["html_url"]}"><b>{repo["name"]}</b></a> '
    f"on <b>{pushed}</b><br/>\n"
    f"<i>{desc}</i><br/>\n"
    f"<code>{lang}</code>"
)

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

updated = re.sub(
    r"(<!--RECENT_REPO:START-->)(.*?)(<!--RECENT_REPO:END-->)",
    lambda m: m.group(1) + "\n" + block + "\n" + m.group(3),
    readme,
    flags=re.S,
)

with open("README.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(updated)

print(f"Updated Recently Working On -> {repo['name']} (pushed {pushed})")
