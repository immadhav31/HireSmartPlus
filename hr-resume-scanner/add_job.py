import requests

url = "http://127.0.0.1:8000/resume/upload-resumes-zip"
files = {"file": open("D:/Books pdf/Studies/Amrita/Resume Scanner/database/cv.zip", "rb")}

response = requests.post(url, files=files)

print(response.json())
