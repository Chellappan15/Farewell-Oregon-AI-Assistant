
from langchain_text_splitters import MarkdownHeaderTextSplitter

with open("DAYS GONE.md", "r", encoding="utf-8") as file:
    markdown = file.read()

headers = [
    ("#", "title"),
    ("##", "section"),
    ("###", "subsection"),
    ("####", "topic")
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers,
    strip_headers=False
)

documents = splitter.split_text(markdown)

from langchain_text_splitters import RecursiveCharacterTextSplitter

chunker = RecursiveCharacterTextSplitter(
    chunk_size=550,
    chunk_overlap=20
)

chunks = chunker.split_documents(documents)
print(chunks)

# for chunk in chunks[:6]:
#     print(chunk.page_content)
#     print(chunk.metadata)