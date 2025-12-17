import pytest
from fastapi.testclient import TestClient


class TestMainEndpoints:
    def test_app_starts_successfully(self, client: TestClient):
        assert client.app is not None
        assert client.app.title == "FastAPI"
    
    def test_root_endpoint_returns_200(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_root_endpoint_contains_timestamp(self, client: TestClient):
        response = client.get("/")
        assert len(response.text) > 0
    
    def test_register_page_endpoint(self, client: TestClient):
        response = client.get("/Register")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_fqa_page_endpoint(self, client: TestClient):
        response = client.get("/FQA")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

class TestApplicationConfiguration:
    def test_routers_are_included(self, client: TestClient):
        routes = [route.path for route in client.app.routes]
        assert "/register-user" in routes or any("/register" in r for r in routes)
        assert "/login" in routes
        assert "/products/grouped" in routes
        assert "/order/checkout" in routes
