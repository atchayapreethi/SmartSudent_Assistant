from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama

# Read FAQ document
file_path = Path("data/faq/student_faq.txt")
text = file_path.read_text(encoding="utf-8")

# Split document
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_text(text)

# Ollama model
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

question = input("Student: ")

# Simple retrieval: find relevant chunks
relevant_chunks = []

for chunk in chunks:
    if any(word.lower() in chunk.lower() for word in question.split()):
        relevant_chunks.append(chunk)

if not relevant_chunks:
    relevant_chunks = chunks

context = "\n\n".join(relevant_chunks)

prompt = f"""
You are an AI Student Support Assistant.

Answer the student's question using the information in the context below.
If the answer is not available in the context, clearly say that the information
is not available in the knowledge base.

Context:
{context}

Student Question:
{question}
"""

response = llm.invoke(prompt)

print("\nAssistant:", response.content)