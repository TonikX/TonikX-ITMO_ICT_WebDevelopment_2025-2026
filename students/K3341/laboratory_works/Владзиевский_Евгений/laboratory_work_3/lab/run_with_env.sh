#!/usr/bin/env bash
set -euo pipefail

# Директория с docker-compose.yml
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Значения окружения по умолчанию
export DB_NAME=${DB_NAME:-postgres}
export DB_USER=${DB_USER:-postgres}
export DB_PASSWORD=${DB_PASSWORD:-test}
export JWT_SECRET_KEY=${JWT_SECRET_KEY:-test}

export S3_BUCKET=${S3_BUCKET:-images}
export S3_ACCESS_KEY=${S3_ACCESS_KEY:-minio}
export S3_SECRET_KEY=${S3_SECRET_KEY:-minio123}

# Для контейнера MinIO и внутренних ссылок
export S3_URL=${S3_URL:-http://minio:9000}
# Публичный адрес MinIO, который будет сохранён в БД и отдаваться клиенту
export S3_PUBLIC_URL=${S3_PUBLIC_URL:-http://127.0.0.1:9000}

echo "DB_NAME=${DB_NAME}"
echo "DB_USER=${DB_USER}"
echo "DB_PASSWORD=${DB_PASSWORD}"
echo "JWT_SECRET_KEY=${JWT_SECRET_KEY}"
echo "S3_BUCKET=${S3_BUCKET}"
echo "S3_ACCESS_KEY=${S3_ACCESS_KEY}"
echo "S3_SECRET_KEY=${S3_SECRET_KEY}"
echo "S3_URL=${S3_URL}"
echo "S3_PUBLIC_URL=${S3_PUBLIC_URL}"

docker-compose -f "${SCRIPT_DIR}/docker-compose.yml" up -d --build
