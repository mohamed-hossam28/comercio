

import pytest
from fastapi.testclient import TestClient
from models.products import Product

class TestSearchProducts:
    
    def test_search_products_by_name(self, client: TestClient, sample_products: list[Product]):
        response = client.get("/products/search?q=laptop")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        assert len(data) > 0
        assert any("laptop" in p["name"].lower() for p in data)
    
    def test_search_products_case_insensitive(self, client: TestClient, sample_products: list[Product]):
        response_lower = client.get("/products/search?q=laptop")
        response_upper = client.get("/products/search?q=LAPTOP")
        response_mixed = client.get("/products/search?q=LaPtOp")
        
        assert response_lower.status_code == 200
        assert response_upper.status_code == 200
        assert response_mixed.status_code == 200
        
        data_lower = response_lower.json()
        data_upper = response_upper.json()
        data_mixed = response_mixed.json()
        
        assert len(data_lower) == len(data_upper) == len(data_mixed)
    
    def test_search_products_partial_match(self, client: TestClient, sample_products: list[Product]):
        response = client.get("/products/search?q=test")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) >= 2 
    
    def test_search_products_no_results(self, client: TestClient, sample_products: list[Product]):
        response = client.get("/products/search?q=nonexistentproduct12345")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_search_products_empty_query(self, client: TestClient, sample_products: list[Product]):
        response = client.get("/products/search?q=")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

