
export SOURCE_DATABASE ?= POSTGRES
export TARGET_DATABASE ?= DUCKDB
export TABLES ?= HOCKEY

## Install Python requirements for running
requirements:
	uv add --upgrade -r requirements.txt

## Install python requirements for running and testing
requirements-test: requirements
	uv add --upgrade -r requirements-test.txt --dev

## Run formatters
.PHONY: fix
fix:
	uv run ruff format .
	uv run ruff check --fix .

## Python lint and formatting checks
.PHONY: check
check:
	uv run ruff format --check .
	uv run ruff check .

.PHONY: load-envs
load-envs:
	export $(cat .env|xargs)


.PHONY:run-app
run-app:
	uv run nohup streamlit run entrypoint/app.py

.PHONY: test
test:
	rm -rf tests/tmp
	uv run pytest tests