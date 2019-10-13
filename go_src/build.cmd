set CGO_CFLAGS=-I../C_porting_XTP/include/XTP -I../C_porting_XTP/include/CXTPApi
set CGO_LDFLAGS=-L./../C_porting_XTP/lib/XTP/win64 -L./../C_porting_XTP/lib/CXTPApi/ -lCXTPApi -lxtpquoteapi -lxtptraderapi
set GOOS=windows
set GOARCH=amd64
set CGO_ENABLED=1

echo %CGO_CFLAGS%
echo %CGO_LDFLAGS%
echo %GOOS%

go build -o go_xtp_trader.exe main.go
