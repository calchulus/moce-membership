#!/usr/bin/env python3
"""Build a self-contained single-file version of the MOCE membership demo.

Reads index.html (source of truth, all CSS/JS already inline) and produces:
  - moce-membership-single.html : full standalone document (open via file:// or serve anywhere)
  - _artifact_body.html         : body-only fragment (no html/head/body tags) for Artifact publish

The single file drops the external manifest / apple-touch-icon links and the service-worker
registration, because a true PWA install requires separate manifest + sw.js files over http(s).
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "index.html")
SINGLE = os.path.join(HERE, "moce-membership-single.html")
BODY = os.path.join(HERE, "_artifact_body.html")

html = open(SRC, encoding="utf-8").read()

# 1) drop external resource links that cannot exist in a single file
html = re.sub(r'[ \t]*<link rel="manifest"[^>]*>\n', "", html)
html = re.sub(r'[ \t]*<link rel="apple-touch-icon"[^>]*>\n', "", html)

# 2) drop the service-worker registration block (needs a separate sw.js over http(s))
html = re.sub(
    r"\n[ \t]*// ---- PWA ----\n[ \t]*if\('serviceWorker' in navigator\)\{.*?\n[ \t]*\}\n",
    "\n",
    html,
    flags=re.S,
)

# 3) retag title/description so the single file is self-identifying
html = html.replace(
    "<title>MOCE 会员卡 · Alipay Mini-App Demo</title>",
    "<title>MOCE 会员卡 · Single-File Demo</title>",
)

open(SINGLE, "w", encoding="utf-8").write(html)

# 4) build body-only fragment for the Artifact publisher
style = re.search(r"<style>.*?</style>", html, flags=re.S).group(0)
body_inner = re.search(r"<body>\n(.*)</body>", html, flags=re.S).group(1)
open(BODY, "w", encoding="utf-8").write(style + "\n" + body_inner)

print("wrote", SINGLE, os.path.getsize(SINGLE), "bytes")
print("wrote", BODY, os.path.getsize(BODY), "bytes")
# sanity: no external refs remain in the single file
ext = re.findall(r'(?:src|href)="(?!#)(?!data:)([^"]+)"', html)
print("external refs in single file:", ext or "none")
