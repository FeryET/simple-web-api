PHONY: test install-dev create-venv

SHELL = /bin/bash

.ONESHELL:

ACTIVATE_VENV = source .venv/bin/activate

create-venv:
	@python -m virtualenv .venv

install-dev:
	@$(ACTIVATE_VENV)
	@pip install -e '.[dev]'

test:
	@$(ACTIVATE_VENV)
	@pytest
