from pathlib import Path
from pypdf import PdfReader

def text_extracter():
    pdf_path = Path(__file__).resolve().parents[2] / "DAYS GONE.pdf"

    reader = PdfReader(pdf_path)
    print(f"Pages: {len(reader.pages)}")

    text_from_pdf = ""
    for i in range(len(reader.pages)):
        text_from_pdf += reader.pages[i].extract_text()
    print("Done")

    return text_from_pdf