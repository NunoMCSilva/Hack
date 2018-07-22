#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Hack CPU"""


# TODO: turn 0b into ints
def alu(x: int, y: int, comp: int) -> (int, int, int):
    zx = (comp & 0b100000) >> 5
    nx = (comp & 0b010000) >> 4
    zy = (comp & 0b000100) >> 3
    ny = (comp & 0b000010) >> 2
    f = (comp & 0b000010) >> 1
    no = comp & 0b000001

    if zx:
        x = 0
        print('x=0, ', end='')
    if nx:
        x = ~x
        print('~x, ', end='')
    if zy:
        y = 0
        print('y=0, ', end='')
    if ny:
        y = ~y
        print('~y, ', end='')

    out = x + y if f else x & y
    print('x + y, ' if f else 'x & y, ', end='')
    out = out & 0b1111111111111111     # remove carry

    if no:
        out = ~out
        print('~out, ', end='')

    zr = int(out == 0)
    ng = int(out < 0)
    print('zr={0}, ng={1}; '.format(zr, ng), end='')

    return out, zr, ng


class CPU:

    def __init__(self, instruction_memory, data_memory):
        self.inst_mem = instruction_memory
        self.data_mem = data_memory

        self.pc = 0             # program counter
        self.registerA = 0
        self.registerD = 0

    def __repr__(self):
        s = 'ROM: {}\n'.format(self.inst_mem)
        s += 'RAM: {}\n'.format(self.data_mem)
        s += 'PC={}, A={}, D={}'.format(self.pc, self.registerA, self.registerD)
        return s

    def run(self):
        while True:
            print(self, end='\n\n')
            self.step()

    # TODO: ok, it needs a lot of refactoring
    def step(self):
        instruction = self.inst_mem[self.pc]

        # decode instruction
        opcode = (instruction & 32768) >> 15

        if opcode:
            # C-instruction

            a = (instruction & 4096) >> 12
            comp = (instruction & 4032) >> 6
            dest = (instruction & 56) >> 3
            jump = instruction & 7

            # execute instruction - comp
            x = self.registerD
            y = self.data_mem[self.registerA] if a else self.registerA
            print('D, M; ' if a else 'D, A; ', end='')
            out, zr, ng = ALU(x, y, comp)

            # execute instruction - dest -- TODO: refactor this
            if dest == 1:
                print('M; ', end='')
                self.data_mem[self.registerA] = out
            elif dest == 2:
                print('D; ', end='')
                self.registerD = out
            elif dest == 3:
                print('MD; ', end='')
                self.data_mem[self.registerA] = out
                self.registerD = out
            elif dest == 4:
                print('A; ', end='')
                self.registerA = out
            elif dest == 5:
                print('AM; ', end='')
                self.registerA = out
                self.data_mem[self.registerA] = out
            elif dest == 6:
                print('AD; ', end='')
                self.registerA = out
                self.registerD = out
            elif dest == 7:
                print('AMD; ', end='')
                self.registerA = out
                self.data_mem[self.registerA] = out
                self.registerD = out

            # execute instruction - jmp
            if jump == 0:
                print('null')
                self.pc += 1
            elif jump == 1:
                # JGT
                print('JGT')
                if out > 0:
                    self.pc = self.registerA
            elif jump == 2:
                # JEQ
                print('JEQ')
                if zr:
                    self.pc = self.registerA
            elif jump == 3:
                # JGE
                print('JGE')
                if out >= 0:
                    self.pc = self.registerA
            elif jump == 4:
                # JLT
                print('JLT')
                if ng:
                    self.pc = self.registerA
            elif jump == 5:
                # JNE
                print('JNE')
                if out != 0:
                    self.pc = self.registerA
            elif jump == 6:
                # JLE
                print('JLE')
                if out <= 0:
                    self.pc = self.registerA
            elif jump == 7:
                print('JMP')
                self.pc = self.registerA
        else:
            # A-instruction - execute instruction
            print('@{}'.format(instruction))
            self.registerA = instruction
            self.pc += 1
