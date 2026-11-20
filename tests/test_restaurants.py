from app.core.jwt import create_access_token
from app.models.food_model import User, Restaurant
from app.core.security import hash_password
from sqlalchemy import select
def test_create_restaurant(test_user, client):
    restaurant_data = {
        "name" : "Test Restaurant",
        "location" : "Test location"
    }

    token = create_access_token(
        data = {"sub" : test_user.username}
    )

    response = client.post("/restaurant",json = restaurant_data, headers = {"Authorization" : f"Bearer {token}"})
    data = response.json()

    assert response.status_code == 201
    assert data["name"] == "Test Restaurant"
    assert data["location"] == "Test location"
    assert data["owner_id"] == test_user.id

def test_get_all_restaurants(test_restaurant, test_user, client):
    token = create_access_token(data = {"sub" : test_user.username})

    response = client.get("/restaurant", headers = {"Authorization" : f"Bearer {token}"})
    data = response.json()

    assert response.status_code == 200
    assert len(data) >= 1
    assert data == [{
        'id': test_restaurant.id,
        'name': 'Test Restaurant', 'location': 'Kathmandu',
        'owner_id': test_user.id
    }]

def test_get_restaurant_by_id(test_restaurant, test_user, client):
    token = create_access_token(
        data = {"sub" : test_user.username}
    )
    
    response = client.get(f"/restaurant/{test_restaurant.id}", headers = {"Authorization" : f"Bearer {token}"})
    assert response.status_code == 200

    assert response.json() == {
        'id': test_restaurant.id,
        'name': 'Test Restaurant', 'location': 'Kathmandu',
        'foods': []
    }

def test_unauthorized_access(test_user,test_restaurant,db_session, client):
    new_user = User(
        username = 'username test',
        email = 'usernametest@example.com',
        hashed_password = hash_password('new_hashed_password')
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    new_user_token = create_access_token(
        data = {"sub" : new_user.username}
    )

    response = client.get(f"/restaurant/{test_restaurant.id}", headers = {"Authorization" : f"Bearer {new_user_token}"})

    assert response.status_code == 404

def test_restaurant_not_found(test_user, client):
    token = create_access_token(
        data = {"sub" : test_user.username}
    )
    response = client.get("/restaurant/500", headers = {"Authorization" : f"Bearer {token}"})

    assert response.status_code == 404

def test_update_restaurant(test_user, test_restaurant, client):
    token = create_access_token(
        data = {"sub" : test_user.username}
    )
    new_restaurant_data = {
        "name" : "My new Restaurant",
        "location" : "Restaurant_location_unidentified"
    }

    response = client.patch(f"/restaurant/{test_restaurant.id}",json = new_restaurant_data, headers = {"Authorization" : f"Bearer {token}"})

    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "My new Restaurant"
    assert data["location"] == "Restaurant_location_unidentified"

def test_update_restaurant_not_found(test_user, client):
    token = create_access_token(
        data = {"sub" : test_user.username}
    )
    new_restaurant_data = {
        "name" : "My new Restaurant",
        "location" : "Restaurant_location_unidentified"
    }

    response = client.patch("/restaurant/500", json = new_restaurant_data,headers = {"Authorization" : f"Bearer {token}"})

    assert response.status_code == 404

def test_unauthorized_update_restaurant(test_restaurant,client, db_session):
    new_user = User(
        username = 'username test',
        email = 'usernametest@example.com',
        hashed_password = hash_password('new_hashed_password')
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    new_user_token = create_access_token(
        data = {"sub" : new_user.username}
    )

    new_restaurant_data = {
        "name" : "My new Restaurant",
        "location" : "Restaurant_location_unidentified"
    }

    response = client.patch(f"/restaurant/{test_restaurant.id}", headers = {"Authorization" : f"Bearer {new_user_token}"}, json = new_restaurant_data)

    assert response.status_code == 404

def test_delete_restaurant(test_restaurant, test_user,db_session, client):
    token = create_access_token(
        data = {"sub" : test_user.username}
    )
    response = client.delete(f"/restaurant/{test_restaurant.id}", headers = {"Authorization" : f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {"message" : f"Successfully deleted the record of restaurant number {test_restaurant.id}"}

    deleted_restaurant = db_session.scalar(select(Restaurant).where(Restaurant.id == test_restaurant.id))
    assert deleted_restaurant is None

def test_restaurant_not_exists(test_user, client):
    token = create_access_token(
        data = {"sub" : test_user.username}
    )
    response = client.delete("/restaurant/500", headers = {"Authorization" : f"Bearer {token}"})

    assert response.status_code == 404

def test_delete_authorize(test_user, test_restaurant,db_session, client):
    new_user = User(
        username = 'username test',
        email = 'usernametest@example.com',
        hashed_password = hash_password('new_hashed_password')
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    new_user_token = create_access_token(
        data = {"sub" : new_user.username}
    )
    response = client.delete(f"/restaurant/{test_restaurant.id}", headers = {"Authorization" : f"Bearer {new_user_token}"})

    assert response.status_code == 404

    remaining_database = db_session.scalar(select(Restaurant).where(Restaurant.id == test_restaurant.id))
    assert remaining_database is not None