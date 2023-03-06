FROM apache/airflow:2.3.3-python3.8

USER root

RUN mkdir -p /opt/airflow

WORKDIR /opt/airflow/
# RUN apt-get update
# RUN apt-get install inetutils-ping

USER airflow

RUN pip install --upgrade pip

COPY requirement.txt /opt/airflow/
COPY .env /opt/airflow/

RUN pip install -r requirement.txt


