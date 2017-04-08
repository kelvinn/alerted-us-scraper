FROM frolvlad/alpine-python2
ENV PYTHONUNBUFFERED 1
RUN apk update
RUN apk add libxml2-dev libxslt-dev python-dev musl-dev gcc
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
CMD ["python", "clock.py"]