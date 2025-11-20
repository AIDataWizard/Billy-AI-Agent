import io
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

def pdf_to_images(pdf_bytes: bytes):
    """Convert each PDF page to a PIL image."""
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    for page_index in range(len(pdf)):
        page = pdf[page_index]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

def ocr_extract(file_bytes, ext):
    """Lightweight PDF text extractor with PyMuPDF fallback."""
    try:
        with fitz.open(stream=file_bytes, filetype=ext) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text.strip()
    except:
        return ""
    
# def ocr_extract(file_bytes: bytes, file_type: str):
#     """
#     Extracts text using Tesseract OCR.
#     Works perfectly on Render Free Tier.
#     """
#     text_output = []

#     if file_type.lower() == "pdf":
#         images = pdf_to_images(file_bytes)
#         for img in images:
#             extracted = pytesseract.image_to_string(img)
#             text_output.append(extracted)
#     else:
#         # Image file (JPG/PNG)
#         img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
#         extracted = pytesseract.image_to_string(img)
#         text_output.append(extracted)

#     return "\n".join(text_output)
