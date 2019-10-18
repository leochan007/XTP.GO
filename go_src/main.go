package main

import (
	"fmt"
	"os"
	"os/signal"

	"sync"
	"github.com/urfave/cli"
	"github.com/op/go-logging"
	. "github.com/leochan007/xtp.go/go_src/xtp_wrapper"
)

type StockMap map[string]string

var (
	log = logging.MustGetLogger("go_xtp_trader")
	Stocks = make(StockMap)
	wg sync.WaitGroup
	c chan os.Signal
)

func waitForSignal() {
	LOOP:
	for {
		select {
			case <-c:
			break LOOP
		default:
		}
	}

	log.Info("---waitForSignal---")
	wg.Done()
}

func main() {
	
	c = make(chan os.Signal, 1)
    signal.Notify(c, os.Interrupt, os.Kill)

	var quotehost string
	var quoteport int
	var traderhost string
	var traderport int
	var username string
	var password string
	var softKey string
	var host string
	var file string
	var debug bool

	app := cli.NewApp()
	app.UseShortOptionHandling = true
	app.Version = "0.0.1"
	app.Flags = []cli.Flag {
		cli.StringFlag{Name: "quotehost, q", Destination: &quotehost},
		cli.IntFlag{Name: "quoteport, p", Destination: &quoteport},
		cli.StringFlag{Name: "traderhost, r", Destination: &traderhost},
		cli.IntFlag{Name: "traderport, o", Destination: &traderport},
		cli.StringFlag{Name: "username, u", Destination: &username},
		cli.StringFlag{Name: "password, w", Destination: &password},
		cli.StringFlag{Name: "softkey, k", Destination: &softKey},
		cli.StringFlag{Name: "host, H", Destination: &host},
		cli.StringFlag{Name: "file, f", Destination: &file},
		cli.BoolFlag{Name: "debug, d", Destination: &debug},
	}

	app.Action = func(c *cli.Context) error {
		fmt.Println("Hello %q", c.Args())

		fmt.Println("quotehost:", quotehost)
		fmt.Println("quoteport:", quoteport)
		fmt.Println("traderhost:", traderhost)
		fmt.Println("traderport:", traderport)
		fmt.Println("username:", username)
		fmt.Println("password:", password)
		fmt.Println("softKey:", softKey)
		fmt.Println("file:", file)
		fmt.Println("debug:", debug)

		folder := "xtp_con"

		/*
		trader_api := GoCreateLCTraderApi(1, folder)
		trader_spi := GoCreateLCTraderSpi()

		Go_trader_apiRegisterSpi(trader_api, trader_spi)

		session_id := Go_trader_apiLogin(trader_api, traderhost, traderport, username, password, softKey)

		if session_id != 0 {
			fmt.Println("--- trader login OK.")
		} else {
			fmt.Println("--- trader failed.")
		}
		*/

		quote_api := GoCreateLCQuoteApi(2, folder)
		quote_spi := GoCreateLCQuoteSpi()

		Go_quote_apiRegisterSpi(quote_api, quote_spi)
		
		session_id := Go_quote_apiLogin(quote_api, quotehost, quoteport, username, password)

		if session_id != 0 {
			fmt.Println("--- md login OK. session_id=", session_id)
		} else {
			fmt.Println("--- md failed.")
		}

		wg.Add(1)
		go waitForSignal()
		wg.Wait()

		return nil
	  }

	err := app.Run(os.Args)

	if err != nil {
		log.Fatal(err)
	}

}
