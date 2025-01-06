.PHONY=migrate,revision,dev,test


test:
	uv run pytest --cov-report html --cov=src tests

all-test:
	uv run pytest --cov-report html --cov=src tests

dev:
	uv run uvicorn src.main:app --reload

revision:
	uv run alembic revision --autogenerate -m $(NAME)

migrate:
	uv run alembic upgrade head

rollback:
	uv run alembic downgrade $(NUM)

HOST ?= 0.0.0.0
PORT ?= 8080
start:
	uv run uvicorn src.main:app --host $(HOST) --port $(PORT)