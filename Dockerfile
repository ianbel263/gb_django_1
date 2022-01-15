FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# создаем отдельного пользователя
RUN useradd -g www-data -m django

# создание каталога для приложения
ENV HOME=/home/django
ENV APP_HOME=/home/django/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

# установка зависимостей и копирование из builder
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        memcached \
        libmemcached-dev
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY ./requirements.txt $APP_HOME
RUN pip install -r requirements.txt
RUN pip install python-memcached

#memcached
COPY ./memcached.conf /etc/memcached.conf

# копирование проекта Django
COPY . $APP_HOME

# изменение прав для пользователя app
RUN chown -R django:www-data $APP_HOME

# изменение рабочего пользователя
USER django
