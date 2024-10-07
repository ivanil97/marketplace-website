FROM python:3.10

ENV PYTHONBUFFERED=1

WORKDIR /var/team42_app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY django_marketplace .

RUN ["python", "manage.py", "collectstatic", "--noinput"]
