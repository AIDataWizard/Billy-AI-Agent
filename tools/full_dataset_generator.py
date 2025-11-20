import os
import random
import pandas as pd
from faker import Faker
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

fake = Faker()

# Create all folders
def ensure_dirs():
    os.makedirs("data/invoices", exist_ok=True)
    os.makedirs("data/claims_cms1500", exist_ok=True)
    os.makedirs("data/clinical_notes", exist_ok=True)
    os.makedirs("data/lab_reports", exist_ok=True)
    os.makedirs("data/reference_tables", exist_ok=True)
    os.makedirs("data/denial_patterns", exist_ok=True)

# Sample ICD / CPT tables
ICD_CODES = [
    ("J18.9", "Pneumonia, unspecified organism"),
    ("E11.9", "Type 2 diabetes mellitus"),
    ("I10", "Essential (primary) hypertension"),
    ("M54.5", "Low back pain"),
    ("R07.9", "Chest pain, unspecified"),
]

CPT_CODES = [
    ("71045", "Chest X-ray, single view"),
    ("99213", "Office Visit, established"),
    ("80050", "General Health Panel"),
    ("93000", "Electrocardiogram"),
    ("87502", "Influenza test"),
]

MODIFIERS = [
    "26", "59", "TC", "RT", "LT", "50"
]

# Generate PDF invoice
def generate_invoice_pdf(idx):
    patient = fake.name()
    dob = fake.date_of_birth().strftime("%Y-%m-%d")
    provider = fake.company()
    icd, icd_desc = random.choice(ICD_CODES)
    cpt, cpt_desc = random.choice(CPT_CODES)
    amount = random.randint(80, 500)

    pdf_path = f"data/invoices/invoice_{idx:03}.pdf"

    styles = getSampleStyleSheet()
    story = [
        Paragraph("Medical Invoice", styles["Title"]),
        Spacer(1, 0.2 * inch),
        Paragraph(f"Patient Name: {patient}", styles["Normal"]),
        Paragraph(f"Patient DOB: {dob}", styles["Normal"]),
        Paragraph(f"Provider: {provider}", styles["Normal"]),
        Paragraph(f"Date of Service: {fake.date_this_year()}", styles["Normal"]),
        Spacer(1, 0.2 * inch),
        Paragraph("<b>Diagnoses (ICD-10)</b>", styles["Heading3"]),
        Paragraph(f"{icd} - {icd_desc}", styles["Normal"]),
        Spacer(1, 0.2 * inch),
        Paragraph("<b>Procedures (CPT)</b>", styles["Heading3"]),
        Paragraph(f"{cpt} - {cpt_desc}", styles["Normal"]),
        Spacer(1, 0.2 * inch),
        Paragraph("<b>Charges</b>", styles["Heading3"]),
        Paragraph(f"{cpt_desc}: ${amount}", styles["Normal"]),
        Paragraph(f"Total: ${amount}", styles["Normal"]),
        Spacer(1, 0.2 * inch),
        Paragraph("Insurance: Medicare", styles["Normal"]),
        Paragraph(f"Policy Number: {fake.random_number(9)}", styles["Normal"]),
    ]

    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    doc.build(story)

# Generate CMS-1500 Claim (Text Version)
def generate_claim(idx):
    icd, icd_desc = random.choice(ICD_CODES)
    cpt, cpt_desc = random.choice(CPT_CODES)

    claim = f"""
    CMS-1500 CLAIM
    Patient: {fake.name()}
    DOB: {fake.date_of_birth()}
    Provider: {fake.company()}
    ICD-10: {icd} - {icd_desc}
    CPT: {cpt} - {cpt_desc}
    Insurance: Medicare
    Charge: ${random.randint(80, 300)}
    """

    with open(f"data/claims_cms1500/claim_{idx:03}.txt", "w") as f:
        f.write(claim)

# Generate Clinical Notes
def generate_clinical_note(idx):
    icd, icd_desc = random.choice(ICD_CODES)

    note = f"""
    CLINICAL NOTE
    Chief Complaint: {fake.sentence()}
    Findings: {fake.text(200)}
    Assessment: Diagnosis suspected is {icd_desc} ({icd}).
    Plan: Imaging/labs recommended.
    """

    with open(f"data/clinical_notes/note_{idx:03}.txt", "w") as f:
        f.write(note)

# Generate Lab Reports
def generate_lab_report(idx):
    lab = f"""
    LAB REPORT
    Patient: {fake.name()}
    Test: Complete Blood Count
    WBC: {random.uniform(3.0, 15.0):.1f}
    RBC: {random.uniform(3.5, 6.0):.1f}
    Hemoglobin: {random.uniform(10.0, 17.0):.1f} g/dL
    Notes: {fake.sentence()}
    """

    with open(f"data/lab_reports/lab_{idx:03}.txt", "w") as f:
        f.write(lab)

# Generate Reference Tables
def generate_reference_tables():
    pd.DataFrame(ICD_CODES, columns=["icd_code", "description"]).to_csv("data/reference_tables/icd10.csv", index=False)
    pd.DataFrame(CPT_CODES, columns=["cpt_code", "description"]).to_csv("data/reference_tables/cpt.csv", index=False)
    pd.DataFrame(MODIFIERS, columns=["modifier"]).to_csv("data/reference_tables/modifiers.csv", index=False)

# Generate Denial Patterns CSV
def generate_denial_dataset():
    records = []
    for i in range(200):
        icd, _ = random.choice(ICD_CODES)
        cpt, _ = random.choice(CPT_CODES)
        dob_missing = random.choice([0, 1])
        policy_missing = random.choice([0, 1])
        denial = 1 if (dob_missing + policy_missing + random.choice([0, 1]) >= 2) else 0

        records.append([icd, cpt, dob_missing, policy_missing, denial])

    df = pd.DataFrame(records, columns=["icd_code", "cpt_code", "missing_dob", "missing_policy", "denied"])
    df.to_csv("data/denial_patterns/denial_training.csv", index=False)

# MAIN FUNCTION
def generate_all(n=20):
    ensure_dirs()

    print("Generating invoices PDFs...")
    for i in range(1, n+1):
        generate_invoice_pdf(i)

    print("Generating CMS-1500 claims...")
    for i in range(1, n+1):
        generate_claim(i)

    print("Generating clinical notes...")
    for i in range(1, n+1):
        generate_clinical_note(i)

    print("Generating lab reports...")
    for i in range(1, n+1):
        generate_lab_report(i)

    print("Generating reference tables...")
    generate_reference_tables()

    print("Generating denial ML dataset...")
    generate_denial_dataset()

    print("\n🎉 Synthetic dataset generation complete!")

if __name__ == "__main__":
    generate_all()
