FROM alpine:3.8
RUN apk add --no-cache python3 python3-dev libffi-dev build-base gcc libxslt-dev libxml2-dev openssl-dev py3-lxml  && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r /code/requirements.txt
ADD . /code/
CMD ["python", "main.py"]