from sqlalchemy.ext.asyncio import create_async_engine  , async_sessionmaker, AsyncSession
from fastapi import APIRouter , Depends
from typing import Annotated
from models import Base

# Асинхронный движок и асинхронные сессии для общения с бд  
engine = create_async_engine('sqlite+aiosqlite:///MainData.db')
FabricSession = async_sessionmaker(engine, expire_on_commit=False) # данныее  после комита не устаревают и можно их дальше читать без повторного запроса

router3 = APIRouter()

async def GetSession(): # функция генератор для работы с сессией базы 
    async with FabricSession() as session:
        yield session 




@router3.post("/setupDataBase")
async def setupDataBase():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    return {"status": "succes"}




SessionDepends = Annotated[AsyncSession , Depends(GetSession)] # зависимость с генератором сеси1













