from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Prompt(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "AI server running"}

@app.post("/chat")
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
