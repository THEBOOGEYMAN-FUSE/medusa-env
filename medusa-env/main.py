from jose import jwt
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User, UserCreate  # Import the User model and UserCreate Pydantic model
from database import get_db
from passlib.context import CryptContext
from pydantic import EmailStr
from datetime import datetime, timedelta

app = FastAPI()

# Secret key to encode and decode JWT tokens
SECRET_KEY = "your_secret_key"  # Replace with a stronger secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry time (in minutes)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify JWT token
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dependency to get a database session
@app.post("/signup")
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if the email already exists
    async with db.begin():
        result = await db.execute(select(User).filter(User.email == user.email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash the password
        hashed_password = hash_password(user.password)

        # Create new user with hashed password
        new_user = User(email=user.email, password=hashed_password, username=user.username)

        db.add(new_user)
        await db.commit()
        return {"message": "User created successfully"}

@app.post("/login")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if the email exists
    async with db.begin():
        result = await db.execute(select(User).filter(User.email == user.email))
        existing_user = result.scalar_one_or_none()

        if not existing_user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        # Verify password
        if not verify_password(user.password, existing_user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        # Create a JWT token
        access_token = create_access_token(data={"sub": existing_user.email})
        return {"access_token": access_token, "token_type": "bearer"}

# Secure Route (Example)
@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(verify_token)):
    return {"user": current_user}

