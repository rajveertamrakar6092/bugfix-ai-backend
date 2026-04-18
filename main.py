from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# ✅ Get API key safely
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY is missing!")

# Configure Gemini
genai.configure(api_key=api_key)

# Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

# Request schema
class CodeRequest(BaseModel):
    code: str

# Optional test route
@app.get("/")
def home():
    return {"status": "running"}

# Main API
@app.post("/fix")
async def fix_code(request: CodeRequest):
    try:
        prompt = f"""
You are an expert programmer.

Fix the following code and return ONLY the corrected code.
Do NOT include explanation or extra text.

Code:
{request.code}
"""

        response = model.generate_content(prompt)

        if not response or not response.text:
            return {"result": "Error: No response from AI"}

        return {"result": response.text.strip()}

    except Exception as e:
        return {"error": str(e)}
