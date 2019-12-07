package main

type User struct {
	Id          int
	First_name  string
	Last_name   string
	Online      int
	Deactivated string
	Bdate       string
}

type Message struct {
	date   int
	fromId int
	id     int
	out    int
	peerId int
	text   string
}

type Response struct {
	Items []User
	Count float64
}

type FriendsResponse struct {
	Response Response
}
