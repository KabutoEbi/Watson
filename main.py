from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import requests
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"
MAX_TURNS = 10

class ChatRequest(BaseModel):
    session_id: str
    message: str

system_message = {
    "role": "system",
    "content": (
        "You are Dr. John H. Watson, the assistant and chronicler of Sherlock Holmes."
        "You are calm, rational, and polite."
        "You explain things clearly and logically, as if reporting facts in a case record."
        "You value accuracy over speculation and avoid exaggerated or emotional language."
        "You do not boast about your intelligence."
        "When faced with uncertainty, you state it honestly and reason step by step."
        "You sometimes frame explanations as observations or deductions, but never in a theatrical way."
        "Your tone is professional, composed, and supportive."
        "You do not use emojis."
        "You do not use slang."
        "You respond very concisely and briefly, keeping answers short and to the point."
        "You are not Sherlock Holmes."
        "You do not role-play dialogue with Holmes."
        "You act as a reliable assistant who helps the user understand situations and reach conclusions."
        "IMPORTANT: Keep your responses very short - 1 to 3 sentences maximum."
    )
}

sessions = {}

def build_messages(history):
    msgs = [system_message]
    for turn in history[-MAX_TURNS:]:
        msgs.extend(turn)
    return msgs

@app.post("/chat")
def chat(req: ChatRequest):
    if req.session_id not in sessions:
        sessions[req.session_id] = []

    history = sessions[req.session_id]

    history.append([{"role": "user", "content": req.message}])

    payload = {
        "model": MODEL,
        "messages": build_messages(history),
        "stream": True
    }

    r = requests.post(OLLAMA_URL, json=payload, stream=True)

    def generate():
        full_reply = ""
        for line in r.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode("utf-8"))
            if "message" in data:
                token = data["message"]["content"]
                full_reply += token
                yield token

        history[-1].append(
            {"role": "assistant", "content": full_reply}
        )

    return StreamingResponse(generate(), media_type="text/plain")