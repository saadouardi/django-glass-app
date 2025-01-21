from sqlite3 import connect
from passlib.context import CryptContext # type: ignore
from datetime import datetime, timedelta
from jose import jwt, JWTError # type: ignore
from services.db import dict_factory

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key and algorithm for JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str):
    return pwd_context.hash(password)

# 🔹 Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 🔹 Authenticate user
def authenticate_user(username: str, password: str):
    conn = connect("image_data.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()

    if not user or not verify_password(password, user["password"]):
        return None  # ❌ Authentication failed

    return user  # ✅ Authentication successful

# 🔹 Create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
