from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from starlette_admin.contrib.sqla import Admin, ModelView

from api import router as api_router

DATABASE_URL = "postgresql+asyncpg://postgres:web_password_1991@localhost:5432/practice"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
# Models
class Profession(Base):
    __tablename__ = "professions"

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    description = Column(String)

    warriors = relationship("Warrior", back_populates="profession", lazy="selectin")

    def __repr__(self):
        return f"<Profession {self.title}>"

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)

    warrior_links = relationship("SkillOfWarrior", back_populates="skill", cascade="all, delete-orphan", lazy="selectin")

    def __repr__(self):
        return f"<Skill {self.title}>"

class Warrior(Base):
    __tablename__ = "warriors"

    id = Column(Integer, primary_key=True)
    race = Column(String(50), nullable=False)
    name = Column(String(120), nullable=False)
    level = Column(Integer, default=0, nullable=False)

    profession_id = Column(Integer, ForeignKey("professions.id", ondelete="SET NULL"), nullable=True)

    profession = relationship("Profession", back_populates="warriors", lazy="selectin")

    # через промежуточную таблицу
    skills = relationship("SkillOfWarrior", back_populates="warrior",
                          cascade="all, delete-orphan",
                          lazy="selectin")

    def __repr__(self):
        return f"<Warrior {self.name}>"


class SkillOfWarrior(Base):
    __tablename__ = "skill_of_warrior"

    id = Column(Integer, primary_key=True)

    warrior_id = Column(Integer, ForeignKey("warriors.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)

    level = Column(Integer, nullable=False)

    warrior = relationship("Warrior", back_populates="skills", lazy="selectin")
    skill = relationship("Skill", back_populates="warrior_links", lazy="selectin")

    def __repr__(self):
        return f"<SkillOfWarrior W={self.warrior_id} S={self.skill_id} L={self.level}>"



app = FastAPI(title="Warriors System")

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


# админ панель
admin = Admin(engine, title="Warriors Admin")

admin.add_view(ModelView(Warrior))
admin.add_view(ModelView(Profession))
admin.add_view(ModelView(Skill))
admin.add_view(ModelView(SkillOfWarrior))

admin.mount_to(app)

app.include_router(api_router)