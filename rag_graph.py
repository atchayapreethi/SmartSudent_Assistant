from pathlib import Path
from typing import TypedDict

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END

from tools import attendance_tool, exam_tool, office_tool, notice_tool
from memory import save_memory, get_memory


class State(TypedDict):
    question: str
    context: str
    answer: str


# Load all documents
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


# Split documents
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


# Ollama
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# Retrieve relevant documents
def retrieve(state: State):

    question = state["question"]

    relevant_chunks = []

    for item in all_chunks:

        if any(
            word.lower() in item["text"].lower()
            for word in question.split()
        ):
            relevant_chunks.append(item)

    if not relevant_chunks:
        relevant_chunks = all_chunks

    context = ""

    for item in relevant_chunks:
        context += f"\nSource: {item['file']}\n"
        context += item["text"] + "\n"

    return {
        "context": context
    }


# Tools
def use_tool(state: State):

    question = state["question"].lower()

    if "attendance" in question:
        answer = attendance_tool("Aashika")

    elif "exam" in question or "examination" in question:
        answer = exam_tool()

    elif "office" in question:
        answer = office_tool()

    elif "notice" in question or "announcement" in question:
        answer = notice_tool()

    else:
        answer = ""

    return {
        "answer": answer
    }


# Generate answer
def generate_answer(state: State):

    if state["answer"]:
        return {
            "answer": state["answer"]
        }

    prompt = f"""
You are an AI Student Support Assistant.

Answer the student's question using the context provided below.

If the information is not available, clearly say:
"Information is not available in the knowledge base."

Context:
{state["context"]}

Student Question:
{state["question"]}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }


# Save memory
def save_conversation(state: State):

    save_memory(
        state["question"],
        state["answer"]
    )

    return {}


# LangGraph
graph = StateGraph(State)

graph.add_node("retrieve", retrieve)
graph.add_node("use_tool", use_tool)
graph.add_node("generate_answer", generate_answer)
graph.add_node("save_memory", save_conversation)

graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "use_tool")
graph.add_edge("use_tool", "generate_answer")
graph.add_edge("generate_answer", "save_memory")
graph.add_edge("save_memory", END)

app = graph.compile()


# Chat
print("AI Student Support Assistant")
print("Type 'exit' to stop.")

while True:

    question = input("\nStudent: ")

    if question.lower() in ["exit", "quit", "bye"]:

        print("\nConversation Memory:")

        for item in get_memory():
            print("Student:", item["question"])
            print("Assistant:", item["answer"])

        break

    result = app.invoke({
        "question": question,
        "context": "",
        "answer": ""
    })

    print("\nAssistant:", result["answer"])