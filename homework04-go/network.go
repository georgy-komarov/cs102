package main

import "fmt"

func isFriend(arr []User, user User) bool {
	for _, friend := range arr {
		if friend == user {
			return true
		}
	}
	return false
}

func getNetwork(userId int, asEdgeList bool) [][]int {
	if asEdgeList {
		return getNetworkEdges(userId)
	}
	return getNetworkMatrix(userId)
}

func getNetworkEdges(userId int) [][]int {
	friendsItems := getFriends(userId, "").Response.Items
	friendsCount := len(friendsItems)
	result := make([][]int, friendsCount)

	for i, myFriend := range friendsItems {
		friendFriends := getFriends(myFriend.Id, "").Response.Items
		for j, friendFriend := range friendFriends {
			if isFriend(friendsItems, friendFriend) {
				result = append(result, []int{i, j})
			}
		}
	}
	return result
}

func getNetworkMatrix(userId int) [][]int {
	friendsItems := getFriends(userId, "").Response.Items
	friendsCount := len(friendsItems)

	result := make([][]int, friendsCount)
	for i := range result {
		result[i] = make([]int, friendsCount)
	}

	for i, myFriend := range friendsItems {
		friendFriends := getFriends(myFriend.Id, "").Response.Items
		for j, friendFriend := range friendFriends {
			if isFriend(friendsItems, friendFriend) {
				result[i][j] = 1
			}
		}
	}
	return result
}

func plotGraph() {
	fmt.Println("Not available in Golang!")
}
