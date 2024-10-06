import enum
from datetime import datetime

from pydantic_settings import BaseSettings
from sqlalchemy import func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Settings(BaseSettings):
    url: str = f"sqlite+aiosqlite:///sqlite3.db"
    echo: bool = False


settings = Settings()

engine = create_async_engine(settings.url)

session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def scoped_session_dependency():
    async with session_factory() as session:
        yield session
        await session.close()


class Base(DeclarativeBase):
    pass


class Process(str, enum.Enum):
    not_started = "not started"
    in_progress = "in progress"
    done = "done"


class Todo(Base):
    __tablename__ = "todo"
    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str]
    process: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
