FROM python:3.10

ENV PYTHONBUFFERED=1

ENV APP_HOME=/var/team42_app
RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/staticfiles
RUN mkdir -p $APP_HOME/mediafiles
RUN mkdir -p $APP_HOME/import
RUN mkdir -p $APP_HOME/fixtures
WORKDIR $APP_HOME

RUN apt update
RUN apt install gettext -y

#COPY requirements.txt requirements.txt
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
RUN pip install --upgrade pip "poetry==1.8.2"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY start_prod.sh start_prod.sh
RUN chmod +x /var/team42_app/start_prod.sh
COPY django_marketplace .
