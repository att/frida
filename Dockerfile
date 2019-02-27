# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

FROM python:3.6-slim
LABEL author=sm663k@att.com name=frida version=0.0.1
WORKDIR /usr/src/app
COPY . .
RUN pip --proxy="http://one.proxy.att.com:8080/" install -r requirements.txt
EXPOSE 5000
CMD [ "gunicorn", "-w 4", "-b 0.0.0.0:5000", "app:app" ]