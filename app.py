from flask import Flask
import google.generativeai as genai
from google.generativeai import ChatSession
from os import environ as env

app = Flask(__name__)
API_KEY = env.get("API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')


# id: Int -> chat: array of some shit
chats = dict()

@app.route("/history/<chat_id>")
def history(chat_id: int):
    if chat_id not in chats:
        return f"No history for chat with id {chat_id}"

    history = []

    for msg in chats[chat_id].history:
        history.append(
            {
                "role": msg.role,
                "text": msg.parts[0].text
            }
        )

    return history

@app.route('/chat/<chat_id>/<query>')
def chat(chat_id: int, query: str):  # put application's code here
    if chat_id in chats:
        chat = model.start_chat(history=chats[chat_id].history)
        # send preset message to Chat to make it behave as Mercedes consultant
        with open("preset.txt", 'r') as f:
            text = f.read()
            chat.send_message(text)
    else:
        chat = model.start_chat(history=[])
        chats[chat_id] = chat

    response = chat.send_message(query)
    chats[chat_id] = chat

    return response.parts[0].text


if __name__ == '__main__':
    app.run()
