install:
	poetry install

install-kernel:
	python -m ipykernel install --user

docs:
	docker-compose up
