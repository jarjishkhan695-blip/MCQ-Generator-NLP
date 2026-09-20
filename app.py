
import streamlit as st

from src.pdf_processor import extract_text_from_pdf
from src.image_processor import generate_mcqs_from_image
from src.question_generator import generate_mcqs_from_text
from src.validator import validate_mcqs

# PAGE CONFIGURATION

st.set_page_config(
    page_title="MCQ Generator",
    layout="wide"
)

# HEADER

st.title("AI Study Assistant")

st.write(
    "Generate interactive MCQ quizzes from your study material "
    "using AI."
)

st.caption(
    "Supports PDF, Image, and Text input"
)

st.divider()

# SIDEBAR


with st.sidebar:

    st.header("Quiz Settings")

    input_type = st.radio(
        "Choose your input type:",
        ["PDF", "Image", "Text"]
    )

    st.divider()

    number_of_questions = st.slider(
        "Number of questions",
        min_value=1,
        max_value=20,
        value=5
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    st.divider()

    st.caption(
        "Upload or enter your study material "
        "and generate an interactive quiz."
    )
# PDF INPUT

if input_type == "PDF":

    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.success("PDF uploaded successfully!")

        if st.button("Generate MCQs", type="primary"):

            with st.spinner(
                "Reading PDF and generating MCQs..."
            ):

                try:

                    extracted_text = extract_text_from_pdf(
                        uploaded_file
                    )

                    if not extracted_text.strip():

                        st.error(
                            "No readable text was found in this PDF."
                        )

                    else:

                        mcqs = generate_mcqs_from_text(
                            extracted_text,
                            number_of_questions,
                            difficulty
                        )

                        is_valid, message = validate_mcqs(
                             mcqs,
                              number_of_questions)

                        if is_valid:

                            st.session_state["mcqs"] = mcqs
                            st.session_state["quiz_submitted"] = False

                        else:
                            st.error(f"MCQ validation failed: {message}")
                          

    

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# IMAGE INPUT

elif input_type == "Image":

    uploaded_file = st.file_uploader(
        "Upload your image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        st.success("Image uploaded successfully!")

        st.image(
            uploaded_file,
            caption="Uploaded Image",
            use_container_width=True
        )

        if st.button("Generate MCQs", type="primary"):

            with st.spinner("Generating MCQs..."):

                try:

                    mcqs = generate_mcqs_from_image(
                        uploaded_file,
                        number_of_questions,
                        difficulty
                    )

                    is_valid, message = validate_mcqs(
                        mcqs,
                        number_of_questions
                         )
                    
                    if is_valid:


                        st.session_state["mcqs"] = mcqs
                        st.session_state["quiz_submitted"] = False

                    else:

                        st.error(f"MCQ validation failed: {message}")

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# TEXT INPUT

elif input_type == "Text":

    text_input = st.text_area(
        "Paste your study material here:",
        height=250
    )

    if st.button("Generate MCQs", type="primary"):

        if not text_input.strip():

            st.warning(
                "Please enter some study material first."
            )

        else:

            with st.spinner("Generating MCQs..."):

                try:

                    mcqs = generate_mcqs_from_text(
                        text_input,
                        number_of_questions,
                        difficulty
                    )
                    is_valid, message = validate_mcqs(
                        mcqs,
                        number_of_questions)

                    if is_valid:

                        st.session_state["mcqs"] = mcqs
                        st.session_state["quiz_submitted"] = False

                    else:

                        st.error(f"MCQ validation failed: {message}")

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )
# DISPLAY QUIZ
if "mcqs" in st.session_state:

    st.divider()

    st.subheader("Quiz")

    questions = st.session_state["mcqs"]["questions"]

    for i, question in enumerate(questions):

        st.markdown(
            f"### Q{i + 1}. {question['question']}"
        )

        options = question["options"]

        st.radio(
            "Choose your answer:",
            [
                f"A. {options['A']}",
                f"B. {options['B']}",
                f"C. {options['C']}",
                f"D. {options['D']}"
            ],
            key=f"question_{i}"
        )

# SUBMIT QUIZ
 
    st.divider()

    if st.button("Submit Quiz", type="primary"):

        score = 0

        for i, question in enumerate(questions):

            selected_answer = st.session_state.get(
                f"question_{i}"
            )

            if selected_answer is None:
                continue

            selected_letter = selected_answer[0]

            correct_answer = question["correct_answer"]

            if selected_letter == correct_answer:
                score += 1

        total_questions = len(questions)

        percentage = (
            score / total_questions
        ) * 100

        st.session_state["quiz_submitted"] = True
        st.session_state["score"] = score
        st.session_state["percentage"] = percentage

# QUIZ RESULTS

if (
    st.session_state.get("quiz_submitted", False)
    and "mcqs" in st.session_state
):

    questions = st.session_state["mcqs"]["questions"]

    st.divider()

    st.subheader("Quiz Result")

    score = st.session_state["score"]

    percentage = st.session_state["percentage"]

    st.success(
        f"You scored {score} out of {len(questions)}"
    )

    st.write(
        f"### Percentage: {percentage:.1f}%"
    )

    st.divider()

    st.subheader("Answer Review")

    for i, question in enumerate(questions):

        selected_answer = st.session_state.get(
            f"question_{i}"
        )

        correct_answer = question["correct_answer"]

        st.markdown(
            f"### Q{i + 1}. {question['question']}"
        )

        if selected_answer is None:

            st.warning(
                "Not answered"
            )

        else:

            selected_letter = selected_answer[0]

            if selected_letter == correct_answer:

                st.success(
                    f"Correct — Your answer: {selected_letter}"
                )

            else:

                st.error(
                    f"Incorrect — Your answer: {selected_letter}"
                )

                st.info(
                    f"Correct answer: {correct_answer}"
                )

        st.write(
            f"**Explanation:** {question['explanation']}"
        )
# --------------------------------
# NEW QUIZ
# --------------------------------

if "mcqs" in st.session_state:

    st.divider()

    if st.button("Generate New Quiz"):

        st.session_state.pop("mcqs", None)
        st.session_state.pop("quiz_submitted", None)
        st.session_state.pop("score", None)
        st.session_state.pop("percentage", None)

        for key in list(st.session_state.keys()):

            if key.startswith("question_"):
                del st.session_state[key]

        st.rerun()