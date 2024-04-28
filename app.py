from flask import Flask
import google.generativeai as genai
from os import environ as env
from flask import request
from lib.safety_instructions import safety_instructions

app = Flask(__name__)
API_KEY = env.get("API_KEY")
genai.configure(api_key=API_KEY)
with open("preset.txt", 'r') as f:
    text = f.read()

model = genai.GenerativeModel(
    'gemini-1.5-pro-latest',
    system_instruction=text
)

del text
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


@app.route('/reset/<chat_id>')
def reset(chat_id):
    if chat_id in chats:
        del chats[chat_id]
    return "Chat reset"


@app.route('/chat', methods=['POST'])
def handle_chat():
    data = request.get_json()
    chat_id = data['chatId']
    message = data['message']

    if chat_id in chats:
        chat = model.start_chat(history=chats[chat_id].history)
    else:
        chat = model.start_chat()
        chats[chat_id] = chat

    try:
        response = chat.send_message(message)
    except Exception as e:
        print(e)
        return "I'm really sorry, but I can't chat right now. Please try again later."

    chats[chat_id] = chat

    return response.parts[0].text


if __name__ == '__main__':
    app.run()
