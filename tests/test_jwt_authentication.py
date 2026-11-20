from app.core.jwt import create_access_token
from datetime import timedelta


def test_valid_jwt_token(test_user, test_restaurant, client):
    token = create_access_token(data = {"sub" : test_user.username})

    headers = {
        "Authorization" : f"Bearer {token}"
    }
    
    response = client.get("/restaurant", headers = headers)

    assert response.status_code == 200

def test_missing_jwt_token(client):
    response = client.get("/restaurant")
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

def test_invalid_jwt_token(client):
    token = "invalid_token"

    response = client.get("/restaurant", headers = {"Authorization" : f"Bearer {token}"})

    assert response.status_code == 401

def test_expired_jwt(test_user,client):
    token = create_access_token(
        data = {"sub" : test_user.username},
        expires_delta = timedelta(minutes = -1)
    )

    response = client.get("/restaurant", headers = {"Authorization" : f"Bearer {token}"})

    assert response.status_code == 401

def test_inactive_user(test_user, client):
    test_user.is_active = False
    token = create_access_token(
        data = {"sub" : test_user.username}
    )

    response = client.get("/restaurant", headers = {"Authorization" : f"Bearer {token}"})

    assert response.status_code == 403

    assert response.json() == {"detail": "Inactive user"}