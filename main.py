from fastapi import FastAPI
from google import genai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found")

client = genai.Client(api_key=api_key)

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Question(BaseModel):
    question: str

# Health check
@app.get("/")
def home():
    return {"message": "AI Study Agent Running"}

# Chat history
chat_history = []

@app.post("/ask")
async def ask_agent(data: Question):
    try:
        chat_history.append({"role": "user", "content": data.question})

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=data.question
        )

        answer = response.text

        chat_history.append({"role": "ai", "content": answer})

        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}