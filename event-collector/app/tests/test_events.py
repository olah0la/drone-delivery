import pytest

@pytest.mark.asyncio
async def test_create_event(client):
    delivery_id = "some-id"
    payload = {
        "type": "TAKEN_OFF",
        "timestamp": "2025-06-24T12:00:00Z"
    }
    response = await client.post(f"/deliveries/{delivery_id}/events", json=payload)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_delivery_events(client):
    delivery_id = "some-id"
    response = await client.get(f"/deliveries/{delivery_id}/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

