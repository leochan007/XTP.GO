package strategies

import (
	. "leochan007/xtp.go/go_src/defs"
)

type IStrategy interface {
	OnMarketData(marketData *MarketData)
}
