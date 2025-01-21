from sqlite3 import connect
import logging
from services.db import dict_factory


logger = logging.getLogger(__name__)


def get_images(search=None, page=1, page_size=10, username: dict = None):
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
