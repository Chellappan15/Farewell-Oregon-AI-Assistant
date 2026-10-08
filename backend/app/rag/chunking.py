from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.pdf_parser import text_extracter
# from app.utils.pdf_parser import text_extracter

def chunking_function():
    text = text_extracter()
    print(text_extracter)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_text(text)

    print(f"Total chunks: {len(chunks)}")

    return chunks