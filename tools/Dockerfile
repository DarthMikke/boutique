FROM ghcr.io/darthmikke/wsgi:0.0.1-b5 AS base

FROM base AS build

ARG DB_NAME

RUN apk add openssh git bash python3 py3-pip gcc python3-dev musl-dev

COPY . /repo
WORKDIR /repo
RUN git stash

RUN rm -r /app
RUN mv /repo/wsgi /app
WORKDIR /app
RUN rm -rf venv .env db.sqlite3
COPY tools/sample.env .env
RUN mkdir -p $DB_NAME
RUN rmdir $DB_NAME
RUN pip3 install --root-user-action=ignore -r requirements.txt
RUN python3 manage.py migrate

FROM base

LABEL org.opencontainers.image.source=https://github.com/DarthMikke/boutique
COPY --from=build /app /app
COPY --from=build /db /db

WORKDIR /app
RUN pip3 install --root-user-action=ignore -r requirements.txt

ENV APP_DIR="/app"
ENV ASGI_APPLICATION="boutique.asgi:application"

VOLUME /media
VOLUME /db
