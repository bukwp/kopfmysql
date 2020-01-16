VERSION=v1alpha1

docker-build:
	docker build --tag=quay.io/bukwp/kopfmysql:${VERSION} ./kopfmysql

docker-run:
	docker run --rm -it quay.io/bukwp/kopfmysql:${VERSION}

docker-build-run: docker-build docker-run
