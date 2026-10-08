PYTHON = uv run


COMMENTS_MD = comments.md

# One target per configuration file at the root, e.g. config-2028.yaml -> make 2028.
YEARS := $(patsubst config-%.yaml,%,$(wildcard config-*.yaml))

.PHONY: $(YEARS) clean clean-test clean-pyc clean-build test

$(YEARS): %: config-%.yaml $(COMMENTS_MD)
	mkdir -p docs/$@
	$(PYTHON) make-calendar.py $< -o docs/$@/calendar-$@.html
	cp $^ docs/$@
	ln -sf calendar-$@.html docs/$@/index.html


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

test: ## run tests quickly with the default Python
	uv run pytest tests
