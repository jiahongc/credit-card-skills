#!/usr/bin/env python3
"""
Generate a PDF from a card skill markdown report.

Renders markdown faithfully: pandoc (md -> styled HTML) then
headless Chrome (HTML -> PDF).

Usage:
    python3 generate-pdf.py <input.md> [output.pdf]

Requires: pandoc, Google Chrome (or Chromium/Brave/Edge)
"""

import sys
import os
import subprocess
import shutil
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(SCRIPT_DIR, "pdf-style.css")


def find_browser():
    """Find a Chrome-based browser for headless PDF printing."""
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    for name in ["google-chrome", "chromium", "chromium-browser"]:
        found = shutil.which(name)
        if found:
            return found
    return None


def md_to_pdf(md_path, pdf_path):
    """Convert markdown to PDF: pandoc (md->HTML) then Chrome (HTML->PDF)."""
    if not shutil.which("pandoc"):
        print("Error: pandoc not found. Install with: brew install pandoc")
        sys.exit(1)

    browser = find_browser()
    if not browser:
        print("Error: No Chrome-based browser found for PDF printing.")
        sys.exit(1)

    import re as _re

    html_path = tempfile.mktemp(suffix=".html")

    try:
        # pandoc markdown -> standalone HTML with embedded CSS
        cmd = [
            "pandoc", md_path,
            "-t", "html",
            "--standalone",
            "--metadata", "title=Card Report",
        ]
        if os.path.exists(CSS_PATH):
            cmd += ["--css", CSS_PATH]

        with open(html_path, "w") as out:
            subprocess.run(cmd, stdout=out, check=True)

        # Inline CSS — pandoc adds a <link> tag but Chrome file:// can't
        # resolve external stylesheets reliably. Replace any <link
        # rel="stylesheet"> with an inline <style> block in one pass.
        if os.path.exists(CSS_PATH):
            with open(CSS_PATH, "r") as f:
                css_content = f.read()
            with open(html_path, "r") as f:
                html = f.read()
            html = _re.sub(
                r'<link\s+rel="stylesheet"\s+href="[^"]*"\s*/?>',
                f"<style>\n{css_content}\n</style>",
                html,
                count=1,
            )
            with open(html_path, "w") as f:
                f.write(html)

        # headless Chrome HTML -> PDF
        result = subprocess.run(
            [
                browser,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                f"--print-to-pdf={pdf_path}",
                "--print-to-pdf-no-header",
                f"file://{html_path}",
            ],
            capture_output=True,
            text=True,
        )

        if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) < 500:
            print(f"Error: PDF was not created. Chrome stderr: {result.stderr}")
            sys.exit(1)

        size = os.path.getsize(pdf_path)
        print(f"PDF generated: {pdf_path} ({size:,} bytes)")

    finally:
        if os.path.exists(html_path):
            os.unlink(html_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate-pdf.py <input.md> [output.pdf]")
        sys.exit(1)

    input_path = sys.argv[1]
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        output_path = os.path.splitext(input_path)[0] + ".pdf"

    md_to_pdf(input_path, output_path)
