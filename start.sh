#!/bin/bash
# app="docker.test"
# docker build -t ${app} .
docker run -d -p 56733:80 \
  --name=moviesearcher \
  -v $PWD:/app ${app}