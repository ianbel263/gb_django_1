###########
# BUILDER #
###########

FROM python:3.9.6-slim as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# установка зависимостей
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

COPY . .

#########
# FINAL #
#########

FROM python:3.9.6-slim

# создаем директорию для пользователя
RUN mkdir -p /home/django

# создаем отдельного пользователя
RUN useradd -g www-data -m django
#RUN adduser -S django -G www-data

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
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/src/app/wheels ./wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
#RUN pip install --no-cache /wheels/*
RUN pip install -r requirements.txt

# копирование entrypoint-prod.sh
COPY ./entrypoint.prod.sh $APP_HOME

# копирование проекта Django
COPY . $APP_HOME

# изменение прав для пользователя app
RUN chown -R django:www-data $APP_HOME

# изменение рабочего пользователя
USER django

#ENTRYPOINT ["/home/django/web/entrypoint.prod.sh"]
