#!/usr/bin/env bash

CWD=$(pwd | sed 's/\//\n/g' | tail -n 1)

if [ $CWD == "tools" ]
then
	cd ..
fi

source tools/sample.env

TAG=ghcr.io/darthmikke/boutique:$(git log -n 1 --format="%h")

docker build \
	-t $TAG \
	-f tools/Dockerfile \
 	--build-arg DB_NAME=$DB_NAME \
	.

echo "Built $TAG"
