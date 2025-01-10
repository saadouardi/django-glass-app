from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlite3 import connect

app = FastAPI()

origins = ["http://localhost:5173", "http://localhost:8000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.get("/data")
async def read_root(
    search: str = Query(default=None), page: int = Query(default=1), page_size: int = Query(default=10)
):
    """
    Fetch paginated data with optional search filtering.
    """
    try:
        conn = connect("image_data.db")
        conn.row_factory = dict_factory
        cur = conn.cursor()

        # Query for total count
        if search:
            total_query = "SELECT COUNT(*) as total FROM image_data WHERE title LIKE ? OR description LIKE ?"
            total_result = cur.execute(total_query, [f"%{search}%", f"%{search}%"]).fetchone()
        else:
            total_query = "SELECT COUNT(*) as total FROM image_data"
            total_result = cur.execute(total_query).fetchone()

        total = total_result["total"]

        # Query for paginated results
        query = "SELECT * FROM image_data "
        params = []
        if search:
            query += "WHERE title LIKE ? OR description LIKE ? "
            params = [f"%{search}%", f"%{search}%"]
        query += "LIMIT ? OFFSET ?"
        params.extend([page_size, (page - 1) * page_size])
        cur.execute(query, params)

        images = cur.fetchall()
        return {"images": images, "total": total}
    except Exception as e:
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


# from sqlite3 import connect
# from fastapi import Query, FastAPI, HTTPException # type: ignore
# from fastapi.middleware.cors import CORSMiddleware # type: ignore


# app = FastAPI()
# origins = [
#     "http://localhost:5173",
#     "http://localhost:8000"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# def dict_factory(cursor, row):
#     fields = [column[0] for column in cursor.description]
#     return {key: value for key, value in zip(fields, row)}

# @app.get("/data")
# def read_root(search: str = Query(None)):
#     conn = connect("image_data.db")
#     conn.row_factory = dict_factory
#     cur = conn.cursor()
#     if search:
#         query = """
#         SELECT * FROM image_data
#         WHERE title LIKE :search OR description LIKE :search
#         """
#         result = cur.execute(query, {'search': f'%{search}%'})
#     else:
#         result = cur.execute("SELECT * FROM image_data")
#     return result.fetchall()

# @app.get("/data")
# def read_root(search: str = Query(None), page: int = Query(1), page_size: int = Query(10)):
#     conn = connect("image_data.db")
#     conn.row_factory = dict_factory
#     cur = conn.cursor()
#     offset = (page - 1) * page_size
#     if search:
#         query = """
#         SELECT * FROM image_data
#         WHERE title LIKE :search OR description LIKE :search
#         LIMIT :page_size OFFSET :offset
#         """
#         result = cur.execute(query, {'search': f'%{search}%', 'page_size': page_size, 'offset': offset})
#     else:
#         result = cur.execute("SELECT * FROM image_data LIMIT ? OFFSET ?", (page_size, offset))
#     return result.fetchall()

# @app.put("/update/{image_id}")
# def update_image(image_id: str, image: dict):
#     conn = connect("image_data.db")
#     try:
#         cur = conn.cursor()
#         # Update image data
#         cur.execute("""
#             UPDATE image_data
#             SET title = ?, description = ?, ispublic = ?
#             WHERE id = ?
#         """, (image["title"], image["description"], image["ispublic"], image_id))
        
#         if cur.rowcount == 0:
#             raise HTTPException(status_code=404, detail="Image not found")
        
#         conn.commit()
#         return {"message": "Image updated successfully"}
#     except Exception as e:
#         conn.rollback()
#         raise HTTPException(status_code=500, detail=str(e))


# # move search and filtering to the backend
# # move pagination logic to the backend
# # add error handling for the backend
# # minimize the code used in the frontend
# # add unit tests using pytest (test / integration tests)
# # add integration test using pytest (library in python) and requests (library in python) (in big projects) 
# # add unit test comments: giving when then
# # add function comments()
# # error handling
