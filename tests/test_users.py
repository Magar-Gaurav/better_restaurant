from sqlalchemy import select
from app.models.food_model import User
from app.core.security import verify_password

def test_users(test_user):
    assert test_user.username == "testuser5"
    assert test_user.email == "testuser5@example.com"
    assert test_user.id is not None

def test_register_user(client, db_session, test_user):
    user_data = {
        "username" : "new username",
        "email" : "newtestemail@example.com",
        "password" : "newpasswordtoenter"
    }
    response = client.post(
        "/auth/register", json = user_data
    )

    assert response.status_code == 201
    data = response.json()

    existed_email = db_session.scalar(
        select(User).where(User.email == user_data["email"])
    )
    assert existed_email is not None

    correct_password = verify_password(user_data["password"] ,existed_email.hashed_password)

    assert correct_password is True
    assert data["username"] == "new username"
    assert data["email"] == "newtestemail@example.com"
    assert data["is_active"] is True

def test_registered_email(test_user, client):
    user_data = {
        "username" : "test_username",
        "email" : test_user.email,
        "password" : "some_text_hash"
    }
    response = client.post(
        "/auth/register", json = user_data
    )

    assert response.status_code == 409

def test_registered_username(test_user, client):
    user_data = {
        "username" : test_user.username,
        "email" : "usertest@example.com",
        "password" : "plain_password"
    }
    response = client.post("/auth/register", json = user_data)

    assert response.status_code == 409

def test_user_login(test_user, client):
    login_credentials = {
        "username" : test_user.username,
        "email" : test_user.email,
        "password" : "some_text_hash"
    }

    response = client.post("/auth/login", data = login_credentials)

    assert response.status_code == 200

    response_data = response.json()

    assert "access_token" in response_data
    assert response_data["token_type"] == 'bearer'

def test_invalid_login_username(client):
    login_credentials = {
        "username" : "random_username",
        "password" : "some_text_hash"
    }

    response = client.post("/auth/login", data = login_credentials)

    assert response.status_code == 401

def test_invalid_login_password(test_user, client):
    login_credentials = {
        "username" : test_user.username,
        "password" : "notvalidpassword"
    }

    response = client.post("/auth/login", data = login_credentials)

    assert response.status_code == 401
