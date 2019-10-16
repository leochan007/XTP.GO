package xtp_wrapper

/*
#cgo CFLAGS: -I../../C_porting_XTP/include/XTP -I../../C_porting_XTP/include/CXTPApi
#include <string.h>
#include "xtp_cmessage.h"
#include "LCxtp_quote_api.h"
*/
import "C"

import (
	. "github.com/leochan007/xtp.go/go_src/defs"
	. "github.com/leochan007/xtp.go/go_src/queue"

	"unsafe"
)

//#include "xtp_api_data_type.h"

//export Go_quote_apiOnSubMarketData
func Go_quote_apiOnSubMarketData(spiPtr C.ulonglong, ticker *C.XTPST, error_info *C.XTPRI, is_last C.bool) {
	ctpLogger.Infof("Go_quote_apiOnSubMarketData")
}

//export Go_quote_apiOnMarketData
func Go_quote_apiOnMarketData(spiPtr C.ulonglong, market_data *C.XTPMD) {
	marketData := new(MarketData)
	marketData.Exchange_id = (XTP_EXCHANGE_TYPE)(market_data.exchange_id)
	marketData.Ticker = GetGoString(&market_data.ticker[0])
	marketData.Last_price = (float64)(market_data.last_price)
	marketData.Qty = (int64)(market_data.qty)
	marketData.Date_time = (int64)(market_data.data_time)

	marketData.Open_price = (float64)(market_data.open_price)
	marketData.High_price = (float64)(market_data.high_price)
	marketData.Low_price = (float64)(market_data.low_price)
	marketData.Close_price = (float64)(market_data.close_price)

	for i := 0; i < 10; i++ {
		marketData.Bid[i] = (float64)(market_data.bid[i])
		marketData.Ask[i] = (float64)(market_data.ask[i])
		marketData.Bid_qty[i] = (int64)(market_data.bid_qty[i])
		marketData.Ask_qty[i] = (int64)(market_data.ask_qty[i])
	}
	ctpLogger.Infof("Go_quote_apiOnMarketData:%v", marketData)

	Enqueue(QuoteQueue, getIntValOfPtr(spiPtr), MD_ONDEPTHMARKETDATA, unsafe.Pointer(marketData), nil, -1, 1)
}

//export Go_quote_apiOnSubOrderBook
func Go_quote_apiOnSubOrderBook(spiPtr C.ulonglong, ticker *C.XTPST, error_info *C.XTPRI, is_last C.bool) {
	ctpLogger.Infof("Go_quote_apiOnSubOrderBook")
}

//export Go_quote_apiOnOrderBook
func Go_quote_apiOnOrderBook(spiPtr C.ulonglong, order_book *C.XTPOB) {
	ctpLogger.Infof("Go_quote_apiOnOrderBook. %v", order_book)
}
