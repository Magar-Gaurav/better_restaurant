import pytest

from main import app
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from configs.config import TEST_DATABASE_URL
from app.models.food_model import User, Restaurant, Food
from app.database import get_session
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from app.core.security import hash_password

engine = create_engine(TEST_DATABASE_URL, echo = True)
TestingSessionLocal = sessionmaker(bind = engine, autoflush = False, autocommit = False)

@pytest.fixture
def db_connection(apply_migrations):
    connection = engine.connect()
    transaction = connection.begin()
    try:
        yield connection
    finally:
        transaction.rollback()
        connection.close()

@pytest.fixture
def db_session(db_connection):
    session = TestingSessionLocal(
        bind = db_connection, join_transaction_mode = "create_savepoint"
    )
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):
    def override_get_session():
        yield db_session
    try:
        app.dependency_overrides[get_session] = override_get_session
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()

@pytest.fixture( scope= "session",autouse = True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

@pytest.fixture
def test_user(db_session):
    new_user = User(
        username = 'testuser5',
        email = 'testuser5@example.com',
        hashed_password = hash_password('some_text_hash')
    )

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user

@pytest.fixture
def test_restaurant(test_user, db_session):
    new_restaurant = Restaurant(
        name = "Test Restaurant",
        location = "Kathmandu",
        owner_id = test_user.id
    )

    db_session.add(new_restaurant)
    db_session.commit()
    db_session.refresh(new_restaurant)
    return new_restaurant

@pytest.fixture
def test_food(test_restaurant, db_session):
    new_food = Food(
        name = "Test food",
        description = "Test food description",
        price = 199,
        category = "Test category",
        restaurant_id = test_restaurant.id
    )

    db_session.add(new_food)
    db_session.commit()
    db_session.refresh(new_food)
    return new_food