#! /usr/bin/env bash

set -o errexit -o xtrace

flake8 --config=.flake8
isort . --check
black . --check --diff --config pyproject.toml
mypy .
