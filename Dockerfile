FROM python:3.10-slim-buster

RUN pip install poetry gunicorn

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV DEBUG=false
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && pip3 install django-environ 

COPY . .

# CMD ["gunicorn", "--bind", ":8080", "--workers", "3", "manage.wsgi:application"]