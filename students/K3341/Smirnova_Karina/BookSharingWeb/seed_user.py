import datetime
import os

from passlib.context import CryptContext
from sqlalchemy import create_engine, text

DB_ADMIN = os.getenv("DB_ADMIN")
if not DB_ADMIN:
    raise RuntimeError("DB_ADMIN is not set")

engine = create_engine(DB_ADMIN)

def main():
    with engine.begin() as conn:
        pwd_context = CryptContext(schemes=['bcrypt'])
        conn.execute(
            text("""
                            INSERT INTO users (id, username, email, password, created_at)
                            VALUES (:id, :username, :email, :password, NOW())
                            ON CONFLICT (id) DO NOTHING
                        """),
            {
                "id": 1,
                "username": "seed_user",
                "email": "seed_user@example.com",
                "password": "seed_password"
            },
        )

if __name__ == "__main__":
    main()