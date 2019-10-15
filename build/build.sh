#!/bin/bash

cd ../C_porting_XTP/pyfiles

python3 gen_cgo_code.py

cd ../../build

rm -rf build_prj

mkdir build_prj

cd build_prj

cmake ../../C_porting_XTP/src/Platform -G "Unix Makefiles" -Wno-dev -DBoost_DEBUG=OFF

make

cd ..
