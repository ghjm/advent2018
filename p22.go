package main

import (
	"bufio"
	"container/heap"
	"flag"
	"fmt"
	"log"
	"os"
	"runtime/pprof"
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

var boundsMargin int = 100
func getErosion(pos xy) int {
	if len(erosionValues) == 0 {
		erosionValues = initErosionValues(xy{100, 100}, erosionValues)
	}
	newsize := xy{len(erosionValues[0]), len(erosionValues)}
	sizeChanged := false
	for pos.x + boundsMargin >= newsize.x {
		newsize.x *= 2
		sizeChanged = true
	}
	for pos.y + boundsMargin >= newsize.y {
		newsize.y *= 2
		sizeChanged = true
	}
	if sizeChanged {
		erosionValues = initErosionValues(newsize, erosionValues)
	}
	if ero := erosionValues[pos.y][pos.x]; ero >= 0 {
		return ero
	}
	for y := 0; y <= pos.y + boundsMargin; y++ {
		for x := 0; x <= pos.x + boundsMargin; x++ {
			if erosionValues[y][x] < 0 {
				var geo int
				if x == 0 && y == 0 {
					geo = 0
				} else if x == target.x && y == target.y {
					geo = 0
				} else if y == 0 {
					geo = x * 16807
				} else if x == 0 {
					geo = y * 48271
				} else {
					geo = erosionValues[y][x-1] * erosionValues[y-1][x]
				}
				ero := (geo + depth) % 20183
				erosionValues[y][x] = ero
			}
		}
	}
	return erosionValues[pos.y][pos.x]
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

var cpuprofile = flag.String("cpuprofile", "", "write cpu profile to file")

func main() {

	// Enable profiling support
	flag.Parse()
	if *cpuprofile != "" {
		f, err := os.Create(*cpuprofile)
		if err != nil {
			log.Fatal(err)
		}
		_ = pprof.StartCPUProfile(f)
		defer pprof.StopCPUProfile()
	}

	readData22()

	// Precalculate
	_ = getErosion(xy{target.x + 100, target.y + 100})

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