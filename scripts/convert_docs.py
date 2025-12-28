#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marker-pdf",
# ]
# ///
"""
Convert documents in docs/raw to markdown in docs/books.
- EPUB files: converted using pandoc
- PDF files: converted using marker
"""

import subprocess
import sys
from pathlib import Path


def convert_epub(input_path: Path, output_path: Path) -> bool:
    """Convert EPUB to Markdown using pandoc."""
    try:
        subprocess.run(
            [
                "pandoc",
                str(input_path),
                "-o",
                str(output_path),
                "--wrap=none",
                "--extract-media",
                str(output_path.parent / f"{output_path.stem}_media"),
            ],
            check=True,
            capture_output=True,
        )
        print(f"✓ Converted EPUB: {input_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed EPUB: {input_path.name} - {e.stderr.decode()}")
        return False


def convert_pdf(input_path: Path, output_dir: Path) -> bool:
    """Convert PDF to Markdown using marker."""
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered

    try:
        converter = PdfConverter(artifact_dict=create_model_dict())
        rendered = converter(str(input_path))
        text, _, _ = text_from_rendered(rendered)

        output_path = output_dir / f"{input_path.stem}.md"
        output_path.write_text(text)
        print(f"✓ Converted PDF: {input_path.name}")
        return True
    except Exception as e:
        print(f"✗ Failed PDF: {input_path.name} - {e}")
        return False


def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    raw_dir = project_root / "docs" / "raw"
    output_dir = project_root / "docs" / "books"

    if not raw_dir.exists():
        print(f"Error: {raw_dir} does not exist")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    epubs = list(raw_dir.glob("*.epub"))
    pdfs = list(raw_dir.glob("*.pdf"))

    print(f"Found {len(epubs)} EPUB and {len(pdfs)} PDF files\n")

    # Convert EPUBs first (faster, no model loading)
    for epub in epubs:
        output_path = output_dir / f"{epub.stem}.md"
        convert_epub(epub, output_path)

    # Convert PDFs (slower, requires model loading)
    if pdfs:
        print("\nLoading marker models (this may take a moment)...")
        for pdf in pdfs:
            convert_pdf(pdf, output_dir)

    print(f"\nDone! Output saved to: {output_dir}")


if __name__ == "__main__":
    main()
