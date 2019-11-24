package main

import (
	. "./bot"
	"github.com/go-telegram-bot-api/telegram-bot-api"
)

func Echo(update *tgbotapi.Update) {
	msg := tgbotapi.NewMessage(update.Message.Chat.ID, update.Message.Text)
	_, _ = Bot.Send(msg)
}
func main() {
	updates := GetUpdatesChannel(Token, Proxy)
	for updateObject := range updates {
		update := &updateObject
		// Skip, if it's not text message
		if update.Message == nil {
			continue
		}
		if update.Message.Text != "" {
			go Echo(update)
		}
	}
}
