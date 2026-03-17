from fastapi import FastAPI, Body
from google import genai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

app = FastAPI()

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Study Agent Running"}

@app.post("/ask")
async def ask_agent(data: dict = Body(...)):

    question = data.get("question")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=question
        )

        return {"answer": response.text}

    except Exception as e:
        return {"error": str(e)}