compile:
	yum install -y gcc libffi-devel openssl-devel python27-virtualenv
	virtualenv /tmp/venv
	/tmp/venv/bin/pip install --upgrade pip setuptools
	/tmp/venv/bin/pip install -r requirements.txt
	cp -r /tmp/venv/lib/python2.7/site-packages/. ./vendored
	cp -r /tmp/venv/lib64/python2.7/site-packages/. ./vendored
	pip install

test:
	python tests.py

deploy:
	npm install -g serverless
	serverless deploy

lambda-deps:
	@echo "--> Compiling lambda dependencies"
	docker run -it -v ${CURDIR}:/src -w /src amazonlinux make compile

lambda-test:
	@echo "--> Running tests"
	docker run -it -v ${CURDIR}:/src -w /src amazonlinux make test

.PHONY: lambda-deps compile