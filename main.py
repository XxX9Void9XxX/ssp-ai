from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()

# Allow frontend JS to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Prompt(BaseModel):
    message: str

@app.get("/api/status")
def status():
    return {"status": "AI server running"}

@app.post("/api/chat")
def chat(prompt: Prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt.message}
        ]
    )
    return {
        "reply": response.choices[0].message.content
    }

# Serve frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
