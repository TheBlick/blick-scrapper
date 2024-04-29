build:
	docker-compose build
up:
	docker-compose up --force-recreate --build -d
py:
	docker-compose run --rm python-env main.py
	docker-compose logs -f python-env
env:
	docker-compose run --rm -i --entrypoint bash python-env

test:
	PYTHONPATH=$(PWD)/src:$${PYTHONPATH} pytest -v -s