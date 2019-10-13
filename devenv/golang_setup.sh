#!/bin/bash

VER=1.13.1


file=go$VER.linux-amd64.tar.gz
goroot=/usr/local/go

if [ ! -d "tar_files" ]; then
    mkdir -p tar_files
fi

cd tar_files

if [ ! -d "$goroot" ]; then

    if [ ! -f "$file" ]; then
        wget https://studygolang.com/dl/golang/$file
        #wget http://www.golangtc.com/static/go/$VER/$file
        rm -rf go
    fi
    
    if [ ! -d "go" ]; then
        tar -xzvf $file
    fi
    
    sudo cp -rf go /usr/local/
fi

cd ..

echo export GOROOT=$goroot >> ~/.bashrc
echo export PATH=$goroot/bin:$PATH >> ~/.bashrc
echo export GOPATH=~/gopath >> ~/.bashrc
