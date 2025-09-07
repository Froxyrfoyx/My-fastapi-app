from passlib.context import CryptContext # для хэширования паролей 
from jose import  jwt, JWTError #токены
from models import UserCreate , UserModel  
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException 
from fastapi.security import OAuth2PasswordBearer
from authx import AuthX , AuthXConfig

ouath2 = OAuth2PasswordBearer(tokenUrl="login") # берем токен из заголовка 

cipher  = CryptContext(schemes=["bcrypt"], deprecated= "auto") #хэширование паролей по алгоритму bcrypt

config = AuthXConfig()
config.JWT_SECRET_KEY = "swfeuhgi9pfgw9dvobnw9oey0y)*WYFE()_HE_8eyu-rghw0hewg0e8wu7tg02w9ejhgo0i8wheoghw0eg_##poeirgjeobnvoenorvheorh"
config.JWT_COOKIE_CSRF_PROTECT = False
config.JWT_ACCESS_COOKIE_NAME = "accestoken"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_TOKEN_EXPIRES 

Security_AUTH = AuthX(config=config)




