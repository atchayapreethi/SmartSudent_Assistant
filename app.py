from flask import Flask, render_template, request
from rag_graph import app as ai_app

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    answer = ""
    question = ""

    if request.method == "POST":

        question = request.form["question"]

        result = ai_app.invoke({
            "question": question,
            "context": "",
            "answer": ""
        })

        answer = result["answer"]

    return render_template(
        "index.html",
        question=question,
        answer=answer
    )


if __name__ == "__main__":
    app.run(debug=True)