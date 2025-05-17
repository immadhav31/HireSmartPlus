from fastapi import FastAPI
from app.routes.routes import router as job_router
from app.routes.routes import router as upload_resume

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hire-smart-plus.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job_router, prefix="/jobs", tags=["jobs"])
app.include_router(upload_resume, prefix="/resume", tags=["resume"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Job API"}
