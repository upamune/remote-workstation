#!/bin/bash -eu

docker run -it --rm -v "$(pwd)/.lego:/.lego" --env DO_AUTH_TOKEN="${DO_AUTH_TOKEN}" goacme/lego \
  --email="upamune@gmail.com" \
  --domains="serizawa.dev" \
  --dns=digitalocean \
  run

