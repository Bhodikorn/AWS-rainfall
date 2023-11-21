FROM ubuntu:22.04

WORKDIR /main-website

COPY . .

RUN apt-get update

RUN apt install python3.10 -y

RUN apt install python3-pip -y

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
