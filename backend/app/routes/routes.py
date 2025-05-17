from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from typing import List, Optional
import os
import shutil
import zipfile
from app.utils.matching import process_resumes, match_candidates
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter()

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class HRPreferences(BaseModel):
    skills: List[str]
    candidates: int

@router.post("/api/hr/preferences/")
async def get_top_candidates(preferences: HRPreferences):
    try:
        result = match_candidates(preferences.skills, preferences.candidates)
        return {
            "top_candidates": result['top_candidates'],
            "total_applications": result['total_applications'],
            "matched_applications": result['matched_applications']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing HR preferences: {str(e)}")
    

class Candidate(BaseModel):
    name: str
    skills: str
    score: int

@router.get("/api/results", response_model=dict)
async def get_results(
    hr_skills: List[str] = Query(..., description="List of skills HR is looking for"),
    top_n: int = Query(5, description="Number of top candidates to return")
):
    try:
        top_candidates = match_candidates(hr_skills, top_n)
        return {"results": top_candidates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching results: {str(e)}")


@router.post("/upload-resumes-zip/")
async def upload_resumes_zip(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only zip files are allowed.")

    zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(zip_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    extracted_folder = os.path.join(UPLOAD_FOLDER, "extracted")
    os.makedirs(extracted_folder, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extracted_folder)
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid zip file format.")

    process_resumes(extracted_folder)
    shutil.rmtree(extracted_folder)
    os.remove(zip_path)

    return JSONResponse(
        content={"message": "Resumes uploaded and processed successfully."},
        headers={
            "Access-Control-Allow-Origin": "https://hire-smart-plus.vercel.app",
            "Access-Control-Allow-Credentials": "true"
        }
    )

