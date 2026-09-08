from tools import (
    attendance_tool,
    exam_tool,
    office_tool,
    notice_tool
)


def student_agent(question):
    question = question.lower()

    if "attendance" in question:
        return attendance_tool("Aashika")

    elif "exam" in question:
        return exam_tool()

    elif "office" in question:
        return office_tool()

    elif "notice" in question:
        return notice_tool()

    else:
        return "Sorry, I don't have information about this question."


if __name__ == "__main__":
    print("AI Student Support Assistant")
    print("----------------------------")

    question = input("Ask your question: ")

    answer = student_agent(question)

    print("\nAssistant:", answer)