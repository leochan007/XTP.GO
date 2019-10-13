package defs

type XTP_EXCHANGE_TYPE int32

const (
	XTP_EXCHANGE_SH XTP_EXCHANGE_TYPE = 1 + iota
	XTP_EXCHANGE_SZ
	XTP_EXCHANGE_UNKNOWN
)

type MarketData struct {
	Exchange_id XTP_EXCHANGE_TYPE
	Ticker      string

	Date_time int64

	Last_price float64
	Qty        int64

	Open_price  float64
	High_price  float64
	Low_price   float64
	Close_price float64

	Bid     [10]float64
	Ask     [10]float64
	Bid_qty [10]int64
	Ask_qty [10]int64
}
