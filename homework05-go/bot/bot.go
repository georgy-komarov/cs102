package bot

import (
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api"
	"log"
	"net/http"
	"net/url"
	"strings"
)

var Bot *tgbotapi.BotAPI

func GetUpdatesChannel(token, proxy string) tgbotapi.UpdatesChannel {
	var err error

	if token == "" {
		log.Fatal("TOKEN variable not specified!")
	}

	// Init new Bot (with proxy)
	if proxy != "" {
		proxyUrl, _ := url.Parse(proxy)
		proxyClient := http.Client{Transport: &http.Transport{Proxy: http.ProxyURL(proxyUrl)}}

		Bot, err = tgbotapi.NewBotAPIWithClient(token, &proxyClient)
	} else {
		Bot, err = tgbotapi.NewBotAPI(token)
	}
	if err != nil {
		log.Fatal(err)
	}

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60
	updates, _ := Bot.GetUpdatesChan(u)
	return updates
}

func IsCommand(update *tgbotapi.Update, commands ...string) bool {
	for _, command := range commands {
		if command[0] != '/' {
			command = "/" + command
		}
		if strings.HasPrefix(update.Message.Text, command+" ") || update.Message.Text == command {
			return true
		}
	}
	return false
}
