conversation_memory = []


def save_memory(question, answer):
    conversation_memory.append({
        "question": question,
        "answer": answer
    })


def get_memory():
    return conversation_memory