FROM python:3.13-alpine

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN pip install --upgrade pip
RUN pip install --no-cache-dir pika python-dotenv

EXPOSE 5672

COPY . /code
COPY ../home_api/settings.py /code

CMD ["python3", "listen.py"]