#!/usr/bin/env bash

CWD=`echo $(pwd) | sed 's/\//\n/g' | tail -n 1`
if [ $CWD == "tools" ]
then
  cd ..
fi

cd wsgi/design-system
npm i
npm run build
cd ../..
cp wsgi/design-system/public/assets/bundle.css wsgi/app/static/assets \
  && echo Copied
