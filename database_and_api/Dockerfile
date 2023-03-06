FROM python:3.11

RUN apt-get update && apt-get install -y libpq-dev gcc git tk

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.2.0

RUN mkdir -p /opt/app
WORKDIR /opt/app

ENV PYTHONPATH /opt/app

RUN pip install "poetry==$POETRY_VERSION"

COPY ./pyproject.toml /opt/app/

RUN poetry update
RUN poetry install

COPY ./app /opt/app
COPY ./run.sh /opt/app

RUN chmod +x run.sh

CMD ["./run.sh"]
