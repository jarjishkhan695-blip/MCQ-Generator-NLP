import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_mcqs_from_image(
    image_file,
    number_of_questions,
    difficulty,
    subject="",
    topic=""
):
    """
    Generate structured MCQs from an educational image.
    """

    image_bytes = image_file.getvalue()

    prompt = f"""
You are an expert educational MCQ generator.

Analyze the educational content in the provided image.

Generate exactly {number_of_questions} multiple-choice questions
with {difficulty} difficulty.
Subject: {subject if subject else "Not specified"}
Topic: {topic if topic else "Not specified"}

Use the subject and topic as additional context.
If provided, keep the questions focused on them.

Questions must still be based ONLY on information present in the image.
Do not introduce outside knowledge.

Rules:
- Questions must be based ONLY on information present in the image.
- Do not use outside knowledge.
- Do not invent facts.
- Avoid duplicate questions.
- Each question must have exactly four options.
- There must be exactly one correct answer.
- The correct_answer must be one of: A, B, C, D.
- Include a short explanation.

Return the result as JSON matching the required schema.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=image_file.type
            ),
            prompt
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "questions": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "question": {
                                    "type": "STRING"
                                },
                                "options": {
                                    "type": "OBJECT",
                                    "properties": {
                                        "A": {"type": "STRING"},
                                        "B": {"type": "STRING"},
                                        "C": {"type": "STRING"},
                                        "D": {"type": "STRING"}
                                    },
                                    "required": ["A", "B", "C", "D"]
                                },
                                "correct_answer": {
                                    "type": "STRING"
                                },
                                "explanation": {
                                    "type": "STRING"
                                }
                            },
                            "required": [
                                "question",
                                "options",
                                "correct_answer",
                                "explanation"
                            ]
                        }
                    }
                },
                "required": ["questions"]
            }
        )
    )

    return json.loads(response.text)

def analyze_image_content(image_file):
    """
    Detect the subject and main topic from an educational image.
    """

    image_bytes = image_file.getvalue()

    prompt = """
You are an expert educational content analyzer.

Analyze the educational content in the provided image and identify:

1. The most appropriate academic subject.
2. The main topic or chapter covered by the image.

Rules:
- Use ONLY information present in the image.
- Do not invent information.
- Keep the subject concise.
- Keep the topic concise.
- Return only the requested JSON structure.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=image_file.type
            ),
            prompt
        ],
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

def generate_summary_from_image(image_file, subject="", topic=""):
    """
    Generate a concise study summary from an educational image.
    """

    image_bytes = image_file.getvalue()

    prompt = f"""
You are an expert study assistant.

Create a concise and easy-to-understand study summary
from the educational content in the provided image.

Subject: {subject if subject else "Not specified"}
Topic: {topic if topic else "Not specified"}

Rules:
- Use ONLY information present in the image.
- Do not add outside knowledge.
- Do not invent facts.
- Focus on important concepts, definitions, facts,
  and relationships.
- Use clear bullet points.
- Keep the summary concise.
- Make it useful for exam revision.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=image_file.type
            ),
            prompt
        ]
    )

    return response.text