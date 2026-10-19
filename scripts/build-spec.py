#!/usr/bin/env python3
"""Render docs/spec.md as site/spec.html with the site's stylesheet. Minimal Markdown: headings, paragraphs, lists, tables, code, bold, links, blockquotes."""
import re, html, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
src = (root / "docs" / "spec.md").read_text().split("\n")
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s
def slug(t): return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
out, i, para = [], 0, []
def flush():
    global para
    if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
while i < len(src):
    line = src[i]
    if line.startswith("#"):
        flush(); level = len(line) - len(line.lstrip("#")); text = line[level:].strip()
        out.append(f'<h{level} id="{slug(text)}">{inline(text)}</h{level}>')
    elif line.startswith("```"):
        flush(); buf = []; i += 1
        while i < len(src) and not src[i].startswith("```"): buf.append(src[i]); i += 1
        out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
    elif line.startswith("|"):
        flush(); rows = []
        while i < len(src) and src[i].startswith("|"): rows.append(src[i]); i += 1
        i -= 1
        cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows if not re.match(r"^\|[\s:|-]+\|$", r)]
        if cells:
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells[0]) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cells[1:]) + "</tbody></table>")
    elif re.match(r"^\s*([-*]|\d+\.)\s", line):
        flush(); ordered = bool(re.match(r"^\s*\d+\.", line)); items = []
        while i < len(src) and (re.match(r"^\s*([-*]|\d+\.)\s", src[i]) or (src[i].startswith("  ") and items)):
            if re.match(r"^\s*([-*]|\d+\.)\s", src[i]): items.append(re.sub(r"^\s*([-*]|\d+\.)\s", "", src[i]))
            else: items[-1] += " " + src[i].strip()
            i += 1
        i -= 1
        tag = "ol" if ordered else "ul"
        out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
    elif line.startswith(">"):
        flush(); out.append("<blockquote><p>" + inline(line.lstrip("> ")) + "</p></blockquote>")
    elif line.strip() == "": flush()
    else: para.append(line.strip())
    i += 1
flush()
page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Swarm Bank spec</title><meta name="description" content="The Swarm Bank design: pool contract, seat quorum, the oracle lane, anti-whale rules, open decisions and the development flow.">
<link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="spec.css"></head>
<body><header class="mast"><a class="wordmark" href="index.html"><svg class="wm-fig" viewBox="0 0 20 40" aria-hidden="true"><circle cx="10" cy="6" r="5.5"/><path d="M3 13.5h14l1.5 11h-3.5l-0.8 15h-4.4l-0.8-10-0.8 10H4.8L4 24.5H0.5z"/></svg><span>Swarm Bank</span></a>
<p class="mast-line">The spec. <em>Nothing built, no job paid.</em></p><nav class="mast-nav" aria-label="Site"><a href="index.html">Overview</a><a href="#8-owner-decisions-needed-before-a-build">Decisions</a><a href="#10-development-flow-brainstorm-with-the-owner-2026-10-18-nothing-started">Development flow</a></nav></header>
<main class="spec">{"".join(out)}</main>
<footer class="foot"><p>Source: docs/spec.md in github.com/swarmbank/bank. Rendered by scripts/build-spec.py.</p></footer></body></html>"""
(root / "site" / "spec.html").write_text(page)
print("wrote site/spec.html", len(page), "bytes")
