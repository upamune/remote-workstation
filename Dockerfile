FROM ubuntu:20.04

RUN apt-get update -y && apt-get install -y curl
RUN mkdir -p /root/.bootstrap
WORKDIR /root/.bootstrap

RUN curl -sL https://github.com/itamae-kitchen/mitamae/releases/latest/download/mitamae-x86_64-linux.tar.gz | tar xvz && \
    mv ./mitamae-x86_64-linux ./mitamae

RUN echo "#!/bin/bash -eu" > bootstrap.sh
RUN echo "./mitamae local recipe.rb" >> bootstrap.sh
RUN chmod +x bootstrap.sh

COPY recipe.rb .

RUN ./bootstrap.sh
