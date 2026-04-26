FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY antispoof ./antispoof
COPY scripts ./scripts
COPY pyproject.toml .
COPY setup.cfg .

RUN python scripts/download_models.py

EXPOSE 8001

CMD ["uvicorn", "antispoof.api.main:app", "--host", "0.0.0.0", "--port", "8001"]
