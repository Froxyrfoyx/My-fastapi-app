from fastapi import HTTPException, APIRouter , Response
from security import  cipher
from models import UserCreate ,  UserLogin , UserModel
from database import SessionDepends
from  sqlalchemy.future import select
from security import Security_AUTH , config
router = APIRouter()
@router.post("/register/")
async def register( session: SessionDepends , uc: UserCreate  ):
     check = select(UserModel).where(UserModel.username == uc.username )
     request = await session.execute(check)
     result = request.scalars().first()
     if  result:
         raise HTTPException(status_code= 406 , detail= "the user already exists")
     new_user = UserModel(username = uc.username , password = uc.password)
     session.add(new_user)
     await session.commit()
     
     return {"succes": new_user.username}

@router.post("/login/")
async def login(  session: SessionDepends,  login:UserLogin  , response : Response):
     check = select(UserModel).where(UserModel.username == login.username)
     request = await session.execute(check)
     result = request.scalars().first()
     if not result:
         raise HTTPException(status_code= 404 , detail="User not found")
     if not cipher.verify(login.password , result.password ):
         raise HTTPException(status_code=401 , detail= "Invalid password")
     acces_token = Security_AUTH.create_access_token( uid ="2342342352135235")
     response.set_cookie(config.JWT_ACCESS_COOKIE_NAME , acces_token)
     
     return{"succes": True ,  "AccesToken": acces_token }

  
    




