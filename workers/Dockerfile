FROM python:3.12-alpine

WORKDIR /code

RUN pip install --no-cache-dir pika python-dotenv

EXPOSE 5672

COPY . /code

CMD ["python3", "listen.py"]