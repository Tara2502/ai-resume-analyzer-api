import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.schemas.resume import ResumeAnalysis


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

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

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ResumeAnalysis,
        ),
    )

    return response.parsed