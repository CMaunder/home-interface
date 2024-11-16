FROM python:3.12-alpine

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY . /code

EXPOSE 8000

RUN python3 manage.py collectstatic
RUN python3 manage.py migrate


CMD ["gunicorn", "--config", "gunicorn_config.py", "home_api.wsgi:application"]