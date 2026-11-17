import logging
from pathlib import Path

from pypdf import PdfReader

logger = logging.getLogger(__name__)


def text_extracter():
    pdf_path = Path(__file__).resolve().parents[2] / "DAYS GONE.pdf"

    reader = PdfReader(pdf_path)
    logger.info("Extracting text from %d PDF pages", len(reader.pages))

    text_from_pdf = ""
    for page in reader.pages:
        text_from_pdf += page.extract_text()

    return text_from_pdf
