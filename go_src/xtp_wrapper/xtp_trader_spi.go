package xtp_wrapper

/*
#cgo CFLAGS: -Wno-error=implicit-function-declaration -I../../C_porting_XTP/include/XTP -I../../C_porting_XTP/include/CXTPApi
#include <string.h>
#include "xtp_cmessage.h"
#include "LCxtp_trader_api.h"
*/
import "C"

import (
	//"os"
	"unsafe"

	. "github.com/leochan007/xtp.go/go_src/queue"
)

//export Go_trader_apiOnError
func Go_trader_apiOnError(spiPtr C.ulonglong, error_info *C.XTPRI) {
	ctpLogger.Infof("Go_trader_apiOnError error_info=", error_info)
}

//export Go_trader_apiOnDisconnected
func Go_trader_apiOnDisconnected(spiPtr C.ulonglong, session_id C.uint64_t, reason C.int)  {
	Enqueue(TraderQueue, getIntValOfPtr(spiPtr), TRADER_ONDISCONNECTED, nil,
	nil, -1, 1)
}

//export Go_trader_apiOnOrderEvent
func Go_trader_apiOnOrderEvent(spiPtr C.ulonglong, order_info *C.XTPQueryOrderRsp, error_info *C.XTPRI) {
	Enqueue(TraderQueue, getIntValOfPtr(spiPtr), TRADER_ONORDEREVENT, unsafe.Pointer(order_info),
		unsafe.Pointer(error_info), -1, 1)
}

//export Go_trader_apiOnTradeEvent
func Go_trader_apiOnTradeEvent(spiPtr C.ulonglong, trade_info *C.XTPQueryTradeRsp) {
	Enqueue(TraderQueue, getIntValOfPtr(spiPtr), TRADER_ONTRADEEVENT, unsafe.Pointer(trade_info), nil, -1, 1)
}

//export Go_trader_apiOnQueryOrder
func Go_trader_apiOnQueryOrder(spiPtr C.ulonglong, order_info *C.XTPQueryOrderRsp, error_info *C.XTPRI, request_id C.int, is_last C.bool) {
	Enqueue(TraderQueue, getIntValOfPtr(spiPtr), TRADER_ONQUERYORDER, unsafe.Pointer(order_info),
		unsafe.Pointer(error_info), (int)(request_id), (int)(is_last))
}

//export Go_trader_apiOnQueryTrade
func Go_trader_apiOnQueryTrade(spiPtr C.ulonglong, trade_info *C.XTPQueryTradeRsp, error_info *C.XTPRI, request_id C.int, is_last C.bool) {
	Enqueue(TraderQueue, getIntValOfPtr(spiPtr), TRADER_ONQUERYTRADE, unsafe.Pointer(trade_info),
		unsafe.Pointer(error_info), (int)(request_id), (int)(is_last))
}

//export Go_trader_apiOnQueryPosition
func Go_trader_apiOnQueryPosition(spiPtr C.ulonglong, position *C.XTPQueryStkPositionRsp_, error_info *C.XTPRI, request_id C.int, is_last C.bool) {
	Enqueue(TraderQueue, getIntValOfPtr(spiPtr), TRADER_ONQUERYPOSITION, unsafe.Pointer(position),
		unsafe.Pointer(error_info), (int)(request_id), (int)(is_last))
}

//export Go_trader_apiOnQueryAsset
func Go_trader_apiOnQueryAsset(spiPtr C.ulonglong, asset *C.XTPQueryAssetRsp_, error_info *C.XTPRI, request_id C.int, is_last C.bool) {
	Enqueue(TraderQueue, getIntValOfPtr(spiPtr), TRADER_ONQUERYASSET, unsafe.Pointer(asset),
		unsafe.Pointer(error_info), (int)(request_id), (int)(is_last))
}
