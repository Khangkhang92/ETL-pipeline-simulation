#! /bin/bash

cd database_and_api

docker compose up -d --build

cd ..

cd airflow

docker compose up -d --build
