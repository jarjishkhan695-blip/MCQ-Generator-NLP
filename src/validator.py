def validate_mcqs(mcqs, expected_count):
    """
    Validate the structure of generated MCQs.
    """

    # Check main structure
    if not isinstance(mcqs, dict):
        return False, "MCQ result must be a dictionary."

    if "questions" not in mcqs:
        return False, "MCQ result does not contain questions."

    questions = mcqs["questions"]

    if not isinstance(questions, list):
        return False, "Questions must be a list."

    # Check number of questions
    if len(questions) != expected_count:
        return False, (
            f"Expected {expected_count} questions, "
            f"but received {len(questions)}."
        )

    # Validate each question
    for i, question in enumerate(questions):

        question_number = i + 1

        if not isinstance(question, dict):
            return False, (
                f"Question {question_number} is invalid."
            )

        # Check required fields
        required_fields = [
            "question",
            "options",
            "correct_answer",
            "explanation"
        ]

        for field in required_fields:

            if field not in question:
                return False, (
                    f"Question {question_number} is missing "
                    f"'{field}'."
                )

        # Check question text
        if not str(question["question"]).strip():
            return False, (
                f"Question {question_number} has empty question text."
            )

        # Check options
        options = question["options"]

        if not isinstance(options, dict):
            return False, (
                f"Options for question {question_number} "
                f"must be a dictionary."
            )

        required_options = ["A", "B", "C", "D"]

        for option in required_options:

            if option not in options:
                return False, (
                    f"Question {question_number} is missing "
                    f"option {option}."
                )

            if not str(options[option]).strip():
                return False, (
                    f"Option {option} in question "
                    f"{question_number} is empty."
                )

        # Check correct answer
        correct_answer = question["correct_answer"]

        if correct_answer not in required_options:
            return False, (
                f"Question {question_number} has an invalid "
                f"correct answer."
            )

        # Check explanation
        if not str(question["explanation"]).strip():
            return False, (
                f"Question {question_number} has no explanation."
            )

    # Check for duplicate questions
    question_texts = [
        question["question"].strip().lower()
        for question in questions
    ]

    if len(question_texts) != len(set(question_texts)):
        return False, "Duplicate questions were generated."

    # Check for duplicate options within each question
    for i, question in enumerate(questions):

        options = question["options"]

        option_values = [
            str(options["A"]).strip().lower(),
            str(options["B"]).strip().lower(),
            str(options["C"]).strip().lower(),
            str(options["D"]).strip().lower()
        ]

        if len(option_values) != len(set(option_values)):
            return False, (
                f"Question {i + 1} contains duplicate options."
            )

    return True, "MCQs are valid."