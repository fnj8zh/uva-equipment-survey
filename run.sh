#!/bin/bash
set -e

docker build -t final-project .

docker run -p 5000:5000 \
  -v "$(pwd)/data:/app/data" \
  final-project