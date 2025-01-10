import requests # type: ignore

def test_fetch_data():
    # Given: An endpoint URL
    url = "http://localhost:9000/data"
    
    # When: Sending a GET request to the endpoint
    response = requests.get(url)
    
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
