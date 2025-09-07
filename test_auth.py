import pytest
from httpx import AsyncClient, ASGITransport #симулируем запросы не поднимая сервер 

from security import JwtToken

from mainLaunch import app

transport = ASGITransport(app=app)
@pytest.mark.asyncio 
async def test_register_user():
    async with AsyncClient(transport=transport , base_url="http://test" ) as acync_client:
        payload = {"username": "Froxy" , "password": "topsecretpassword66666"}
        print("Payload:" , payload)
        response = await acync_client.post("/auth/register/" , json=payload)
        
        
        assert response.status_code == 200

        
