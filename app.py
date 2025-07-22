from flask import Flask, render_template, request
from code_reviewer import app as langgraph_app  

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        question = request.form["question"]
        user_solution = request.form["user_solution"]

        initial_state = {
            "question": question,
            "user_solution": user_solution
        }
        result = langgraph_app.invoke(initial_state)
        return render_template("result.html", result=result)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True,port=5050)
