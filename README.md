## xtp.go
golang version xtp api

# preinstall:
1. vagrant
2. virtualbox

enter devenv directory, execute "vagrant up", then "vagrant ssh" to use the centos7 virtual machine for dev environment.

build dir:
./build.sh for generate c code for xtp api wrapper.

go_src dir:
"make dep" for fetching go library dependencies.
"make build" for build go src.

# boost build

wget https://dl.bintray.com/boostorg/release/1.70.0/source/boost_1_70_0.tar.bz2

tar -jxvf boost_1_70_0.tar.bz2

cd boost_1_70_0

./bootstrap.sh

    --with-python

sudo ./b2 install --prefix=/usr/lib64/boost_1_70_0 --build-type=complete --layout=tagged link=static runtime-link=static --debug-configuration threading=multi debug release address-model=64 cflags=-fPIC cxxflags=-fPIC

#vs2010
b2 --build-type=complete toolset=msvc-10.0 link=static runtime-link=shared --debug-configuration threading=multi debug release address-model=32

#vs2017
b2 --build-type=complete toolset=msvc-14.1 link=static runtime-link=shared --debug-configuration threading=multi debug release architecture=x86 address-model=64

tar -cjf boost_compiled_gcc8.tar.bz2 /usr/lib64/boost_1_70_0

#gcc7
#!/bin/bash

sudo yum install centos-release-scl
sudo yum install devtoolset-7-gcc*
scl enable devtoolset-7 bash
which gcc
gcc --version
