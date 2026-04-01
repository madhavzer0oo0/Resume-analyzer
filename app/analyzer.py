import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are an expert ATS (Applicant Tracking System) and career coach.

Analyze the resume below against the job description and return a JSON with:
1. "ats_score": integer 0-100 (keyword match score)
2. "matched_skills": list of skills found in both resume and JD
3. "missing_skills": list of important skills in JD but missing from resume
4. "improvement_tips": list of 5 specific, actionable tips to improve the resume
5. "overall_feedback": 2-3 sentence summary

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON, no extra text.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Best free Groq model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)
