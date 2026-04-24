#!/usr/bin/env bash

set -e

echo "Creating Pipenv environment..."

# Initialize pipenv (uses current Python)
pipenv --python 3

echo "Installing dependencies..."

pipenv install \
    flask \
    requests \
    deep-translator \
    python-dotenv

echo "Generating lockfile..."

pipenv lock --clear

echo "Done!"
echo "To enter the environment, run: pipenv shell"