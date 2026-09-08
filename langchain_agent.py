from langchain_core.tools import tool
from langchain_ollama import ChatOllama

from tools import (
    attendance_tool,
    exam_tool,
    office_tool,
    notice_tool
)

from memory import save_memory, get_memory


@tool
def attendance(student_name: str) -> str:
    """Get a student's attendance."""
    return attendance_tool(student_name)


@tool
def exam_information() -> str:
    """Get examination information."""
    return exam_tool()


@tool
def office_information() -> str:
    """Get college office information."""
    return office_tool()


@tool
def college_notice() -> str:
    """Get the latest college notice."""
    return notice_tool()


model = ChatOllama(
    model="llama3.2",
    temperature=0
)


def student_agent(question):

    question_lower = question.lower()

    if "attendance" in question_lower:
        answer = attendance.invoke({
            "student_name": "Aashika"
        })

    elif "exam" in question_lower:
        answer = exam_information.invoke({})

    elif "office" in question_lower:
        answer = office_information.invoke({})

    elif "notice" in question_lower:
        answer = college_notice.invoke({})

    else:
        answer = model.invoke(question).content

    save_memory(question, answer)

    return answer


if __name__ == "__main__":

    print("AI Student Support Assistant")
    print("----------------------------")

    question = input("Ask your question: ")

    answer = student_agent(question)

    print("\nAssistant:", answer)

    print("\nMemory:")
    print(get_memory())