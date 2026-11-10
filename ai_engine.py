
import re

# Skills and their keywords
SKILL_DATABASE = {
    "Python": ["python"],
    "SQL": ["sql", "mysql", "sqlite", "postgresql"],
    "Flask": ["flask"],
    "Django": ["django"],
    "HTML": ["html"],
    "CSS": ["css"],
    "JavaScript": ["javascript"],
    "React": ["react", "reactjs"],
    "Machine Learning": ["machine learning"],
    "Deep Learning": ["deep learning"],
    "Generative AI": ["generative ai", "genai", "gen ai"],
    "Artificial Intelligence": ["artificial intelligence"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Git": ["git", "github"],
    "REST API": ["rest api", "restful api"],
    "Bootstrap": ["bootstrap"],
    "Java": ["java"],
    "C++": ["c++"],
    "AWS": ["aws", "amazon web services"]
}


# Extract skills from text
def extract_skills(text):

    text = text.lower()
    found_skills = []

    for skill, keywords in SKILL_DATABASE.items():

        for keyword in keywords:

            pattern = (
                r"(?<![a-z0-9+#])"
                + re.escape(keyword)
                + r"(?![a-z0-9+#])"
            )

            if re.search(pattern, text):
                found_skills.append(skill)
                break

    return found_skills


# Compare resume skills with job requirements
def analyze_skills(resume_text, job_description):

    candidate_skills = extract_skills(resume_text)
    required_skills = extract_skills(job_description)

    matched_skills = [
        skill for skill in required_skills
        if skill in candidate_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in candidate_skills
    ]

    if required_skills:
        match_percentage = round(
            len(matched_skills) / len(required_skills) * 100,
            2
        )
    else:
        match_percentage = 0

    return {
        "candidate_skills": candidate_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage
    }


# Learning recommendations
LEARNING_RESOURCES = {
    "Python": "Study functions, OOP, exception handling and coding problems.",
    "SQL": "Practice joins, subqueries, grouping and database design.",
    "Flask": "Learn routing, APIs, SQLAlchemy and Flask authentication.",
    "Django": "Learn MVT architecture, ORM, authentication and admin.",
    "HTML": "Practice semantic HTML and accessible forms.",
    "CSS": "Learn Flexbox, Grid and responsive design.",
    "JavaScript": "Study ES6, DOM, events, promises and fetch API.",
    "React": "Learn components, props, state and hooks.",
    "Machine Learning": "Study regression, classification and model evaluation.",
    "Deep Learning": "Learn neural networks and backpropagation.",
    "Generative AI": "Study LLMs, prompt engineering, embeddings and RAG.",
    "Artificial Intelligence": "Learn AI fundamentals and practical applications.",
    "Git": "Practice commits, branches, merge and GitHub.",
    "REST API": "Study HTTP methods, status codes and API testing.",
    "Pandas": "Practice data cleaning and data analysis.",
    "NumPy": "Study arrays and numerical operations.",
    "AWS": "Learn cloud fundamentals and AWS services.",
    "Bootstrap": "Learn responsive layouts and Bootstrap components.",
    "Java": "Study OOP, collections and exception handling.",
    "C++": "Study object-oriented programming and data structures."
}


# Generate learning roadmap
def generate_roadmap(missing_skills):

    roadmap = []

    for skill in missing_skills:

        recommendation = LEARNING_RESOURCES.get(
            skill,
            f"Learn {skill} fundamentals and build a small project."
        )

        roadmap.append({
            "skill": skill,
            "recommendation": recommendation
        })

    return roadmap
