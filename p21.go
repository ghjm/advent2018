package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type progline [4]int
type program []progline
type regs [6]int

func opAdd(a, b int) int {
	return a + b
}

func opMult(a, b int) int {
	return a * b
}

func opAnd(a, b int) int {
	return a & b
}

func opOr(a, b int) int {
	return a | b
}

func opSet(a, b int) int {
	return a
}

func opGreater(a, b int) int {
	if a > b {
		return 1
	} else {
		return 0
	}
}

func opEqual(a, b int) int {
	if a == b {
		return 1
	} else {
		return 0
	}
}

func modeImm(regs regs, param int) int {
	return param
}

func modeReg(regs regs, param int) int {
	return regs[param]
}

type instruction struct {
	mnem string
	mode1 func(regs regs, param int) int
	mode2 func(regs regs, param int) int
	oper func(a, b int) int
}

var instructions = []instruction {
	instruction { "addr", modeReg, modeReg, opAdd },
	instruction { "addi", modeReg, modeImm, opAdd },
	instruction { "mulr", modeReg, modeReg, opMult },
	instruction { "muli", modeReg, modeImm, opMult },
	instruction { "banr", modeReg, modeReg, opAnd },
	instruction { "bani", modeReg, modeImm, opAnd },
	instruction { "borr", modeReg, modeReg, opOr },
	instruction { "bori", modeReg, modeImm, opOr },
	instruction { "setr", modeReg, nil, opSet },
	instruction { "seti", modeImm, nil, opSet },
	instruction { "gtir", modeImm, modeReg, opGreater },
	instruction { "gtri", modeReg, modeImm, opGreater },
	instruction { "gtrr", modeReg, modeReg, opGreater },
	instruction { "eqir", modeImm, modeReg, opEqual },
	instruction { "eqri", modeReg, modeImm, opEqual },
	instruction { "eqrr", modeReg, modeReg, opEqual },
}

func findMnem(mnem string) int {
	for i := range instructions {
		if instructions[i].mnem == mnem {
			return i
		}
	}
	panic("Invalid instruction " + mnem)
}

func readData(filename string) (program, int) {
	file, err := os.Open(filename)
	if err != nil { panic(err) }
	defer func() { if err := file.Close(); err != nil { panic(err) } }()

	scanner := bufio.NewScanner(file)
	var ipreg int
	var program program
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "#ip") {
			ipreg64, err := strconv.ParseInt(line[4:], 10, 32)
			if err != nil { panic(err) }
			ipreg = int(ipreg64)
		} else {
			toks := strings.Fields(line)
			var progline progline
			progline[0] = findMnem(toks[0])
			for i := 1; i <= 3; i++ {
				p64, err := strconv.ParseInt(toks[i], 10, 32)
				if err != nil { panic(err) }
				progline[i] = int(p64)
			}
			program = append(program, progline)
		}
	}
	return program, ipreg
}

func op(regs regs, progline progline) regs {
	mode1 := instructions[progline[0]].mode1
	mode2 := instructions[progline[0]].mode2
	oper := instructions[progline[0]].oper
	newregs := regs
	var a = 0
	if mode1 != nil {
		a = mode1(regs, progline[1])
	}
	var b = 0
	if mode2 != nil {
		b = mode2(regs, progline[2])
	}
	newregs[progline[3]] = oper(a,b)
	return newregs
}

func runProgram(program program, ipreg int, r0init int, limit int) regs {
	var regs regs
	regs[0] = r0init
	ip := 0
	count := 0
	prev_regs := regs
	seen := make(map[int]bool)
	for 0 <= ip && ip < len(program) {
		regs[ipreg] = ip
		if ip == 28 {
			count++
			if limit > 0 && count >= limit {
				return regs
			}
			if seen[regs[5]] {
				return prev_regs
			} else {
				prev_regs = regs
				seen[regs[5]] = true
			}
		}
		regs = op(regs, program[ip])
		ip = regs[ipreg] + 1
	}
	return regs
}

func main() {
	program, ipreg := readData("input21.txt")
	regs := runProgram(program, ipreg, 0, 1)
	fmt.Println("Part A:", regs[5])
	regs = runProgram(program, ipreg, 0, 0)
	fmt.Println("Part B:", regs[5])
}