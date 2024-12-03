from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.database.database import get_db_connection
from app.utils.text_extraction import extract_resume_details, extract_text_from_pdf
import os

def process_resumes(folder_path):
    db_conn = get_db_connection()
    cursor = db_conn.cursor()

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if not file.lower().endswith(".pdf"):
            continue

        try:
            with open(file_path, "rb") as pdf_file:
                resume_text = extract_text_from_pdf(pdf_file)
                resume_details = extract_resume_details(resume_text)

                if not resume_details['skills']:
                    predefined_keywords = ["python", "java", "sql", "javascript", "html", "css"]
                    resume_details['skills'] = [
                        keyword for keyword in predefined_keywords if keyword in resume_text.lower()
                    ]

                cursor.execute("""
                    INSERT INTO resumes (name, email, skills)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (email) DO UPDATE SET
                        name = EXCLUDED.name,
                        skills = EXCLUDED.skills;
                """, (
                    resume_details['name'],
                    resume_details['email'],
                    ", ".join(resume_details['skills']),
                ))
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    db_conn.commit()
    cursor.close()
    db_conn.close()


from sqlalchemy import create_engine, text
from typing import List, Dict

DATABASE_URL = "postgresql://postgres:madhav@localhost:5432/resume_scanner"

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine, text
from typing import List, Dict

def match_candidates(hr_skills: List[str], top_n: int = 5) -> Dict:
    engine = create_engine(DATABASE_URL)

    query = "SELECT id, name, email, skills FROM resumes"
    candidates = []
    total_applications = 0
    matched_applications = 0

    with engine.connect() as conn:
        result = conn.execute(text(query))
        for row in result:
            total_applications += 1
            
            if row.skills:
                candidate_skills = [skill.strip().lower() for skill in row.skills.split(',')]
                
                if any(hr_skill.lower() in candidate_skills for hr_skill in hr_skills):
                    matched_applications += 1
                    
                    candidates.append({
                        "id": row.id,
                        "name": row.name.strip(),
                        "email": row.email.strip(),
                        "skills": row.skills.strip()
                    })

    if not candidates:
        return {
            "top_candidates": [],
            "total_applications": total_applications,
            "matched_applications": 0
        }

    hr_skills_str = ", ".join(hr_skills)

    candidate_skills_list = [candidate["skills"] for candidate in candidates]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform([hr_skills_str] + candidate_skills_list)

    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    for i, candidate in enumerate(candidates):
        candidate["similarity_score"] = cosine_similarities[i]

    sorted_candidates = sorted(candidates, key=lambda x: x["similarity_score"], reverse=True)
    
    return {
        "top_candidates": sorted_candidates[:top_n],
        "total_applications": total_applications,
        "matched_applications": matched_applications
    }