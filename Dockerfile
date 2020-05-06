FROM ubuntu:20.04

COPY recipe.rb .

RUN apt-get update -y && apt-get install -y curl
RUN mkdir -p /root/.bootstrap
WORKDIR /root/.bootstrap

RUN curl -sL https://github.com/itamae-kitchen/mitamae/releases/latest/download/mitamae-x86_64-linux.tar.gz | tar xvz && \
    mv ./mitamae-x86_64-linux ./mitamae
RUN curl -sLO https://raw.githubusercontent.com/upamune/remote-workstation/master/recipe.rb

RUN echo "#!/bin/bash -eu" > bootstrap.sh
RUN echo "./mitamae local recipe.rb" >> bootstrap.sh
RUN chmod +x bootstrap.sh
RUN ./bootstrap.sh
