FROM python:3.10

ENV PYTHONUNBEFFERED 1

COPY ./app /project/app
COPY ./requirements.txt /project/requirements.txt
COPY ./alembic.ini /project/alembic.ini

WORKDIR /project

RUN python -m venv /pyvenv && \
    /pyvenv/bin/pip install --upgrade pip && \
    /pyvenv/bin/pip install -r requirements.txt

ENV PATH="/pyvenv/bin:$PATH"
