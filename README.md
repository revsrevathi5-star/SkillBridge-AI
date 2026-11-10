
# SkillBridge AI
### Smart Career & Skill Gap Analyzer

## Project Overview
SkillBridge AI is a Python Flask-based web application
that compares a candidate's resume with a job description.

It identifies matching skills, missing skills and
suggests a personalized learning roadmap.

## Features
- User registration and login
- Resume upload (PDF and DOCX)
- Resume text extraction
- Skill extraction using Python
- Resume and job skill comparison
- Skill match percentage
- Missing skill identification
- Personalized learning recommendations
- SQLite database integration
- Previous analysis history

## Technologies Used
- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- HTML
- CSS
- JavaScript
- PyPDF
- python-docx

## How to Run

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies.
4. Configure your environment variables.
5. Run the Flask application.

```bash
python -m venv .venv
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## AI Implementation
The current version uses a Python-based skill
matching engine with keyword detection and
rule-based learning recommendations.

Future enhancements:
- LLM integration
- Semantic resume matching
- Vector databases
- RAG-based career assistance
- AI-powered interview preparation

## Database
SQLite stores user accounts, resume information,
job descriptions and analysis results.

## Developer
Python Full Stack Developer Project
