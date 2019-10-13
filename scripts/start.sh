#!/bin/bash
cur_dir=`pwd`
CGO_LDFLAGS="-L$cur_dir -lCTPCApi -lthostmduserapi -lthosttraderapi" LD_LIBRARY_PATH="$cur_dir" ./go_ctp_trader -f=strategy_d.json -H=0.0.0.0:18080
