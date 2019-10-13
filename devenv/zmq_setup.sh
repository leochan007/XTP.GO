#!/bin/bash

ver=4.1.5

if [ ! -d "tar_files" ]; then
    mkdir -p tar_files
fi

if [ ! -f "/usr/local/lib/libzmq.so" ]; then

cd tar_files

if [ ! -d "./zeromq-$ver" ]; then
    echo 'dir not existed.'
    if [ ! -f "zeromq-$ver.tar.gz" ]; then
        wget --no-check-certificate https://github.com/zeromq/zeromq4-1/releases/download/v$ver/zeromq-$ver.tar.gz
    fi
    tar -xzvf zeromq-$ver.tar.gz

    cd zeromq-$ver
    ./configure
    #./configure --prefix=/home/libdev/zmq4
    make
else
    cd zeromq-$ver
fi

sudo make install
#sudo sh -c 'echo "/home/libdev/zmq4" >> /etc/ld.so.conf'
#sudo ldconfig
#sudo ln -s /home/libdev/zmq4/lib/libzmq.so /usr/lib/libzmq.so
#export PKG_CONFIG_PATH=`pwd`/zeromq-4.1.5/src
#CGO_CFLAGS=-I/home/libdev/zmq4/include CGO_LDFLAGS=-L/home/libdev/zmq4/lib 

sudo sh -c "echo /usr/local/lib >> /etc/ld.so.conf"
sudo ldconfig

cd ../..

fi

export PKG_CONFIG_PATH=`pwd`/tar_files/zeromq-$ver/src
go get github.com/op/go-logging
go get -tags zmq_4_x github.com/alecthomas/gozmq
