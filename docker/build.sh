#!/usr/bin/env bash

CWD=$(pwd | sed 's/\//\n/g' | tail -n 1)

if [ $CWD == "docker" ]
then
	cd ..
fi

TAG=ghcr.io/darthmikke/boutique:$(git log -n 1 --format="%h")

docker build \
	-t $TAG \
	-f docker/Dockerfile \
	.

echo "Built $TAG"
