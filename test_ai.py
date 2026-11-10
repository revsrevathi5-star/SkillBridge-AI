from ai_engine import analyze_skills, generate_roadmap

resume = """
Python, SQL, Flask, HTML, CSS and Git
"""

job = """
Required skills: Python, SQL, Flask,
Django, JavaScript, HTML, CSS and React.
"""

result = analyze_skills(resume, job)

print("Candidate Skills:", result["candidate_skills"])
print("Matched Skills:", result["matched_skills"])
print("Missing Skills:", result["missing_skills"])
print("Match Percentage:", result["match_percentage"])

roadmap = generate_roadmap(result["missing_skills"])

print("\nLearning Roadmap:")

for item in roadmap:
    print(item["skill"], ":", item["recommendation"])