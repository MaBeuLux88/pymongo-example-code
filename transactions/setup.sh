#!/usr/bin/env bash

#wget or change to curl or whatever your favourite command line download tool is

if [ ! -f mongodb-osx-ssl-x86_64-4.0.0-rc0.tgz ];then
    echo "Download mongodb"
    wget https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-4.0.0-rc0.tgz
fi
if [ ! -d mongodb-osx-x86_64-4.0.0-rc0 ];then
    echo "unpack mongodb"
    tar xvzf mongodb-osx-ssl-x86_64-4.0.0-rc0.tgz
else
    echo "Mongodb 4.0 RC0 already downloaded"
fi
#setup a virtualenv

if [ ! -d venv ];then
    echo "setup virtual env in venv"
    python3 -m venv venv
fi

source venv/bin/activate

# required to simplying installing replica sets

if ! python -c "import mtools" 2> /dev/null ;then
    pip install mtools
fi

if  ! python -c "import psutil" 2> /dev/null ;then
    pip install psutil
fi

#pymongo beta

if ! python -c "import pymongo" 2> /dev/null ;then
    python -m pip install https://github.com/mongodb/mongo-python-driver/archive/3.7.0b0.tar.gz
fi

./mongod.sh start
