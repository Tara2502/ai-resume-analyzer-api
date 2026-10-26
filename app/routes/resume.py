import os
import tempfile
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ai_exceptions import (
    AIRateLimitError,
    AIUnavailableError,
    AIResponseError,
)

from app.services.pdf_service import (
    extract_text_from_pdf,
    validate_pdf_signature
)
from app.services.ai_service import analyze_resume
from app.schemas.resume import ResumeAnalysis, ResumeUploadResponse

router = APIRouter(prefix="/api/v1")


@router.post("/resumes/upload",
    response_model=ResumeUploadResponse)
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

        if not validate_pdf_signature(temp_path):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file."
            )

        text = extract_text_from_pdf(temp_path)

        try:
            analysis = analyze_resume(text)

        except AIRateLimitError:
            raise HTTPException(
        status_code=429,
        detail="AI service rate limit or quota exceeded. Please try again later.",
    )

        except AIUnavailableError:
            raise HTTPException(
        status_code=503,
        detail="AI service is temporarily unavailable. Please try again later.",
    )

        except AIResponseError:
            raise HTTPException(
        status_code=502,
        detail="Unable to generate resume analysis.",
    )

        return {
            "filename": file.filename,
            "analysis": analysis
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    finally:
        os.remove(temp_path)