#!/bin/sh

docker exec geekshop_web python3 manage.py migrate --noinput
docker exec geekshop_web python3 manage.py collectstatic --noinput
docker exec geekshop_web python3 manage.py createsuperuser --noinput --email 1@1.ru
docker exec geekshop_web python3 manage.py loaddata ./fixtures/categories.json
docker exec geekshop_web python3 manage.py loaddata ./fixtures/products.json
