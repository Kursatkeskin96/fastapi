.PHONY: run-dev run-prod install-dependencies venv

run-dev: install-dependencies
	fastapi dev

run-prod: install-dependencies
	fastapi run
	
install-dependencies: venv
	pip3 install -r requirements.txt

venv:
	python -m venv ./venv