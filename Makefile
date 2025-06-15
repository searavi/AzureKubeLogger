bootstrap:
	./scripts/k8s-bootstrap.sh

deploy:
	./scripts/deploy.sh

logs:
	kubectl logs -n monitoring deployment/azurekubelogger

status:
	kubectl rollout status deployment azurekubelogger -n monitoring

lint:
	flake8 --config=flake8 .

test:
	pytest

format:
	black .

fix:
	black .
	flake8 .