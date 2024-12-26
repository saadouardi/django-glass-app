from sqlite3 import connect

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://localhost:8000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


@app.get("/data")
def read_root():
    conn = connect("image_data.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM image_data")
    return result.fetchall()


@app.put("/update/{image_id}")
def update_image(image_id: str, image: dict):
    conn = connect("image_data.db")
    cur = conn.cursor()

    # Update image data
    cur.execute("""
        UPDATE image_data
        SET title = ?, description = ?, ispublic = ?
        WHERE id = ?
    """, (image["title"], image["description"], image["ispublic"], image_id))
    
    conn.commit()
    return {"message": "Image updated successfully"}

