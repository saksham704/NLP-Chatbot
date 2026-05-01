from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

synonyms = {
    "hello": ["hi", "hey"],
    "bye": ["goodbye", "see you"],
    "name": ["who are you"]
}

data = [
    "hello","how are you","what is your name","bye","what can you do",
    "tell me a joke","thank you","who created you","what is ai",
    "what is nlp","good morning","good night","what is your favorite color",
    "i love you","are you human","help me","how old are you",
    "what is programming","what is javascript","what is machine learning"
]

responses = [
    ["Hello!", "Hi there!", "Hey! 👋"],
    ["I'm doing great!", "All good 😊"],
    ["I'm your smart NLP chatbot 🤖"],
    ["Goodbye!", "See you later 👋"],
    ["I can chat, answer questions, and help you learn!"],
    ["Why did the computer go to the doctor? Because it caught a virus! 😄"],
    ["You're welcome! 😊"],
    ["I was created by a developer learning AI 🤖"],
    ["AI = Artificial Intelligence"],
    ["NLP helps computers understand language"],
    ["Good morning! ☀️"],
    ["Good night! 🌙"],
    ["I like blue 💙"],
    ["I love you too 🤖❤️"],
    ["I’m an AI, not human 🤖"],
    ["Sure! Ask me anything"],
    ["I’m timeless 😎"],
    ["Programming = giving instructions to computers"],
    ["JavaScript is used for web development"],
    ["Machine learning lets computers learn from data"]
]

stopwords = ["is","am","are","the","a","an","what","how","your"]

def preprocess(text):
    text = text.lower()
    for ch in ".,!?":
        text = text.replace(ch, "")
    words = text.split()
    words = [w for w in words if w not in stopwords]

    normalized = []
    for word in words:
        replaced = False
        for key, vals in synonyms.items():
            if word in vals:
                normalized.append(key)
                replaced = True
                break
        if not replaced:
            normalized.append(word)

    return normalized

def similarity(a, b):
    match = [w for w in a if w in b]
    return len(match) / max(len(a), len(b)) if max(len(a), len(b)) > 0 else 0

def get_response(user_input):
    tokens = preprocess(user_input)

    best_score = 0
    best_index = -1

    for i, item in enumerate(data):
        score = similarity(tokens, preprocess(item))
        if score > best_score:
            best_score = score
            best_index = i

    if best_score < 0.3:
        return "Sorry, I didn't understand 😅"

    return random.choice(responses[best_index])

@app.route("/")
def home():
    return render_template("face.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    return jsonify({"reply": get_response(user_msg)})

if __name__ == "__main__":
    app.run(debug=True, port=5001)