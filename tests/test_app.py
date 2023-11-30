import pytest
from app import app, socketio, drivers_collection
from unittest.mock import patch

@pytest.fixture
def test_client():
    client = socketio.test_client(app)
    yield client
    client.disconnect()

def test_index_route():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_update_location_socket(test_client):
    driver_id = str(drivers_collection.find_one()["_id"])

    data = {
        "id": driver_id,
        "lat": 35.0,
        "lon": -120.0
    }

    test_client.emit('update_location', data)
    received = test_client.get_received()
    assert len(received) == 1
    print(received)
    assert received[0]['name'] == 'update_location_success'  # Assuming you emit a message event on update_location

def test_find_drivers_socket(test_client):
    data = {
        "lat": 40.7128,  # New York City coordinates
        "lon": -74.006,
        "scan_distance": 10000
    }

    test_client.emit('find_drivers', data)
    received = test_client.get_received()
    assert len(received) == 1
    assert received[0]['name'] == 'nearby_drivers'