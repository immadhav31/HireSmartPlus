from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import Response
import os, shutil, zipfile
from app.utils.matching import process_resumes

resume_router = APIRouter()

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@resume_router.post("/upload-resumes-zip/")
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

    return {"message": "Resumes uploaded and processed successfully."}
