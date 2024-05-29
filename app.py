from flask import Flask, render_template, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
from AI import get_response, cost_of_message, get_messages # type: ignore

app = Flask(__name__)
CORS(app)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: check if text is valid
    messages = get_messages(text)
    cost_of_message(messages) # Print cost to terminal
    response = get_response(messages)
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)