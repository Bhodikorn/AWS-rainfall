FROM ubuntu:22.04

WORKDIR /rain-api

COPY . .

RUN apt-get update

RUN apt install python3.10 -y

RUN apt install python3-pip -y

RUN apt-get install -y gdal-bin python3-gdal

RUN pip3 install -r requirements.txt

EXPOSE 8001

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]
