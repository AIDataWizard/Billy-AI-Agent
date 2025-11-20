🩺 AI Healthcare Claims + Clinical Document Compliance Agent
A Multi-Agent LLM System for Medical Invoices, Claims, Coding Validation, Compliance Audits & Denial Prediction

📌 Overview

Healthcare billing generates massive administrative overhead, high denial rates, and complex compliance requirements across ICD-10, CPT/HCPCS, Medicare rules, NCCI bundling, and medical necessity documentation.

This project implements a full multi-agent AI system that reads medical invoices, CMS-1500 claims, clinical notes, and lab reports, then performs:

✔ Document parsing

✔ ICD-10 & CPT validation

✔ Clinical justification checks

✔ Compliance auditing

✔ Denial likelihood prediction

✔ Automatic claim correction

✔ Appeal letter generation

The project uses Groq + Llama-3.3-70b Versatile (free, extremely fast) for all LLM reasoning.

This is a complete Kaggle-capstone-ready project with code, synthetic datasets, pipeline, and results.

🎯 Key Features
🧩 Multi-Agent Architecture
Agent	Responsibility
DocumentParserAgent	Reads PDFs, extracts structured fields
ClinicalCodingAgent	Validates ICD-10 ↔ CPT pairings
MedicalNecessityAgent	Checks documentation supports billed procedures
ComplianceAgent	Validates bundling, modifiers, payer rules
DenialPredictorAgent	Predicts denial likelihood
CorrectionAgent	Fixes claim fields + generates appeal letter
🧠 Technical Stack

Backend: Python

Agents: Custom classes + Groq LLM

LLM Model: llama-3.3-70b-versatile

PDF Parsing: pdfplumber

Synthetic Dataset: Faker, ReportLab