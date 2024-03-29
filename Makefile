.PHONY: clean clean-test clean-pyc clean-build help

COMMENTS_MD = comments.md

2026: config-2026.yaml $(COMMENTS_MD)
	python make-calendar.py $<
	mkdir -p docs/$@
	mv calendar-$@.html docs/$@
	cp $^ docs/$@
	cd docs/$@ && ln -s calendar-$@.html index.html

2025: config-2025.yaml $(COMMENTS_MD)
	python make-calendar.py $<
	mkdir -p docs/$@
	mv calendar-$@.html docs/$@
	cp $^ docs/$@
	cd docs/$@ && ln -s calendar-$@.html index.html

2024: config-2024.yaml $(COMMENTS_MD)
	python make-calendar.py $<
	mkdir -p docs/$@
	mv calendar-$@.html docs/$@
	cp $^ docs/$@
	cd docs/$@ && ln -s calendar-$@.html index.html

2023: config-2023.yaml $(COMMENTS_MD)
	python make-calendar.py $<
	mkdir -p docs/$@
	mv calendar-$@.html docs/$@
	cp $^ docs/$@
	cd docs/$@ && ln -s calendar-$@.html index.html


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .cache/

lint:
	pylint kaloot make-calendar.py

test: ## run tests quickly with the default Python
	pytest tests
