VERSION=v1

docker-build:
	docker build --tag=quay.io/bukwp/kopfmysql:${VERSION} ./kopfmysql
