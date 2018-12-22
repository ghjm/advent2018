package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type xy struct {
	x int
	y int
}

type state struct {
	pos xy
	equip rune
}

var depth int
var target xy

func atoi(s string) int {
	i, err := strconv.ParseInt(s, 10, 32)
	if err != nil { panic(err) }
	return int(i)
}

func readData22() {
	file, err := os.Open("input22.txt")
	if err != nil { panic(err) }
	defer func() { if err := file.Close(); err != nil { panic(err) } }()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		ss := strings.FieldsFunc(line, func(r rune) bool {return r == ' ' || r == ',' || r == ':'})
		if ss[0] == "depth" {
			depth = atoi(ss[1])
		} else if ss[0] == "target" {
			target.x = atoi(ss[1])
			target.y = atoi(ss[2])
		}
	}
}

var erosionValues [][]int = make([][]int, 0)

func initErosionValues(size xy, oldEv [][]int) [][]int {
	ev := make([][]int, size.y)
	for y := 0; y < size.y; y++ {
		ev[y] = make([]int, size.x)
		for x := 0; x < size.x; x++ {
			ev[y][x] = -1
		}
	}
	for y := 0; y < len(oldEv); y++ {
		for x := 0; x < len(oldEv[0]); x++ {
			ev[y][x] = oldEv[y][x]
		}
	}
	return ev
}

func getErosion(pos xy) int {
	if len(erosionValues) == 0 {
		erosionValues = initErosionValues(xy{100, 100}, erosionValues)
	}
	newsize := xy{len(erosionValues[0]), len(erosionValues)}
	sizeChanged := false
	for pos.x >= newsize.x {
		newsize.x *= 2
		sizeChanged = true
	}
	for pos.y >= newsize.y {
		newsize.y *= 2
		sizeChanged = true
	}
	if sizeChanged {
		erosionValues = initErosionValues(newsize, erosionValues)
	}
	if ero := erosionValues[pos.y][pos.x]; ero >= 0 {
		return ero
	}
	var geo int
	if pos.x == 0 && pos.y == 0 {
		geo = 0
	} else if pos.x == target.x && pos.y == target.y {
		geo = 0
	} else if pos.y == 0 {
		geo = pos.x * 16807
	} else if pos.x == 0 {
		geo = pos.y * 48271
	} else {
		geo = getErosion(xy{pos.x - 1, pos.y}) * getErosion(xy{pos.x, pos.y - 1})
	}
	ero := (geo + depth) % 20183
	erosionValues[pos.y][pos.x] = ero
	return ero
}

func getType(pos xy) int {
	return getErosion(pos) % 3
}

var usableEquip = [][]rune {{'c','t'}, {'c','n'}, {'t','n'}}
var moves = []xy {{-1,0}, {1,0}, {0,-1}, {0,1}}

func getNextStates(curState state) []state {
	nextStates := make([]state, 0)
	for _, eq := range usableEquip[getType(curState.pos)] {
		if eq != curState.equip {
			nextStates = append(nextStates, state {curState.pos, eq})
		}
	}
	for _, m := range moves {
		newPos := xy {curState.pos.x + m.x, curState.pos.y + m.y}
		if newPos.x >= 0 && newPos.y >= 0 {
			for _, eq := range usableEquip[getType(newPos)] {
				if eq == curState.equip {
					nextStates = append(nextStates, state {newPos, eq})
					break
				}
			}
		}
	}
	return nextStates
}

type QueueItem struct {
	value state
	priority int
	index int
}
type PriorityQueue []*QueueItem

func (pq PriorityQueue) Len() int {
	return len(pq)
}

func (pq PriorityQueue) Less(i, j int) bool {
	return pq[i].priority < pq[j].priority
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*QueueItem)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	item.index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

func abs(x int) int {
	if x < 0 {
		return -x
	} else {
		return x
	}
}

func findShortestPath(start state, dest state) ([]state, int, bool) {
	frontier := make(PriorityQueue, 1)
	frontier[0] = &QueueItem{state{xy{0, 0}, 't'}, 0, 0}
	heap.Init(&frontier)
	cameFrom := make(map[state]state)
	costSoFar := make(map[state]int)
	costSoFar[start] = 0
	for frontier.Len() > 0 {
		current := heap.Pop(&frontier).(*QueueItem).value
		if current == dest {
			break
		}
		nextStates := getNextStates(current)
		for _, nextState := range nextStates {
			newCost := costSoFar[current]
			if nextState.equip == current.equip {
				newCost += 1
			} else {
				newCost += 7
			}
			if csfNext, ok := costSoFar[nextState]; !ok || newCost < csfNext {
				costSoFar[nextState] = newCost
				priority := newCost + abs(dest.pos.x-nextState.pos.x) + abs(dest.pos.y-nextState.pos.y)
				heap.Push(&frontier, &QueueItem{nextState, priority, 0})
				cameFrom[nextState] = current
			}
		}
	}
	if _, ok := costSoFar[dest]; !ok {
		return make([]state, 0), 0, false
	}
	fromPath := make([]state, 1)
	fromPath[0] = dest
	for fromPath[0] != start {
		fromPath = append([]state{cameFrom[fromPath[0]]}, fromPath...)
	}
	return fromPath, costSoFar[dest], true
}

func main() {
	readData22()

	// Part A
	risk := 0
	for y := 0; y <= target.y; y++ {
		for x := 0; x <= target.x; x++ {
			risk += getType(xy{x,y})
		}
	}
	fmt.Println("Part A: ", risk)

	// Part B
	_, cost, ok := findShortestPath(state{xy{0,0},'t'}, state{target,'t'})
	if ok {
		fmt.Println("Part B: ", cost)
	} else {
		fmt.Println("Could not find a solution for Part B")
	}
}