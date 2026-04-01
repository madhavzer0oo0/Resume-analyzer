from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
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
        # Read file bytes
        contents = await resume.read()

        # Extract text from PDF or DOCX
        resume_text = extract_text(contents, resume.filename)

        if not resume_text.strip():
            return JSONResponse(
                content={"error": "Could not extract text from resume. Make sure it is not a scanned image."},
                status_code=400
            )

        # Analyze via LangChain + Groq
        result = analyze_resume(resume_text, job_description)
        return JSONResponse(content=result)

    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": f"Unexpected error: {str(e)}"}, status_code=500)