from flask import Flask, render_template, request

from Chatbot import getAnswer
from neuralnetwork.ReponseNNChatbot import predict_class, getResponse, intents

app = Flask(__name__)


@app.route("/chatbot")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    #result from rule-based chatbot
    rule_based_result = getAnswer(userText)

    #result from deep neural network chatbot
    ints = predict_class(userText)
    nn_result  = getResponse(ints,intents)
    return rule_based_result

if __name__ == "__main__":
    app.run()