package xtp_wrapper

/*
#cgo CFLAGS: -I../../C_porting_XTP/include/XTP -I../../C_porting_XTP/include/CXTPApi
#include <string.h>
#include "xtp_cmessage.h"
#include "LCxtp_trader_api.h"
*/
import "C"

import (
	"os"
	"unsafe"
)

func GoCreateLCTraderApi(client_id int, folder string) unsafe.Pointer {
	folder = folder + "/trader/"
	os.MkdirAll(folder, 0777)
	cs := C.CString(folder)
	defer C.free(unsafe.Pointer(cs))
	return C.CreateLCTraderApi(C.uint8_t(client_id), cs, 0)
}

func GoCreateLCTraderSpi() unsafe.Pointer {
	return C.CreateLCTraderSpi()
}

func Go_trader_apiRegisterSpi(trader_api unsafe.Pointer, trader_spi unsafe.Pointer) {
	C._trader_apiRegisterSpi(trader_api, trader_spi)
}

//_quote_apiLogin(void * pLC_Api, const char* ip, int port, const char* user, const char* password, XTP_PROTOCOL_TYPE sock_type);
func Go_trader_apiLogin(trader_api unsafe.Pointer, ip_addr string, port int, user string, pwd string) int {
	ip_addr_s := C.CString(ip_addr)
	defer C.free(unsafe.Pointer(ip_addr_s))
	user_s := C.CString(user)
	defer C.free(unsafe.Pointer(user_s))
	pwd_s := C.CString(pwd)
	defer C.free(unsafe.Pointer(pwd_s))
	return int(C._trader_apiLogin(trader_api, ip_addr_s, C.int(port), user_s, pwd_s, C.XTP_PROTOCOL_TCP))
}

func GoReleaseLCTraderApi(trader_api unsafe.Pointer) {
	C.ReleaseLCTraderApi(&trader_api)
}

func GoReleaseLCTraderSpi(trader_api unsafe.Pointer) {
	C.ReleaseLCTraderSpi(&trader_api)
}
