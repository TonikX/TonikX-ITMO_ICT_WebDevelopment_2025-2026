FROM python:3.13-slim


RUN apt-get update \
 && apt-get install -y --no-install-recommends \
 postgresql-client \
 gcc \
 g++ \
 python3-dev \
 curl \ 
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .
RUN pip cache purge && \
    pip install --default-timeout=120 --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]
