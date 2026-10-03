#!/usr/bin/env python3
"""Runs in GitHub Actions when someone opens a "Community submission" issue.

It reads the share link (or attached file) from the issue, checks that it is a valid Fox Chess Lab study or
repertoire within size limits, adds it to docs/community, commits and pushes, then comments on the issue and closes it.
Everything in the issue is treated as plain data: nothing from it is ever run.

To take a post down: delete its file in docs/community/ and its entry in docs/community/index.json, then push
(or reopen the issue and ask Claude to do it).
"""
import base64, datetime, json, os, re, subprocess, sys, time, unicodedata, urllib.request, zlib

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DIR = os.path.join(ROOT, "docs", "community")
REPO, TOKEN = os.environ.get("REPO", ""), os.environ.get("GITHUB_TOKEN", "")
NUMBER, USER = os.environ.get("ISSUE_NUMBER", ""), os.environ.get("ISSUE_USER", "")
BODY = os.environ.get("ISSUE_BODY", "") or ""
PER_DAY = 5                       # most posts one GitHub user can publish per day
FEN = re.compile(r"^[1-8pnbrqkPNBRQK/]{15,90} [wb] (?:-|[KQkq]{1,4}) (?:-|[a-h][36]) \d{1,3} \d{1,4}$")


class Reject(Exception):
    pass


def api(method, path, data=None):
    req = urllib.request.Request("https://api.github.com/repos/" + REPO + path, method=method,
                                 data=json.dumps(data).encode() if data is not None else None,
                                 headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github+json", "Content-Type": "application/json", "User-Agent": "fox-chess-lab-bot"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def reply(text, close):
    try:
        api("POST", "/issues/%s/comments" % NUMBER, {"body": text})
        if close:
            api("PATCH", "/issues/%s" % NUMBER, {"state": "closed", "state_reason": "completed"})
    except Exception as e:                                          # the post itself is already saved
        print("couldn't comment on the issue:", e)


def clean(s, n):
    s = "".join(ch for ch in str(s or "") if unicodedata.category(ch)[0] != "C")
    return re.sub(r"\s+", " ", s).strip()[:n]


def field(name):
    m = re.search(r"\*\*" + re.escape(name) + r":\*\*\s*(.*)", BODY)
    return m.group(1).strip() if m else ""


def payload():
    m = re.search(r"#share=([zj][A-Za-z0-9_-]{10,})", BODY)
    if m:
        code = m.group(1)
        raw = base64.urlsafe_b64decode(code[1:] + "=" * (-len(code[1:]) % 4))
        if code[0] == "z":
            d = zlib.decompressobj(-15)
            raw = d.decompress(raw, 2_000_000)
            if d.unconsumed_tail:
                raise Reject("it's too large")
        return json.loads(raw)
    m = re.search(r"https://github\.com/user-attachments/files/\d+/[^\s)\]]+\.txt", BODY)
    if m:
        req = urllib.request.Request(m.group(0), headers={"User-Agent": "fox-chess-lab-bot"})
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read(2_000_001)
        if len(raw) > 2_000_000:
            raise Reject("it's too large")
        return json.loads(raw)
    raise Reject("I couldn't find a share link or an attached .txt file from the site")


def check(p):
    if not isinstance(p, dict) or p.get("app") != "fox-chess-lab" or p.get("k") not in ("study", "rep"):
        raise Reject("it isn't a Fox Chess Lab study or repertoire")
    out = {"app": "fox-chess-lab", "v": 1, "k": p["k"], "name": clean(p.get("name"), 80)}
    if p["k"] == "study":
        chs = p.get("chapters")
        if not isinstance(chs, list) or not 1 <= len(chs) <= 64:
            raise Reject("a study needs between 1 and 64 chapters")
        out["chapters"] = []
        for c in chs:
            if not isinstance(c, dict):
                raise Reject("one of the chapters is damaged")
            fen = clean(c.get("fen") or "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 100)
            if not FEN.match(fen):
                raise Reject("one of the chapters has an invalid position")
            pgn = str(c.get("pgn") or "")
            if len(pgn) > 60000:
                raise Reject("one of the chapters is too long")
            out["chapters"].append({"type": "calc" if c.get("type") == "calc" else "line", "name": clean(c.get("name"), 80) or "Chapter",
                                    "fen": fen, "orient": "b" if c.get("orient") == "b" else "w", "pgn": pgn, "prompt": clean(c.get("prompt"), 400),
                                    **({"mode": "deep"} if c.get("mode") == "deep" else {})})
    else:
        pgn = str(p.get("pgn") or "")
        if not pgn.strip() or len(pgn) > 250000:
            raise Reject("the repertoire is empty or too long")
        root = p.get("root") or []
        skip = p.get("skip") or []
        if not all(isinstance(x, str) and len(x) <= 8 for x in root + skip) or len(root) > 30 or len(skip) > 30:
            raise Reject("the repertoire's starting moves are damaged")
        out.update({"color": "b" if p.get("color") == "b" else "w", "root": root, "skip": skip, "pgn": pgn})
    return out


def git(*args):
    subprocess.run(["git"] + list(args), cwd=ROOT, check=True)


def main():
    try:
        p = check(payload())
    except Reject as e:
        reply("Thanks for the submission! It couldn't be published automatically because %s. "
              "Please make a new share link on the site and submit again, or the site owner will take a look." % e, False)
        return
    except Exception as e:
        reply("Thanks for the submission! Something went wrong reading it (%s), so it wasn't published. "
              "The site owner will take a look." % clean(e, 120), False)
        return
    os.makedirs(DIR, exist_ok=True)
    idx_path = os.path.join(DIR, "index.json")
    idx = json.load(open(idx_path)) if os.path.exists(idx_path) else {"version": 1, "items": []}
    today = datetime.date.today().isoformat()
    if sum(1 for it in idx["items"] if it.get("gh") == USER and it.get("added") == today) >= PER_DAY:
        reply("Thanks! You've already published %d posts today, which is the daily limit. Please submit this again tomorrow." % PER_DAY, True)
        return
    title = clean(field("Title"), 80) or p["name"] or "Untitled"
    p["name"] = title
    author = clean(field("Shown as by"), 40) or USER
    desc = clean(field("About it"), 200)
    if desc == "(none)":
        desc = ""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:50] or "item"
    base, n = slug, 2
    while os.path.exists(os.path.join(DIR, slug + ".json")):
        slug = "%s-%d" % (base, n); n += 1
    json.dump(p, open(os.path.join(DIR, slug + ".json"), "w"), ensure_ascii=False, separators=(",", ":"))
    item = {"title": title, "kind": p["k"], "author": author, "added": today, "desc": desc, "tags": [],
            "file": "community/" + slug + ".json", "gh": USER, "issue": int(NUMBER or 0)}
    if p["k"] == "rep":
        item["color"] = p["color"]
    idx["items"].insert(0, item)
    json.dump(idx, open(idx_path, "w"), indent=1, ensure_ascii=False)
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    git("add", "docs/community")
    git("commit", "-m", "Community: add \"%s\" (issue #%s)" % (title.replace('"', "'"), NUMBER))
    for attempt in range(3):
        try:
            git("push")
            break
        except subprocess.CalledProcessError:
            time.sleep(3 + attempt * 3)
            git("pull", "--rebase")
    else:
        sys.exit("couldn't push")
    reply("Published! **%s** is now on the Community tab (it can take up to about 5 minutes to show). "
          "Thanks for sharing." % title, True)


if __name__ == "__main__":
    main()
