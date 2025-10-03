"""initial schema with default admin

Revision ID: 4673e859dba3
Revises:
Create Date: 2025-10-03 03:01:53
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# ========== Alembic identifiers ==========
revision = "4673e859dba3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("owner", sa.String()),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("description", sa.Text()),
    )
    op.create_index("ix_hotels_name", "hotels", ["name"])

    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("hotel_id", sa.Integer(), sa.ForeignKey("hotels.id", ondelete="CASCADE")),
        sa.Column("room_type", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("amenities", sa.Text()),
    )

    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'bookingstatus') THEN
                CREATE TYPE bookingstatus AS ENUM (
                    'pending','confirmed','cancelled','checked_in','checked_out'
                );
            END IF;
        END
        $$;
        """
    )

    booking_status = postgresql.ENUM(
        "pending", "confirmed", "cancelled", "checked_in", "checked_out",
        name="bookingstatus",
        create_type=False,
    )

    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("room_id", sa.Integer(), sa.ForeignKey("rooms.id", ondelete="CASCADE")),
        sa.Column("check_in_date", sa.Date(), nullable=False),
        sa.Column("check_out_date", sa.Date(), nullable=False),
        sa.Column(
            "status",
            booking_status,
            nullable=False,
            server_default=sa.text("'pending'::bookingstatus"),
        ),
    )

    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("hotel_id", sa.Integer(), sa.ForeignKey("hotels.id", ondelete="CASCADE")),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("stay_period_start", sa.Date()),
        sa.Column("stay_period_end", sa.Date()),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("reviews")
    op.drop_table("bookings")

    op.execute("DROP TYPE IF EXISTS bookingstatus")

    op.drop_table("rooms")
    op.drop_index("ix_hotels_name", table_name="hotels")
    op.drop_table("hotels")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
