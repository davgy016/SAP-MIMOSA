from fastapi.testclient import TestClient
from WebApp.app import app

client = TestClient(app)

def test_validation_route_is_up_and_uses_stub():
    payload = [
      {
        "mapID": "stub",
        "LLMType": "gpt-4o",
        "mappings": []
      }
    ]
    resp = client.post("/check_accuracy", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    # since ScoreManager.scoreOutput returns 0.42, accuracy_score should be 42.0
    assert data["accuracy_score"] == round(0.42 * 100, 2)
    # quality_score & matching_score are hardcoded in the handler
    assert "quality_score" in data
    assert "matching_score" in data
