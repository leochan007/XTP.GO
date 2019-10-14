package xtp_wrapper

/*
#cgo CFLAGS: -I../../C_porting_XTP/include/XTP
#include <stdlib.h>
#include <string.h>
#include "xtp_api_data_type.h"
*/
import "C"

func TXTPTradeTypeType2CharArray(orignalStr string, output *C.TXTPTradeTypeType) {
    for i := 0; i < len(orignalStr); i++ {
        (*output)[i] = C.char(orignalStr[i])
    }
}

func TXTPOrderTypeType2CharArray(orignalStr string, output *C.TXTPOrderTypeType) {
    for i := 0; i < len(orignalStr); i++ {
        (*output)[i] = C.char(orignalStr[i])
    }
}
