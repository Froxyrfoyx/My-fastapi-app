
from fastapi import APIRouter, Depends , HTTPException#обработка ошибок и зависимости 
from sqlalchemy.future  import select
from datetime import time
from models import ServerCreate, ServerRead, ServerUpdate, ServerFullUpdate, ServerModel, UserCreate 

from database import  SessionDepends
from security import Security_AUTH
import asyncio





router = APIRouter() #для создания маршрутов 





@router.get("/servers/" ,  response_model=list[ServerRead] , dependencies=[Depends(Security_AUTH.access_token_required)]) #все ссервера 
async def get_all_servers(  session: SessionDepends ):
    result = await session.execute(select(ServerModel)) #асинхроныый запрос к бд где получаем сервер из нашей ОРМ модели 
    server = result.scalars().all() #Возвращаем только обьекты в виде списка все остальное отсекаем через scalar 

    return server



@router.post ("/servers/" , dependencies=[Depends(Security_AUTH.access_token_required)])
async def create_server(session: SessionDepends ,server:ServerCreate): #создаем сервер
 
  new_server = ServerModel( description = server.description , location = server.location , ip = server.ip , status = server.status) 
  session.add(new_server)
  await session.commit()
  await session.refresh(new_server) # подтягиваем актуальные данные из бд на всякий случай 
  return {"succes": new_server}

@router.get ("/servers/{server_id}", response_model=ServerRead, dependencies=[Depends(Security_AUTH.access_token_required)]) #поиск по айди
async def read_server_id( session: SessionDepends , server_id: str  ):
    
    search = select(ServerModel).where(ServerModel.id == server_id)
    request = await session.execute(search)
    serverResult = request.scalar()
    if not serverResult:
        raise HTTPException(status_code=404 , detail="server not found")    
    return serverResult

@router.delete("/servers/{server_id}" , dependencies=[Depends(Security_AUTH.access_token_required)]) #удаляем сервер
async def delete_the_server( session: SessionDepends, server_id: str ):
    check = select(ServerModel).where(ServerModel.id == server_id)
    result = await session.execute(check)
    clear = result.scalars().first()
    if not clear:
        raise HTTPException(status_code=404 , detail="Server not found")
    
    
    await session.delete(clear)

    await session.commit()
    return {"succes": f"{server_id} was removed" }
  
  
      
      
        
@router.patch("/server/{server_id}" , dependencies=[Depends(Security_AUTH.access_token_required)]) #частичное обновление данных
async def update_the_server(session: SessionDepends  ,server_update:ServerUpdate, server_id:str):
    search =select(ServerModel).where(ServerModel.id == server_id)
    request = await session.execute(search)
    serverResult = request.scalars().first()
    if not serverResult:
        raise HTTPException(status_code=404 , detail="server not found")  
    update = server_update.dict(exclude_unset= True) #обновляем в словаре только те поля который дал пользователь 
    for key,value in update.items(): #items() для удобного перебора 
        setattr(serverResult , key.lower() , value) # задает атрибуты динамически  .lower() чтобы совпадало с атрибутом модели 
    await session.commit()
    await session.refresh(serverResult)
    return {"succes": serverResult}

@router.put("/server/{server_id}" , dependencies=[Depends(Security_AUTH.access_token_required)]) # полное обновление сервера 
async def full_update( session: SessionDepends ,server_full_update:ServerFullUpdate , server_id: str  ):
    search =select(ServerModel).where(ServerModel.id == server_id)
    request = await session.execute(search)
    serverResult = request.scalars().first()
    if not serverResult:
        raise HTTPException(status_code=404 , detail="server not found")
    updateDATA = server_full_update.dict() #обновляем все
    for key,value in updateDATA.items():
        setattr(serverResult , key.lower(), value)
    await session.commit()    
    await session.refresh(serverResult)
    return{"succes": serverResult}
        


@router.get("/server/{server_ip}" , dependencies=[Depends(Security_AUTH.access_token_required)]) #пинг сервера через сокет
async def ping_server( session: SessionDepends , server_ip: str ):
    search = select(ServerModel).where(ServerModel.ip == server_ip)
    request = await session.execute(search)
    serverResult = request.scalars().first()

    if not serverResult:
        raise HTTPException(status_code=404 , detail= "server not found")
        
    serverIP = serverResult.ip

    try:                                                        
        reader,writer =  await asyncio.open_connection(serverIP , 8000) #отдает два значения для чтения и записи  мы ничего не читаем поэтому используем только запись 
        setattr(serverResult , "status" , "online")
        writer.close()
        await writer.wait_closed() #ждем пока закроется коннект 
            
            
    except Exception as e:
        print(e) # корректная обработка ошибок для подключения 
        setattr(serverResult , "status" , "offline")
    await session.commit()
    await session.refresh(serverResult)
    return {"ip": serverIP , "status": serverResult.status}
    
       
  
            
@router.get("/server/status/{server_status}", response_model=list[ServerRead] , dependencies=[Depends(Security_AUTH.access_token_required)]) #ищем сервер по статусу
async def search_status(  session: SessionDepends ,  server_status:str ):
    search = select(ServerModel).where(ServerModel.status == server_status)
    request = await session.execute(search)
    StatusResult = request.scalars().all()
    if not StatusResult:
        raise HTTPException(status_code=404 , detail= "unknown status ")
    return StatusResult



            
    



