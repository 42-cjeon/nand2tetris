import re
import os
from itertools import product

from lib.Errors import ParseError
from lib.CommandType import COMMANDTYPE

class Parser:
    def __init__(self, input_file_path:str) -> None:
        constant = ['0', '1']
        signed_constant = ['-1']
        d_register = ['D']
        m_register = ['A', 'M']
        register = [*m_register, *d_register]
        signed_register = [*map(lambda x: '-'+x, register), *map(lambda x: '!'+x, register)]
        add = [*map(lambda x: x[0]+'+'+x[1], product(d_register, m_register)), *map(lambda x: x[0]+'+'+x[1], product(m_register, d_register))]
        sub = [*map(lambda x: x[0]+'-'+x[1], product(d_register, m_register)), *map(lambda x: x[0]+'-'+x[1], product(m_register, d_register))]
        _and = [*map(lambda x: x[0]+'&'+x[1], product(d_register, m_register)), *map(lambda x: x[0]+'&'+x[1], product(m_register, d_register))]
        _or = [*map(lambda x: x[0]+'|'+x[1], product(d_register, m_register)), *map(lambda x: x[0]+'|'+x[1], product(m_register, d_register))]
        inc = [*map(lambda x: '1+'+x, register), *map(lambda x: x+'+1', register)]
        dec = [*map(lambda x: x+'-1', register)]
        single_operand = [*constant, *signed_constant, *register, *signed_register]
        double_operand = [*add, *sub, *_and, *_or, *inc, *dec]
        
        self.valid_compute = [*single_operand, *double_operand]
        self.valid_jump = ['JGT', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']
        self.input_file_path = os.path.abspath(input_file_path)
        self.input_file = open(input_file_path, 'r')
        self.current_line = ''
        self.valid_line_number = 0
        self.current_line_number = 0

    def advance(self) -> bool:
        while True:
            next_line = self.input_file.readline()
            self.current_line_number += 1
            if next_line:
                # remove all white space character
                next_line = re.sub(r'\s+', '', next_line)
                if next_line == '':
                    continue
                elif len(next_line) < 2:
                    raise ParseError(self.input_file_path, self.current_line_number, 'invalid command length: at least 2 required')
                elif next_line[0:2] == '//':
                    continue
                else:
                    self.current_line = next_line
                    self.valid_line_number += 1
                    return True
            else:
                return False

    def command_type(self) -> COMMANDTYPE:
        signature = self.current_line[0]
        if signature == '@':
            return COMMANDTYPE.A
        elif signature == '(':
            self.valid_line_number -= 1
            return COMMANDTYPE.L
        else:
            return COMMANDTYPE.C
    
    def symbol(self) -> str:
        # (Xxx) -> Xxx or @Xxx -> Xxx
        return re.sub(r'[@\(\)]', '', self.current_line)

    def dest(self) -> str:
        if '=' in self.current_line:
            # AD=A+D -> AD
            dest = re.search(r'(.+)=', self.current_line).group(1)
            dest = ''.join(sorted(dest))
           
            if dest in ['A', 'D', 'M', 'AD', 'AM', 'DM', 'ADM']:
                return dest
            else:
                raise ParseError(self.input_file_path, self.current_line_number, 'DEST field must be A or M or D')
        else:
            return 'null0'

    def comp(self) -> str:
        is_dest_instruction = '=' in self.current_line
        is_jump_instruction = ';' in self.current_line
        if is_dest_instruction and is_jump_instruction:
            raise ParseError(self.input_file_path, self.current_line_number, 'ambiguous instruction: jump or dest?')
        elif is_dest_instruction:
            comp = re.search(r'=(.+)', self.current_line).group(1)
        elif is_jump_instruction:
            comp = re.search(r'(.+);', self.current_line).group(1)
        else:
            raise ParseError(self.input_file_path, self.current_line_number, 'no additional field specified: dest or jump')
        if comp in self.valid_compute:
            return comp
        else:
            raise ParseError(self.input_file_path, self.current_line_number, 'invalid compute field')

    def jump(self) -> str:
        if ';' in self.current_line:
            jump = re.search(r';(.+)', self.current_line).group(1)
            if jump in self.valid_jump:
                return jump
            else:
                raise ParseError(self.input_file_path, self.current_line_number, 'invalid jump field')
        else:
            return 'null'

    def close(self) -> None:
        self.input_file.close()