.DEFAULT_GOAL := clean-dev-environment


# Python Environment
VENV_DIRECTORY := .venv
DEV_REQUIREMENTS_STAMP := $(VENV_DIRECTORY)/dev-requirements-stamp
FROZEN_DEV_REQUIREMENTS_STAMP := $(VENV_DIRECTORY)/frozen-dev-requirements-stamp

${VENV_DIRECTORY}:
	python3 -m venv ${VENV_DIRECTORY}
	. .venv/bin/activate; pip install -r requirements-pip.txt

${DEV_REQUIREMENTS_STAMP}: ${VENV_DIRECTORY} requirements-dev.txt
	. .venv/bin/activate; pip install -r requirements-dev.txt
	touch $@

${FROZEN_DEV_REQUIREMENTS_STAMP}: ${VENV_DIRECTORY} requirements-dev-frozen.txt
	. .venv/bin/activate; pip install -r requirements-dev-frozen.txt
	touch $@

refreeze-dev-requirements: clean-venv ${DEV_REQUIREMENTS_STAMP}
	. .venv/bin/activate; pip freeze --all --exclude-editable > requirements-dev-frozen.txt

clean-venv:
	rm -rf ${VENV_DIRECTORY}


# Python Testing
pylint: ci-environment
	@ make -f Makefile.python pylint

black: ci-environment
	@ make -f Makefile.python black

isort: ci-environment
	@ make -f Makefile.python isort

format-python-code: black isort


# environments
ci-environment: ${FROZEN_DEV_REQUIREMENTS_STAMP}

dev-environment: ci-environment

clean-dev-environment: clean dev-environment

clean: clean-venv
