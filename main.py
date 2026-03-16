from fastapi import FastAPI
from google import genai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home route
@app.get("/")
def home():
    return {"message": "AI Study Agent Running"}

# Ask AI
@app.post("/ask")
async def ask_agent(question: str):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=question
        )

        answer = response.text if response.text else "No response from AI"

        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}