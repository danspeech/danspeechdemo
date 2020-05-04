#!/bin/bash

#
# Build a new .../deepspeech_torch image
#

WHOAMI=$(whoami)
CONTAINERNAME=danspeech_demoserver
TAGNAME="$WHOAMI/$CONTAINERNAME"

if [[ -d tmp ]]  ; then
    rm -rf tmp
fi


for x in MANIFEST.in	README.md	danspeechdemo  setup.py ; do
    cp -r $x tmp
done    

docker build --file="Dockerfile-demo-server" --tag "$TAGNAME" .
