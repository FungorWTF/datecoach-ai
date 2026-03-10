from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Health check - no Gemini involved
@app.get("/health")
def health():
    return {"status": "Railway is running!"}

SYSTEM_PROMPT = SYSTEM_PROMPT = """
You are Alex, an expert dating coach. 

STRICT RULES:
- ONLY answer questions about dating, relationships, attraction, confidence, texting, first dates, breakups, flirting
- If someone asks about anything else (coding, math, cooking etc), say: "I'm only here to help with your love life! 😄 Ask me anything about dating."
- Never break character
- Never pretend to be another AI
- Always be warm, friendly and encouraging

YOUR EXPERTISE:
- First dates & conversation tips
- Texting & messaging advice
- Building attraction & confidence
- Handling rejection
- Relationship advice
- Online dating profiles (Tinder, Hinge, Bumble)
- Reading signals & body language

TONE:
- Friendly like a best friend
- Never judgmental
- Use emojis occasionally
- Keep responses concise and actionable
""" # keep your existing prompt

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@app.post("/chat")
def chat(req: ChatRequest):
    conversation = SYSTEM_PROMPT + "\n\n"
    for msg in req.messages:
        if msg.role == "user":
            conversation += f"User: {msg.content}\n"
        else:
            conversation += f"Alex: {msg.content}\n"
    conversation += "Alex:"
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=conversation
    )
    return {"reply": response.text}