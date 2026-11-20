.PHONY: run lint format test check up down hooks

PORT ?= 8001

run:
	poetry run uvicorn app.main:app --reload --port $(PORT)

lint:
	poetry run ruff check .
	poetry run ruff format --check .
	poetry run mypy

format:
	poetry run ruff check --fix .
	poetry run ruff format .

test:
	poetry run pytest

check: lint test

hooks:
	poetry run pre-commit install -c ci/.pre-commit-config.yaml

up:
	docker compose --env-file .env -f docker/compose.yaml up -d

down:
	docker compose --env-file .env -f docker/compose.yaml down