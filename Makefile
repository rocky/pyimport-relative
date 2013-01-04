# Compatibility for us old-timers.
PHONY=check clean dist distclean test

#: the default target - same as running "check"
all: check

#: Run all tests
check: 
	$(PYTHON) ./setup.py nosetests

#: Clean up temporary files
clean: 
	$(PYTHON) ./setup.py $@

#: Create source (tarball) and binary (egg) distribution
dist: 
	$(PYTHON) ./setup.py sdist bdist

# It is too much work to figure out how to add a new command to distutils
# to do the following. I'm sure distutils will someday get there.
DISTCLEAN_FILES = build dist *.egg-info *.pyc *.so py*.py

#: Remove ALL dervied files 
distclean: clean
	-rm -fr $(DISTCLEAN_FILES) || true

#: Install package locally
install: 
	$(PYTHON) ./setup.py install

#: Same as check
test: check

ChangeLog:
	git log --pretty --numstat --summary | $(GIT2CL) >$@

.PHONY: $(PHONY)
