import io
import numpy as np
import easyocr
from PIL import Image

# Initialize OCR reader once (CPU mode)
reader = easyocr.Reader(['en'], gpu=False)

def ocr_extract(file_bytes: bytes):
    """
    Extracts text from an image or PDF using EasyOCR.
    Works on Render Free Tier (no PaddleOCR dependencies)
    """
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    arr = np.array(image)
    text_results = reader.readtext(arr, detail=0)
    return "\n".join(text_results)

