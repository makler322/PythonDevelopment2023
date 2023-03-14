-include .env

# commands
lint:
	@isort development
	@flake8 development

test:
	@pytest

install:
	@pip install -U -r requirements.dev.txt
	@pip install -U -r requirements.txt

run.cow_say:
	@python

build: install lint test

