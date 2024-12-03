import requests
from bs4 import BeautifulSoup
import psycopg2
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.app.database.database import get_db_connection

def fetch_job_links():
    url = "https://remoteok.io/remote-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch job listings.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.find_all('td', {'class': 'company_and_position'})
    job_links = [
        "https://remoteok.io" + job.find('a', {'itemprop': 'url'})['href']
        for job in jobs if job.find('a', {'itemprop': 'url'})
    ]
    return job_links

def scrape_job_details(job_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(job_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch job details: {job_url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    job = {}

    job['title'] = soup.find('h1', {'itemprop': 'title'}).get_text(strip=True) if soup.find('h1', {'itemprop': 'title'}) else "N/A"
    job['company'] = soup.find('h2', {'itemprop': 'hiringOrganization'}).get_text(strip=True) if soup.find('h2', {'itemprop': 'hiringOrganization'}) else "N/A"

    description = soup.find('div', {'class': 'description'})
    if description:
        desc_text = description.get_text(strip=True).split(".")  # Split into sentences
        job['description'] = ". ".join(desc_text[:2]) + "." if len(desc_text) > 1 else desc_text[0]
    else:
        job['description'] = "N/A"

    job['skills'] = extract_skills_from_description(job['description'])

    job['location'] = soup.find('div', {'class': 'location'}).get_text(strip=True) if soup.find('div', {'class': 'location'}) else "Remote"
    job['salary'] = soup.find('span', {'class': 'salary'}).get_text(strip=True) if soup.find('span', {'class': 'salary'}) else "N/A"

    job['link'] = job_url

    return job

def extract_skills_from_description(description):
    skills_set = {"python", "ruby", "typescript", "graphql", "docker", "vue.js", "sql"}
    return [skill for skill in skills_set if skill.lower() in description.lower()]

def save_jobs_to_db(jobs):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO jobs (title, company, description, location, salary, skills, link)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (link) DO NOTHING;
        """
        for job in jobs:
            cursor.execute(insert_query, (
                job['title'], job['company'], job['description'], job['location'],
                job['salary'], ", ".join(job['skills']), job['link']
            ))

        conn.commit()
        print(f"Saved {len(jobs)} jobs to the database.")
    except Exception as e:
        print("Database error:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    job_links = fetch_job_links()
    all_jobs = []

    for link in job_links[:5]:
        job_details = scrape_job_details(link)
        if job_details:
            all_jobs.append(job_details)

    if all_jobs:
        save_jobs_to_db(all_jobs)
        for job in all_jobs:
            print(job)
