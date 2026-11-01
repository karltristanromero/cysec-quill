#!/usr/bin/env python3
"""
export_pdf.py — Converts a markdown writeup bundle into a styled,
printable HTML report and triggers automated headless PDF rendering.

Usage:
    python3 scripts/export_pdf.py docs/lab-research/detection-engineering/wazuh-ssh-brute-force/index.md [output.pdf]
"""

import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Built-in lightweight markdown to HTML converter to avoid external pip dependencies
def md_to_html(md_text: str) -> str:
    # Strip YAML frontmatter
    md_text = re.sub(r"^---\s*\n.*?\n---\s*\n", "", md_text, flags=re.DOTALL)
    
    # Escape HTML special chars before markdown transforms
    out = []
    in_code_block = False
    code_block_lang = ""
    code_lines = []

    for line in md_text.splitlines():
        if line.startswith("```"):
            if in_code_block:
                escaped_code = html.escape("\n".join(code_lines))
                out.append(f"<pre><code>{escaped_code}</code></pre>")
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
                code_block_lang = line[3:].strip()
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Headings
        if line.startswith("# "):
            out.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("#### "):
            out.append(f"<h4>{html.escape(line[5:])}</h4>")
        elif line.startswith("> "):
            out.append(f"<blockquote><p>{html.escape(line[2:])}</p></blockquote>")
        elif line.strip() == "---":
            out.append("<hr />")
        elif line.startswith("- ") or line.startswith("* "):
            out.append(f"<li>{html.escape(line[2:])}</li>")
        elif line.strip() == "":
            out.append("")
        else:
            # Inline formatting: bold, italic, inline code, images
            l = html.escape(line)
            # Images: ![alt](src)
            l = re.sub(r"!\[(.*?)\]\((.*?)\)", r'<div class="img-container"><img src="\2" alt="\1" /><span class="caption">\1</span></div>', l)
            # Links: [text](href)
            l = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', l)
            # Code: `code`
            l = re.sub(r"`([^`]+)`", r'<code>\1</code>', l)
            # Bold: **bold**
            l = re.sub(r"\*\*([^\*]+)\*\*", r'<strong>\1</strong>', l)
            out.append(f"<p>{l}</p>")

    return "\n".join(out)


REPORT_CSS = """
@page {
    size: A4;
    margin: 20mm;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1a1a1a;
    line-height: 1.6;
    font-size: 11pt;
}
h1 {
    font-size: 20pt;
    border-bottom: 2px solid #2d3748;
    padding-bottom: 8px;
    margin-top: 0;
    color: #0f172a;
}
h2 {
    font-size: 15pt;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 24px;
    color: #1e293b;
}
h3 {
    font-size: 12pt;
    margin-top: 18px;
    color: #334155;
}
pre {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 12px;
    font-family: "Courier New", Courier, monospace;
    font-size: 9.5pt;
    white-space: pre-wrap;
    word-break: break-all;
}
code {
    background-color: #f1f5f9;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: monospace;
    font-size: 10pt;
}
blockquote {
    border-left: 4px solid #3b82f6;
    margin: 12px 0;
    padding: 4px 16px;
    background-color: #f0f9ff;
    color: #1e3a8a;
}
hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 20px 0;
}
.img-container {
    text-align: center;
    margin: 20px 0;
    page-break-inside: avoid;
}
img {
    max-width: 95%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
}
.caption {
    display: block;
    font-size: 9pt;
    color: #64748b;
    margin-top: 6px;
    font-style: italic;
}
"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/export_pdf.py <path/to/index.md> [output.pdf]")
        sys.exit(1)

    md_path = Path(sys.argv[1]).resolve()
    if not md_path.exists():
        print(f"Error: Target file not found: {md_path}")
        sys.exit(1)

    output_pdf = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else md_path.parent / f"{md_path.parent.name}-report.pdf"
    html_temp = md_path.parent / ".export_temp.html"

    md_content = md_path.read_text(encoding="utf-8")
    body_html = md_to_html(md_content)

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{md_path.parent.name}</title>
<style>{REPORT_CSS}</style>
</head>
<body>
{body_html}
</body>
</html>
"""
    html_temp.write_text(full_html, encoding="utf-8")
    print(f"Generated printable HTML: {html_temp.name}")

    # Headless rendering via system tools
    tool_executed = False

    # Check for Chromium / Chrome
    for chrome_bin in ["google-chrome", "chromium", "chromium-browser"]:
        chrome_path = shutil.which(chrome_bin)
        if chrome_path:
            cmd = [
                chrome_path,
                "--headless",
                "--disable-gpu",
                f"--print-to-pdf={output_pdf}",
                str(html_temp),
            ]
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, check=True)
                tool_executed = True
                break
            except Exception:
                pass

    if not tool_executed:
        # Check for Weasyprint
        if shutil.which("weasyprint"):
            try:
                subprocess.run(["weasyprint", str(html_temp), str(output_pdf)], check=True)
                tool_executed = True
            except Exception:
                pass

    if tool_executed:
        print(f"Successfully exported PDF report to:\n  {output_pdf}")
        html_temp.unlink(missing_ok=True)
    else:
        print(f"\nReport ready in HTML format: {html_temp}")
        print("Note: To compile directly to PDF, install chromium or weasyprint (e.g. 'sudo apt install chromium' or 'pip install weasyprint').")
        print(f"Alternatively, open '{html_temp}' in your browser and select Print -> Save as PDF.")


if __name__ == "__main__":
    main()
