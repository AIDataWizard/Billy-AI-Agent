from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
import json
from fastapi import FastAPI, UploadFile, File
import uvicorn
import pdfplumber
import tempfile
from agents.document_parser import DocumentParserAgent
from agents.clinical_coding_agent import ClinicalCodingAgent
from agents.necessity_agent import MedicalNecessityAgent
from agents.compliance_agent import ComplianceAgent
from agents.denial_predictor import DenialPredictorAgent
from agents.correction_agent import CorrectionAgent
from tools.ocr_reader import ocr_extract
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Billy - AI Medical Invoice & Claims Agent")
templates = Jinja2Templates(directory="api/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/ui/full-pipeline", response_class=HTMLResponse)
async def ui_full_pipeline(request: Request, file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    text = extract_text(tmp_path)

    parsed = DocumentParserAgent().parse_document(text)
    coding = ClinicalCodingAgent().validate_codes("auto", "auto")
    necessity = MedicalNecessityAgent().check_necessity(text, "auto", "auto")
    compliance = ComplianceAgent().check_compliance(parsed)
    denial = DenialPredictorAgent().predict(parsed)
    corrections = CorrectionAgent().correct(parsed)

    full_result = {
        "parsed": parsed,
        "coding": coding,
        "necessity": necessity,
        "compliance": compliance,
        "denial_prediction": denial,
        "corrections": corrections
    }

    formatted = json.dumps(full_result, indent=4)

    return templates.TemplateResponse("upload.html", {
        "request": request,
        "result": formatted
    })


# Utility: extract text from PDF (same used in pipeline)
def extract_text(pdf_file):
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = "".join([page.extract_text() or "" for page in pdf.pages])
        if len(text.strip()) > 10:
            return text
    except:
        pass
    return ocr_extract(pdf_file)


@app.post("/parse")
async def parse_document(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    text = extract_text(tmp_path)
    agent = DocumentParserAgent()
    result = agent.parse_document(text)
    return {"parsed": result}


@app.post("/validate")
async def validate_codes(icd: str, cpt: str):
    agent = ClinicalCodingAgent()
    result = agent.validate_codes([icd], [cpt])
    return {"coding_validation": result}


@app.post("/necessity")
async def necessity_check(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    text = extract_text(tmp_path)
    agent = MedicalNecessityAgent()
    result = agent.check_necessity(text, "auto", "auto")
    return {"necessity": result}


@app.post("/compliance")
async def compliance_check(payload: dict):
    agent = ComplianceAgent()
    result = agent.check_compliance(payload)
    return {"compliance": result}


@app.post("/predict")
async def denial_prediction(payload: dict):
    agent = DenialPredictorAgent()
    result = agent.predict(payload)
    return {"denial_prediction": result}


@app.post("/correct")
async def correct_claim(payload: dict):
    agent = CorrectionAgent()
    result = agent.correct(payload)
    return {"corrections": result}


@app.post("/full-pipeline")
async def full_pipeline(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    text = extract_text(tmp_path)

    parsed = DocumentParserAgent().parse_document(text)
    coding = ClinicalCodingAgent().validate_codes("auto", "auto")
    necessity = MedicalNecessityAgent().check_necessity(text, "auto", "auto")
    compliance = ComplianceAgent().check_compliance(parsed)
    denial = DenialPredictorAgent().predict(parsed)
    corrections = CorrectionAgent().correct(parsed)

    return {
        "parsed": parsed,
        "coding": coding,
        "necessity": necessity,
        "compliance": compliance,
        "denial_prediction": denial,
        "corrections": corrections
    }


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)

origins = ["*"]  # or your frontend domain

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)