from fastapi import FastAPI
import requests
import os

app = FastAPI()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.get("/")
def home():
    return {"message": "Feedback Summarization API is running"}

@app.post("/summarize")
def summarize(feedback: str):
    
    
    if not OPENAI_API_KEY:
        return {
            "summary": "This is a sample summarized response (API key not configured)."
        }

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Summarize this feedback briefly."},
            {"role": "user", "content": feedback}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        summary = result["choices"][0]["message"]["content"]

        return {"summary": summary}

    except Exception as e:
        return {
            "error": "Failed to process request",
            "details": str(e)
        }