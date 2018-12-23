package main

import "strconv"

const MaxUint = ^uint(0)
const MinUint = 0
const MaxInt = int(MaxUint >> 1)
const MinInt = -MaxInt - 1

func atoi(s string) int {
	i, err := strconv.ParseInt(s, 10, 32)
	if err != nil { panic(err) }
	return int(i)
}

func abs(x int) int {
	if x < 0 {
		return -x
	} else {
		return x
	}
}

