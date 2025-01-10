import requests # type: ignore

def test_fetch_data():
    url = "http://localhost:9000/data"
    response = requests.get(url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of items

def test_search_data():
    url = "http://localhost:9000/data?search=query"
    response = requests.get(url)
    assert response.status_code == 200
    # More specific tests can be added here based on the expected search results
