venv:
	./make_venv

.PHONY: db
db: venv
	./venmo/ensure_db

.PHONY: rent
rent: venv
	venv/bin/python -m venmo.cli group rent
