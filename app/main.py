from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import io
from app.parser import extract_text
from app.analyzer import analyze_resume

app = FastAPI(title="Resume Analyzer")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        contents = await resume.read()
        file_obj = io.BytesIO(contents)
        resume_text = extract_text(file_obj, resume.filename)
        result = analyze_resume(resume_text, job_description)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)