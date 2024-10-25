FROM python:3.10

ENV PYTHONBUFFERED=1

ENV APP_HOME=/var/team42_app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY start_prod.sh start_prod.sh
RUN chmod +x /var/team42_app/start_prod.sh
COPY django_marketplace .
