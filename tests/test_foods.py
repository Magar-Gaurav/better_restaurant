from app.core.jwt import create_access_token
from app.core.security import hash_password
from app.models.food_model import User, Food
from sqlalchemy import select

def test_create_food(test_restaurant,test_user, client):

    food_data = {
        "name" : "Chicken Mo: Mo:",
        "description" : "Chicken amilo piro wala momo",
        "price" : 199.00,
        "restaurant_id" : test_restaurant.id,
        "category" : "Chicken"
    }
    
    token = create_access_token(
        data = {"sub" : test_user.username}
    )

    header = {
        "Authorization" : f"Bearer {token}"
    }

    response = client.post("/foods", headers = header, json = food_data)

    assert response.status_code == 201
    assert response.json()["name"] == food_data["name"]
    assert response.json()["description"] == food_data["description"]
    assert response.json()["price"] == food_data["price"]
    assert response.json()["category"] == food_data["category"]
    assert response.json()["restaurant_id"] == food_data["restaurant_id"]

def test_get_all_foods(test_user, test_food, client):
    token = create_access_token(
        data = {"sub" : test_user.username}
    )

    header = {
        "Authorization" : f"Bearer {token}"
    }

    response = client.get("/foods", headers = header)
    assert response.status_code == 200
    result = response.json()
    
    assert result == [{
        "id" : test_food.id,
        "name" : test_food.name,
        "category" : test_food.category,
        "description" : test_food.description,
        "price" : test_food.price,
        "restaurant_id" : test_food.restaurant_id
    }]

def test_get_food_by_id(test_food,test_user,client):
    token = create_access_token(
        data = {"sub" : test_user.username}
    )
    header = {
        "Authorization" : f"Bearer {token}"
    }
    response = client.get(f"/foods/{test_food.id}", headers = header)

    assert response.status_code == 200
    assert response.json()["id"] == test_food.id
    assert response.json()["name"] == test_food.name
    assert response.json()["restaurant_id"] == test_food.restaurant_id

def test_food_not_found(test_user, client):
    token = create_access_token(
        data = {"sub" : test_user.username}
    )

    header = {
        "Authorization" : f"Bearer {token}"
    }

    response = client.get("/foods/500", headers = header)

    assert response.status_code == 404
    assert response.json() == {'detail': 'No food data found with food_id 500'}

def test_unauthorized_access(test_food,db_session,client):
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
    header = {"Authorization" : f"Bearer {new_user_token}"}
    response = client.get(f"/foods/{test_food.id}", headers = header)
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"No food data found with food_id {test_food.id}"
    }

def test_update_food(test_food, test_user, client):
    updated_food_data = {
        "name" : "Chinese momo",
        "price" : 149.00
    }

    token = create_access_token(
        data = {"sub" : test_user.username}
    )

    header = {
        "Authorization" : f"Bearer {token}"
    }

    response = client.patch(f"/foods/{test_food.id}", headers = header, json = updated_food_data)

    assert response.status_code == 200
    assert response.json()["name"] == updated_food_data["name"]
    assert response.json()["price"] == updated_food_data["price"]

def test_update_food_not_found(test_user, client): 
    food_data  = {
        "name" : "Chinese momo",
        "price" : 149.00
    }
    token = create_access_token(
        data = {"sub" : test_user.username}
    )

    header = {
        "Authorization" : f"Bearer {token}"
    }

    response = client.patch("/foods/500", headers = header, json = food_data)

    assert response.status_code == 404
    assert response.json() == {"detail": f"No food data found with food_id 500"}

def test_unauthorized_food_update(test_food, db_session, client):
    food_data = {
        "name" : "Chinese momo",
        "price" : 149.00
    }
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
    header = {"Authorization" : f"Bearer {new_user_token}"}
    
    response = client.patch(f"/foods/{test_food.id}", headers = header, json = food_data)

    assert response.status_code == 404

def test_delete_food(test_food, test_user, client, db_session):
    token = create_access_token(
        data = {"sub" : test_user.username}
    )

    header = {
        "Authorization" : f"Bearer {token}"
    }

    response = client.delete(f"/foods/{test_food.id}", headers = header)

    assert response.status_code == 200
    assert response.json() == {"message" : f"successfully deleted food record of {test_food.id}"}

    statement = select(Food).where(Food.id == test_food.id)
    result = db_session.scalar(statement)

    assert result is None

def test_delete_food_not_found(test_user, client):
    token = create_access_token(
        data = {"sub" : test_user.username}
    )

    header = {
        "Authorization" : f"Bearer {token}"
    }

    response = client.delete("/foods/500", headers = header)

    assert response.status_code == 404
    assert response.json() == {
        "detail" : "No food data found with food_id 500"
    }

def test_unauthorized_food_delete(test_food,client, db_session):
    new_user = User(
        username = 'username test',
        email = 'usernametest@example.com',
        hashed_password = hash_password('new_hashed_password')
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    token = create_access_token(
        data = {"sub" : new_user.username}
    )
    header = {"Authorization" : f"Bearer {token}"}
    
    response = client.delete(f"/foods/{test_food.id}", headers = header)

    assert response.status_code == 404
    
    statement = select(Food).where(Food.id == test_food.id)
    result = db_session.scalar(statement)

    assert result is not None