.DEFAULT_GOAL := show-help
.PHONY: show-help
# See <https://gist.github.com/klmr/575726c7e05d8780505a> for explanation.
## This help screen
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)";echo;sed -ne"/^## /{h;s/.*//;:d" -e"H;n;s/^## //;td" -e"s/:.*//;G;s/\\n## /---/;s/\\n/ /g;p;}" ${MAKEFILE_LIST}|LC_ALL='C' sort -f|awk -F --- -v n=$$(tput cols) -v i=29 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"%s%*s%s ",a,-i,$$1,z;m=split($$2,w," ");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;printf"\n%*s ",-i," ";}printf"%s ",w[j];}printf"\n";}'
UNAME := $(shell uname -m)


.PHONY: format
## Format
format:
	@poetry run black .
	@poetry run isort .

.PHONY: lint
## Lint
lint:
	poetry run black --check .
	poetry run flake8 .
	poetry run mypy .
	poetry run isort --check-only .
	poetry run vulture . --min-confidence 80

.PHONY: test
## Run unit tests
test:
	poetry run python -m pytest -m "not integration" -v

.PHONY: all
## Run all required pre-push commands
all: format lint test integration requirements
	@echo -e "\n\n >> All Good!!! << :)"

.PHONY: pre-integration
## Runs pre-integration setups
pre-integration:
	@docker-compose --profile integration pull
	@docker-compose --profile integration up --force-recreate --always-recreate-deps --renew-anon-volumes --remove-orphans -d

.PHONY: integration
## Runs integration tests
integration: pre-integration
	@poetry run python -m pytest -m integration
	@docker-compose --profile integration down

.PHONY: requirements
## Creates the requirements.txt from poetry's env
requirements:
	@poetry run python ./scripts/create_requirements_file.py