import pytest
from fastapi.testclient import TestClient
from models.products import Product
from models.order import OrderDetails, OrderItem
from sqlalchemy.orm import Session


class TestCheckoutEndpoint:    
    def test_checkout_requires_authentication(self, client: TestClient, sample_products: list[Product]):
        checkout_data = {
            "user_id": 999, # The user is not authenticated
            "items": [
                {
                    "product_name": sample_products[0].name,
                    "product_id": sample_products[0].id,
                    "price": sample_products[0].price,
                    "quantity": 1
                }
            ]
        }
        
        response = client.post("/order/checkout", json=checkout_data)
        
        assert response.status_code == 401
        data = response.json()
        assert "must be logged in" in data["message"].lower()
    
    def test_checkout_successful_with_single_item(
        self, 
        authenticated_client: TestClient, 
        sample_products: list[Product],
        db_session: Session
    ):
        product = sample_products[0]
        original_stock = product.stock_avilabilty
        
        checkout_data = {
            "user_id": 1,# Valid user id authenticated user
            "items": [
                {
                    "product_name": product.name,
                    "product_id": product.id,
                    "price": product.price,
                    "quantity": 2
                }
            ]
        }
        
        response = authenticated_client.post("/order/checkout", json=checkout_data)
        
        assert response.status_code == 200 #ok
        data = response.json()
        assert "successfully" in data["message"].lower()
        assert "order_details_id" in data
        assert data["total"] == product.price * 2
        
        db_session.refresh(product)
        assert product.stock_avilabilty == original_stock - 2
    
    def test_checkout_successful_with_multiple_items(
        self,
        authenticated_client: TestClient,
        sample_products: list[Product],
        db_session: Session
    ):
        product1 = sample_products[0]
        product2 = sample_products[1]
        
        original_stock1 = product1.stock_avilabilty
        original_stock2 = product2.stock_avilabilty
        
        checkout_data = {
            "user_id": 1,
            "items": [
                {
                    "product_name": product1.name,
                    "product_id": product1.id,
                    "price": product1.price,
                    "quantity": 1
                },
                {
                    "product_name": product2.name,
                    "product_id": product2.id,
                    "price": product2.price,
                    "quantity": 3
                }
            ]
        }
        
        response = authenticated_client.post("/order/checkout", json=checkout_data)
        
        assert response.status_code == 200
        data = response.json()
        
        expected_total = (product1.price * 1) + (product2.price * 3)
        assert data["total"] == expected_total
        
        db_session.refresh(product1)
        db_session.refresh(product2)
        assert product1.stock_avilabilty == original_stock1 - 1
        assert product2.stock_avilabilty == original_stock2 - 3
    
    def test_checkout_creates_order_details(
        self,
        authenticated_client: TestClient,
        sample_products: list[Product],
        sample_user,
        db_session: Session
    ):
        product = sample_products[0]
        
        checkout_data = {
            "user_id": 1,
            "items": [
                {
                    "product_name": product.name,
                    "product_id": product.id,
                    "price": product.price,
                    "quantity": 1
                }
            ]
        }
        
        response = authenticated_client.post("/order/checkout", json=checkout_data)
        
        assert response.status_code == 200
        order_id = response.json()["order_details_id"]
        
        order = db_session.query(OrderDetails).filter(OrderDetails.id == order_id).first()
        assert order is not None
        assert order.user_id == sample_user.id
        assert order.total_price == product.price
    
    def test_checkout_creates_order_items(
        self,
        authenticated_client: TestClient,
        sample_products: list[Product],
        db_session: Session
    ):
        product = sample_products[0]
        
        checkout_data = {
            "user_id": 1,
            "items": [
                {
                    "product_name": product.name,
                    "product_id": product.id,
                    "price": product.price,
                    "quantity": 2
                }
            ]
        }
        
        response = authenticated_client.post("/order/checkout", json=checkout_data)
        
        assert response.status_code == 200 #ok
        order_id = response.json()["order_details_id"]
        
        order_items = db_session.query(OrderItem).filter(
            OrderItem.order_details_id == order_id
        ).all()
        
        assert len(order_items) == 1
        assert order_items[0].product_id == product.id
        assert order_items[0].quantity == 2
    
    def test_checkout_insufficient_stock_fails(
        self,
        authenticated_client: TestClient,
        sample_products: list[Product],
        db_session: Session
    ):
        product = sample_products[1]  # Has stock of 5
        original_stock = product.stock_avilabilty
        
        checkout_data = {
            "user_id": 1,
            "items": [
                {
                    "product_name": product.name,
                    "product_id": product.id,
                    "price": product.price,
                    "quantity": 10  # More than available
                }
            ]
        }
        
        response = authenticated_client.post("/order/checkout", json=checkout_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "insufficient stock" in data["detail"].lower()
        
        db_session.refresh(product)
        assert product.stock_avilabilty == original_stock
    
    def test_checkout_nonexistent_product_fails(
        self,
        authenticated_client: TestClient
    ):
        checkout_data = {
            "user_id": 1,
            "items": [
                {
                    "product_name": "Nonexistent Product",
                    "product_id": 99999,
                    "price": 100.00,
                    "quantity": 1
                }
            ]
        }
        
        response = authenticated_client.post("/order/checkout", json=checkout_data)
        
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_checkout_out_of_stock_product_fails(
        self,
        authenticated_client: TestClient,
        sample_products: list[Product]
    ):
        out_of_stock = next(p for p in sample_products if p.stock_avilabilty == 0)
        
        checkout_data = {
            "user_id": 1,
            "items": [
                {
                    "product_name": out_of_stock.name,
                    "product_id": out_of_stock.id,
                    "price": out_of_stock.price,
                    "quantity": 1
                }
            ]
        }
        
        response = authenticated_client.post("/order/checkout", json=checkout_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "insufficient stock" in data["detail"].lower()
    
class TestInventoryManagement: # Failed
    def test_inventory_not_reduced_on_validation_failure(
        self,
        authenticated_client: TestClient,
        sample_products: list[Product],
        db_session: Session
    ):
        product1 = sample_products[0]
        product2 = sample_products[1]
        
        stock1_before = product1.stock_avilabilty
        stock2_before = product2.stock_avilabilty
        
        checkout_data = {
            "user_id": 1,
            "items": [
                {
                    "product_name": product1.name,
                    "product_id": product1.id,
                    "price": product1.price,
                    "quantity": 1
                },
                {
                    "product_name": product2.name,
                    "product_id": product2.id,
                    "price": product2.price,
                    "quantity": 100  
                }
            ]
        }
        
        response = authenticated_client.post("/order/checkout", json=checkout_data)
        assert response.status_code == 400
        db_session.refresh(product1)
        db_session.refresh(product2)
        
        assert product1.stock_avilabilty == stock1_before
        assert product2.stock_avilabilty == stock2_before
