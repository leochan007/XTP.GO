package xtp_wrapper

/*
#cgo CFLAGS: -I../../C_porting_XTP/include/XTP -I../../C_porting_XTP/include/CXTPApi
#include <string.h>
#include "xtp_cmessage.h"
#include "LCxtp_quote_api.h"
#include "LCxtp_trader_api.h"
*/
import "C"

import (
	"fmt"

	. "github.com/leochan007/xtp.go/go_src/defs"
	. "github.com/leochan007/xtp.go/go_src/queue"
)

func query_handle() {
	defer close(QueryQueue)
	for {
		select {
		case data, ok := <-QueryQueue:
			if !ok {
				continue
			}
			switch data.Type {
			default:
			}
		}
		if needToClose {
			break
		}
	}
}

func quote_handle() {
	// defer close(QuoteQueue)
	for {
		val, ok, _ := QuoteQueue.Get()
		if !ok {
			//ctpLogger.Infof("no OK!!!\n")
			continue
		}
		/*
			if q := QuoteQueue.Quantity(); q != 0 {
				ctpLogger.Errorf("Quantity Error: [%v] <>[%v]", q, 0)
			}
		*/
		data, ok1 := val.(ChanMsg)
		if !ok1 {
			continue
		}
		switch data.Type {
		case MD_ONDEPTHMARKETDATA:
			market_data := (*MarketData)(data.Data)
			ctpLogger.Infof("%v\n", market_data)
		default:
		}
		if needToClose {
			break
		}
	}
}

func trader_handle() {
	// defer close(TraderQueue)
	for {
		val, ok, _ := TraderQueue.Get()
		if !ok {
			continue
		}
		/*
			if q := TraderQueue.Quantity(); q != 0 {
				ctpLogger.Errorf("Quantity Error: [%v] <>[%v]", q, 0)
			}
		*/
		data, ok1 := val.(ChanMsg)
		if !ok1 {
			continue
		}
		switch data.Type {
		case MD_ONDEPTHMARKETDATA:
			market_data := (*MarketData)(data.Data)
			ctpLogger.Infof("%v\n", market_data)
		case TRADER_ONDISCONNECTED:
			fmt.Println("TRADER_ONDISCONNECTED!")
		case TRADER_ONORDEREVENT:
			fmt.Println("TRADER_ONORDEREVENT!")
			order_info := (*C.XTPQueryOrderRsp)(data.Data)
			fmt.Printf("[%v] [%v] [%v] market:%v\n", order_info.order_xtp_id, order_info.order_client_id,
				GetGoString(&order_info.ticker[0]),
				(XTP_EXCHANGE_TYPE)(order_info.market))
		default:
		}
		if needToClose {
			break
		}
	}
}
