#!/bin/bash

sudo yum -y install centos-release-scl
sudo yum -y install devtoolset-8-gcc devtoolset-8-gcc-c++ devtoolset-8-binutils
sudo bash -c 'echo "source /opt/rh/devtoolset-8/enable" >> /etc/profile'
source /etc/profile
