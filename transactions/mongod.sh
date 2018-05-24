#!/usr/bin/env bash

MONGOD_BINDIR=./mongodb-osx-x86_64-4.0.0-rc0/bin
PATH=${MONGOD_BINDIR}:${PATH}

if [ "$1" == "stop" ];then
    mlaunch stop
elif [ -d "$MONGOD_BINDIR" ]; then
  if [ -d "data/txntest" ]; then
    mlaunch start
  else
    mlaunch init --port 27100 --replicaset --name "txntest"
  fi
fi
