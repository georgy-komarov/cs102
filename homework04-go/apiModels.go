package main

type User struct {
	id          int
	firstName   string
	lastName    string
	online      int
	deactivated string
	bdate       string
}

type Message struct {
	date   int
	fromId int
	id     int
	out    int
	peerId int
	text   string
}
