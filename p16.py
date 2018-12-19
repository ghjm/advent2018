import sys
import re

def read_data():
    samples = list()
    program = list()
    r_bef = re.compile('Before: +\[([0123456789, ]+)\]')
    r_aft = re.compile('After: +\[([0123456789, ]+)\]')
    r_opcode = re.compile('^[0123456789 ]+$')
    with open('input16.txt') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.rstrip()
            if line != '':
                m_bef = r_bef.match(line)
                m_opcode = r_opcode.match(line)
                if m_bef:
                    before = [int(x) for x in m_bef.groups()[0].replace(' ','').split(',')]
                    line = f.readline().rstrip()
                    opcode = [int(x) for x in line.split(' ')]
                    line = f.readline().rstrip()
                    m_aft = r_aft.match(line)
                    if not m_aft:
                        print 'Syntax error'
                        sys.exit(1)
                    after = [int(x) for x in m_aft.groups()[0].replace(' ','').split(',')]
                    samples.append({
                        'before': before,
                        'opcode': opcode,
                        'after': after
                    })
                elif m_opcode:
                    program.append([int(x) for x in line.split(' ')])
    return samples, program

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def bitwise_and(a, b):
    return a & b

def bitwise_or(a, b):
    return a | b

def assignment(a, b):
    return a

def greater_test(a, b):
    if a > b:
        return 1
    else:
        return 0

def equal_test(a, b):
    if a == b:
        return 1
    else:
        return 0

def reg_reg_op(regs, opcode, oper):
    new_regs = [r for r in regs]
    result = oper(regs[opcode[1]], regs[opcode[2]])
    new_regs[opcode[3]] = result
    return new_regs

def reg_imm_op(regs, opcode, oper):
    new_regs = [r for r in regs]
    result = oper(regs[opcode[1]], opcode[2])
    new_regs[opcode[3]] = result
    return new_regs

def imm_reg_op(regs, opcode, oper):
    new_regs = [r for r in regs]
    result = oper(opcode[1], regs[opcode[2]])
    new_regs[opcode[3]] = result
    return new_regs

instruction_processors = {
    'addr': lambda regs, opcode: reg_reg_op(regs, opcode, add),
    'addi': lambda regs, opcode: reg_imm_op(regs, opcode, add),
    'mulr': lambda regs, opcode: reg_reg_op(regs, opcode, multiply),
    'muli': lambda regs, opcode: reg_imm_op(regs, opcode, multiply),
    'banr': lambda regs, opcode: reg_reg_op(regs, opcode, bitwise_and),
    'bani': lambda regs, opcode: reg_imm_op(regs, opcode, bitwise_and),
    'borr': lambda regs, opcode: reg_reg_op(regs, opcode, bitwise_or),
    'bori': lambda regs, opcode: reg_imm_op(regs, opcode, bitwise_or),
    'setr': lambda regs, opcode: reg_reg_op(regs, opcode, assignment),
    'seti': lambda regs, opcode: imm_reg_op(regs, opcode, assignment),
    'gtir': lambda regs, opcode: imm_reg_op(regs, opcode, greater_test),
    'gtri': lambda regs, opcode: reg_imm_op(regs, opcode, greater_test),
    'gtrr': lambda regs, opcode: reg_reg_op(regs, opcode, greater_test),
    'eqir': lambda regs, opcode: imm_reg_op(regs, opcode, equal_test),
    'eqri': lambda regs, opcode: reg_imm_op(regs, opcode, equal_test),
    'eqrr': lambda regs, opcode: reg_reg_op(regs, opcode, equal_test),
}

def main():
    samples, program = read_data()
    possible_ops = dict()
    three_or_more = 0
    for sample in samples:
        ips = set()
        for ip in instruction_processors:
            result = instruction_processors[ip](sample['before'], sample['opcode'])
            if result == sample['after']:
                ips.add(ip)
        if len(ips) >= 3:
            three_or_more += 1
        op = sample['opcode'][0]
        if op not in possible_ops:
            possible_ops[op] = ips
        else:
            possible_ops[op] = possible_ops[op].intersection(ips)
    print 'three or more:', three_or_more

    definite_ops = dict()
    while possible_ops:
        for op in possible_ops:
            if len(possible_ops[op]) == 1:
                definite_ops[op] = possible_ops[op].pop()
        for op in definite_ops:
            if op in possible_ops:
                del possible_ops[op]
        ado = {definite_ops[op] for op in definite_ops}
        zl = set()
        for op in possible_ops:
            possible_ops[op] -= ado
            if len(possible_ops[op]) == 0:
                zl.add(op)
        for op in zl:
            del possible_ops[op]
    print definite_ops

    regs = [0, 0, 0, 0]
    for opcode in program:
        ip = instruction_processors[definite_ops[opcode[0]]]
        regs = ip(regs, opcode)
    print regs

if __name__ == '__main__':
    main()
