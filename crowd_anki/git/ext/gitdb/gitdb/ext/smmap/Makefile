.PHONY: build sdist cover test clean-files clean-docs doc all  

all:
	$(info Possible targets:)
	$(info doc)
	$(info clean-docs)
	$(info clean-files)
	$(info clean)
	$(info test)
	$(info coverage)
	$(info build)
	$(info sdist)

doc:
	cd doc && make html

clean-docs:
	cd doc && make clean

clean-files:
	git clean -fx
	rm -rf build/ dist/

clean: clean-files clean-docs

test:
	nosetests

coverage:
	nosetests --with-coverage --cover-package=smmap
	
build:
	./setup.py build
	
sdist:
	./setup.py sdist

release: clean
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
