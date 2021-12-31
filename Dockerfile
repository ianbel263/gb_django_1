###########
# BUILDER #
###########

FROM python:3.9.6-alpine as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# установка зависимостей
#RUN apk update
#    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip

# установка зависимостей
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

COPY . .

#########
# FINAL #
#########

FROM python:3.9.6-alpine

# создаем директорию для пользователя
RUN mkdir -p /home/django

# создаем отдельного пользователя
RUN adduser -S django -G www-data

# создание каталога для приложения
ENV HOME=/home/django
ENV APP_HOME=/home/django/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# установка зависимостей и копирование из builder
#RUN apk update
#  && apk add libpq
COPY --from=builder /usr/src/app/wheels ./wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# копирование entrypoint-prod.sh
COPY ./entrypoint.prod.sh $APP_HOME

# копирование проекта Django
COPY . $APP_HOME

# изменение прав для пользователя app
RUN chown -R django:www-data $APP_HOME

# изменение рабочего пользователя
USER django

ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]
