from pathlib import Path

# Базовая директория проекта (backend/)
BASE_DIR = Path(__file__).resolve().parents[1]

# Директория для хранения пользовательского контента
CONTENT_ROOT = BASE_DIR / "content"
