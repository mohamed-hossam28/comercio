import pytest
from sqlalchemy.orm import Session
from models.users import User
from models.products import Product
from models.order import OrderDetails, OrderItem


class TestDatabaseConnection:
    
    def test_database_session_is_valid(self, db_session: Session):
        assert db_session is not None
        assert isinstance(db_session, Session)
    
    def test_database_tables_exist(self, db_session: Session):
        try:
            db_session.query(User).first()
            db_session.query(Product).first()
            db_session.query(OrderDetails).first()
            db_session.query(OrderItem).first()
        except Exception as e:
            pytest.fail(f"Database tables not properly created: {e}")


class TestDatabaseCRUD:
    
    def test_create_user_in_database(self, db_session: Session):
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="hashed_password",
            dob="2000-01-01",
            sex="M",
            phone="1234567890",
            country="TestLand"
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.id is not None
        assert user.email == "test@example.com"
    
    def test_read_user_from_database(self, db_session: Session):
        user = User(
            first_name="Read",
            last_name="Test",
            email="read@example.com",
            password="hashed_password",
            dob="2000-01-01",
            sex="F",
            phone="1234567890",
            country="TestLand"
        )
        db_session.add(user)
        db_session.commit()
        
        retrieved_user = db_session.query(User).filter(User.email == "read@example.com").first()
        
        assert retrieved_user is not None
        assert retrieved_user.first_name == "Read"
        assert retrieved_user.last_name == "Test"
    
    def test_update_user_in_database(self, db_session: Session):
        user = User(
            first_name="Update",
            last_name="Test",
            email="update@example.com",
            password="hashed_password",
            dob="2000-01-01",
            sex="M",
            phone="1234567890",
            country="TestLand"
        )
        db_session.add(user)
        db_session.commit()
        
        user.first_name = "Updated"
        db_session.commit()
        
        retrieved_user = db_session.query(User).filter(User.email == "update@example.com").first()
        assert retrieved_user.first_name == "Updated"
    
    def test_delete_user_from_database(self, db_session: Session):
        user = User(
            first_name="Delete",
            last_name="Test",
            email="delete@example.com",
            password="hashed_password",
            dob="2000-01-01",
            sex="M",
            phone="1234567890",
            country="TestLand"
        )
        db_session.add(user)
        db_session.commit()
        user_id = user.id
        
        db_session.delete(user)
        db_session.commit()
        
        retrieved_user = db_session.query(User).filter(User.id == user_id).first()
        assert retrieved_user is None
    
    def test_create_product_in_database(self, db_session: Session):
        product = Product(
            name="Test Product",
            description="A test product",
            price=99.99,
            image_url="http://example.com/image.jpg",
            category="test",
            stock_avilabilty=50
        )
        
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        assert product.id is not None
        assert product.name == "Test Product"
        assert product.price == 99.99
    
class TestDatabaseRelationships:
    def test_order_user_relationship(self, db_session: Session, sample_user: User):
        order = OrderDetails(
            user_id=sample_user.id,
            total_price=100.00
        )
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)
        
        assert order.user_id == sample_user.id
    
    def test_order_items_relationship(self, db_session: Session, sample_user: User, sample_products: list[Product]):
        order = OrderDetails(
            user_id=sample_user.id,
            total_price=0
        )
        db_session.add(order)
        db_session.flush()
        
        product = sample_products[0]
        order_item = OrderItem(
            order_details_id=order.id,
            product_id=product.id,
            product_name=product.name,
            price=product.price,
            quantity=2
        )
        db_session.add(order_item)
        db_session.commit()
        
        db_session.refresh(order)
        assert len(order.items) == 1
        assert order.items[0].product_name == product.name
