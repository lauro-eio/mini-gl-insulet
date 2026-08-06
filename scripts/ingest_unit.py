#!/usr/bin/env python3
"""Import a workshop unit source folder into library/ (raw + SOURCE map only)."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Longer / more specific prefixes first (TraditionalBusinessCaseStudy before CaseStudy).
SOURCE_PREFIX_MAP: list[tuple[str, str]] = [
    ("TraditionalBusinessCaseStudy", "case_study_02.SOURCE.txt"),
    ("InvestigativeReport", "research_article.SOURCE.txt"),
    ("FeatureStory", "opinion_article.SOURCE.txt"),
    ("ParticipantKeyPoints", "key_notes.SOURCE.txt"),
    ("PersonalityQuiz", "self_assessment.SOURCE.txt"),
    ("UnitReflectionQuestions", "commitment_plan.SOURCE.txt"),
    ("RolePlayScenario1v1", "live_roleplay_1v1.SOURCE.txt"),
    ("StrategicRolePlay", "live_roleplay_strategic.SOURCE.txt"),
    ("CaseStudy", "case_study_01.SOURCE.txt"),
]

UNIT_RE = re.compile(r"^u\d{2}$")
PROGRAM_RE = re.compile(r"^[a-z_][a-z0-9_]{1,12}$")


def map_source_name(filename: str) -> str | None:
    stem = Path(filename).name
    lower = stem.lower()
    for prefix, dest in SOURCE_PREFIX_MAP:
        if lower.startswith(prefix.lower()):
            return dest
    return None


def browse_directory() -> Path | None:
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        print("ERROR: tkinter unavailable; pass --src instead of --browse", file=sys.stderr)
        return None
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    chosen = filedialog.askdirectory(title="Select workshop unit source folder")
    root.destroy()
    if not chosen:
        return None
    return Path(chosen)


def ingest(program: str, unit: str, src: Path, *, force: bool) -> int:
    if not PROGRAM_RE.match(program):
        print(f"ERROR: invalid --program {program!r} (use lowercase slug, e.g. atc, tfs)", file=sys.stderr)
        return 1
    if not UNIT_RE.match(unit):
        print(f"ERROR: invalid --unit {unit!r} (expected u01, u02, …)", file=sys.stderr)
        return 1
    if not src.is_dir():
        print(f"ERROR: source is not a directory: {src}", file=sys.stderr)
        return 1

    en_dir = ROOT / "library" / program / unit / "en"
    raw_dir = en_dir / "_raw"
    files = sorted(p for p in src.iterdir() if p.is_file())
    if not files:
        print(f"ERROR: no files in {src}", file=sys.stderr)
        return 1

    if raw_dir.exists() and any(raw_dir.iterdir()) and not force:
        print(
            f"ERROR: {raw_dir} already has files; re-run with --force to overwrite",
            file=sys.stderr,
        )
        return 1

    raw_dir.mkdir(parents=True, exist_ok=True)
    if force:
        for existing in raw_dir.iterdir():
            if existing.is_file():
                existing.unlink()
        for existing in en_dir.glob("*.SOURCE.txt"):
            existing.unlink()

    copied: list[str] = []
    mapped: list[tuple[str, str]] = []
    unmapped: list[str] = []

    for src_file in files:
        dest_raw = raw_dir / src_file.name
        shutil.copy2(src_file, dest_raw)
        copied.append(src_file.name)
        dest_name = map_source_name(src_file.name)
        if dest_name:
            shutil.copy2(src_file, en_dir / dest_name)
            mapped.append((src_file.name, dest_name))
        else:
            unmapped.append(src_file.name)

    print(f"INGEST OK  library/{program}/{unit}/en")
    print(f"  program_id: {program.upper()}")
    print(f"  source:     {src}")
    print(f"  raw files:  {len(copied)}")
    for original, dest in mapped:
        print(f"  SOURCE      {dest}  <-  {original}")
    if unmapped:
        print("  WARN unmapped (left in _raw only):")
        for name in unmapped:
            print(f"    - {name}")
    print(f"  next: rewrite content/{program}/{unit}/en/ then validate/render")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--program", required=True, help="Folder slug (e.g. atc, tfs)")
    parser.add_argument("--unit", required=True, help="Unit id (e.g. u01)")
    parser.add_argument("--src", type=Path, help="Path to unit source directory")
    parser.add_argument(
        "--browse",
        action="store_true",
        help="Open a folder picker instead of --src",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing _raw and SOURCE files",
    )
    args = parser.parse_args()

    src: Path | None = args.src
    if args.browse:
        if src is not None:
            print("ERROR: use either --src or --browse, not both", file=sys.stderr)
            return 1
        src = browse_directory()
        if src is None:
            print("ERROR: no folder selected", file=sys.stderr)
            return 1
    elif src is None:
        print("ERROR: pass --src PATH or --browse", file=sys.stderr)
        return 1

    return ingest(args.program.lower(), args.unit.lower(), src.resolve(), force=args.force)


if __name__ == "__main__":
    sys.exit(main())
