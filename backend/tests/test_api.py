import requests # type: ignore
from unittest.mock import MagicMock
# @pytest.fixture
# def client():
#     return MagicMock()

def test_fetch_data(client):
    response = client.get("/data", params={"searchQuery": "test", "page": 1, "pageSize": 10})
    
    # Then: The response should have a status code of 200
    assert response.status_code == 200
    
    # And: The response should contain a list of images and a total count
    data = response.json()
    assert 'images' in data and isinstance(data['images'], list), "Response does not include an images list"
    assert 'total' in data, "Response does not include a total count"

def test_search_data():
    url = "http://localhost:9000/data?search=query"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert 'images' in data and isinstance(data['images'], list), "Response does not include an images list"
    # Assuming you're looking for a specific field within each image, adjust 'some_field' as needed
    assert all('query' in item['some_field'] for item in data['images']), "Search results do not contain the query"
