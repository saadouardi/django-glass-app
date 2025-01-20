import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from backend.services import get_images, update_image

@pytest.fixture
def mock_db():
    """Mock database connection and cursor."""
    with patch("backend.services.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        return mock_cursor  # ✅ Return the cursor so we can manipulate it

# def test_get_images_no_search(mock_db):
#     """Test fetching images when no search term is provided."""
#     mock_db.fetchall.return_value = [  # ✅ Ensure `.fetchall()` returns mocked data
#         {"id": "1", "title": "Sample Image", "description": "A test image"}
#     ]
#     mock_db.fetchone.return_value = {"total": 1}  # ✅ Ensure `.fetchone()` works

#     result = get_images(search=None, page=1, page_size=10)

#     assert "images" in result
#     assert len(result["images"]) == 1  # ✅ This should now pass

# def test_get_images_with_search(mock_db):
#     """Test searching for images by title."""
#     mock_db.fetchall.return_value = [  # ✅ Mock database query response
#         {"id": "2", "title": "Sunset", "description": "A beautiful sunset"}
#     ]
#     mock_db.fetchone.return_value = {"total": 1}  # ✅ Mock count query

#     result = get_images(search="sunset", page=1, page_size=10)

#     assert "images" in result
#     assert len(result["images"]) == 1  # ✅ This should now pass

def test_update_image_not_found(mock_db):
    """Test updating an image that does not exist."""
    mock_db.execute.return_value = None  # ✅ Avoid calling real DB
    mock_db.rowcount = 0  # ✅ Ensure no rows were updated

    image_data = {
        "title": "Updated Image",
        "description": "New description",
        "ispublic": 1
    }

    result = update_image("999", image_data)

    assert "error" in result  # ✅ Should now pass
    assert result["error"] == "Image not found"
