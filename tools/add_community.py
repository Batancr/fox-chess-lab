#!/usr/bin/env python3
"""Add an approved submission to the Community tab.

Copy the share link (or the attached .txt file) from the GitHub issue, then, from the fox-chess-lab folder:

    python3 tools/add_community.py "https://batancr.github.io/fox-chess-lab/#share=z..." --title "Caro-Kann for club players" --author "magnus" --desc "One line about it"
    python3 tools/add_community.py fox-my-study.txt --title "..." --author "..."

Then push:  git add . && git commit -m "Add community item" && git push
To remove an item later, delete its file in docs/community and its entry in docs/community/index.json.
"""
import argparse, base64, datetime, json, os, re, sys, zlib

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "community")


def decode(arg):
    if os.path.exists(arg):
        return json.load(open(arg))
    m = re.search(r"#share=([zj][A-Za-z0-9_-]+)", arg)
    if not m:
        sys.exit("That isn't a Fox Chess Lab share link or file.")
    code = m.group(1)
    raw = base64.urlsafe_b64decode(code[1:] + "=" * (-len(code[1:]) % 4))
    if code[0] == "z":
        raw = zlib.decompress(raw, -15)          # the site compresses with raw deflate
    return json.loads(raw)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="share link, or the .txt file attached to the issue")
    ap.add_argument("--title", required=True)
    ap.add_argument("--author", default="Anonymous")
    ap.add_argument("--desc", default="")
    ap.add_argument("--tags", default="", help="comma-separated words people might search for")
    a = ap.parse_args()
    p = decode(a.source)
    if p.get("app") != "fox-chess-lab" or p.get("k") not in ("study", "rep"):
        sys.exit("That doesn't look like a Fox Chess Lab study or repertoire.")
    p["name"] = a.title
    os.makedirs(DIR, exist_ok=True)
    idx_path = os.path.join(DIR, "index.json")
    idx = json.load(open(idx_path)) if os.path.exists(idx_path) else {"version": 1, "items": []}
    slug = re.sub(r"[^a-z0-9]+", "-", a.title.lower()).strip("-")[:50] or "item"
    base, n = slug, 2
    while any(it["file"] == "community/" + slug + ".json" for it in idx["items"]):
        slug = "%s-%d" % (base, n); n += 1
    json.dump(p, open(os.path.join(DIR, slug + ".json"), "w"), ensure_ascii=False, separators=(",", ":"))
    item = {"title": a.title, "kind": p["k"], "author": a.author, "added": datetime.date.today().isoformat(), "desc": a.desc,
            "tags": [t.strip() for t in a.tags.split(",") if t.strip()], "file": "community/" + slug + ".json"}
    if p["k"] == "rep":
        item["color"] = p.get("color", "w")
    idx["items"].insert(0, item)
    json.dump(idx, open(idx_path, "w"), indent=1, ensure_ascii=False)
    print("Added '%s' (%s). Now push it with git." % (a.title, "study" if p["k"] == "study" else "repertoire"))


if __name__ == "__main__":
    main()
