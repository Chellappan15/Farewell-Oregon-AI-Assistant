from collections import Counter
from pathlib import Path

import pymupdf

PDF_PATH = Path(__file__).resolve().parent / "backend" / "DAYS GONE.pdf"
TEXT_BLOCK = 0


def get_body_font_size(doc) -> float:
    """Return the most common font size in the document (the body text size)."""
    sizes = Counter()
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != TEXT_BLOCK:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["text"].strip():
                        sizes[round(span["size"], 1)] += len(span["text"])
    return sizes.most_common(1)[0][0]


def is_heading_span(span: dict, body_size: float) -> bool:
    return "Bold" in span["font"] and round(span["size"], 1) > body_size


def get_heading_sizes(doc, body_size: float) -> list[float]:
    """Distinct heading font sizes, largest first. Index 0 = section level."""
    sizes = set()
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != TEXT_BLOCK:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["text"].strip() and is_heading_span(span, body_size):
                        sizes.add(round(span["size"], 1))
    return sorted(sizes, reverse=True)


def clean_heading(text: str) -> str:
    return text.strip().rstrip(":").strip()


def heading_level(text: str, size: float, heading_sizes: list[float]) -> str:
    """
    Decide if a stand-alone heading line is a section or a subsection.
    1. If the PDF uses different heading sizes, the biggest size is a section,
       the next size a subsection.
    2. If every heading has the same size (like this PDF), fall back to style:
       ALL CAPS = section, anything else = subsection.
    """
    if len(heading_sizes) > 1:
        return "section" if heading_sizes.index(size) == 0 else "subsection"
    letters = [c for c in text if c.isalpha()]
    return "section" if letters and all(c.isupper() for c in letters) else "subsection"


def parser(pdf_path: Path = PDF_PATH) -> list[dict]:
    """
    Return the PDF as an ordered list of paragraphs, each tagged with the
    section / subsection / entry it belongs to.
    """
    records: list[dict] = []
    section = subsection = entry = ""

    with pymupdf.open(pdf_path) as doc:
        body_size = get_body_font_size(doc)
        heading_sizes = get_heading_sizes(doc, body_size)

        for page in doc:
            for block in page.get_text("dict")["blocks"]:
                if block.get("type") != TEXT_BLOCK:
                    continue

                paragraph_lines: list[str] = []

                for line in block["lines"]:
                    spans = [s for s in line["spans"] if s["text"].strip()]
                    if not spans:
                        continue

                    # Collect the bold heading spans at the start of the line
                    heading_spans = []
                    for span in spans:
                        if not is_heading_span(span, body_size):
                            break
                        heading_spans.append(span)

                    if not heading_spans:
                        paragraph_lines.append("".join(s["text"] for s in spans).strip())
                        continue

                    heading_text = clean_heading("".join(s["text"] for s in heading_spans))
                    rest = "".join(s["text"] for s in spans[len(heading_spans):]).strip()

                    if rest:
                        # "SAP9 handgun: You can purchase..." -> entry with text
                        entry = heading_text
                        paragraph_lines.append(rest)
                        continue

                    # Heading alone on its line -> section or subsection.
                    # Save any text collected so far before the heading changes.
                    if paragraph_lines:
                        records.append({
                            "section": section, "subsection": subsection, "entry": entry,
                            "text": " ".join(paragraph_lines), "page": page.number + 1,
                        })
                        paragraph_lines = []

                    level = heading_level(heading_text, round(heading_spans[0]["size"], 1), heading_sizes)
                    if level == "section":
                        section, subsection, entry = heading_text, "", ""
                    else:
                        subsection, entry = heading_text, ""

                if paragraph_lines:
                    records.append({
                        "section": section, "subsection": subsection, "entry": entry,
                        "text": " ".join(paragraph_lines), "page": page.number + 1,
                    })

    return records