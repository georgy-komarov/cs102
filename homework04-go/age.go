package main

import (
	"github.com/montanaflynn/stats"
	"time"
)

func agePredict(userId int) float64 {
	friendsItems := getFriends(userId, "bdate").Response.Items
	currentDate := time.Now()
	var result []float64
	for _, friend := range friendsItems {
		birthday, err := time.Parse("2.1.2006", friend.Bdate)
		if err == nil {
			age := currentDate.Sub(birthday).Hours() / 24.0 / 365.25
			result = append(result, age)
		}
	}
	median, _ := stats.Median(result)
	medianR, _ := stats.Round(median, 1)
	return medianR
}
