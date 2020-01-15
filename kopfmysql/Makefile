MYSQL_NAME=bukwp-kopfmysql-mysql-test
VERSION=v1alpha1

.EXPORT_ALL_VARIABLES:
MSYS2_ARG_CONV_EXCL = /bin/sh;/bin/bash;/var/run/docker

test: delete-mysql run-mysql build wait-mysql docker-test
test1: build wait-mysql docker-test

build:
	docker build \
	--tag=kopfmysql:${VERSION} \
	.

run-ls:
	docker run \
	--rm \
	--entrypoint="" \
	kopfmysql:${VERSION} \
	/bin/bash -c "ls"

test-command:
	-docker run \
	--rm \
	-e MYSQL_ROOT_USER=test \
	-e MYSQL_ROOT_PASSWORD=test \
	-e MYSQL_HOST=test \
	-e MYSQL_PORT=test \
	kopfmysql:${VERSION} \
	--verbose

docker-test:
	docker run \
	--rm \
	--entrypoint="" \
	--network="${MYSQL_NAME}" \
	-e MYSQL_TEST_HOST=${MYSQL_NAME} \
	kopfmysql:${VERSION} \
	pytest -v

run-mysql: create-network
	docker run \
    --name=${MYSQL_NAME} \
    --network=${MYSQL_NAME} \
    --expose=3000 \
    -d \
    -e MYSQL_ROOT_PASSWORD="password" \
    quay.io/bukowwp/mysql:latest \
    --default-authentication-plugin=mysql_native_password

wait-mysql:
	docker run \
	--rm \
	--entrypoint="" \
	--network="${MYSQL_NAME}" \
	kopfmysql:${VERSION} \
	wait-for-it ${MYSQL_NAME}:3306 -t 30

create-network:
	-docker network create ${MYSQL_NAME}

delete-network:
	-docker network delete ${MYSQL_NAME}

delete-mysql:
	-docker rm -f ${MYSQL_NAME}
