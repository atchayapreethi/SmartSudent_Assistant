from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Read FAQ document
file_path = Path("data/faq/student_faq.txt")

text = file_path.read_text(encoding="utf-8")

# Split document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_text(text)

print("Document loaded successfully!")
print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk)