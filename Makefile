-include .env

# commands
lint:
	@mypy development
	@flake8 development

test:
	@pytest

dev.install:
	@pip install -U -r requirements.dev.txt
	@pip install -U -r requirements.txt

