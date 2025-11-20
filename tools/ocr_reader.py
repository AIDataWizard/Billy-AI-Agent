from paddleocr import PaddleOCR
import pdf2image
import numpy as np

# Initialize once (fast)
ocr = PaddleOCR(lang='en', use_angle_cls=True)

def ocr_extract(pdf_path):
    try:
        images = pdf2image.convert_from_path(pdf_path)
        full_text = ""

        for img in images:
            img_np = np.array(img)
            result = ocr.ocr(img_np, cls=True)

            for line in result:
                for word_info in line:
                    full_text += word_info[1][0] + " "

            full_text += "\n"

        return full_text.strip()

    except Exception as e:
        return f"OCR error: {e}"
