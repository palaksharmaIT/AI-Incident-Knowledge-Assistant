import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )


client = genai.Client(api_key=api_key)


def generate_resolution(incident, context):

    prompt = f"""
You are an AI incident analysis assistant.

Analyze the new incident using the historical incidents provided below.

NEW INCIDENT:
Incident ID: {incident.incident_id}
Title: {incident.title}
Description: {incident.description}
Severity: {incident.severity}
Service: {incident.service}
Predicted Category: {incident.category}

HISTORICAL INCIDENTS:
{context}

Based only on the information above, provide:

1. Possible Root Cause
2. Recommended Resolution
3. Short Explanation

Do not invent facts that are not supported by the incident
or historical context.
"""

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    print("Gemini generation module ready.")