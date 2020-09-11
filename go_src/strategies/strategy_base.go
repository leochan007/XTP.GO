package strategies

import (
	. "xtp.go/defs"
)

type IStrategy interface {
	OnMarketData(marketData *MarketData)
}
