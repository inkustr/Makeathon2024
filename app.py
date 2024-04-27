from flask import Flask
import google.generativeai as genai
from os import environ as env

import personaAnalysis

app = Flask(__name__)
API_KEY = env.get("API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')


# id: Int -> chat: array of some shit
chats = dict()

@app.route("/<chat_id>/history")
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

@app.route('/<chat_id>/<query>')
def chat(chat_id: int, query: str):  # put application's code here
    if chat_id in chats:
        chat = model.start_chat(history=chats[chat_id].history)
    else: #no previous chat history
        chat = model.start_chat(history=[])
        chats[chat_id] = chat
        personaAdvice = personaAnalysis.createAnalysisPromptFromMessage(query)
        print("PersonaAdvice: personaAdvice")
        query += personaAdvice
    chat.send_message(query)
    chats[chat_id] = chat

    history = []

    for msg in chat.history:
        history.append(
            {
                "role": msg.role,
                "text": msg.parts[0].text
            }
        )

    return history

if __name__ == '__main__':
    app.run()
