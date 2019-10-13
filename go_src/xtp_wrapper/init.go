package xtp_wrapper

import (
	"os"
	"unsafe"

	"github.com/op/go-logging"
)

var Md_api unsafe.Pointer
var Md_spi unsafe.Pointer

var md_id int64
var trader_id int64

var needToClose bool

var ctpLogger *logging.Logger

var format = logging.MustStringFormatter(
	`%{color}%{time:15:04:05.000}  [%{level:.4s}] %{shortfunc} ---> %{color:reset} %{message}`,
)

func SafeShutdown() {
	needToClose = true
}

func init() {
	ctpLogger = logging.MustGetLogger("rest")

	backend1 := logging.NewLogBackend(os.Stderr, "", 0)
	backend2 := logging.NewLogBackend(os.Stderr, "", 0)
	backend2Formatter := logging.NewBackendFormatter(backend2, format)
	backend1Leveled := logging.AddModuleLevel(backend1)
	logging.SetBackend(backend1Leveled, backend2Formatter)

	needToClose = false
	md_id = 0
	trader_id = 0
	go query_handle()
	go quote_handle()
	//go trader_handle()
}
