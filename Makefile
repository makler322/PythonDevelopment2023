-include .env

# commands
lint:
	@isort development
	@flake8 development/PushPip

test:
	@pytest

install:
	@pip install -U -r requirements.dev.txt
	@pip install -U -r requirements.txt

build: install lint test
