# Research-artifact repo entry points. Run `make` or `make help` for targets.
# On Windows, the PowerShell scripts under scripts/ and paper/build/ are the
# native entry points; make targets are thin wrappers for POSIX shells.

PYTHON ?= python

.PHONY: help verify qa test manifest paper package sanitize bootstrap clean

help:
	@echo "targets:"
	@echo "  verify    verify artifact hashes"
	@echo "  qa        run repository QA tests"
	@echo "  test      run repository QA plus TraceGrant Task D tests"
	@echo "  manifest  regenerate artifacts/sha256sums.txt"
	@echo "  bootstrap fetch the pinned upstream checkouts (network)"
	@echo "  paper     build the manuscript PDF with Pandoc + XeLaTeX"
	@echo "  package   build a review zip under dist/ after hash verification"
	@echo "  sanitize  produce the public-release tree under dist/sanitized/"
	@echo "  clean     remove generated paper build output"

verify:
	$(PYTHON) scripts/verify_artifacts.py

qa:
	$(PYTHON) -m pytest -q qa

test: qa
	cd tests/tracegrant_task_d_20261014 && $(PYTHON) -m pytest -q tests

manifest:
	$(PYTHON) scripts/write_manifest.py

bootstrap:
	$(PYTHON) scripts/bootstrap_vendor.py

paper:
	bash paper/build/build.sh

package:
	$(PYTHON) scripts/package_release.py

sanitize:
	$(PYTHON) scripts/sanitize_release.py

clean:
	$(PYTHON) scripts/clean_build.py
