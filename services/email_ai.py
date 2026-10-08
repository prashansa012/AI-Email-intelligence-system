import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b"
)


def analyze_email(subject, body):

    # Limit email body size for the local LLM
    body = body[:6000]

    prompt = f"""
You are an email intelligence system.

Analyze the following email.

Subject:
{subject}

Body:
{body}

Classify the email into exactly ONE category from:

Job
Finance
Shopping
Travel
Education
Social
Promotions
Personal
Important
Other

Also provide:

1. A short summary
2. Priority: High, Medium, or Low
3. Whether action is required: true or false

Return ONLY valid JSON.

Use exactly this format:

{{
    "category": "Job",
    "summary": "Short summary of the email",
    "priority": "High",
    "action_required": true
}}
"""

    print("\n-----------------------------")
    print("Sending email to Ollama...")
    print("Subject:", subject)
    print("Body length:", len(body))
    print("-----------------------------")

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=180
        )

        print("Ollama status:", response.status_code)

        if response.status_code != 200:
            print("Ollama response:")
            print(response.text)

            return {
                "category": "Other",
                "summary": "AI processing failed.",
                "priority": "Low",
                "action_required": False
            }

        data = response.json()

        result = data.get("response", "")

        print("AI response:", result)

        try:
            return json.loads(result)

        except json.JSONDecodeError:

            print("Invalid JSON returned by Ollama.")

            return {
                "category": "Other",
                "summary": result[:500],
                "priority": "Low",
                "action_required": False
            }

    except requests.exceptions.RequestException as e:

        print("Ollama request error:", str(e))

        return {
            "category": "Other",
            "summary": "Unable to connect to local AI model.",
            "priority": "Low",
            "action_required": False
        }