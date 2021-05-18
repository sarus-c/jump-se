# Dockerfile, Image, Container
FROM python:3.9

WORKDIR /jump-services

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "index.py"]