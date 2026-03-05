.PHONY: dev test build deploy

dev:
	uvicorn app.server:app --reload --host 0.0.0.0 --port 80

test:
	pytest

build:
	docker build -t novadynamics .

deploy:
	docker compose up --build -d
