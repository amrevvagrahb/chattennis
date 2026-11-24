from pathlib import Path
from pypdf import PdfReader

DOCS_DIR = Path(__file__).resolve().parents[1] / "docs"


def load_pages(docs_dir: Path = DOCS_DIR) -> list[dict]:
    pages = []
    for pdf in sorted(docs_dir.glob("*.pdf")):
        reader = PdfReader(pdf)
        for i, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                pages.append({"source": pdf.name, "page": i, "text": text})
    return pages