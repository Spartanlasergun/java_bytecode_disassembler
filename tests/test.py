import sys
sys.path.append('C:/Users/bns36/Documents/java_bytecode_disassembler/src/disassembler')

from java_bytecode_disassembler import disassembler

disassembly = disassembler('Main.class', verbose=True)


