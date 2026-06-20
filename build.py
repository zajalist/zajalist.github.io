"""Build blog post pages from posts/*.md and inject the post list into index.html.

Usage:
    python build.py

Each post is a Markdown file in posts/ with YAML-style frontmatter:

    ---
    title: My post title
    date: 2026-04-12          # YYYY-MM-DD, used for ordering + the displayed month
    read: ~10 min            # optional, shown in the meta line
    summary: One-sentence teaser shown on the homepage card.
    ---

    Markdown body goes here...

Running this regenerates posts/<slug>.html for every post and rewrites the
block between the POSTS:START / POSTS:END markers in index.html.
"""

import re
import html
from datetime import date
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
INDEX = ROOT / "index.html"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
         '<line x1="19" y1="12" x2="5" y2="12"/>'
         '<polyline points="12 19 5 12 12 5"/></svg>')


def parse_frontmatter(text):
    """Split a --- delimited frontmatter block from the markdown body."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError("missing frontmatter (--- block) at top of file")
    meta = {}
    for line in m.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, val = line.split(":", 1)
        meta[key.strip()] = val.strip()
    return meta, m.group(2)


def parse_date(s):
    y, mo, d = (int(x) for x in s.split("-"))
    return date(y, mo, d)


def meta_line(d, read):
    parts = [f"{d.year} · {MONTHS[d.month - 1]}"]
    if read:
        parts.append(read)
    return " · ".join(parts)


POST_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} · Badr Zejli</title>
<meta name="description" content="{summary_attr}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="../style.css" />
</head>
<body>
<header class="nav">
  <div class="wrap nav-inner">
    <a class="brand" href="../index.html"><span>badr</span><span class="dim">.zejli()</span></a>
    <nav class="nav-links">
      <a href="../index.html#writing">Writing</a>
      <a href="../index.html#work">Projects</a>
      <a href="../index.html#about">About</a>
      <a class="cta" href="https://github.com/zajalist" target="_blank" rel="noreferrer">GitHub</a>
    </nav>
  </div>
</header>

<article class="article">
  <div class="article-head">
    <a class="back-link" href="../index.html#writing">{arrow} All posts</a>
    <div class="meta">{meta}</div>
    <h1>{title}</h1>
    <p class="summary">{summary}</p>
    <hr />
  </div>
  <div class="prose">
{body}
  </div>
</article>

<footer>
  <div class="wrap foot-inner">
    <span class="mono">© 2026 Badr Zejli · Montréal</span>
    <div class="foot-links">
      <a href="https://github.com/zajalist" target="_blank" rel="noreferrer">GitHub</a>
      <a href="https://linkedin.com/in/badr-zejli-324228328" target="_blank" rel="noreferrer">LinkedIn</a>
      <a href="mailto:zejbadr@gmail.com">Email</a>
    </div>
  </div>
</footer>
</body>
</html>
"""


def build():
    md = markdown.Markdown(extensions=["fenced_code", "tables", "smarty"])
    posts = []

    for path in sorted(POSTS_DIR.glob("*.md")):
        meta, body_md = parse_frontmatter(path.read_text(encoding="utf-8"))
        d = parse_date(meta["date"])
        slug = path.stem
        md.reset()
        body_html = md.convert(body_md)
        summary = meta.get("summary", "")

        page = POST_TEMPLATE.format(
            title=html.escape(meta["title"]),
            summary=html.escape(summary),
            summary_attr=html.escape(summary, quote=True),
            meta=html.escape(meta_line(d, meta.get("read", ""))),
            body=body_html,
            arrow=ARROW,
        )
        (POSTS_DIR / f"{slug}.html").write_text(page, encoding="utf-8")
        posts.append({"slug": slug, "title": meta["title"],
                      "summary": summary, "date": d, "read": meta.get("read", "")})

    posts.sort(key=lambda p: p["date"], reverse=True)

    cards = []
    for p in posts:
        cards.append(
            f'        <a class="post" href="posts/{p["slug"]}.html">\n'
            f'          <div class="meta">{html.escape(meta_line(p["date"], p["read"]))}</div>\n'
            f'          <div class="ptitle">{html.escape(p["title"])}</div>\n'
            f'          <div class="pdesc">{html.escape(p["summary"])}</div>\n'
            f'        </a>'
        )
    block = "\n".join(cards)

    index = INDEX.read_text(encoding="utf-8")
    new_index = re.sub(
        r"(<!-- POSTS:START[^\n]*-->\n).*?([ \t]*<!-- POSTS:END -->)",
        lambda m: m.group(1) + block + "\n        " + m.group(2),
        index, count=1, flags=re.DOTALL,
    )
    INDEX.write_text(new_index, encoding="utf-8")

    print(f"Built {len(posts)} post page(s):")
    for p in posts:
        print(f"  posts/{p['slug']}.html  ({p['date']})")
    print("Injected post list into index.html")


if __name__ == "__main__":
    build()
