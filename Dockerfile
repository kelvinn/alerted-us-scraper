FROM amazonlinux
ENV PYTHONUNBUFFERED 1
RUN yum -y install python-pip gcc python-devel
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -t /code/vendored/ -r /code/requirements.txt
ADD . /code/
CMD ["python", "clock.py"]