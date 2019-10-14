cd ..\C_porting_XTP

python gen_cgo_code.py

cd ..\build

rd /S /Q build

mkdir build_prj

cd build_prj

cmake ../../C_porting_XTP/src/Platform -G "Visual Studio 15 2017 Win64" -Wno-dev -DBoost_DEBUG=ON

cd ..
