import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors as genai_errors

from app.schemas.resume import ResumeAnalysis
from app.services.ai_exceptions import (
    AIRateLimitError,
    AIUnavailableError,
    AIResponseError,
)


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=api_key)


def analyze_resume(resume_text: str) -> ResumeAnalysis:
    prompt = f"""
    Analyze the following resume.

    Identify:
    - A concise professional summary
    - The candidate's skills
    - Their strengths
    - Their weaknesses or areas for improvement
    - Suggestions for improving the resume

    Do not invent information that is not present in the resume.

    Resume:
    {resume_text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ResumeAnalysis,
            ),
        )

    except genai_errors.APIError as exc:
        if exc.code == 429:
            raise AIRateLimitError(
                "AI service rate limit or quota exceeded."
            ) from exc

        if exc.code in (500, 502, 503):
            raise AIUnavailableError(
                "AI service is temporarily unavailable."
            ) from exc

        # Other provider API errors should not expose raw details.
        raise AIResponseError(
            "AI service could not process the request."
        ) from exc

    except (TimeoutError, ConnectionError) as exc:
        raise AIUnavailableError(
            "Could not connect to the AI service."
        ) from exc

    if response.parsed is None:
        raise AIResponseError(
            "AI service returned no valid analysis."
        )

    return response.parsed