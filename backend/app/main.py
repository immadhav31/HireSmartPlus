from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes.job_routes import job_router
from app.routes.resume_routes import resume_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hire-smart-plus.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job_router, prefix="/jobs", tags=["jobs"])
app.include_router(resume_router, prefix="/resume", tags=["resume"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Job API"}