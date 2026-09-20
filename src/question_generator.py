import json

from src.image_processor import client
from google.genai import types


def generate_mcqs_from_text(
    text,
    number_of_questions,
    difficulty,
    subject="",
    topic=""
):
    """
    Generate structured MCQs from extracted study material.
    """

    prompt = f"""
You are an expert educational MCQ generator.

Generate exactly {number_of_questions} multiple-choice questions
from the study material provided below.

Subject: {subject if subject else "Not specified"}
Topic: {topic if topic else "Not specified"}
Difficulty: {difficulty}

Use the subject and topic as additional context for understanding
the study material.

If a subject or topic is provided, keep the questions focused on
that subject or topic.

Questions must still be based ONLY on the provided study material.
Do not introduce information that is not present in the study material.

Rules:
- Questions must be based ONLY on the provided study material.
- Do not use outside knowledge.
- Do not invent facts.
- Avoid duplicate or nearly identical questions.
- Each question must have exactly four options.
- There must be exactly one correct answer.
- The correct_answer must be A, B, C, or D.
- Include a short explanation for every question.

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
                                    "required": [
                                        "A",
                                        "B",
                                        "C",
                                        "D"
                                    ]
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