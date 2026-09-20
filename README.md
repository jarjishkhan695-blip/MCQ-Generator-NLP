# AI Study Assistant — NLP MCQ Generator

An AI-powered study assistant that analyzes educational material from PDFs, images, or text and automatically generates study summaries and interactive multiple-choice quizzes.

The application uses a pretrained Gemini language model for natural language understanding and generation, combined with structured output validation to produce reliable MCQs.

## Live Demo

https://mcq-generator-nlp-8ocz.onrender.com

## GitHub Repository

https://github.com/jarjishkhan695-blip/MCQ-Generator-NLP

---

## Features

- Upload study material as PDF
- Upload educational images
- Paste text-based study material
- Automatic subject detection
- Automatic topic detection
- AI-generated study summaries
- AI-generated multiple-choice questions
- Easy, Medium, and Hard difficulty levels
- Customizable number of questions
- Four-option MCQs
- Correct answer for every question
- Explanation for every question
- MCQ structure validation
- Duplicate question detection
- Duplicate option detection
- Interactive quiz interface
- Automatic score calculation
- Percentage calculation
- Performance evaluation
- Answer review with explanations
- Generate a new quiz
- Deployed as a web application using Render

---

## NLP and Generative AI

This project is an **NLP-based Generative AI application** built around a pretrained Gemini language model.

The Gemini model is accessed through the Gemini API. The underlying language model is not trained from scratch by this project. Instead, the project focuses on designing an NLP processing pipeline around the pretrained model.

The NLP components include:

### 1. Content Understanding

The system analyzes educational material and identifies the important information contained in the input.

### 2. Subject and Topic Detection

The application automatically identifies the main academic subject and topic from the provided study material.

Example:

```
Subject: Anatomy
Topic: Respiratory System
```

### 3. Text Summarization

The system generates a concise study summary containing important concepts, definitions, facts, and relationships from the provided material.

### 4. Question Generation

The application generates multiple-choice questions based on the supplied study material.

The generation process is instructed to:

- Use only the provided material
- Avoid introducing unrelated information
- Generate exactly the requested number of questions
- Generate four options for each question
- Provide exactly one correct answer
- Provide an explanation

### 5. Natural Language Generation

The language model generates:

- Study summaries
- Questions
- Answer options
- Explanations

### 6. Structured Output Validation

Generated MCQs are returned in a structured JSON format and validated by the application before being displayed to the user.

---

## Application Workflow

```
                    Study Material
                          |
             +------------+------------+
             |            |            |
            PDF         Image         Text
             |            |            |
             +------------+------------+
                          |
                          v
             Text Extraction /
             Multimodal Processing
                          |
                          v
                  Content Analysis
                          |
                 +--------+--------+
                 |                 |
          Subject Detection   Topic Detection
                 |                 |
                 +--------+--------+
                          |
                          v
                   Study Summary
                          |
                          v
                   MCQ Generation
                          |
                          v
                  MCQ Validation
                          |
                          v
                  Interactive Quiz
                          |
                          v
                Score + Answer Review
```

---

## How the Application Works

### PDF Input

PyMuPDF is used to extract readable text from uploaded PDF files.

```
PDF
 ↓
PyMuPDF
 ↓
Extracted Text
 ↓
Content Analysis
 ↓
Summary + MCQs
```

### Image Input

Educational images are processed using the multimodal capabilities of Gemini.

The application can analyze the image to:

- Detect the subject
- Detect the topic
- Generate a study summary
- Generate MCQs

### Text Input

Users can directly paste their study material into the application.

The text is then processed by the NLP pipeline for:

- Subject detection
- Topic detection
- Summarization
- MCQ generation

---

## MCQ Validation

The application includes a separate validation layer to check the generated questions before displaying them.

The validator checks:

- Correct number of questions
- Required question fields
- Non-empty question text
- Four required options: A, B, C, and D
- Non-empty options
- Valid correct answer
- Non-empty explanation
- Duplicate questions
- Duplicate options within a question

