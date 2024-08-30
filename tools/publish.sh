#!/usr/bin/env bash

source sample.env

CWD=`echo $(pwd) | sed 's/\//\n/g' | tail -n 1`
if [ $CWD == "tools" ]
then
  cd ..
fi

IMAGE=ghcr.io/darthmikke/boutique
VERSION=$(git tag -l | tail -n 1 | sed 's/^[a-zA-Z]//g')

if [ -e $VERSION ]
then
  echo "Missing version tag. Aborting."
  exit 1
fi

echo Will build image with following tag:
echo $IMAGE:$VERSION

docker buildx create --driver docker-container --name millim
docker buildx use millim

docker login ghcr.io
docker buildx build \
 --platform linux/amd64,linux/arm64,linux/arm64/v6 \
 --build-arg DB_NAME=$DB_NAME \
 -t $IMAGE:$VERSION \
 -t $IMAGE:latest \
 --push \
 -f tools/Dockerfile \
 .
