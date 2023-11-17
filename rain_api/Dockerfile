FROM ubuntu:latest

WORKDIR /rain-api

COPY requirements.txt requirements.txt

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    file \
    git

RUN apt-get install -y python3 python3-pip

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"
ENV PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:$PATH"

RUN pip install -r requirements.txt

EXPOSE 8001
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]
