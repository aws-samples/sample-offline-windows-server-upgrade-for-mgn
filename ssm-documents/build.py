#!/usr/bin/env python3
"""Convert the commented YAML sources in custom/ into minified JSON in dist/.

SSM limits customer-owned documents to 64 KiB. The customized upgrade runbooks are
close to that limit as YAML, so they are published as minified JSON (comments and
whitespace removed). Terraform equivalent: jsonencode(yamldecode(file("<source>.yaml"))).
"""
import json
import pathlib
import sys

import yaml

LIMIT = 64 * 1024
root = pathlib.Path(__file__).parent
dist = root / "dist"
dist.mkdir(exist_ok=True)

failed = False
for src in sorted((root / "custom").glob("*.yaml")):
    content = json.dumps(yaml.safe_load(src.read_text()), separators=(",", ":"))
    size = len(content.encode("utf-8"))
    out = dist / (src.stem + ".json")
    out.write_text(content)
    status = "OK" if size < LIMIT else "TOO LARGE"
    failed |= size >= LIMIT
    print(f"{out.name:60} {size / 1024:5.1f} KiB  {status}")

sys.exit(1 if failed else 0)
