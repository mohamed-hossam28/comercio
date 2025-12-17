import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import Base, get_db
import auth
from models.users import User
from models.products import Product
from controller import hash_password

TEST_DATABASE_URL = "sqlite:///./test_db.sqlite3"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def test_db() -> Generator:
    Base.metadata.create_all(bind=test_engine)
    
    yield test_engine
    
    Base.metadata.drop_all(bind=test_engine)
    
    auth._sessions.clear()


@pytest.fixture(scope="function")
def db_session(test_db) -> Generator[Session, None, None]:
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


def override_get_db(db_session: Session):
    def _override():
        try:
            yield db_session
        finally:
            pass
    return _override


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient: # dah wa7ed da5l 3ady m3ndosh mail asln fa asmo client
    
    app.dependency_overrides[get_db] = override_get_db(db_session)
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


# new data base implementation success and then start to add

@pytest.fixture(scope="function")
def sample_user(db_session: Session) -> User:
    user = User(
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        password=hash_password("TestPassword123"),
        dob="1990-01-01",
        sex="M",
        phone="+1234567890",
        country="USA"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def auth_token(sample_user: User) -> str:
    token = auth.create_session(sample_user.id)
    return token #token dah al bkml behb al byb2a feh al id bta3t al session deh w 2bd2l a test beh


@pytest.fixture(scope="function")
def authenticated_client(client: TestClient, auth_token: str) -> TestClient:
    client.cookies.set("session_token", auth_token)
    return client #dah keda al token b7ot 3leha al cookies w keda daha la by2b2a al client


@pytest.fixture(scope="function")
def sample_products(db_session: Session) -> list[Product]:
    products = [
        Product(
            name="Test Laptop",
            description="A test laptop for testing",
            price=999.99,
            image_url="http://example.com/laptop.jpg",
            category="electronics",
            stock_avilabilty=10
        ),
        Product(
            name="Test Phone",
            description="A test phone for testing",
            price=499.99,
            image_url="http://example.com/phone.jpg",
            category="electronics",
            stock_avilabilty=5
        ),
        Product(
            name="Test Shirt",
            description="A test shirt for testing",
            price=29.99,
            image_url="http://example.com/shirt.jpg",
            category="clothing",
            stock_avilabilty=20
        ),
        Product(
            name="Out of Stock Item",
            description="This item is out of stock",
            price=19.99,
            image_url="http://example.com/oos.jpg",
            category="clothing",
            stock_avilabilty=0
        ),
    ]
    
    for product in products:
        db_session.add(product)
    
    db_session.commit()
    
    for product in products:
        db_session.refresh(product)
    
    return products
    # b3d ma 5lst al conftest b2a m3ak session feha client bl cookies bt3to w 3mlt push ll products fel data base 
    # fa anta b2a m3ak virtual website b test 3leh nfs al functionallty al website al origin
