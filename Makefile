.PHONY: py up
up:
	docker-compose up --force-recreate --build -d
	sleep 2
	make py
py:
	docker-compose run --rm python-env main.py
	docker-compose logs -f python-env