import os
import sys
import re

from lib.Parser import Parser
from lib.Code import Code
from lib.SymbolTable import SymbolTable
from lib.CommandType import COMMANDTYPE
from lib.Errors import *


if len(sys.argv) != 2:
    print('[Invalid args] usage: python assembler.py <input file path>')
    exit()

input_file_path = sys.argv[1]
if not os.path.isfile(input_file_path):
    print('[!] file not found')
    exit()

parser = Parser(input_file_path)
code = Code()
symbol_table = SymbolTable()
parsed_code = []

while parser.advance():
    try:
        command_type = parser.command_type()
        if command_type == COMMANDTYPE.L:
            symbol = parser.symbol()
            symbol_table.get(symbol, parser.valid_line_number)
        elif command_type == COMMANDTYPE.A:
            symbol = parser.symbol()
            parsed_code.append({'type': COMMANDTYPE.A, 'symbol': symbol})
        elif command_type == COMMANDTYPE.C:
            dest = parser.dest()
            comp = parser.comp()
            jump = parser.jump()
            parsed_code.append({'type': COMMANDTYPE.C, 'dest': dest, 'comp': comp, 'jump': jump})
    except ParseError as e:
        print(f"[ParseError] at line {e.line}: {e.message}")
        exit()
    except MomoryError as e:
        print(f"[MomoryError] at line {e.line}: {e.message}")
        exit()

parser.close()
output_file_path = re.match(r'(.*)[.]', input_file_path).group(1) + '.hack'

with open(output_file_path, 'w') as f:
    for line in parsed_code:
        if line['type'] == COMMANDTYPE.A and not line['symbol'].isdigit():
            line['symbol'] = symbol_table.get(line['symbol'])
        f.write(code.convert(line)+'\n')