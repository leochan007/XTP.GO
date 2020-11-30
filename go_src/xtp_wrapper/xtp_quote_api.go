package xtp_wrapper

/*
#cgo CFLAGS: -Wno-error=implicit-function-declaration -I../../C_porting_XTP/include/XTP -I../../C_porting_XTP/include/CXTPApi
#cgo LDFLAGS: -L../../C_porting_XTP/lib/CXTPApi -lCXTPApi -lxtpquoteapi -lxtptraderapi
#include <string.h>
#include "xtp_cmessage.h"
#include "LCxtp_quote_api.h"
*/
import "C"

import (
	"os"
	"unsafe"
)

func GoCreateLCQuoteApi(client_id int8, folder string) unsafe.Pointer {
	folder = folder + "/quote/"
	os.MkdirAll(folder, 0777)
	cs := C.CString(folder)
	defer C.free(unsafe.Pointer(cs))
	return C.CreateLCQuoteApi(C.uint8_t(client_id), cs, C.XTP_LOG_LEVEL_DEBUG)
}

func GoCreateLCQuoteSpi() unsafe.Pointer {
	return C.CreateLCQuoteSpi()
}

func Go_quote_apiRegisterSpi(quote_api unsafe.Pointer, quote_spi unsafe.Pointer) {
	C._quote_apiRegisterSpi(quote_api, quote_spi)
}

func Go_quote_apiLogin(quote_api unsafe.Pointer, ip_addr string, port int, user string, pwd string) int {
	ip_addr_s := C.CString(ip_addr)
	defer C.free(unsafe.Pointer(ip_addr_s))
	user_s := C.CString(user)
	defer C.free(unsafe.Pointer(user_s))
	pwd_s := C.CString(pwd)
	defer C.free(unsafe.Pointer(pwd_s))
	return int(C._quote_apiLogin(quote_api, ip_addr_s, C.int(port), user_s, pwd_s, C.XTP_PROTOCOL_UDP))
}

func Go_quote_apiSubscribeMarketData(quote_api unsafe.Pointer, stocks map[string]string, e_type int) uint64 {
	buf := make([]*C.char, 0)
	for k, _ := range stocks {
		uptr := unsafe.Pointer(C.CString(k))
		defer C.free(uptr)
		buf = append(buf, (*C.char)(uptr))
	}
	pointer := (**C.char)(unsafe.Pointer(&buf[0]))
	return uint64(C._quote_apiSubscribeMarketData(quote_api, pointer, C.int(len(stocks)), C.XTP_EXCHANGE_TYPE(e_type)))
}

func GoReleaseLCQuoteApi(quote_api unsafe.Pointer) {
	C.ReleaseLCQuoteApi(&quote_api)
}

func GoReleaseLCQuoteSpi(quote_api unsafe.Pointer) {
	C.ReleaseLCQuoteSpi(&quote_api)
}
