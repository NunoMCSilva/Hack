#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Memory modules"""


class ReadOnlyMemory:

    def __init__(self, size: int):
        self.size = size
        self.mem = []

    def __getitem__(self, pos: int) -> int:
        # TODO: test this
        try:
            return self.mem[pos]
        except:
            if pos < self.size - 1:
                return 0
            else:
                raise ValueError('out of bounds')

    def __repr__(self) -> str:
        return repr(self.mem)

    def load_program(self, fpath):
        # TODO: detect program above rom maximum size
        with open(fpath) as f:
            for line in f:
                self.mem.append(int(line, 2))


class ReadWriteMemory:

    def __init__(self, size: int):
        self.size = size
        self.mem = {}

    # TODO: reduce redundant code
    def __getitem__(self, pos: int) -> int:
        # TODO: test this
        try:
            return self.mem[pos]
        except:
            if pos < self.size - 1:
                return 0
            else:
                raise ValueError('out of bounds')

    def __setitem__(self, pos: int, word: int):
        self.mem[pos] = word

    def __repr__(self):
        return repr(self.mem)


if __name__ == '__main__':
    rom = ReadOnlyMemory(32 * 1024)
    rom.load_program('Mult.hack')
    print(rom)
    print(rom[100])
    # print(rom[100000])

    ram = ReadWriteMemory(16 * 1024)
    print(ram)
    ram[10] = 0xFFDD
    print(ram)
    print(ram[100])
    print(ram[0])
