from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Update this with your actual database URL
DATABASE_URL = "postgresql+asyncpg://postgres:M3M3NT0M0r!@localhost/medusa_env_db"

# SQLAlchemy engine and session setup
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base class for defining ORM models
Base = declarative_base()

# Dependency to get a database session
async def get_db():
    async with async_session() as session:
        yield session

