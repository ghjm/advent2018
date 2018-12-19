import sys
import re

def read_data():
    program = list()
    ipreg = None
    with open('input19.txt', 'r') as f:
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
    while 0 <= ip < len(program) and (limit is None or count <= limit):
        count += 1
        regs[ipreg] = ip
        regs = op(regs, *program[ip])
        ip = regs[ipreg] + 1
    return regs

def main():
    program, ipreg = read_data()
    print 'Part A:', run_program(program, ipreg, [0, 0, 0, 0, 0, 0])[0]
    regs = run_program(program, ipreg, [1, 0, 0, 0, 0, 0], limit=10000)
    print 'Part B:', sum_of_divisors(max(regs))

if __name__ == '__main__':
    main()
