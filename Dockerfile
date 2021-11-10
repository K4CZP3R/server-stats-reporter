FROM python:3.7

WORKDIR /app

RUN pip install psutil

COPY main.py .

RUN mkdir database

CMD ["python", "main.py"]