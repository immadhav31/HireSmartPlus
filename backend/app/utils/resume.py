import pdfplumber
import psycopg2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def get_jobs_from_db():
    conn = psycopg2.connect(
        host="localhost", 
        database="resume_scanner", 
        user="postgres", 
        password="madhav"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT title, company, description, required_skills FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    return jobs

def extract_skills_from_resume(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    
    skills = re.findall(r"\b(?:Python|Java|SQL|React|Django|JavaScript|Ruby|PostgreSQL|Node.js|AWS|Docker|FastAPI)\b", text, re.IGNORECASE)
    print(skills)
    return list(set(skills))

def get_job_vectors(jobs, resume_skills):
    job_descriptions = [job[2] for job in jobs]
    all_text = job_descriptions + [" ".join(resume_skills)]

    vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix = vectorizer.fit_transform(all_text)

    job_vectors = tfidf_matrix[:-1]
    resume_vector = tfidf_matrix[-1]

    return job_vectors, resume_vector

def get_top_job_matches(job_vectors, resume_vector, jobs):
    cosine_similarities = cosine_similarity(resume_vector, job_vectors)
    
    top_5_indices = cosine_similarities.argsort()[0][-5:][::-1]

    top_5_jobs = []
    for idx in top_5_indices:
        job = jobs[idx]
        top_5_jobs.append({
            "title": job[0],
            "company": job[1],
            "description": job[2],
            "skills": job[3],
            "link": f"https://remoteok.io/remote-jobs/{job[0].replace(' ', '-')}-{job[1].replace(' ', '-')}-{idx+1}"
        })

    return top_5_jobs

def main(pdf_path):
    jobs = get_jobs_from_db()

    resume_skills = extract_skills_from_resume(pdf_path)
    
    job_vectors, resume_vector = get_job_vectors(jobs, resume_skills)
    
    top_5_jobs = get_top_job_matches(job_vectors, resume_vector, jobs)

    for idx, job in enumerate(top_5_jobs):
        print(f"Job {idx+1}: {job['title']} at {job['company']}")
        print(f"Description: {job['description'][:200]}...")  # First 200 chars
        print(f"Skills: {job['skills']}")
        print(f"Link: {job['link']}")
        print()

if __name__ == "__main__":
    resume_pdf_path = "D:/Books pdf/Studies/Amrita/Madhav.pdf"
    main(resume_pdf_path)
