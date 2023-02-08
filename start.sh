#!/bin/bash
app="movie_searcher"
docker build -t ${app} .
docker run -d -p 3000:5000 \
  --name=moviesearcher \
  -v $PWD:/app ${app}