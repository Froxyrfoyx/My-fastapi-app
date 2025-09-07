from typing import Callable # обьект который можно вызвать как функцию  
import time # чтобы засекать время сколько выполняется запрос 
from mainLaunch import app
from fastapi import Request # обьект который хранит всю информацию из  http  запроса 
import logging # для логирования 
from mainLaunch import app
 
logger = logging.getLogger("my_appLogger") #название логера 
logger.setLevel(logging.DEBUG) # уровень логера 
consoleHandler = logging.StreamHandler() # вывод логов в консоль 
consoleHandler.setLevel(logging.INFO) 
formate = logging.Formatter(
    "[%(asctime)s]  %(levelname)s - %(name)s  - %(message)s" 
) #формат лога здесь время , уровень , имя , сообщение 
consoleHandler.setFormatter(formate) # задаем такой формат хэндлеру  и логи будут выводится красиво в консоль 
logger.addHandler(consoleHandler) #  связываем логер и хэндлер 


@app.middleware("http") #глобальный миддлвар на все приложение, http  значит  что будет обрабатывать только запросы  http
async def logREQUESTS (request : Request , call_next: Callable):
    startTIME = time.perf_counter()
    logger.info(f"Запрос: {request.method} , {request.url} , {request.user}")
    response = await call_next(request)
    endTIME = time.time()
    execution = endTIME - startTIME
    logger.info(f"Конец запроса: {request.method} , {request.url}  статус запроса - {response.status_code} , время выполнения составило {execution}")
    return response

