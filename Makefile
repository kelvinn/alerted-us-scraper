compile:
	yum install -y gcc libffi-devel openssl-devel python-virtualenv python2-setuptools libxml2-devel libxml2-python libxslt-devel tar gzip
	virtualenv /tmp/venv
	/tmp/venv/bin/pip install --upgrade pip setuptools
	/tmp/venv/bin/pip install -r requirements.txt
	cp -r /tmp/venv/lib/python2.7/site-packages/. ./vendored
	cp -r /tmp/venv/lib64/python2.7/site-packages/. ./vendored

test:
	python tests.py

deploy:
	npm install -g serverless
	serverless deploy

lambda-deps:
	@echo "--> Compiling lambda dependencies"
	docker run -it -v ${PWD}:/src -w /src amazonlinux /bin/bash -c "yum install make -y; make compile"

lambda-test:
	@echo "--> Running tests"
	docker run -it -v ${PWD}:/src -w /src amazonlinux /bin/bash -c "yum install make -y; make test"

.PHONY: lambda-deps compile