import sys
import os
import re

from lib.Parser import Parser
from lib.CodeWriter import CodeWriter
from lib.CommandType import COMMANDTYPE

if len(sys.argv) != 2:
    print('[Invalid args] usage: python assembler.py <input file/folder path>')
    exit(1)

input_path = sys.argv[1]

if os.path.isfile(input_path):
    input_files = [ input_path ]
    output_file_path = re.match(r"(.*)[.]", input_path).group(1) + '.asm'
elif os.path.isdir(input_path):
    if not os.path.isfile(os.path.join(input_path, 'Sys.vm')):
        print('[!] Sys.vm not found')
        exit(1)
    input_files = [os.path.join(input_path, vmfile) for vmfile in os.listdir(input_path) if re.match(r".*(?<!Sys)[.]vm", vmfile)]
    input_files = [os.path.join(input_path, 'Sys.vm'), *input_files]
    output_file_path = os.path.split(input_path)[1] + '.asm'
else:
    print('[!] file or folder not found')
    exit(1)

code_writer = CodeWriter(output_file_path)

for input_file_path in input_files:
    parser = Parser(input_file_path)
    code_writer.context["file"] = parser.input_file_name_no_extension
    while parser.advance():
        command_type = parser.command_type()
        if command_type == COMMANDTYPE.ARITHMETIC:
            code_writer.write_arithmetic(parser.get_command())
        elif command_type == COMMANDTYPE.PUSH or command_type == COMMANDTYPE.POP:
            code_writer.write_memory(parser.get_command())
        elif command_type == COMMANDTYPE.LABEL:
            code_writer.write_label(parser.get_command())
        elif command_type == COMMANDTYPE.GOTO:
            code_writer.write_goto(parser.get_command())
        elif command_type == COMMANDTYPE.IF:
            code_writer.write_if(parser.get_command())
    parser.close()
code_writer.close()