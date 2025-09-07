from pydantic import  BaseModel, Field , model_validator
from typing import Optional
from sqlalchemy.orm import DeclarativeBase , Mapped , mapped_column
import uuid
from sqlalchemy import String, Text

class ServerCreate(BaseModel): # входящие данные 
    ip : str =Field(...,example="192.168.1.1" ) #обязательно поле 
    description:str = Field(..., example= "Основной VPN")
    location : str = Field(..., example="Unites States")
    status : str = Field(..., example= "unknown") 


class ServerRead(BaseModel): #чтение данных
    id : str
    status: str
    location : str
    description : str
    ip : str


class ServerUpdate(BaseModel): # частичное обновление сервера
    description: Optional[str] = None
    location: Optional[str]  = None
    status: Optional[str] = "unknown"



class ServerFullUpdate(BaseModel): #полное обновление сервера   
     ip : str = Field(..., example="192.168.1.1")
     description: str = Field(..., example= "VPN")
     location : str = Field(..., example= "United States")
     status : str = Field(..., example= "online")

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(... , min_length= 10 )

    @model_validator(mode = "before") # валидатор для пароля нужен чтобы автоматически хэшировать пароль  и заменить  его в обьекте модели
    def hashed(cls , value:dict) -> dict:
     if isinstance(value, dict): #cls  модель UserCreate  pydantic  передает ее автоматически без нее не будет работать
        from security import cipher # локальный импорт чтобы не создавался цикличный импорт 
        password = value.get("password")
        if password is None:
            return value
        if not isinstance(password, str):
            raise TypeError(f"password is not string {type(password)}" )
        value["password"] = cipher.hash(password) 
        return value                                      


 
class UserLogin(BaseModel):
    username:str
    password:str

class Base(DeclarativeBase): # для создания моделей базы данных 
    pass


class ServerModel(Base):
    __tablename__ = "servers" #таблица в базе данных
    ip: Mapped[str] #mapped  нужен чтобы указать что это колонка таблицы  а не обычная переменная 
    id: Mapped[str] = mapped_column(primary_key= True , default= lambda: str(uuid.uuid4())) # айди первичный ключ для таблицы 
    description: Mapped[str]
    location : Mapped[str]
    status : Mapped[str]


class UserModel(Base):
    __tablename__ = "users"
    username : Mapped[str] = mapped_column(String,unique= True , nullable= False) #unique в бд не может хранится дв пользователя с одинаковым юсернеймом, nullable False  значение обязательно и не может быть Null 
    password : Mapped[str] = mapped_column(Text,nullable= False)
    id: Mapped[str] = mapped_column(primary_key= True , default=  lambda: str(uuid.uuid4()))
    