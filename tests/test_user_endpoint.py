import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_register_user(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        })
        assert response.status_code == 200
        assert "user_id" in response.json()


@pytest.mark.asyncio
async def test_authenticate_user(test_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login", data={
            "username": "testuser",
            "password": "testpassword"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
