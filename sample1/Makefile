SHELL:=/bin/bash
.DEFAULT_GOAL := help
.PHONY: help home env

CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
USER_ID:=$(shell id -u ${USER})
USER_GROUP:=$(shell id -g ${USER})
APPLICATION_ENV=env


help:
	@echo ''
	@echo 'Makefile for '
	@echo '     make help			show this information'
	@echo '     make env			create application virtual environment'
	@echo ''

env:
	python3 -m venv $(APPLICATION_ENV)

pip:
	pip install --upgrade pip

act: 
	source $(CURRENT_DIR)/$(APPLICATION_ENV)/bin/activate

deact:
	deactivate

deps:
	pip install -r $(CURRENT_DIR)/requirements.txt

run:
	python src/main.py