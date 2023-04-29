import sys
sys.path.append('C:/Users/bns36/Documents/java_bytecode_disassembler/src/disassembler')

from java_bytecode_disassembler import java_bytecode_disassembler

java_bytecode_disassembler('Main.class', verbose=True)
