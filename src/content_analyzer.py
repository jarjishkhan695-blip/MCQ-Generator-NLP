import json

from src.image_processor import client
from google.genai import types


def analyze_content(text):
    """
    Detect the subject and main topic from study material.
    """

    prompt = f"""
You are an expert educational content analyzer.

Analyze the study material provided below and identify:

1. The most appropriate academic subject.
2. The main topic or chapter covered by the material.

Rules:
- Use ONLY information present in the provided material.
- Do not invent information.
- Keep the subject concise.
- Keep the topic concise.
- The topic should describe the main concept discussed.
- Do not include explanations.

Study material:

{text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "subject": {
                        "type": "STRING"
                    },
                    "topic": {
                        "type": "STRING"
                    }
                },
                "required": [
                    "subject",
                    "topic"
                ]
            }
        )
    )

    return json.loads(response.text)