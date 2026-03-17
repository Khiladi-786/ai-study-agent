from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS middleware must be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow localhost and deployed frontend
    allow_credentials=True,
    allow_methods=["*"],  # includes OPTIONS
    allow_headers=["*"],
)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


@app.get("/")
def home():
    return {"message": "AI Study Agent Running"}


@app.post("/ask")
async def ask_agent(request: Request):
    data = await request.json()
    question = data.get("question")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=question
        )

        return {"answer": response.text}

    except Exception as e:
        return {"error": str(e)}