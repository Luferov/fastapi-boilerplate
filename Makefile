.PHONY=migrate,revision,dev,test


test:
	poetry run pytest --cov-report html --cov=src tests

all-test:
	poetry run pytest --cov-report html --cov=src tests

dev:
	poetry run uvicorn src.main:app --reload

revision:
	poetry run alembic revision --autogenerate -m $(NAME)

migrate:
	poetry run alembic upgrade head

rollback:
	poetry run alembic downgrade $(NUM)

HOST ?= 0.0.0.0
PORT ?= 8080
start:
	poetry run uvicorn src.main:app --host $(HOST) --port $(PORT)