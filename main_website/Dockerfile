FROM python:3
 
WORKDIR /app
 
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
 
COPY . .
 
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# docker run -d -p 8000:8000 -v $(pwd):/app test1:latest