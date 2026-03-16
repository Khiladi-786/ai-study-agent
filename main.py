from fastapi import FastAPI
from google import genai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Study Agent Running"}

@app.post("/ask")
async def ask_agent(question: str):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=question
        )
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}