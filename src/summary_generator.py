from src.image_processor import client


def generate_summary(text, subject="", topic=""):
    """
    Generate a concise study summary from the provided material.
    """

    prompt = f"""
You are an expert study assistant.

Create a concise and easy-to-understand study summary
from the material provided below.

Subject: {subject if subject else "Not specified"}
Topic: {topic if topic else "Not specified"}

Rules:
- Use ONLY information from the provided material.
- Do not add outside knowledge.
- Do not invent facts.
- Focus on the important concepts, definitions, facts,
  and relationships.
- Use clear bullet points.
- Keep the summary concise.
- Make it useful for exam revision.

Study material:

{text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text