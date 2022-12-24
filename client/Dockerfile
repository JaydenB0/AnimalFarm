# syntax=docker/dockerfile:1
FROM python:3.9.16-slim
WORKDIR /app
RUN pip install pdm && pdm --pep582 >> ~/.bash_profile && eval "$(pdm --pep582)"
RUN pdm install