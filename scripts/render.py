#!/usr/bin/env python3
"""Render a GL workshop content pack to preview HTML."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_markdown_file(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    meta: dict = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            meta = yaml.safe_load(text[3:end]) or {}
            body = text[end + 4 :].lstrip("\n")
    return meta, body


def md_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    in_ul = False
    in_ol = False
    in_table = False
    table_rows: list[str] = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def flush_table() -> None:
        nonlocal in_table, table_rows
        if not table_rows:
            return
        out.append('<div class="table-wrap"><table>')
        for i, row in enumerate(table_rows):
            cells = [c.strip() for c in row.strip("|").split("|")]
            tag = "th" if i == 0 else "td"
            if i == 1 and all(re.match(r"^:?-+:?$", c or "") for c in cells):
                continue
            out.append("<tr>" + "".join(f"<{tag}>{md_inline(c)}</{tag}>" for c in cells) + "</tr>")
        out.append("</table></div>")
        table_rows = []
        in_table = False

    for line in lines:
        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            close_lists()
            in_table = True
            table_rows.append(line)
            continue
        if in_table:
            flush_table()

        if not line.strip():
            close_lists()
            continue
        if line.startswith("### "):
            close_lists()
            out.append(f"<h3>{md_inline(line[4:])}</h3>")
        elif line.startswith("## "):
            close_lists()
            out.append(f"<h3>{md_inline(line[3:])}</h3>")
        elif line.startswith("# "):
            close_lists()
            out.append(f"<h2>{md_inline(line[2:])}</h2>")
        elif re.match(r"^- ", line):
            if not in_ul:
                close_lists()
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{md_inline(line[2:])}</li>")
        elif re.match(r"^\d+\. ", line):
            if not in_ol:
                close_lists()
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{md_inline(re.sub(r'^\d+\. ', '', line))}</li>")
        else:
            close_lists()
            out.append(f"<p>{md_inline(line)}</p>")

    close_lists()
    if in_table:
        flush_table()
    return "\n".join(out)


def section_fold(sid: str, label: str, title: str, body_html: str) -> str:
    return f"""
    <section id="{html.escape(sid)}">
      <details class="fold">
        <summary>
          <div class="fold-heading">
            <p class="section-label">{html.escape(label)}</p>
            <h2>{html.escape(title)}</h2>
          </div>
          <span class="fold-chevron" aria-hidden="true"></span>
        </summary>
        <div class="fold-body prose">{body_html}</div>
      </details>
    </section>
    """


def render_pack(program: str, unit: str, locale: str) -> Path:
    pack_dir = ROOT / "content" / program / unit / locale
    manifest = load_yaml(pack_dir / "manifest.yaml")
    assets = manifest["assets"]

    sections: list[str] = []
    toc: list[tuple[str, str]] = []

    def add(sid: str, label: str, ref: dict) -> None:
        meta, body = parse_markdown_file(pack_dir / ref["path"])
        title = ref.get("title") or meta.get("title") or sid
        toc.append((sid, title))
        sections.append(section_fold(sid, label, title, md_to_html(body)))

    add("research", "Pre-work · Research", assets["research_article"])
    add("opinion", "Pre-work · Opinion", assets["opinion_article"])
    add("assessment", "Pre-work · Diagnostic", assets["self_assessment"])
    for i, case in enumerate(assets.get("cases", []), 1):
        add(f"case-{i}", f"Live · Case {i}", case)
    add("framework", "Live · Framework", assets["framework_tool"])
    if assets.get("live_roleplay_1v1"):
        add("roleplay-1v1", "Live · Role-play", assets["live_roleplay_1v1"])
    if assets.get("live_roleplay_strategic"):
        add("roleplay-strategic", "Live · Strategic role-play", assets["live_roleplay_strategic"])
    add("key-notes", "Take-away · Key notes", assets["key_notes"])
    add("commitment", "Close · Commitment", assets["commitment_plan"])

    toc_html = "\n".join(
        f'<a href="#{html.escape(sid)}">{html.escape(title[:48])}</a>' for sid, title in toc
    )
    title = manifest["public_title"]
    audience = manifest["audience_id"]
    program_id = manifest["program_id"]

    page = f"""<!DOCTYPE html>
