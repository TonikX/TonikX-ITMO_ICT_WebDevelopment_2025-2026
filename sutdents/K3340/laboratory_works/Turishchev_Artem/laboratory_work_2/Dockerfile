# Use Python 3.13 as base image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml uv.lock ./

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install Python dependencies
RUN uv pip install --system -r pyproject.toml

# Copy Django project
COPY tour_site ./tour_site

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "cd tour_site && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
