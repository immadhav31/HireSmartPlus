import re
import pdfplumber

def extract_resume_details(resume_text):
    details = {
        'name': None,
        'email': None,
        'phone': None,
        'skills': [],
        'cgpa': None
    }

    lines = resume_text.split('\n')
    details['name'] = lines[0].strip() if lines else None
    
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text)
    details['email'] = email_match.group(0) if email_match else None
    
    phone_match = re.search(r'\+?\d{10,13}', resume_text)
    details['phone'] = phone_match.group(0) if phone_match else None
    
    cgpa_match = re.search(r'CGPA[:\s]+([\d.]+)', resume_text, re.IGNORECASE)
    details['cgpa'] = float(cgpa_match.group(1)) if cgpa_match else None
    
    predefined_skills = {'python', 'data analysis', 'excel', 'machine learning', 'sql', 'java'}
    
    found_skills = {word.lower() for word in resume_text.split() if word.lower() in predefined_skills}
    
    details['skills'] = list(found_skills)
    
    return details

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    return text.strip()