"""
extract_templates.py
Builds a simple category -> suggested reply template lookup from the
Bitext dataset's `response` column, and saves it as templates.json.

This is the "ticket response" automation piece: once a ticket is classified
into a category, we can instantly suggest a starting reply for the agent
to review/edit, instead of writing one from scratch every time.

Usage:
    python src/extract_templates.py
"""
import json
import re
from collections import Counter

import pandas as pd

RAW_PATH = "C:\\For ME\\ticket-classisfication-system\\ml-service\\data\\raw\\tickets.csv"
OUTPUT_PATH = "C:\\For ME\\ticket-classisfication-system\\ml-service\\models\\templates.json"


def tidy_placeholders(text: str) -> str:
    """
    Bitext responses contain placeholders like {{Order Number}}.
    We keep them, but make them clearly stand out as "fill in" spots
    for the agent, e.g. {{Order Number}} -> [ORDER NUMBER].
    """
    def replace(match):
        inner = match.group(1).strip()
        return f"[{inner.upper()}]"

    return re.sub(r"\{\{(.*?)\}\}", replace, text)


def main():
    df = pd.read_csv(RAW_PATH)
    df = df[["category", "response"]].dropna()

    templates = {}

    for category, group in df.groupby("category"):
        # Pick the most common response length bucket as a proxy for
        # "a typical, well-formed example" rather than the shortest/oddest one.
        # Simple approach: take the response closest to the median length.
        lengths = group["response"].str.len()
        median_len = lengths.median()
        closest_idx = (lengths - median_len).abs().idxmin()
        chosen_response = group.loc[closest_idx, "response"]

        templates[category] = tidy_placeholders(chosen_response)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(templates, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(templates)} category templates to {OUTPUT_PATH}\n")
    for cat, resp in templates.items():
        print(f"--- {cat} ---")
        print(resp)
        print()


if __name__ == "__main__":
    main()
