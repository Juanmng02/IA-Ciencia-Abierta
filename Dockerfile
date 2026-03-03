FROM python:3.10-slim

LABEL maintainer="[Juan Manuel Novoa] <juanmng02@gmail.com>"
LABEL description="AI Open Science Task 1: Text extraction and analysis from scientific papers"
LABEL version="1.0"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/papers/ ./data/papers/
COPY README.md .

# output directories
RUN mkdir -p data/processed results/figures results/outputs
# Environmental variables
ENV PYTHONUNBUFFERED=1
ENV GROBID_URL=http://host.docker.internal:8070

CMD ["python", "-c", "print('Available scripts:\\n  - python src/extract_text.py\\n  - python src/keyword_cloud.py\\n  - python src/figures_analysis.py\\n  - python src/links_extraction.py')"]

