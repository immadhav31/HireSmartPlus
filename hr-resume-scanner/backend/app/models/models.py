from pydantic import BaseModel

class Job(BaseModel):
    title: str
    company: str
    description: str
    location: str
    required_skills: str
    link: str

class User(BaseModel):
    username: str
    skills: str
