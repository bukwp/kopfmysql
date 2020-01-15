MYSQL_NAME=bukwp-kopfmysql-mysql-test
VERSION=v1alpha

.EXPORT_ALL_VARIABLES:
MSYS2_ARG_CONV_EXCL = /bin/sh;/bin/bash;/var/run/docker

test: delete-mysql run-mysql build docker-test
test1: build docker-test

build:
	docker build \
	--tag=kopfmysql:${VERSION} \
	.

docker-test:
	docker run \
	--rm \
	--entrypoint="" \
	--network="${MYSQL_NAME}" \
	kopfmysql:${VERSION} \
	wait-for-it ${MYSQL_NAME}:3306 && python -m unittest -v

run-mysql: create-network
	docker run \
    --name=${MYSQL_NAME} \
    --network=${MYSQL_NAME} \
    -d \
    -p 8765:3306 \
    -e MYSQL_ROOT_PASSWORD="password" \
    quay.io/bukowwp/mysql:latest \
    --default-authentication-plugin=mysql_native_password

create-network:
	-docker network create ${MYSQL_NAME}

delete-network:
	-docker network delete ${MYSQL_NAME}

delete-mysql:
	-docker rm -f ${MYSQL_NAME}
