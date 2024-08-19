FROM ghcr.io/darthmikke/wsgi:0.0.1-b5 as env

ENV DJANGO_DEBUG=True
ENV SECRET_KEY="django-insecure-lwyh*yitd$0=k3uo2)oiqz6()yqi4d9t9l-u!1#&caz6l43tfh"
ENV ALLOWED_HOSTS="*"
ENV CSRF_TRUSTED_ORIGINS="http://*:*"
ENV MEDIA_ROOT="/media/"
ENV DB_NAME='/db/db.sqlite3'

FROM env as build

RUN apk add openssh git bash python3 py3-pip gcc python3-dev musl-dev

COPY . /repo
WORKDIR /repo
RUN git stash

RUN rm -r /app
RUN mv /repo/wsgi /app
WORKDIR /app
RUN rm -rf venv .env db.sqlite3
RUN touch .env
RUN mkdir -p $DB_NAME
RUN rmdir $DB_NAME
RUN pip3 install --root-user-action=ignore -r requirements.txt
RUN python3 manage.py migrate

FROM env

LABEL org.opencontainers.image.source https://github.com/DarthMikke/boutique
COPY --from=build /app /app
COPY --from=build /db /db

WORKDIR /app
RUN pip3 install --root-user-action=ignore -r requirements.txt

ENV APP_DIR="/app"
ENV ASGI_APPLICATION="boutique.asgi:application"

VOLUME /media
VOLUME /db
