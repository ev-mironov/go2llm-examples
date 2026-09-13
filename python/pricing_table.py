#!/usr/bin/env python3
"""Print the live price list as a table, ordered by what a coding agent actually pays.

`GET /api/pricing` needs no key. A price table typed by hand into a README is a
snapshot that starts lying the day the catalogue moves, so this reads the
catalogue instead and prints the version and timestamp it read.

Columns are USD per 1M tokens:

    in       input tokens and cache writes
    out      output tokens
    cache    cache reads — for a coding agent this is most of the bill
    blended  in/out/cache weighted by the profile the catalogue itself publishes
    vendor   the model owner's own published rate, where we have it verified

Standard library only, no dependencies.

    ./pricing_table.py              # everything, cheapest blended price first
    ./pricing_table.py anthropic    # filter by family or model id
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request

BASE_URL = os.environ.get("GO2LLM_BASE_URL", "https://go2llm.tech")


def fetch(url: str) -> dict:
    request = urllib.request.Request(url, headers={"user-agent": "go2llm-examples/pricing-table"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main(argv: list[str]) -> int:
    needle = (argv[1] if len(argv) > 1 else "").strip().lower()
    data = fetch(f"{BASE_URL}/api/pricing")

    profile = data.get("comparisonProfile", {})
    fresh = profile.get("freshInputShare", 0.10)
    output = profile.get("outputShare", 0.05)
    cached = profile.get("cacheReadShare", 0.85)

    rows = []
    for model in data["models"]:
        if model.get("lifecycle") != "published":
            continue
        haystack = f"{model['id']} {model.get('family', '')}".lower()
        if needle and needle not in haystack:
            continue
        price_in, price_out = model.get("in"), model.get("out")
        if price_in is None or price_out is None:
            continue  # image models are billed per image, not per token
        price_cache = model.get("cacheRead")
        blended = price_in * fresh + price_out * output + (price_cache or 0) * cached

        direct = model.get("direct") or {}
        vendor = "-"
        if direct.get("input") is not None and direct.get("output") is not None:
            vendor = f"{direct['input']:g}/{direct['output']:g}"

        rows.append((blended, model["id"], price_in, price_out, price_cache, vendor))

    if not rows:
        print(f"nothing matched {needle!r}", file=sys.stderr)
        return 1

    rows.sort()
    print(f"catalogue v{data['version']}, generated {data['generatedAt']}")
    print(
        f"blended profile: {fresh:.0%} input / {output:.0%} output / {cached:.0%} cache read"
        f" ({profile.get('label', 'unnamed')})"
    )
    print()
    print(f"{'model':<28}{'in':>9}{'out':>9}{'cache':>9}{'blended':>10}  vendor in/out")
    print("-" * 88)
    for blended, model_id, price_in, price_out, price_cache, vendor in rows:
        cache_text = "-" if price_cache is None else f"{price_cache:.4g}"
        print(
            f"{model_id:<28}{price_in:>9.4g}{price_out:>9.4g}"
            f"{cache_text:>9}{blended:>10.4g}  {vendor}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