<html lang="{html.escape(locale)}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)} — {html.escape(program_id)} {html.escape(unit.upper())}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Outfit:wght@400;500;600&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --ink: #14221c; --ink-soft: #2a3d34; --paper: #f3efe6; --paper-2: #e8e2d4;
      --line: #c9c0ae; --accent: #0f6e56; --accent-deep: #0a4f3d; --warm: #c45c26;
      --white: #fbfaf6; --shadow: 0 18px 40px rgba(20, 34, 28, 0.08); --wide: 68rem; --max: 44rem;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; color: var(--ink); font-family: "Outfit", system-ui, sans-serif; line-height: 1.65;
      background: radial-gradient(1200px 600px at 10% -10%, rgba(15,110,86,.12), transparent 55%),
        linear-gradient(180deg, #f7f3ea 0%, var(--paper) 40%, #efe9db 100%);
    }}
    .hero {{
      min-height: min(70vh, 560px); display: grid; align-items: end; color: var(--white);
      padding: 1.25rem clamp(1.25rem,4vw,3rem) 2.5rem;
      background: linear-gradient(165deg, rgba(10,40,32,.92), rgba(15,70,54,.88) 45%, rgba(20,34,28,.94));
    }}
    .brand {{ font-family: "Fraunces", Georgia, serif; font-size: clamp(2rem,6vw,3.5rem); font-weight: 700; margin: 0 0 .5rem; }}
    .hero h1 {{ font-family: "Fraunces", Georgia, serif; font-size: clamp(1.25rem,3vw,1.85rem); font-weight: 500; max-width: 22ch; margin: 0 0 1rem; }}
    .hero-lead {{ max-width: 40rem; color: rgba(251,250,246,.88); }}
    .hero-meta {{ display: flex; flex-wrap: wrap; gap: .75rem 1.25rem; margin-top: 1.25rem; color: rgba(251,250,246,.7); font-size: .95rem; }}
    .toc {{ position: sticky; top: 0; z-index: 20; backdrop-filter: blur(10px); background: rgba(243,239,230,.9); border-bottom: 1px solid var(--line); }}
    .toc-inner {{ max-width: var(--wide); margin: 0 auto; padding: .65rem clamp(1.25rem,4vw,3rem); display: flex; gap: .35rem 1rem; overflow-x: auto; }}
    .toc a {{ flex: 0 0 auto; text-decoration: none; color: var(--ink-soft); font-size: .82rem; font-weight: 500; }}
    main {{ max-width: var(--wide); margin: 0 auto; padding: 1.5rem clamp(1.25rem,4vw,3rem) 4rem; }}
    section {{ padding: .5rem 0; border-bottom: 1px solid var(--line); }}
    .section-label {{ font-size: .78rem; letter-spacing: .14em; text-transform: uppercase; color: var(--accent); font-weight: 600; margin: 0 0 .35rem; }}
    h2 {{ font-family: "Fraunces", Georgia, serif; font-size: clamp(1.35rem,2.8vw,1.85rem); margin: 0; letter-spacing: -.02em; }}
    .fold > summary {{ list-style: none; cursor: pointer; display: grid; grid-template-columns: 1fr auto; gap: .35rem 1rem; padding: 1.25rem 0; }}
    .fold > summary::-webkit-details-marker {{ display: none; }}
    .fold-chevron {{ width: 2.1rem; height: 2.1rem; border-radius: 999px; border: 1px solid var(--line); background: var(--white); display: inline-flex; align-items: center; justify-content: center; }}
    .fold-chevron::before {{ content: ""; width: .4rem; height: .4rem; border-right: 2px solid var(--ink-soft); border-bottom: 2px solid var(--ink-soft); transform: rotate(45deg) translate(-1px,-1px); }}
    .fold[open] > summary .fold-chevron {{ transform: rotate(180deg); background: var(--ink); border-color: var(--ink); }}
    .fold[open] > summary .fold-chevron::before {{ border-color: var(--white); }}
    .fold-body {{ padding: 0 0 1.75rem; max-width: var(--max); }}
    .prose p {{ margin: 0 0 1rem; }}
    .prose ul, .prose ol {{ margin: 0 0 1rem; padding-left: 1.2rem; }}
    .prose h2:first-child {{ display: none; }}
    .table-wrap {{ overflow-x: auto; margin: 1rem 0; border: 1px solid var(--line); border-radius: 12px; background: var(--white); }}
    table {{ width: 100%; border-collapse: collapse; font-size: .92rem; }}
    th, td {{ padding: .7rem .9rem; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ background: var(--paper-2); }}
    footer {{ max-width: var(--wide); margin: 0 auto; padding: 1rem clamp(1.25rem,4vw,3rem) 3rem; color: var(--ink-soft); font-size: .88rem; }}
  </style>
</head>
<body>
  <header class="hero">
    <div>
      <p class="brand">Global Leadership</p>
      <h1>{html.escape(title)}</h1>
      <p class="hero-lead">{html.escape(manifest.get("unit_goal", "").strip())}</p>
      <div class="hero-meta">
        <span>{html.escape(program_id)} · {html.escape(unit.upper())}</span>
        <span>{html.escape(audience)}</span>
        <span>Locale: {html.escape(locale)}</span>
      </div>
    </div>
  </header>
  <nav class="toc" aria-label="Sections"><div class="toc-inner">{toc_html}</div></nav>
  <main id="contenido">
    {''.join(sections)}
  </main>
  <footer>
    <p>{html.escape(program_id)} · Global Leadership · Factory preview (not for client brand review until approved)</p>
  </footer>
  <script>
    (function () {{
      function openFoldTarget(id) {{
        if (!id) return;
        var el = document.getElementById(id);
        if (!el) return;
        var node = el;
        while (node && node !== document.body) {{
          if (node.tagName === "DETAILS") node.open = true;
          node = node.parentElement;
        }}
        if (el.tagName !== "DETAILS") {{
          var child = el.querySelector(":scope > details.fold");
          if (child) child.open = true;
        }}
      }}
      function syncHash() {{ openFoldTarget((location.hash || "").slice(1)); }}
      window.addEventListener("hashchange", syncHash);
      syncHash();
    }})();
  </script>
</body>
</html>
"""

    out_dir = ROOT / "preview" / program / unit / locale
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(page, encoding="utf-8")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--program", default="atc")
    parser.add_argument("--unit", default="u01")
    parser.add_argument("--locale", default="en")
    args = parser.parse_args()
    path = render_pack(args.program, args.unit, args.locale)
    print(f"RENDER OK  {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
