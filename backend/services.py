import logging
from sqlite3 import connect
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError

# Configure logging
logger = logging.getLogger(__name__)



# Secret key and algorithm for JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)

def dict_factory(cursor, row):
    """Converts database row objects to dictionaries."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# 🔹 Hash password
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


def get_images(search=None, page=1, page_size=10):
    """Fetch paginated image data with optional search."""
    try:
        conn = connect("image_data.db")
        conn.row_factory = dict_factory
        cur = conn.cursor()

        # Get total count
        total_query = "SELECT COUNT(*) as total FROM image_data"
        params = []
        if search:
            total_query += " WHERE title LIKE ? OR description LIKE ?"
            params = [f"%{search}%", f"%{search}%"]
        total_result = cur.execute(total_query, params).fetchone()
        total = total_result["total"]

        # Fetch paginated data
        query = "SELECT * FROM image_data"
        if search:
            query += " WHERE title LIKE ? OR description LIKE ?"
        query += " LIMIT ? OFFSET ?"
        params.extend([page_size, (page - 1) * page_size])
        cur.execute(query, params)

        images = cur.fetchall()
        print(f"DEBUG: Queried {len(images)} images from database")  # ✅ Debugging
        logger.info(f"✅ Fetched {len(images)} images | Search: {search} | Page: {page}")
        return {"images": images, "total": total}

    except Exception as e:
        logger.error(f"❌ Error fetching images: {str(e)}")
        return {"error": str(e)}

def update_image(image_id, image):
    """
    Update an image's title, description, and public status.
    """
    try:
        conn = connect("image_data.db")
        cur = conn.cursor()
        cur.execute(
            "UPDATE image_data SET title = ?, description = ?, ispublic = ? WHERE id = ?",
            (image["title"], image["description"], image["ispublic"], image_id),
        )

        if cur.rowcount == 0:  # ✅ Return proper error if image not found
            return {"error": "Image not found"}

        conn.commit()
        logger.info(f"✅ Updated image {image_id}")
        return {"message": "Image updated successfully"}

    except Exception as e:
        logger.error(f"❌ Error updating image {image_id}: {str(e)}")
        return {"error": str(e)}
