# seti 123 0 5      0:  r5 = 123
# bani 5 456 5      1:  r5 = r5 and 456
# eqri 5 72 5       2:  r5 = r5 == 72
# addr 5 3 3        3:  ip = ip + r5   (if r5 == 1 goto 5)
# seti 0 0 3        4:  goto 1 (infinite loop)

# seti 0 5 5        5:  r5 = 0101
# bori 5 65536 2    6:  r2 = r5 or 1 0000 0000 0000 0000
# seti 10362650 3 5 7:  r5 = 1001 1110 0001 1111 0001 1010
# bani 2 255 4      8:  r4 = r2 and 1111 1111
# addr 5 4 5        9:  r5 = r4 + r5
# bani 5 16777215 5 10: r5 = r5 and 1111 1111 1111 1111 1111 1111
# muli 5 65899 5    11: r5 = r5 * 0001 0000 0001 0110 1011
# bani 5 16777215 5 12: r5 = r5 and 1111 1111 1111 1111 1111 1111
# gtir 256 2 4      13: r4 = 1 0000 0000 > r2
# addr 4 3 3        14: goto ip + r4   (if r4 == 1 goto 16)
# addi 3 1 3        15: goto 17
# seti 27 4 3       16: goto 28
# seti 0 3 4        17: r4 = 0
# addi 4 1 1        18: r1 = r4 + 1
# muli 1 256 1      19: r1 = r1 * 1 0000 0000
# gtrr 1 2 1        20: r1 = r1 > r2
# addr 1 3 3        21: goto ip + r1   (if r1 == 1 goto 23)
# addi 3 1 3        22: goto 24
# seti 25 2 3       23: goto 26
# addi 4 1 4        24: r4 = r4 + 1
# seti 17 7 3       25: goto 18
# setr 4 0 2        26: r2 = r4
# seti 7 8 3        27: goto 8
# eqrr 5 0 4        28: r4 = r5 == r0
# addr 4 3 3        29: goto ip + r4   (if r4 == 1 halt)
# seti 5 1 3        30: goto 6

import sys
import re

def read_data():
    program = list()
    ipreg = None
    with open('input21.txt', 'r') as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('#ip'):
                ipreg = int(line[4:])
            else:
                toks = line.split(' ')
                program.append((toks[0], tuple([int(t) for t in toks[1:]])))
    return program, ipreg

def ad_imm(regs, param):
    return param

def ad_reg(regs, param):
    return regs[param]

instructions = {
    'addr': (ad_reg, ad_reg, lambda a, b: a + b),
    'addi': (ad_reg, ad_imm, lambda a, b: a + b),
    'mulr': (ad_reg, ad_reg, lambda a, b: a * b),
    'muli': (ad_reg, ad_imm, lambda a, b: a * b),
    'banr': (ad_reg, ad_reg, lambda a, b: a & b),
    'bani': (ad_reg, ad_imm, lambda a, b: a & b),
    'borr': (ad_reg, ad_reg, lambda a, b: a | b),
    'bori': (ad_reg, ad_imm, lambda a, b: a | b),
    'setr': (ad_reg, None, lambda a, b: a),
    'seti': (ad_imm, None, lambda a, b: a),
    'gtir': (ad_imm, ad_reg, lambda a, b: 1 if a > b else 0),
    'gtri': (ad_reg, ad_imm, lambda a, b: 1 if a > b else 0),
    'gtrr': (ad_reg, ad_reg, lambda a, b: 1 if a > b else 0),
    'eqir': (ad_imm, ad_reg, lambda a, b: 1 if a == b else 0),
    'eqri': (ad_reg, ad_imm, lambda a, b: 1 if a == b else 0),
    'eqrr': (ad_reg, ad_reg, lambda a, b: 1 if a == b else 0),
}

def op(regs, mnem, op_params):
    instr = instructions[mnem]
    new_regs = list(regs)
    new_regs[op_params[2]] = instr[2](*(0 if instr[i] is None else instr[i](regs, op_params[i]) for i in [0, 1]))
    return new_regs

def sum_of_divisors(n):
    s = 0
    for i in xrange(1, int(n**0.5)):
        if n % i == 0:
            s += i + int(n/i)
    return s

def run_program(program, ipreg, init_regs, limit=None):
    regs = list(init_regs)
    ip = 0
    count = 0
    seen = set()
    prev_regs = regs
    while 0 <= ip < len(program) and (limit is None or count <= limit):
        regs[ipreg] = ip
        if ip == 28:
            count += 1
            if limit is not None and count >= limit:
                return regs
            print count, regs[5]
            if regs[5] in seen:
                return prev_regs
            else:
                prev_regs = regs
            seen.add(regs[5])
        regs = op(regs, *program[ip])
        ip = regs[ipreg] + 1
    return regs

def main():
    program, ipreg = read_data()
    regs = run_program(program, ipreg, [0, 0, 0, 0, 0, 0], limit=1)
    print 'Part A:', regs[5]
    regs = run_program(program, ipreg, [0, 0, 0, 0, 0, 0])
    print 'Part B:', regs[5]

if __name__ == '__main__':
    main()

