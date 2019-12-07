package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"net/http"
	"net/url"
	"strconv"
	"time"
)

func Get(url string, params url.Values, timeout, maxRetries int, backoffFactor float64) (*http.Response, error) {
	client := http.Client{Timeout: time.Duration(timeout) * time.Second}

	// Add config vars
	params.Add("access_token", AccessToken)
	params.Add("v", V)

	for retry := 0; retry < maxRetries; retry++ {
		response, err := client.PostForm(url, params)
		if err != nil {
			if retry == maxRetries-1 {
				return nil, err
			}
			time.Sleep(time.Duration(backoffFactor * math.Pow(2, float64(retry))))
		} else {
			return response, nil
		}
	}
	return nil, nil
}

func getFriends(userId int, fields string) interface{} {
	params := url.Values{}
	params.Add("user_id", strconv.Itoa(userId))
	params.Add("fields", fields)

	url := fmt.Sprintf("%s/friends.get", Domain)

	resp, _ := Get(url, params, 5, 3, 0.3)
	body, _ := ioutil.ReadAll(resp.Body)

	var jsonMap map[string]interface{}
	_ = json.Unmarshal(body, &jsonMap)
	return jsonMap
}
