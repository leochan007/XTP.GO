#!/bin/bash

sudo yum update

sudo yum install -y dos2unix python-pip python-devel

sudo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip

sudo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy
