FROM alpine:3.18

RUN apk add openssh git bash python3 py3-pip gcc python3-dev musl-dev
RUN pip3 install fastwsgi

COPY run.sh /run.sh
RUN chmod +x /run.sh

RUN mkdir /app
WORKDIR /app

ENTRYPOINT [ "/run.sh" ]
CMD [ "production" ]

EXPOSE 5000
