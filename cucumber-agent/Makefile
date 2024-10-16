SHELL:=/bin/bash
.DEFAULT_GOAL := help
.PHONY: help home env

CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
USER_ID:=$(shell id -u ${USER})
USER_GROUP:=$(shell id -g ${USER})
APPLICATION_ENV=venv


help:
	@echo ''
	@echo 'Makefile for '
	@echo '     make help			show this information'
	@echo '     make env			create application virtual environment'
	@echo ''

add-venv:
	sudo apt install python3.10-venv

env:
	python3 -m venv $(CURRENT_DIR)/$(APPLICATION_ENV)

renv:
	rm -rf $(CURRENT_DIR)/$(APPLICATION_ENV)

pip:
	$(CURRENT_DIR)/$(APPLICATION_ENV)/bin/pip install -U pip setuptools

act:
	$(eval ENV_ACTIVATE := $(shell echo $(CURRENT_DIR)/$(APPLICATION_ENV)/bin/activate))
	@echo $(ENV_ACTIVATE)

dact:
	@echo deactivate

deps:
	pip install -r $(CURRENT_DIR)/requirements.txt

run:
	python main.py