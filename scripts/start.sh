#!/bin/bash
cur_dir=`pwd`
CGO_LDFLAGS="-L$cur_dir -lCXTPApi -lxtpquoteapi -lxtptraderapi" LD_LIBRARY_PATH="$cur_dir" \
    ./go_xtp_trader --file strategy_d.json --host 0.0.0.0:18080
    