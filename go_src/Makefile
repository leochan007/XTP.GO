TARG=go_xtp_trader
CGOFILES=*.go
out_dir=bin

currdir=$(shell pwd)
#  -fno-eliminate-unused-debug-types
CGO_CFLAGS+='-I../C_porting_XTP/include/XTP -I../C_porting_XTP/include/CXTPApi'
CGO_LDFLAGS+='-L$(currdir)/../C_porting_XTP/lib/XTP/linux/ -L$(currdir)/../C_porting_XTP/lib/CXTPApi/ -lCXTPApi -lxtpquoteapi -lxtptraderapi'

LD_LIBRARY_PATH+=$(currdir)/../C_porting_XTP/lib/CXTPApi:$(currdir)/../C_porting_XTP/lib/XTP/linux

ifdef M
LOG=$(M)C
else
LOG=modify
endif

ifdef I
suffix=$(I)
else
suffix=-d=1 -f=strategy_d.json -u=15030798 -w=UgDUqNeK -r=120.27.164.69 -o=6001 -q=120.27.164.138 -p=6002
endif

TF_TYPE=cpu
# Change to "gpu" for GPU support
TARGET_DIRECTORY=/usr/local
    
tensorflow:
	sudo tar -xzvf tar_files/libtensorflow-$(TF_TYPE)-linux-x86_64-1.2.0-rc1.tar.gz -C $(TARGET_DIRECTORY)
	sudo ldconfig
	go get github.com/tensorflow/tensorflow/tensorflow/go
	go test github.com/tensorflow/tensorflow/tensorflow/go

goml:
	go get github.com/cdipaolo/goml/base
	go get github.com/cdipaolo/goml/perceptron
	go get github.com/sjwhitworth/golearn

gosl:
	sudo apt-get -y install libopenmpi-dev libhwloc-dev libsuitesparse-dev libmumps-dev && \
	sudo apt-get -y install gfortran libvtk6-dev python-scipy python-matplotlib dvipng && \
	mkdir -p $(GOPATH)/src/github.com/cpmech && \
	cd $(GOPATH)/src/github.com/cpmech && \
	git clone https://github.com/cpmech/gosl.git && \
	cd gosl && \
	./all.bash

talib:
	cd ../ThirdParty && rm ta-lib -rf && tar -xzvf ta-lib-0.4.0-src.tar.gz && \
	cd ta-lib && ./configure LDFLAGS="-lm" && make && sudo make install
	go get github.com/d4l3k/talib

dep:
	go get github.com/op/go-logging
	go get github.com/urfave/cli

dep2:
	sudo chown ubuntu:ubuntu /home/ubuntu/gopath/ -R
	sudo apt-get install -y pkg-config
	go get github.com/op/go-logging
	go get github.com/jessevdk/go-flags
	go get github.com/qiniu/py
	go get github.com/nsf/termbox-go
	go get github.com/garyburd/redigo/redis
	#go get -u github.com/astaxie/beego
	#go get -u github.com/beego/bee
	go get github.com/yireyun/go-queue
	go get github.com/go-martini/martini
	go get github.com/gorilla/websocket
	go get -u github.com/mkideal/cli
	go get -u github.com/mkideal/goplus

gen_wc:
	@find ../C_porting_XTP/include/CXTPApi ../C_porting_XTP/src/Platform/CXTPApiImpl -name *.c* -or -name *.h* | xargs wc -l
	@find . -name 'xtp_convert_util.go' -o -name 'xtp_message.go' | xargs wc -l

src_wc:
	@find ../C_porting_XTP -name 'gen_cgo_code.py' | xargs wc -l
	@find . -name '*.go' ! -name 'xtp_convert_util.go' ! -name 'xtp_message.go' | xargs wc -l

fmt:
	@find .. -type f -name '*.sh' ! -name 'fmt.sh' ! -path '../ThirdParty/*'  | xargs dos2unix
	@find ../C_porting_XTP -type f -name '*.py' | xargs dos2unix
	@find ../go_src -type f -name '*' ! -path 'bin/*' | xargs dos2unix
	@find ../devenv -type f -name '*' ! -name '*.gz' ! -path '../devenv/go/*' ! -path '../devenv/.vagrant/*' | xargs dos2unix

prepare_g:
	cd ../C_porting_XTP && python3 gen_cgo_code.py

prepare_b:
	cd ../build && ./build.sh
    
prepare: 
	sudo go get github.com/urfave/cli
	sudo go get github.com/op/go-logging

build:
	@CGO_CFLAGS=$(CGO_CFLAGS) CGO_LDFLAGS=$(CGO_LDFLAGS) go build -o $(TARG) $(CGOFILES)
	@rm -rf $(out_dir)
	@mkdir $(out_dir)
	@mv $(TARG) $(out_dir)
	@cp -rf $(currdir)/../C_porting_XTP/lib/CXTPApi/*.so $(currdir)/../C_porting_XTP/lib/XTP/linux/*.so ../scripts/start.sh $(out_dir)
	#@cp -rf strategy_d.json $(out_dir)
	#@chmod +x $(out_dir)/*.sh

run:
	cd bin && ./start.sh
	
web:
	cd lctp && go run *.go
	cd ..

clean:
	@rm -rf $(TARG) bin

sogou:
	pidof fcitx | xargs kill
	pidof sogou-qimpanel | xargs kill
	nohup fcitx  1>/dev/null 2>/dev/null &
	nohup sogou-qimpanel  1>/dev/null 2>/dev/null &
