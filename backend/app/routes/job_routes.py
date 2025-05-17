from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.utils.matching import match_candidates
from pydantic import BaseModel

job_router = APIRouter()

class HRPreferences(BaseModel):
    skills: List[str]
    candidates: int

@job_router.post("/api/hr/preferences/")
async def get_top_candidates(preferences: HRPreferences):
    try:
        result = match_candidates(preferences.skills, preferences.candidates)
        return {
            "top_candidates": result['top_candidates'],
            "total_applications": result['total_applications'],
            "matched_applications": result['matched_applications']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@job_router.get("/api/results")
async def get_results(
    hr_skills: List[str] = Query(...),
    top_n: int = Query(5)
):
    try:
        return {"results": match_candidates(hr_skills, top_n)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
