FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get -y install gcc libpq-dev curl \
    && apt-get clean

RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/

COPY requirements.txt .

RUN uv venv --python python3 \
  && uv pip install -r requirements.txt

ENV PATH="/app/.venv/bin:$PATH"

COPY . .