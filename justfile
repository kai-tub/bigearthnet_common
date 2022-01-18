install:
	poetry install
	poetry run python -m ipykernel install --user

docs:
	docker-compose up
