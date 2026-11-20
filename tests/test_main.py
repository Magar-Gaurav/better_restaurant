def test_main_app(client):

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Food Management API" : "Food and Restaurant data"}