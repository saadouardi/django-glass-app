from fastapi import FastAPI, Query, HTTPException # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from sqlite3 import connect
import logging

app = FastAPI()

origins = ["http://localhost:5173", "http://localhost:8000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend.log"),  # Save logs in backend.log
        logging.StreamHandler()  # Show logs in the console
    ]
)
logger = logging.getLogger(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.get("/data")
async def read_root(search: str = None, page: int = 1, page_size: int = 10):
    try:
        logger.info(f"📌 Fetching data | Search: {search} | Page: {page} | Page Size: {page_size}")
        conn = connect("image_data.db")
        conn.row_factory = dict_factory
        cur = conn.cursor()

        total_query = "SELECT COUNT(*) as total FROM image_data"
        if search:
            total_query += " WHERE title LIKE ? OR description LIKE ?"
            total_result = cur.execute(total_query, [f"%{search}%", f"%{search}%"]).fetchone()
        else:
            total_result = cur.execute(total_query).fetchone()

        total = total_result["total"]

        query = "SELECT * FROM image_data"
        params = []
        if search:
            query += " WHERE title LIKE ? OR description LIKE ?"
            params = [f"%{search}%", f"%{search}%"]
        query += " LIMIT ? OFFSET ?"
        params.extend([page_size, (page - 1) * page_size])
        cur.execute(query, params)

        images = cur.fetchall()
        logger.info(f"✅ Successfully fetched {len(images)} images")
        return {"images": images, "total": total}

    except Exception as e:
        logger.error(f"❌ Internal Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.put("/update/{image_id}")
async def update_image(image_id: str, image: dict):
    """
    Update an image's information.
    - **image_id**: The unique identifier for the image.
    - **image**: A dictionary containing image fields to update.
    """
    conn = connect("image_data.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE image_data SET title = ?, description = ?, ispublic = ?
        WHERE id = ?
    """, (image['title'], image['description'], image['ispublic'], image_id))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Image not found")
    conn.commit()
    return {"message": "Image updated successfully"}

# move search and filtering to the backend ✅
# move pagination logic to the backend ✅
# add error handling for the backend ✅
# minimize the code used in the frontend ✅
# add unit tests using pytest (test / integration tests) ✅
# add integration test using pytest (library in python) and requests (library in python) (in big projects) ✅
# add unit test comments: giving when then ✅
# add function comments() ✅