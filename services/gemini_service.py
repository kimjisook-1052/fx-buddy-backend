import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def ask_gemini(system_prompt: str, history: list, user_message: str) -> str:
    model = genai.GenerativeModel(
        model_name="gemini-3.6-flash",
        system_instruction=system_prompt,
    )

    gemini_history = []
    for m in history:
        role = m["role"] if isinstance(m, dict) else m.role
        content = m["content"] if isinstance(m, dict) else m.content
        gemini_role = "model" if role == "assistant" else "user"
        gemini_history.append({"role": gemini_role, "parts": [content]})

    chat = model.start_chat(history=gemini_history)
    response = chat.send_message(user_message)
    return response.text