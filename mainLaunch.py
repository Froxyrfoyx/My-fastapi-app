from fastapi import FastAPI
from servers import router as server_router  
from auth  import router as AuthRout
from database import router3 as DBrouter


app = FastAPI(title= "inf eye 3000" , description="мой апишник") #главное приложение и описание
app.include_router(server_router,prefix = "/servers" , tags = ["servers"]) # маршруты будут доступны по пути /servers
app.include_router(AuthRout, prefix="/auth" , tags= ["auth"])
app.include_router(DBrouter , prefix="/database" , tags=["database"])

@app.get("/")
async def root():
    return {"succes": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0" , port=8000)