# FROM python:3.10-slim

# ENV DEBIAN_FRONTEND=noninteractive

# # Install Tesseract + Poppler (PDF)
# RUN apt-get update && apt-get install -y \
#     tesseract-ocr \
#     tesseract-ocr-eng \
#     poppler-utils \
#     libglib2.0-0 libsm6 libxrender1 libxext6 \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000

# CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "api.main:app", "--bind", "0.0.0.0:8000"]

# FROM python:3.10-slim

# ENV DEBIAN_FRONTEND=noninteractive

# # Install Tesseract + PDF utilities + image libs
# RUN apt-get update && apt-get install -y \
#     tesseract-ocr \
#     tesseract-ocr-eng \
#     poppler-utils \
#     libjpeg62-turbo \
#     libpng16-16 \
#     libtiff5 \
#     libglib2.0-0 \
#     libsm6 \
#     libxrender1 \
#     libxext6 \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000

# CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "api.main:app", "--bind", "0.0.0.0:8000"]

FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install Tesseract + PDF libs
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    libjpeg62-turbo \
    libpng16-16 \
    libtiff-tools \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Tesseract data location
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "api.main:app", "--bind", "0.0.0.0:8000", "--timeout", "120"]
