from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import openai
import os

openai.api_key = "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"
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://sarthakmahale0:hxzYg07MIslbgRqc@cluster0.eseu6ts.mongodb.net/chatgpt?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    myChats = [chat for chat in chats]
    print(myChats)
    return render_template("index.html", myChats = myChats)

@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        print(request.json)
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question": question})
        print(chat)
        if chat:
            data = {"question": question, "answer": f"{chat['answer']}"}
            return jsonify(data)
        else:
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
               {
                "role": "user",
                "content": question
               }
                     ],
            temperature=1,
            max_tokens=256,
            top_p=1,    
            frequency_penalty=0,
            presence_penalty=0
            )
            print(response)
            data = {"question":question,"answer":response["choices"][0]["message"]["content"]}
            mongo.db.chats.insert_one({"question":question,"answer":response["choices"][0]["message"]["content"]})
            return jsonify(data)
    data = {"result":"Thankyou Im just a machine learning model"}

app.run(debug=True, port=5001)