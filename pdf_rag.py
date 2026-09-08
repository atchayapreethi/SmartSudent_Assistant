from pathlib import Path
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents():
    documents = []

    folders = [
        Path("data/regulations"),
        Path("data/syllabus"),
        Path("data/faq"),
        Path("data/notices")
    ]

    for folder in folders:

        if not folder.exists():
            continue

        for file_path in folder.iterdir():

            if file_path.suffix.lower() == ".pdf":

                try:
                    reader = PdfReader(str(file_path))

                    text = ""

                    for page in reader.pages:
                        page_text = page.extract_text()

                        if page_text:
                            text += page_text + "\n"

                    if text.strip():
                        documents.append({
                            "file": file_path.name,
                            "text": text
                        })

                except Exception as error:
                    print(f"Could not read {file_path.name}: {error}")

            elif file_path.suffix.lower() in [".txt", ".md"]:

                try:
                    text = file_path.read_text(encoding="utf-8")

                    if text.strip():
                        documents.append({
                            "file": file_path.name,
                            "text": text
                        })

                except Exception as error:
                    print(f"Could not read {file_path.name}: {error}")

    return documents


documents = load_documents()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


all_chunks = []

for document in documents:

    chunks = text_splitter.split_text(document["text"])

    for chunk in chunks:
        all_chunks.append({
            "file": document["file"],
            "text": chunk
        })


print("Documents loaded:", len(documents))
print("Total chunks:", len(all_chunks))

for item in all_chunks:

    print("\n---", item["file"], "---")
    print(item["text"][:300])