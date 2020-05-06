#!/bin/bash -eu

docker build .

if [ $? -eq 0 ]
then
  echo "Passed."
  exit 0
else
  echo "Failed." >&2
  exit 1
fi

