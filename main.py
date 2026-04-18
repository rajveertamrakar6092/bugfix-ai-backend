from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"))

class CodeRequest(BaseModel):
    code: str

@app.post("/fix")
async def fix_code(request: CodeRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are an expert programmer and debugger."},
                {
                    "role": "user",
                    "content": f"""
Fix the following code.

Return:
1. Corrected Code
2. Explanation of the bug
3. Optimized version (if possible)

Code:
{request.code}
"""
                }
            ]
        )

        result = response.choices[0].message.content

        return {"result": result}

    except Exception as e:
        return {"error": str(e)}