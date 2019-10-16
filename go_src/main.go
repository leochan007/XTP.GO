package main

import (
	"fmt"
	"os"

	"github.com/urfave/cli"
	"github.com/op/go-logging"
	. "github.com/leochan007/xtp.go/go_src/xtp_wrapper"
)

type argT struct {
	QuoteHost  string `cli:"q,quotehost" usage:"quotehost" prompt:"type quotehost"`
	QuotePort  int    `cli:"p,quoteport" usage:"quoteport" prompt:"type quoteport"`
	TraderHost string `cli:"r,traderhost" usage:"traderhost" prompt:"type traderhost"`
	TraderPort int    `cli:"o,traderport" usage:"traderport" prompt:"type traderport"`
	Username   string `cli:"u,username" usage:"account" prompt:"type account"`
	Password   string `pw:"w,password" usage:"password of account" prompt:"type the password"`
	Debug      bool   `cli:"d,debug" usage:"debug flag" prompt:"if it is in debug mode"`
	File       string `cli:"f,file" usage:"file for strategy" prompt:"type json file name"`
}

type StockMap map[string]string

var (
	log = logging.MustGetLogger("main.go")
	Stocks = make(StockMap)
)

func main() {
	app := cli.NewApp()
	app.UseShortOptionHandling = true
	app.Commands = []cli.Command{
		{
			Name:  "short",
			Usage: "complete a task on the list",
			Flags: []cli.Flag{
				cli.StringFlag{Name: "quotehost, q"},
				cli.StringFlag{Name: "quoteport, p"},
				cli.StringFlag{Name: "traderhost, r"},
				cli.StringFlag{Name: "traderport, o"},
				cli.StringFlag{Name: "username, u"},
				cli.StringFlag{Name: "password, w"},
				cli.StringFlag{Name: "file, f"},
				cli.BoolFlag{Name: "debug, d"},
			},
			Action: func(c *cli.Context) error {
				fmt.Println("quotehost:", c.String("quotehost"))
				fmt.Println("quoteport:", c.String("quoteport"))
				fmt.Println("traderhost:", c.String("traderhost"))
				fmt.Println("traderport:", c.Int("traderport"))
				fmt.Println("username:", c.String("username"))
				fmt.Println("password:", c.String("password"))
				fmt.Println("file:", c.String("file"))
				fmt.Println("debug:", c.Bool("debug"))

				folder := "bin"

				trader_api := GoCreateLCTraderApi(1, folder)
				trader_spi := GoCreateLCTraderSpi()
				Go_trader_apiRegisterSpi(trader_api, trader_spi)
				loginResult := Go_trader_apiLogin(trader_api, c.String("traderhost"), c.Int("traderport"), c.String("username"), c.String("password"))

				if loginResult == 0 {
					fmt.Println("trader login OK.")
				} else {
					fmt.Println("trader failed.")
				}

				return nil
			},
		},
	}

	err := app.Run(os.Args)
	if err != nil {
		log.Fatal(err)
	}

}
