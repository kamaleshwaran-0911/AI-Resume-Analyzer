
from flask import Flask, render_template, request
import os

app = Flask(__name__)

skills = [
    "Python",
    "C",
    "C++",
    "Java",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "Flask",
    "Git",
    "AWS",
    "Machine Learning",
    "OOP",
    "Data Structures",
    "Linux",
    "Embedded Systems",
    "Arduino"
]

role_skills = {
    "Python Developer": [
        "Python", "Flask", "SQL", "Git", "OOP"
    ],

    "Java Developer": [
        "Java", "SQL", "Git", "OOP"
    ],

    "Data Analyst": [
        "Python", "SQL", "Machine Learning"
    ],

    "AI/ML Engineer": [
        "Python", "Machine Learning", "SQL", "Git"
    ],

    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "Git"
    ],

    "Cloud Engineer": [
        "AWS", "Linux", "Python", "Git"
    ]
}


UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['resume']

    role = request.form['role']
    company = request.form['company']

    if file:

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            file.filename
        )

        file.save(filepath)

        import pdfplumber

        text = ""

        with pdfplumber.open(filepath) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted

        found_skills = []

        for skill in skills:

            if skill.lower() in text.lower():

                found_skills.append(skill)
                
        required_skills = role_skills.get(role,[])

        matched = len(set(found_skills) & set(required_skills))

        if len(required_skills) > 0:
          score = (matched / len(required_skills)) * 100
        else:
          score = 0

        ats_score = round(score)
 
        matched_skills = []

        for skill in required_skills:
            if skill in found_skills:
               matched_skills.append(skill)

        missing_skills = []

        for skill in required_skills:
            if skill not in found_skills:
               missing_skills.append(skill)

        suggestions = []

        for skill in missing_skills:
           suggestions.append(f"Learn {skill}")

           if ats_score >= 85:
             level = "Excellent"
           elif ats_score >= 70:
             level = "Good"
           elif ats_score >= 50:
             level = "Average"
           else:
             level = "Needs Improvement"
        
        
        return render_template(
        "result.html",
        found_skills=found_skills,
        required_skills=required_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        score=round(score),
        ats_score=ats_score,
        suggestions=suggestions,
        role=role,
        company=company,
        level=level



)
    return "No file selected"

if __name__ == "__main__":
    app.run(debug=True)