test: build run-mysql wait-mysql pytest

build:
	docker-compose build

run-ls:
	docker-compose run kopfmysql /bin/bash -c "ls"

pytest:
	docker-compose run --entrypoint="" kopfmysql pytest -v

wait-mysql:
	docker-compose run --entrypoint="" kopfmysql wait-for-it mysql:3306 -t 30

run-mysql:
	docker-compose up -d mysql

run-mysql-local:
	docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password quay.io/bukowwp/mysql
