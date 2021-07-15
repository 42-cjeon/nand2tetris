import re
from command_type import COMMANDTYPE

class Parser:
    def __init__(self, input_file_path):
        self.input_file = open(input_file_path, 'r')
        self.current_command = ''

    def advance(self) -> bool:
        next_command = self.input_file.readline()
        if next_command:
            next_command
            self.current_command = re.sub(r"\s+", '', next_command)
            if self.current_command == '':
                return self.advance()
            return True
        else:
            return False

    def command_type(self) -> COMMANDTYPE:
        first_char = self.current_command[0]
        if first_char == "@":
            return COMMANDTYPE.A_COMMAND
        elif first_char == "(":
            return COMMANDTYPE.L_COMMAND
        elif first_char == "/":
            return COMMANDTYPE.COMMENT
        else:
            return COMMANDTYPE.C_COMMAND

    def symbol(self) -> str:
        symbol = re.sub(r"[@\(\)]", '', self.current_command)
        return symbol

    def dest(self) -> str:
        if '=' in self.current_command:
            return self.current_command.split('=')[0]
        else:
            return "null0"

    def comp(self) -> str:
        if '=' in self.current_command:
            return self.current_command.split("=")[1]
        elif ';' in self.current_command:
            return self.current_command.split(";")[0]
        else:
            return self.current_command

    def jump(self) -> str:
        if ';' in self.current_command:
            return self.current_command.split(";")[1]
        else:
            return "null"