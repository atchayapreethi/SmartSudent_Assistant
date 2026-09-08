from langgraph.graph import StateGraph, START, END
from typing import TypedDict

from langchain_agent import student_agent


class AgentState(TypedDict):
    question: str
    answer: str


def agent_node(state: AgentState):
    try:
        answer = student_agent(state["question"])

        return {
            "answer": answer
        }

    except Exception as e:
        return {
            "answer": "Sorry, an error occurred while processing your question."
        }


graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)

graph.add_edge(START, "agent")
graph.add_edge("agent", END)

agent_graph = graph.compile()


if __name__ == "__main__":

    print("AI Student Support Assistant - LangGraph")
    print("-----------------------------------------")

    question = input("Ask your question: ")

    result = agent_graph.invoke({
        "question": question,
        "answer": ""
    })

    print("\nAssistant:", result["answer"])