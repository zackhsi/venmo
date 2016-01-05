venv:
	./make_venv

.PHONY: db
db: venv
	./venmo/ensure_db

.PHONY: rent
rent: venv
	venv/bin/python -m venmo.cli group rent

.PHONY: token
token: venv
	venv/bin/python -m venmo.cli refresh-token
