package main

import (
	. "./bot"
	"fmt"
	"github.com/anaskhan96/soup"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api"
	"strings"
	"time"
)

var days = []string{"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
var daysRussian = []string{"понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"}
var cache = make(map[string]string)

func index(slice []string, s string) int {
	for i, t := range slice {
		if t == s {
			return i
		}
	}
	return -1
}

func zip(slices ...[]string) ([][]string, error) {
	if len(slices) < 2 {
		return nil, fmt.Errorf("zip: you should pass 2 or more arguments")
	}
	length := len(slices[0])
	count := len(slices)
	for _, i := range slices {
		if length != len(i) {
			return nil, fmt.Errorf("zip: arguments must be of same length")
		}
	}

	r := make([][]string, length, length)

	for i := range slices[0] {
		r[i] = make([]string, count, count)
		for j, s := range slices {
			r[i][j] = s[i]
		}
	}

	return r, nil
}

func getCurrentDate() (string, time.Time) {
	var scheduleWeek string
	webPage, _ := getPage("M3139", "0")
	html := soup.HTMLParse(webPage)

	weekText := html.Find("h2", "class", "schedule-week").FullText()
	weekTextLower := strings.ToLower(weekText)
	if strings.Contains(weekTextLower, "нечетная") {
		scheduleWeek = "2"
	} else {
		scheduleWeek = "1"
	}
	date := time.Now()
	return scheduleWeek, date
}

func getPage(group, week string) (string, error) {
	if week != "" {
		week = week + "/"
	}
	url := fmt.Sprintf("%[1]s/%[2]s/%[3]sraspisanie_zanyatiy_%[2]s.htm", Domain, group, week)
	if val, ok := cache[url]; ok {
		return val, nil
	} else {
		body, err := soup.Get(url)
		if err == nil {
			cache[url] = body
		}
		return body, err
	}
}

func parseScheduleForDay(page string, num int) ([]string, []string, []string) {
	html := soup.HTMLParse(page)
	scheduleTable := html.Find("table", "id", fmt.Sprintf("%dday", num))
	if scheduleTable.Error == nil {
		var (
			timesList     []string
			locationsList []string
			lessonsList   []string
		)
		// Время проведения занятий
		times := scheduleTable.FindAll("td", "class", "time")
		for _, time_ := range times {
			timesList = append(timesList, strings.TrimSpace(time_.Find("span").Text()))
		}

		locations := scheduleTable.FindAll("td", "class", "room")
		for _, location := range locations {
			room := strings.TrimSpace(location.Find("dd").Text())
			building := strings.TrimSpace(location.Find("span").Text())
			locationAll := strings.TrimSpace(fmt.Sprintf("%s %s", building, room))
			locationsList = append(locationsList, locationAll)
		}

		// Название дисциплин и имена преподавателей
		lessons := scheduleTable.FindAll("td", "class", "lesson")
		for _, lesson := range lessons {
			lessonName := strings.TrimSpace(lesson.Find("dd").Text())
			teacher := strings.TrimSpace(lesson.Find("b").Text())
			lessonAll := strings.TrimSpace(fmt.Sprintf("%s %s", lessonName, teacher))
			lessonsList = append(lessonsList, lessonAll)
		}

		return timesList, locationsList, lessonsList
	}
	return nil, nil, nil
}

func getDayScheduleText(webPage string, day int) string {
	times, locations, lessons := parseScheduleForDay(webPage, day)
	if times != nil && locations != nil && lessons != nil {
		timetable, err := zip(times, locations, lessons)
		if err != nil {
			return "Ошибка парсинга расписания!"
		} else {
			var msg string
			for i := range timetable {
				msg += fmt.Sprintf("<b>%s</b>; %s; %s\n", times[i], locations[i], lessons[i])
			}
			return strings.TrimSpace(msg)
		}
	} else {
		return "В этот день пар нет."
	}
}

func StartHelp(update *tgbotapi.Update) {
	text := `Я бот, который получает расписание занятий в ИТМО. Мой создатель - Комаров Георгий из группы К3141.

Команды:
near - <группа> - ближайшее занятие
tomorrow - <группа> - расписание на завтра
all - <группа> <неделя> - расписание на всю неделю
monday - <группа> <неделя> - расписание на понедельник
tuesday - <группа> <неделя> - расписание на вторник
wednesday - <группа> <неделя> - расписание на среду
thursday - <группа> <неделя> - расписание на четверг
friday - <группа> <неделя> - расписание на пятницу
saturday - <группа> <неделя> - расписание на субботу
sunday - <группа> <неделя> - расписание на воскресенье

Недели:
0 - все недели
1 - чётная неделя
2 - нечётная неделя`

	msg := tgbotapi.NewMessage(update.Message.Chat.ID, text)
	_, _ = Bot.Send(msg)
}

func GetSchedule(update *tgbotapi.Update) {
	var msg string
	text := strings.Fields(update.Message.Text)
	if len(text) != 3 {
		msg = "Некорректный ввод"
	} else {
		command, group, week := text[0], text[1], text[2]
		if len(group) == 5 && (week == "0" || week == "1" || week == "2") {
			dayNum := index(days, command[1:]) + 1
			webPage, err := getPage(group, week)
			if err != nil {
				msg = "Ошибка загрузки страницы!"
			} else {
				msg = getDayScheduleText(webPage, dayNum)

			}
		} else {
			msg = "Некорректный ввод"
		}
	}
	tgmsg := tgbotapi.NewMessage(update.Message.Chat.ID, msg)
	tgmsg.ParseMode = "HTML"
	_, _ = Bot.Send(tgmsg)
}

func GetTomorrow(update *tgbotapi.Update) {
	var msg string
	text := strings.Fields(update.Message.Text)
	if len(text) != 2 {
		msg = "Некорректный ввод!"
	} else {
		group := text[1]
		if len(group) != 5 {
			msg = "Неверный номер группы!"
		} else {
			week, today := getCurrentDate()
			dayNum := int(today.Weekday())
			if dayNum == 7 {
				dayNum = 1
				if week == "1" {
					week = "2"
				} else {
					week = "1"
				}
			} else {
				dayNum += 1
			}
			webPage, err := getPage(group, week)
			if err != nil {
				msg = "Ошибка загрузки страницы!"
			} else {
				msg = getDayScheduleText(webPage, dayNum)
			}
		}
	}
	tgmsg := tgbotapi.NewMessage(update.Message.Chat.ID, msg)
	tgmsg.ParseMode = "HTML"
	_, _ = Bot.Send(tgmsg)
}

func GetAll(update *tgbotapi.Update) {
	var msg string
	text := strings.Fields(update.Message.Text)
	if len(text) != 3 {
		msg = "Некорректный ввод"
	} else {
		group, week := text[1], text[2]
		if len(group) == 5 && (week == "0" || week == "1" || week == "2") {
			webPage, err := getPage(group, week)
			if err != nil {
				msg = "Ошибка загрузки страницы!"
			} else {
				for day := 1; day <= 7; day++ {
					dayName := strings.Title(daysRussian[day-1])
					msg += fmt.Sprintf("%s:\n%s\n\n", dayName, getDayScheduleText(webPage, day))
				}
			}
		} else {
			msg = "Некорректный ввод"
		}
	}
	tgmsg := tgbotapi.NewMessage(update.Message.Chat.ID, msg)
	tgmsg.ParseMode = "HTML"
	_, _ = Bot.Send(tgmsg)
}

func GetNear(update *tgbotapi.Update) {
	var msg string
	text := strings.Fields(update.Message.Text)
	if len(text) != 2 {
		msg = "Некорректный ввод!"
	} else {
		group := text[1]
		if len(group) != 5 {
			msg = "Неверный номер группы!"
		} else {
			week, today := getCurrentDate()
			msg = getNextLesson(group, week, today)
		}
	}
	tgmsg := tgbotapi.NewMessage(update.Message.Chat.ID, msg)
	tgmsg.ParseMode = "HTML"
	_, _ = Bot.Send(tgmsg)
}

func getNextLesson(group, week string, day time.Time) string {
	webPage, err := getPage(group, week)
	if err != nil {
		return "Ошибка загрузки страницы!"
	} else {
		timesList, locationsList, lessonsList := parseScheduleForDay(webPage, int(day.Weekday()))
		for i, times := range timesList {
			timesSplit := strings.Split(times, "-")
			timeStart, _ := time.Parse("15:04", timesSplit[0])
			timeEnd, _ := time.Parse("15:04", timesSplit[1])

			if day.Sub(timeStart) >= 0 && day.Sub(timeEnd) <= 0 {
				if i != len(timesList)-1 {
					return fmt.Sprintf("Следующее занятие:\n<b>%s</b>; %s; %s", timesList[i+1], locationsList[i+1], lessonsList[i+1])
				}
				break // No further lessons today
			}
		}
		// Find next lesson this week
		for dayN := int(day.Weekday()) + 1; dayN <= 7; dayN++ {
			timesList, locationsList, lessonsList := parseScheduleForDay(webPage, dayN)
			if len(timesList) != 0 && len(locationsList) != 0 && len(lessonsList) != 0 {
				return fmt.Sprintf("Следующее занятие:\n<b>%s</b>; %s; %s", timesList[0], locationsList[0], lessonsList[0])
			}
		}
		// Find lesson next week
		if week == "1" {
			week = "2"
		} else {
			week = "1"
		}
		webPage, err := getPage(group, week)
		if err != nil {
			return "Ошибка загрузки страницы!"
		} else {
			for dayN := 0; dayN <= 7; dayN++ {
				timesList, locationsList, lessonsList := parseScheduleForDay(webPage, dayN)
				if len(timesList) != 0 && len(locationsList) != 0 && len(lessonsList) != 0 {
					return fmt.Sprintf("<b>%s</b>; %s; %s", timesList[0], locationsList[0], lessonsList[0])
				}
			}
		}
		return "Следующее занятие не найдено. Возможно такой группы не существует!"
	}
}

func main() {
	updates := GetUpdatesChannel(Token, Proxy)
	for updateObject := range updates {
		update := &updateObject
		// Skip, if it"s not text message
		if update.Message == nil {
			continue
		}
		if IsCommand(update, "start", "help") {
			go StartHelp(update)
		}
		if IsCommand(update, days...) {
			go GetSchedule(update)
		}
		if IsCommand(update, "tomorrow") {
			go GetTomorrow(update)
		}
		if IsCommand(update, "all") {
			go GetAll(update)
		}
		if IsCommand(update, "near") {
			go GetNear(update)
		}
	}
}
