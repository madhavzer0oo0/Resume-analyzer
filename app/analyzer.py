import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0.3
)

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert ATS (Applicant Tracking System) and career coach.
Always respond with ONLY valid JSON, no markdown, no backticks, no extra text."""),
    ("human", """
Analyze the resume below against the job description and return a JSON with exactly these keys:
1. "ats_score": integer 0-100 (keyword match score)
2. "matched_skills": list of skills found in both resume and JD
3. "missing_skills": list of important skills in JD but missing from resume
4. "improvement_tips": list of 5 specific actionable tips to improve the resume
5. "overall_feedback": 2-3 sentence summary

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
""")
])

chain = prompt | llm | parser

def analyze_resume(resume_text: str, job_description: str) -> dict:
    try:
        result = chain.invoke({
            "resume_text": resume_text,
            "job_description": job_description
        })
        return result
    except Exception as e:
        raise ValueError(f"Analysis failed: {str(e)}")