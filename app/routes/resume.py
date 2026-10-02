import os
import tempfile
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_service import extract_text_from_pdf


router = APIRouter(prefix="/api/v1")


@router.post("/resumes/upload")
def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )
    fd, temp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)

    try:
        with open(temp_path, "wb") as temp:
            shutil.copyfileobj(file.file, temp)

        text = extract_text_from_pdf(temp_path)

        return {
            "filename": file.filename,
            "text": text
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    finally:
        os.remove(temp_path)