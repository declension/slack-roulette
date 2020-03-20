SHELL:=/bin/bash
URL = $(shell poetry run chalice url)
.PHONY: clean build local


deploy: build
	poetry run chalice deploy --stage ci --no-autogen-policy

requirements.txt:
	poetry export -f requirements.txt -o requirements.txt

local:
	poetry run chalice local

clean:
	rm requirements.txt; poetry install
