from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
)

from starlette_admin.contrib.sqla import Admin, ModelView

DATABASE_URL = "postgresql+asyncpg://postgres:web_password_1991@localhost:5432/practice"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


# Models
class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True)
    last_name = Column(String(40), nullable=False)
    first_name = Column(String(40), nullable=False)
    birth_date = Column(DateTime, nullable=True)
    passport_number = Column(String(20), nullable=False)
    home_address = Column(String(100), nullable=True)
    nationality = Column(String(40), nullable=True)

    licenses = relationship("DriverLicense", back_populates="user", cascade="all, delete-orphan", lazy="selectin")
    ownerships = relationship("Ownership", back_populates="user", cascade="all, delete-orphan", lazy="selectin")
    cars = relationship("Car", secondary="ownerships", back_populates="users", overlaps="ownerships", lazy="selectin")


class DriverLicense(Base):
    __tablename__ = "driver_licenses"

    id_license = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"), nullable=False)
    license_number = Column(String(10), nullable=False, unique=True)
    type = Column(String(10), nullable=False)
    issue_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="licenses", lazy="selectin")


class Car(Base):
    __tablename__ = "cars"

    id_car = Column(Integer, primary_key=True)
    plate = Column(String(15), nullable=False, unique=True)
    brand = Column(String(20), nullable=False)
    model = Column(String(20), nullable=False)
    color = Column(String(30), nullable=False)

    ownerships = relationship("Ownership", back_populates="car", cascade="all, delete-orphan", overlaps="cars", lazy="selectin")
    users = relationship("User", secondary="ownerships", back_populates="cars", overlaps="ownerships", lazy="selectin")


class Ownership(Base):
    __tablename__ = "ownerships"

    id_user_car = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"), nullable=False)
    id_car = Column(Integer, ForeignKey("cars.id_car", ondelete="CASCADE"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)

    user = relationship(
        "User",
        back_populates="ownerships",
        overlaps="cars,users",
        lazy="selectin"
    )
    car = relationship(
        "Car",
        back_populates="ownerships",
        overlaps="cars,users",
        lazy="selectin"
    )

    __table_args__ = (UniqueConstraint("id_user", "id_car", "start_date", name="uq_user_car_start"),)


app = FastAPI(title="Cars & Owners System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


admin = Admin(engine, title="My Admin")

admin.add_view(ModelView(User))
admin.add_view(ModelView(Car))
admin.add_view(ModelView(Ownership))
admin.add_view(ModelView(DriverLicense))

admin.mount_to(app)