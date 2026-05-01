from fastapi.testclient import TestClient
from main import app
import io

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "up"}

def test_extract_receipt_endpoint():
    # Create fake image bytes
    fake_image = io.BytesIO(b"fake_image_data_simulating_receipt")
    
    # The endpoint expects 'file'
    response = client.post(
        "/api/v1/ocr/extract",
        files={"file": ("receipt.jpg", fake_image, "image/jpeg")}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # The dummy NLP engine is expected to return these values
    assert data["supplier_name"] == "Aliou Glace"
    assert data["total_amount"] == 15000.0
    assert data["currency"] == "FCFA"
    assert data["category"] == "GLACE"
    assert data["confidence_score"] == 0.92
