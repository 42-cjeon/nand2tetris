import re

from lib.CommandType import COMMANDTYPE
from lib.Errors import ParseError

class Parser:
    def __init__(self, input_file_path:str) -> None:
        self.input_file = open(input_file_path, 'r')
        self.current_line = []
        self.line_number = 0
        self.commands = {
            'add': COMMANDTYPE.ARITHMETIC,
            'sub': COMMANDTYPE.ARITHMETIC,
            'neg': COMMANDTYPE.ARITHMETIC,
            'eq': COMMANDTYPE.ARITHMETIC,
            'gt': COMMANDTYPE.ARITHMETIC,
            'lt': COMMANDTYPE.ARITHMETIC,
            'and': COMMANDTYPE.ARITHMETIC,
            'or': COMMANDTYPE.ARITHMETIC,
            'not': COMMANDTYPE.ARITHMETIC,
            'push': COMMANDTYPE.PUSH,
            'pop': COMMANDTYPE.POP,
            'label': COMMANDTYPE.LABEL,
            'goto': COMMANDTYPE.GOTO,
            'if-goto': COMMANDTYPE.IF,
            'function': COMMANDTYPE.FUNCTION,
            'call': COMMANDTYPE.CALL,
            'return': COMMANDTYPE.RETURN
        }

    def advance(self) -> bool:
        while True:
            line = self.input_file.readline()
            self.line_number += 1
            if not line:
                return False
            line_comment_removed = re.sub(r'//.*', '', line)
            line_striped = line_comment_removed.strip()
            if line_striped == '':
                continue
            line_tokens = re.split(r'\s+', line_striped)
            self.current_line = line_tokens
            return True

    def command_type(self) -> COMMANDTYPE:
        try:
            return self.commands[self.current_line[0]]
        except:
            raise ParseError('', self.line_number, 'Invilid command')

    def get_command(self) -> list:
        return self.current_line

    def close(self) -> None:
        self.input_file.close()