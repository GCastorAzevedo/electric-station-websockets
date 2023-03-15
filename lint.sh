#! /usr/bin/env bash

flake8 --config=.flake8
isort .
black . --config pyproject.toml
mypy .