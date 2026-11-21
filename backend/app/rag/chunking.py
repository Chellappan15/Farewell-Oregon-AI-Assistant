import logging
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.games import DEFAULT_GAME, get_game

logger = logging.getLogger(__name__)


def chunking_function_v1():
    """Legacy PDF-based chunking (kept for reference)."""
    from utils.pdf_parser import text_extracter

    text = text_extracter()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_text(text)
    logger.info("Created %d chunks from PDF", len(chunks))

    return chunks


def chunking_function(game: str = DEFAULT_GAME) -> list[Document]:
    markdown_path = Path(get_game(game).knowledge_base_path)
    try:
        markdown = markdown_path.read_text(encoding="utf-8")

        headers = [
            ("#", "section"),
            ("##", "subsection"),
            ("###", "topic"),
        ]
        header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers,
            strip_headers=False,
        )
        documents = header_splitter.split_text(markdown)

        chunker = RecursiveCharacterTextSplitter(
            chunk_size=550,
            chunk_overlap=20,
        )
        chunks = chunker.split_documents(documents)
        logger.info("Created %d chunks from %s", len(chunks), markdown_path.name)

        return chunks
    except (OSError, ValueError) as exc:
        logger.exception("Failed to chunk Markdown file %s", markdown_path)
        raise RuntimeError("Unable to create document chunks") from exc
