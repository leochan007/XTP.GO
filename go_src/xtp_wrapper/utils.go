package xtp_wrapper

/*
#include <string.h>
*/
import "C"

import (
	"fmt"
	"unsafe"
)

func getIntValOfPtr(spiPtr C.ulonglong) uint64 {
	return uint64(spiPtr)
}

func GetInstrumentsPointer(input_arr []string) **C.char {
	var buf []*C.char
	for i, _ := range input_arr {
		buf = append(buf, (*C.char)(unsafe.Pointer(C.CString(input_arr[i]))))
	}
	pointer := (**C.char)(unsafe.Pointer(&buf[0]))
	return pointer
}

func CharsToGoString(any interface{}) string {
	value, ok := any.([]C.char)
	if !ok {
		fmt.Println("covert error")
		return ""
	}
	var charray []byte
	for i := range value {
		if value[i] != 0 {
			charray = append(charray, byte(value[i]))
		}
	}
	return string(charray)
}

func GetGoString(data_ptr *C.char) string {
	return C.GoStringN(data_ptr, (C.int)(C.strlen(data_ptr)))
}
