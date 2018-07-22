#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import memory
import cpu


def run(program_fpath: str):
    rom = memory.ReadOnlyMemory(32 * 1024)
    rom.load_program(program_fpath)

    ram = memory.ReadWriteMemory(16 * 1024)

    cpu_ = cpu.CPU(rom, ram)
    cpu_.run()


if __name__ == '__main__':
    run('Mult.hack')
