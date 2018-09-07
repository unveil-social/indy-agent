FROM ubuntu:16.04

ARG uid=1000
ARG indy_stream=stable

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ENV SHELL="/bin/bash"

# Install environment
RUN apt-get update -y && apt-get install -y \
    software-properties-common \
    git \
    wget \
    python3.5 \
    python3-pip \
    python-setuptools \
    python3-nacl \
    apt-transport-https \
    ca-certificates \
    build-essential \
    pkg-config \
    cmake \
    libssl-dev \
    libsqlite3-dev \
    libsodium-dev \
    curl \
    vim

# Install LibIndy
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 68DB5E88
RUN echo "deb https://repo.sovrin.org/sdk/deb xenial $indy_stream" >> /etc/apt/sources.list

# Fix LibIndy version to 1.5.0
RUN echo "Package: libindy" >> /etc/apt/preferences
RUN echo "Pin: version 1.6.1" >> /etc/apt/preferences
RUN echo "Pin-Priority: 1000" >> /etc/apt/preferences

RUN apt-get update && apt-get install -y libindy
RUN apt-get update && apt-get install -y indy-cli

# Install nodejs
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y \
        nodejs \
        build-essential

# Install python 3.7
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y python3.6 python3.6-dev python3-pip python3.6-venv

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

ENV LD_LIBRARY_PATH=$HOME/.local/lib:/usr/local/lib:/usr/lib

WORKDIR /agent

# Install pip dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy rest of the app
COPY . .
RUN chmod +x index.py


EXPOSE 3210

#ENV RUST_LOG trace
ENTRYPOINT python3.6 index.py
