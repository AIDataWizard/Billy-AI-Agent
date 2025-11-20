# import json
# import pdfplumber

# from agents.document_parser import DocumentParserAgent
# from agents.clinical_coding_agent import ClinicalCodingAgent
# from agents.necessity_agent import MedicalNecessityAgent
# from agents.compliance_agent import ComplianceAgent
# from agents.denial_predictor import DenialPredictorAgent
# from agents.correction_agent import CorrectionAgent
# from tools.ocr_reader import ocr_extract

# import os
# from tools.ocr_reader import ocr_extract

# def load_document(file_path):
#     ext = file_path.split(".")[-1].lower()
#     with open(file_path, "rb") as f:
#         file_bytes = f.read()
#     return file_bytes, ext

# def extract_text_from_pdf(pdf_path):
#     """
#     Extract text from PDF.
#     1. Try pdfplumber (for digital PDFs)
#     2. If text is empty → fallback to OCR (for scanned PDFs)
#     """
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             text = ""
#             for page in pdf.pages:
#                 extracted = page.extract_text()
#                 if extracted:
#                     text += extracted + "\n"

#         # If digital text exists → return it
#         if len(text.strip()) > 20:
#             return text.strip()

#     except:
#         pass

#     # Otherwise → use OCR
#     return ocr_extract(pdf_path)


# def run_full_pipeline(pdf_path):
#     print("📄 Loading document...")
#     raw_text = extract_text_from_pdf(pdf_path)

#     print("🤖 Step 1: Parsing document...")
#     parser = DocumentParserAgent()
#     parsed = parser.parse_document(raw_text)
#     print("Parsed:", parsed)

#     print("\n🧠 Step 2: Validate Clinical Coding...")
#     coding = ClinicalCodingAgent()
#     coding_result = coding.validate_codes(
#         icd_list="auto-extracted by parser",
#         cpt_list="auto-extracted by parser",
#     )
#     print("Coding Result:", coding_result)

#     print("\n🩺 Step 3: Medical Necessity Check...")
#     necessity = MedicalNecessityAgent()
#     necessity_result = necessity.check_necessity(
#         clinical_text=raw_text,
#         diagnoses="from parsed document",
#         procedures="from parsed document"
#     )
#     print("Necessity:", necessity_result)

#     print("\n⚖️ Step 4: Compliance Check...")
#     compliance = ComplianceAgent()
#     compliance_result = compliance.check_compliance(parsed)
#     print("Compliance:", compliance_result)

#     print("\n📉 Step 5: Denial Prediction...")
#     predictor = DenialPredictorAgent()
#     denial_result = predictor.predict(parsed)
#     print("Denial Risk:", denial_result)

#     print("\n🛠 Step 6: Correction & Fixes...")
#     corrector = CorrectionAgent()
#     correction = corrector.correct(parsed)
#     print("Corrections:", correction)

#     print("\n✅ Pipeline Completed.")

#     final_output = {
#         "parsed_document": parsed,
#         "coding_validation": coding_result,
#         "medical_necessity": necessity_result,
#         "compliance": compliance_result,
#         "denial_prediction": denial_result,
#         "suggested_corrections": correction,
#     }
    

#     print("\n📦 Saving output to outputs/final_result.json")
#     import os
#     # Ensure output folder exists
#     os.makedirs("outputs", exist_ok=True)
#     with open("outputs/final_result.json", "w") as f:
#         json.dump(final_output, f, indent=4)

#     return final_output


# if __name__ == "__main__":
#     print("🚀 Running Healthcare Claims + Clinical Document Pipeline")

#     # SAMPLE_PDF = "data/invoices/sample_medical_invoice.pdf"  # Replace soon
#     SAMPLE_PDF = "data/invoices/real_medical_invoice.pdf"  # Replace soon

#     output = run_full_pipeline(SAMPLE_PDF)
#     print("\n🎉 Final Output:")
#     print(output)


import json
import pdfplumber

from agents.document_parser import DocumentParserAgent
from agents.clinical_coding_agent import ClinicalCodingAgent
from agents.necessity_agent import MedicalNecessityAgent
from agents.compliance_agent import ComplianceAgent
from agents.denial_predictor import DenialPredictorAgent
from agents.correction_agent import CorrectionAgent
from tools.ocr_reader import ocr_extract


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF. If empty → use OCR."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        if len(text.strip()) > 20:
            return text.strip()

    except Exception:
        pass

    # Fallback: Read file bytes + OCR
    with open(pdf_path, "rb") as f:
        file_bytes = f.read()

    return ocr_extract(file_bytes, "pdf")


def run_full_pipeline(pdf_path):
    print("📄 Loading document...")
    raw_text = extract_text_from_pdf(pdf_path)

    print("🤖 Step 1: Parsing document...")
    parser = DocumentParserAgent()
    parsed = parser.parse_document(raw_text)
    print("Parsed:", parsed)

    print("\n🧠 Step 2: Validate Clinical Coding...")
    coding = ClinicalCodingAgent()
    coding_result = coding.validate_codes(
        icd_list="auto-extracted by parser",
        cpt_list="auto-extracted by parser",
    )
    print("Coding Result:", coding_result)

    print("\n🩺 Step 3: Medical Necessity Check...")
    necessity = MedicalNecessityAgent()
    necessity_result = necessity.check_necessity(
        clinical_text=raw_text,
        diagnoses="from parsed document",
        procedures="from parsed document"
    )
    print("Necessity:", necessity_result)

    print("\n⚖️ Step 4: Compliance Check...")
    compliance = ComplianceAgent()
    compliance_result = compliance.check_compliance(parsed)
    print("Compliance:", compliance_result)

    print("\n📉 Step 5: Denial Prediction...")
    predictor = DenialPredictorAgent()
    denial_result = predictor.predict(parsed)
    print("Denial Risk:", denial_result)

    print("\n🛠 Step 6: Correction & Fixes...")
    corrector = CorrectionAgent()
    correction = corrector.correct(parsed)
    print("Corrections:", correction)

    print("\n✅ Pipeline Completed.")

    final_output = {
        "parsed_document": parsed,
        "coding_validation": coding_result,
        "medical_necessity": necessity_result,
        "compliance": compliance_result,
        "denial_prediction": denial_result,
        "suggested_corrections": correction,
    }

    print("\n📦 Saving output to outputs/final_result.json")
    import os
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/final_result.json", "w") as f:
        json.dump(final_output, f, indent=4)

    return final_output


if __name__ == "__main__":
    print("🚀 Running Healthcare Claims + Clinical Document Pipeline")

    SAMPLE_PDF = "data/invoices/real_medical_invoice.pdf"
    output = run_full_pipeline(SAMPLE_PDF)

    print("\n🎉 Final Output:")
    print(output)
