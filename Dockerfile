FROM node:10-slim

# Create and define the node_modules's cache directory.
RUN mkdir /usr/src/cache
WORKDIR /usr/src/cache

# Install the application's dependencies into the node_modules's cache directory.
COPY package.json ./
COPY package-lock.json ./
RUN npm install

WORKDIR /kerckhoff
COPY package.json package-lock.json /kerckhoff/
COPY ./webpack.config.js ./jsconfig.json ./
COPY ./kerckhoff/assets ./kerckhoff/assets
RUN cp -r /usr/src/cache/node_modules/. /kerckhoff/node_modules/
RUN npm run build

RUN apt update && \
    apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget && \
    wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz && \
    tar xzf Python-3.7.4.tgz && \
    cd Python-3.7.4 && \
    ./configure && \
    make && \
    make install

ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y curl \
                                         build-essential \
                                         libpq-dev \
                                         git \
                                         zlib1g
ENV LIBRARY_PATH=/lib:/usr/lib
ADD requirements.txt /kerckhoff/
RUN python3.7 -m pip install --upgrade pip && python3.7 -m pip install -r requirements.txt
ADD . /kerckhoff/
EXPOSE 5000
ENTRYPOINT [ "./prod-entrypoint.sh" ]
CMD "./prod.sh"