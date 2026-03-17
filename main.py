from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.get("/")
def home():
    return {"message": "AI Study Agent Running"}


@app.post("/ask")
async def ask_agent(request: Request):

    data = await request.json()
    question = data.get("question")

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": question}
                ]
            }
        )

        result = response.json()

        answer = result["choices"][0]["message"]["content"]

        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}