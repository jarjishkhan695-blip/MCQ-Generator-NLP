import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_mcqs_from_image(image_file, number_of_questions, difficulty):
    """
    Generate structured MCQs from an educational image.
    """

    image_bytes = image_file.getvalue()

    prompt = f"""
You are an expert educational MCQ generator.

Analyze the educational content in the provided image.

Generate exactly {number_of_questions} multiple-choice questions
with {difficulty} difficulty.

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