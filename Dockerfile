FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip
RUN pip3 install requests grequests aiohttp django django-bootstrap3 django-bootstrap-form
