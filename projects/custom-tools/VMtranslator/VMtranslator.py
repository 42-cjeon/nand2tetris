import sys
import os
import re

from lib.Parser import Parser
from lib.CodeWriter import CodeWriter
from lib.CommandType import COMMANDTYPE

if len(sys.argv) != 2:
    print('[Invalid args] usage: python assembler.py <input file path>')
    exit()

input_file_path = sys.argv[1]
if not os.path.isfile(input_file_path):
    print('[!] file not found')
    exit()

input_file_name_no_extension = re.match(r'(.*)[.]', input_file_path).group(1)
output_file_path = input_file_name_no_extension + '.asm'

parser = Parser(input_file_path)
code_writer = CodeWriter(input_file_name_no_extension, output_file_path)

while parser.advance():
    command_type = parser.command_type()
    if command_type == COMMANDTYPE.ARITHMETIC:
        code_writer.write_arithmetic(parser.get_command())
    elif command_type == COMMANDTYPE.PUSH or command_type == COMMANDTYPE.POP:
        code_writer.write_memory(parser.get_command())
parser.close()
code_writer.close()