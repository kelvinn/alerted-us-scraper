FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y python-dev libxml2-dev libxslt1-dev 
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
CMD ["python", "clock.py"]