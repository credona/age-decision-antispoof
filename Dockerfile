FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG VERSION
ARG REPOSITORY
ARG TITLE
ARG DESCRIPTION
ARG LICENSE

LABEL org.opencontainers.image.title="${TITLE}"
LABEL org.opencontainers.image.description="${DESCRIPTION}"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.licenses="${LICENSE}"
LABEL org.opencontainers.image.source="${REPOSITORY}"

RUN apt-get update && apt-get install -y \
    git \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY antispoof ./antispoof
COPY scripts ./scripts
COPY pyproject.toml .
COPY setup.cfg .
COPY project.json .
COPY compatibility.json .

RUN chmod +x scripts/dev/*.sh scripts/ci/*.sh scripts/docker/*.sh || true

EXPOSE 8001

CMD ["uvicorn", "antispoof.api.main:app", "--host", "0.0.0.0", "--port", "8001"]
