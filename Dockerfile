# Dockerfile, Image, Container
FROM python:3.9

WORKDIR /jump-services

COPY . .

RUN pip install -r requirements.txt

ENV SERVER_PORT=8080
ENV SERVER_URL=0.0.0.0
ENV API_ITEMS=https://jumpbe.cert.cfapps.eu10.hana.ondemand.com/api/items/create

CMD [ "python", "index.py"]