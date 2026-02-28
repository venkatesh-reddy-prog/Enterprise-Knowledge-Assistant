.PHONY: start-dev run-tests build-images clean lint format

start-dev:
	docker compose -f docker-compose.dev.yml up --build

run-tests:
	pytest

build-images:
	docker compose -f docker-compose.dev.yml build

clean:
	docker compose -f docker-compose.dev.yml down -v
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

lint:
	ruff check .
	black --check .

format:
	black .
	ruff check --fix .

