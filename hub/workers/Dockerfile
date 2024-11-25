FROM python:3.13-alpine

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

COPY requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5672

COPY workers/. /code/workers/
COPY /home_api/. /code/home_api/
COPY /monitoring/. /code/monitoring/

CMD ["python3", "workers/listen.py"]