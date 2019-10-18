#!/bin/bash

file_name=redis-stable

if [ ! -d "tar_files" ]; then
    mkdir -p tar_files
fi

cd tar_files

if [ ! -f "$file_name.tar.gz" ]; then
    wget http://download.redis.io/$file_name.tar.gz
fi
    
if [ ! -d "$file_name" ]; then
    tar -xzvf $file_name.tar.gz
fi

cd redis-stable

make clean

make MALLOC=libc

make test

sudo make install

cd ../..
