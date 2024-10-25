FROM python:3.10

ENV PYTHONBUFFERED=1

WORKDIR /var/team42_app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY start_prod.sh start_prod.sh
COPY django_marketplace .