This prevents incorrectly structured AI output from directly reaching the quiz interface.

---

## Interactive Quiz

After MCQs are generated, users can answer the questions through the Streamlit interface.

After submitting the quiz, the application calculates:

```
Score
Percentage
Performance
Answer Review
```

The answer review shows whether each answer was correct and provides the explanation generated for the question.

---

## Technology Stack

### Programming Language

- Python

### Application Framework

- Streamlit

### AI / NLP

- Google Gemini API
- Generative AI
- Natural Language Processing
- Multimodal AI

### PDF Processing

- PyMuPDF

### Configuration

- python-dotenv

### Data Format

- JSON

### Version Control

- Git
- GitHub

### Deployment

- Render

---

## Project Structure

```
MCQ-Generator-NLP/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
└── src/
    ├── __init__.py
    ├── pdf_processor.py
    ├── image_processor.py
    ├── question_generator.py
    ├── validator.py
    ├── content_analyzer.py
    └── summary_generator.py
```

---

## Project Modules

### `app.py`

Main Streamlit application.

Responsible for:

- User interface
- Input selection
- File uploads
- Quiz settings
- Connecting the processing modules
- Displaying summaries
- Displaying MCQs
- Quiz submission
- Score calculation
- Answer review

### `pdf_processor.py`

Extracts text from uploaded PDF files using PyMuPDF.

### `image_processor.py`

Handles image-based AI processing, including:

- Image-based subject/topic analysis
- Image-based summary generation
- Image-based MCQ generation

### `question_generator.py`

Generates MCQs from text-based study material using Gemini.

### `content_analyzer.py`

Analyzes text-based study material and automatically detects:

- Subject
- Topic

### `summary_generator.py`

Generates concise study summaries from text-based study material.

### `validator.py`

Validates the structure and quality requirements of generated MCQs.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jarjishkhan695-blip/MCQ-Generator-NLP.git
```

### 2. Navigate to the Project

```bash
cd MCQ-Generator-NLP
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```powershell
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API Key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

The `.env` file should never be committed to GitHub.

### 7. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Environment Variables

The application requires the following environment variable:

```text
GEMINI_API_KEY
```

The API key is loaded using `python-dotenv`.

For deployment, the API key should be added as an environment variable on the hosting platform rather than being stored in the source code.

---

## Deployment

The application is deployed using Render.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
```

The deployed application is available at:

https://mcq-generator-nlp-8ocz.onrender.com

---

## Security

The Gemini API key is not stored in the source code.

The project uses:

```
.env
```

for local development, and the `.env` file is excluded from Git using `.gitignore`.

For deployment, the API key is stored as a Render environment variable.

---

## Limitations

- The quality of generated questions depends on the quality and readability of the supplied study material.
- AI-generated content may occasionally contain inaccuracies and should be reviewed before academic use.
- Scanned or low-quality PDFs may not produce usable extracted text.
- Very complex educational images may be interpreted differently by the AI model.
- The application depends on the availability of the Gemini API.
- The Render Free instance may spin down after inactivity, which can increase the initial response time.

---

## Future Improvements

Potential improvements include:

- Semantic similarity-based duplicate question detection
- Quiz timer
- Downloadable quiz and result reports
- Weak-topic analysis
- Persistent quiz history
- Database-backed user progress
- User accounts
- Advanced question-generation controls
- Additional question formats

---

## Key Learning Outcomes

Through this project, the following concepts were implemented:

- Python application development
- Streamlit application development
- PDF text extraction
- Multimodal AI processing
- Natural Language Processing
- Text summarization
- Topic and subject identification
- Natural Language Generation
- Prompt engineering
- Structured JSON generation
- AI output validation
- Error handling
- Environment variable management
- Git and GitHub
- Cloud deployment using Render

---

## Author

**Khan Jarjish**

B.E. Artificial Intelligence & Data Science

Mumbai, India

---

## License

This project is intended for educational and portfolio purposes.
