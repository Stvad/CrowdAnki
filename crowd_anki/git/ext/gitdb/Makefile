PYTHON = python
SETUP = $(PYTHON) setup.py
TESTRUNNER = $(shell which nosetests)
TESTFLAGS =

all::
	@grep -Ee '^[a-z].*:' Makefile | cut -d: -f1 | grep -vF all

release:: clean
	# Check if latest tag is the current head we're releasing
	echo "Latest tag = $$(git tag | sort -nr | head -n1)"
	echo "HEAD SHA       = $$(git rev-parse head)"
	echo "Latest tag SHA = $$(git tag | sort -nr | head -n1 | xargs git rev-parse)"
	@test "$$(git rev-parse head)" = "$$(git tag | sort -nr | head -n1 | xargs git rev-parse)"
	make force_release

force_release:: clean
	git push --tags
	python3 setup.py sdist bdist_wheel
	twine upload -s -i 763629FEC8788FC35128B5F6EE029D1E5EB40300 dist/*

doc:: 
	make -C doc/ html

build::
	$(SETUP) build
	$(SETUP) build_ext -i

build_ext::
	$(SETUP) build_ext -i
	
install::
	$(SETUP) install

clean::
	$(SETUP) clean --all
	rm -f *.so

coverage:: build
	PYTHONPATH=. $(PYTHON) $(TESTRUNNER) --cover-package=gitdb --with-coverage --cover-erase --cover-inclusive gitdb

