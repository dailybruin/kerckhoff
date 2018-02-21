FROM python:3.6.2
ENV PYTHONUNBUFFERED 1
RUN mkdir /kerckhoff

RUN apt-get update && apt-get install -y curl \
                                         build-essential
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash
RUN apt-get install -y nodejs
RUN npm install -g webpack

WORKDIR /kerckhoff

ADD requirements.txt /kerckhoff/
RUN pip install -r requirements.txt

ADD package.json package-lock.json /kerckhoff/
RUN npm install

ADD . /kerckhoff/
