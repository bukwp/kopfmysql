VERSION=v1alpha

deploy:
	kubectl create -f . --save-config

context:
	kubectl config set-context --current --namespace=wordpress

restart-kopf:
	kubectl rollout restart -f 6_kopf.dpl.yaml
