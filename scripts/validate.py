#!/usr/bin/env python3
"""Validate a GL workshop content pack against schemas and editorial rules."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "unit_manifest.schema.json"


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip("\n")
    return text


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def validate_pack(program: str, unit: str, locale: str) -> list[str]:
    errors: list[str] = []
    pack_dir = ROOT / "content" / program / unit / locale
    manifest_path = pack_dir / "manifest.yaml"
    if not manifest_path.exists():
        return [f"Missing manifest: {manifest_path}"]

    manifest = load_yaml(manifest_path)
    schema = load_yaml(SCHEMA_PATH) if SCHEMA_PATH.suffix in {".yaml", ".yml"} else None
    if SCHEMA_PATH.suffix == ".json":
        import json

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    Draft202012Validator(schema).validate(manifest)

    if manifest.get("program_id", "").lower() != program.lower() and manifest.get("program_id") != program.upper():
        # allow ATC vs atc folder naming
        if manifest.get("program_id") != program.upper():
            errors.append(f"program_id mismatch: {manifest.get('program_id')} vs folder {program}")

    if manifest.get("unit_id") != unit:
        errors.append(f"unit_id mismatch: {manifest.get('unit_id')} vs folder {unit}")
    if manifest.get("locale") != locale:
        errors.append(f"locale mismatch: {manifest.get('locale')} vs folder {locale}")

    banned = [b.lower() for b in manifest.get("banned_phrases", [])]
    budgets = manifest.get("word_budgets", {})

    refs: list[dict] = []
    assets = manifest.get("assets", {})
    for key, val in assets.items():
        if key == "cases":
            refs.extend(val)
        elif isinstance(val, dict) and "path" in val:
            refs.append(val)

    for ref in refs:
        path = pack_dir / ref["path"]
        if not path.exists():
            errors.append(f"Missing asset file: {path}")
            continue
        raw = path.read_text(encoding="utf-8")
        body = strip_front_matter(raw)
        lower = body.lower()
        for phrase in banned:
            if phrase.lower() in lower:
                errors.append(f"Banned phrase '{phrase}' found in {path.name}")
        # also scan front matter titles lightly
        if "atomic habits" in raw.lower():
            errors.append(f"Banned brand 'Atomic Habits' found in {path.name}")

        asset_id = ref.get("asset_id", "")
        budget = budgets.get(asset_id)
        if budget:
            wc = word_count(body)
            if wc > budget["max"]:
                errors.append(f"{path.name}: {wc} words exceeds max {budget['max']}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--program", default="atc")
    parser.add_argument("--unit", default="u01")
    parser.add_argument("--locale", default="en")
    args = parser.parse_args()

    errors = validate_pack(args.program, args.unit, args.locale)
    if errors:
        print("VALIDATE FAIL")
        for e in errors:
            print(f" - {e}")
        return 1
    print(f"VALIDATE OK  content/{args.program}/{args.unit}/{args.locale}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
