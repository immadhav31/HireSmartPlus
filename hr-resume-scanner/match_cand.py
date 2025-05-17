import requests

url = "http://127.0.0.1:8000/resume/api/results"
params = {
    "hr_skills": ["python", "java"], 
    "top_n": 5 
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Top Candidates:")
    for candidate in data["top_candidates"]:
        print(f"Name: {candidate['name']}, Email: {candidate['email']}, Skills: {candidate['skills']}")
else:
    print(f"Error: {response.status_code}, {response.text}")
