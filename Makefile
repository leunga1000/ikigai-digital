PHONY: test coverage deploy docker-run

test:
		pytest
coverage:
		coverage run -m pytest && coverage report
docker-run:
		docker build -t ikdi . && docker run -p 80:8080 ikdi
deploy:
		terraform init && terraform plan && terraform apply