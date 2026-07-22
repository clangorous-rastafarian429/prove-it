.PHONY: test validate

test: validate
	python3 -m unittest discover -s tests -v
	bash -n install.sh uninstall.sh
	bash tests/test_installer.sh

validate:
	python3 -m py_compile skills/prove-it/scripts/evidence.py
	python3 tests/validate_skill.py
