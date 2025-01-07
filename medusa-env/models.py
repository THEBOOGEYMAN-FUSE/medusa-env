from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel
from database import Base
from datetime import datetime
from passlib.context import CryptContext

# Initialize the password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SQLAlchemy model for the 'users' table
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Pydantic model for user creation
class UserCreate(BaseModel):
    email: str
    username: str
    password: str

    class Config:
        orm_mode = True  # Tells Pydantic to treat this model as an ORM-like object (i.e., from SQLAlchemy)

# Pydantic model for user output (returning user info)
class UserOut(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime  # Use the standard Python datetime type
    updated_at: datetime  # Use the standard Python datetime type

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Ensure DateTime fields are serialized correctly
        }

# Function to hash a password before storing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify a password (e.g., for login)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

