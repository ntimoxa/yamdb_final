FROM python:3.8.5

LABEL author='Ntimoxa' version=1 broken_keyboards=0

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
