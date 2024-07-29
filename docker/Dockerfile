FROM alpine:3.18 as build

RUN apk add openssh git bash python3 py3-pip gcc python3-dev musl-dev

COPY . /repo
WORKDIR /repo
RUN git stash

ENV DJANGO_DEBUG=True
ENV SECRET_KEY="django-insecure-lwyh*yitd$0=k3uo2)oiqz6()yqi4d9t9l-u!1#&caz6l43tfh"
ENV ALLOWED_HOSTS="*"
ENV CSRF_TRUSTED_ORIGINS="http://*:*"
ENV MEDIA_ROOT="/media/"
ENV DB_NAME='/db/db.sqlite3'

RUN mv /repo/wsgi /app
WORKDIR /app
RUN rm -rf venv .env db.sqlite3
RUN touch .env
RUN mkdir -p $DB_NAME
RUN rmdir $DB_NAME
# RUN python -m venv venv
# RUN source venv/bin/activate && pip3 install -r requirements.txt
# RUN source venv/bin/activate && python3 manage.py migrate
RUN pip3 install --root-user-action=ignore -r requirements.txt
RUN python3 manage.py migrate

RUN exit

FROM ghcr.io/darthmikke/wsgi:fc3c109

LABEL org.opencontainers.image.source https://github.com/DarthMikke/boutique
COPY --from=build /app /app
COPY --from=build /db /db

WORKDIR /app
RUN pip3 install --root-user-action=ignore -r requirements.txt

ENV DJANGO_DEBUG=True
ENV SECRET_KEY="django-insecure-lwyh*yitd$0=k3uo2)oiqz6()yqi4d9t9l-u!1#&caz6l43tfh"
ENV ALLOWED_HOSTS="*"
ENV CSRF_TRUSTED_ORIGINS="http://*:*"
ENV MEDIA_ROOT="/media/"
ENV DB_NAME='/db/db.sqlite3'

ENV APP_DIR="/app"
ENV ASGI_APPLICATION="boutique.asgi:application"

VOLUME /media
VOLUME /db
