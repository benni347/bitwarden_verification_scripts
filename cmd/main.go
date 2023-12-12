package main

import (
	"net/http"
	"os"
	"time"

	"github.com/benni347/bitwarden_verification_scripts/pkg/utils"

	_ "net/http/pprof"

	// "github.com/pkg/profile"
	log "github.com/sirupsen/logrus"
	cli "github.com/urfave/cli/v2"
	"github.com/urfave/cli/v2/altsrc"
)

const appName = "bitwarden-verification-scripts"

var (
	Hash    = ""
	Version = "develop"
)

func main() {
	app := cli.NewApp()
	app.Name = appName
	app.Usage = "An internal mock CRM service"
	app.Version = Version
	app.Authors = []*cli.Author{
		{
			Name:  "Cédric Skwar",
			Email: "cdrc@5y5.one",
		},
	}
	// Define flags
	flags := []cli.Flag{
		&cli.StringFlag{Name: "config"},
		altsrc.NewStringFlag(&cli.StringFlag{
			Name:  "log.level",
			Value: log.InfoLevel.String(),
			Usage: "Log level",
		}),
		altsrc.NewBoolFlag(&cli.BoolFlag{
			Name:  "profile",
			Value: false,
			Usage: "Activates Profiling support via 'net/http/pprof'",
		}),
	}
	app.Suggest = true
	app.Compiled = time.Now()

	app.Before = func(c *cli.Context) error {
		err := altsrc.InitInputSourceWithContext(flags, altsrc.NewYamlSourceFromFlagFunc("config"))(c)
		if err != nil {
			return err
		}
		return nil
	}

	// Define action to be executed when the app is run
	app.Action = func(c *cli.Context) error {
		initApp(c)
		runApp(c)
		return nil
	}

	app.Flags = flags
	// Run the app
	err := app.Run(os.Args)
	if err != nil {
		panic(err)
	}
}

func initApp(c *cli.Context) {
	// logging
	initLogging(c)
}

// initLogging
func initLogging(c *cli.Context) {
	logLevel, _ := log.ParseLevel(c.String("log.level"))
	utils.NewLogger(logLevel)
	utils.Logger.WithField("log-level", logLevel).Debug("logger setup")
}

func runApp(c *cli.Context) {
	utils.Logger.WithFields(log.Fields{
		"Profiling": c.Bool("profile"),
	}).Debug("Programm Arguments")

	utils.Logger.WithFields(log.Fields{
		"appStart": appName,
	}).Debug("started")

	if c.Bool("profile") {
		go func() {
			utils.Logger.Debug(http.ListenAndServe("localhost:6060", nil))
		}()
	}
}
