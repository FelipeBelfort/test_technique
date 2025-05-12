mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(patsubst %/,%,$(dir $(mkfile_path)))

api:
	docker compose build server

front:
	docker compose build front

run:
	docker compose up -d

logs:
	docker compose logs -f

prod:
	docker compose -f docker-compose-prod.yml up -d

test:
	docker compose -f docker-compose-test.yml run --rm server coverage run -m pytest

coverage:
	docker compose -f docker-compose-test.yml run --rm server coverage report

coverage_html:
	- docker compose -f docker-compose-test.yml run --rm server coverage html
	@echo "\033[0;32mHTML Report: \033[0;34m${current_dir}/app/coverage/html_coverage/index.html\033[0m"

lint_api:
	flake8 glados-api-draft-master/app --config=glados-api-draft-master/.flake8

lint_front:
	cd glados-front-draft-master && npm install && npm run lint && rm -rf node_modules package-lock.json

db:
	docker compose exec db psql -U postgres -d glados

db_history:
	docker compose run --rm server flask db history

db_upgrade:
	docker compose exec -T server flask db upgrade

db_downgrade:
	docker compose run --rm server flask db downgrade

shell:
	docker compose exec server flask shell

bash:
	docker compose exec server bash

stop:
	docker compose down

clean:
	- docker compose down
	- docker compose ${compose.test} down
