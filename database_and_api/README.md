# FastAPI

1. Prerequisite
- Poetry
- Python >= 3.11
- Docker

2. Installation guide
- Run
```
> poetry install
```

- Copy the content in .env.example to src/.env then fill in the value

- cd to `src` then run

```
> poetry run alembic upgrade head
```

- Run

```
> poetry run uvicorn main:app --reload
```

- Navigate to your desired browser, then enter `localhost:8000`
