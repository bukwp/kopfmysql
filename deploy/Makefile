VERSION=v1alpha1

deploy:
	kubectl create -f . --save-config

apply:
	kubectl apply -f .

delete:
	kubectl delete -f .

context:
	kubectl config set-context --current --namespace=wordpress

restart-kopf:
	kubectl rollout restart -f 6_kopf.dpl.yaml

delete-crd:
	kubectl delete -f 4_kopf.crd.yaml

patch-crd:
	kubectl patch customresourcedefinitions.apiextensions.k8s.io accounts.bukwp.kopfmysql -p '{"metadata":{"finalizers":[]}}' --type=merge

create-crd:
	kubectl create -f 4_kopf.crd.yaml --save-config
