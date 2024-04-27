from google.generativeai import GenerativeModel

def createAnalysisPromptFromMessage(msg: str, model: GenerativeModel) -> str:
    prompt = f"Given the following message, analyse the type of person and give recomendations on how to communicate better with them:\n{msg}"
    res = model.start_chat(history=[]).send_message(prompt).resolve()
    return res