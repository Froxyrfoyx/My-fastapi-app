FROM python:3.13.5
WORKDIR /work 
COPY . /work
RUN pip install -r requirements.txt
CMD [ "python", "mainLaunch.py"]




