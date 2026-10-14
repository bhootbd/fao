#!/usr/bin/env python3
"""Merge catalog entries into catalog.json and rename media files to descriptive names.

Usage: python scripts/apply_catalog.py <archive_dir> <entries.json>
Each entry has "file" (current name) and "slug"; the file becomes <id>_<n>__<slug>.<ext>.
index.json media paths are updated to match.
"""
import json
import os
import subprocess
import sys

archive, entries_path = sys.argv[1], sys.argv[2]
media = os.path.join(archive, "media")
catalog_path = os.path.join(archive, "catalog.json")
index_path = os.path.join(archive, "index.json")

catalog = {e["key"]: e for e in json.load(open(catalog_path, encoding="utf-8"))} if os.path.exists(catalog_path) else {}
index = json.load(open(index_path, encoding="utf-8"))
captions = {p["id"]: p["text"] for p in index}
renames = {}

for e in json.load(open(entries_path, encoding="utf-8")):
    old = e.pop("file")
    key, ext = old.split("__")[0].rsplit(".", 1)[0], old.rsplit(".", 1)[1]
    new = f"{key}__{e['slug']}.{ext}"
    if old != new and os.path.exists(os.path.join(media, old)):
        subprocess.run(["git", "mv", os.path.join(media, old), os.path.join(media, new)], check=True)
        renames[f"media/{old}"] = f"media/{new}"
    post = int(key.split("_")[0])
    catalog[key] = {"key": key, "file": f"media/{new}", "post": post,
                    "link": f"https://t.me/Meme_Template_bd/{post}", "caption": captions.get(post, ""), **e}

for p in index:
    p["media"] = [renames.get(m, m) for m in p["media"]]

with open(index_path, "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=1)
with open(catalog_path, "w", encoding="utf-8") as f:
    json.dump(sorted(catalog.values(), key=lambda c: c["key"]), f, ensure_ascii=False, indent=1)
print(f"renamed {len(renames)}, catalog has {len(catalog)} entries")
