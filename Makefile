init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

test:
	py.test --disable-socket tests
