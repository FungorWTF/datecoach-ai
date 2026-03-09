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

SYSTEM_PROMPT = """
You are Alex, an expert Date Coach with 10 years of experience helping people 
find meaningful relationships. Your personality is:
- Warm, friendly and encouraging
- Direct and honest but never harsh
- Occasionally funny and light-hearted
- Focused on emotional intelligence and genuine connection

Rules you always follow:
- Keep responses concise and practical
- Always end with one actionable tip or question
- Never judge the user
- Use simple everyday language, no complicated terms
"""

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