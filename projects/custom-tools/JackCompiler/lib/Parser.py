import re
import json
import os

class Parser:
    def __init__(self, input_file_path) -> None:
        input_file = open(input_file_path, 'r')
        self.input_file_string = input_file.read()
        input_file.close()
        grammer_file = open(os.path.join('lib', 'grammer.json'), 'r')
        self.grammer = json.load(grammer_file)
        grammer_file.close()
        self.input_token = []
        self.symbols = ['{', '}', '[', ']', '(', ')', ',', '.', ';', '=', '+', '-', '*', '/', '&', '|', '~', '<', '>']
        self.keywords = ['class,' ,'constructor,' ,'method,' ,'function,' ,'var,' ,'static,' ,'field,' ,'int,' ,'char,' ,'boolean,' ,'void,' ,'let,' ,'do,' ,'if,' ,'else,' ,'while,' ,'return,' ,'true,' ,'false,' ,'null,' ,'this']
        
    def tokenize(self):
        input_file_string_no_comment = re.sub(r'(?s)//[^\n]*?\n|/\*.*?\*/', '', self.input_file_string)
        print(input_file_string_no_comment)
        tmp = ''
        is_string_constant = False
        for char in input_file_string_no_comment:
            if char in self.symbols:
                if tmp != '':
                    self.input_token.append(tmp)
                self.input_token.append(char)
                tmp = ''
            elif char == '"':
                tmp += '"'
                is_string_constant = not is_string_constant
            elif re.match(r'\s', char) and not is_string_constant:
                if tmp != '':
                    self.input_token.append(tmp)
                tmp = ''
            else:
                tmp += char

    def parse(self):
        result, _ = self._parse(self.grammer['class'], 0)
        return "<class>"+result+"</class>"

    def _parse(self, node, i):
        result = ''
        for and_rule in node:
            or_success = False
            for or_rule in and_rule:
                if or_rule["isTerminal"]:
                    m = re.match(or_rule["value"], self.input_token[i])
                    if m:
                        terminal_type = m.group()
                        if terminal_type in self.symbols:
                            result += f"<symbol>{self.input_token[i]}</symbol>"
                        elif terminal_type in self.keywords:
                            result += f"<keyword>{self.input_token[i]}</keyword>"
                        else:
                            result += self.input_token[i]
                        or_success = True
                        i += 1
                        break
                else:
                    if or_rule['repeat'] == '?':
                        or_success = True
                        tmp_result, tmp_i = self._parse(self.grammer[or_rule["value"]], i)
                        if tmp_result != '':
                            i = tmp_i
                            result += f"<{or_rule['value']}>{tmp_result}</{or_rule['value']}>"
                            break
                    elif or_rule['repeat'] == '*':
                        or_success = True
                        tmp_result, tmp_i = self._parse(self.grammer[or_rule["value"]], i)
                        while tmp_result != '':
                            i = tmp_i
                            result += f"<{or_rule['value']}>{tmp_result}</{or_rule['value']}>"
                            tmp_result, tmp_i = self._parse(self.grammer[or_rule["value"]], i)
                    else:
                        tmp_result, tmp_i = self._parse(self.grammer[or_rule["value"]], i)
                        if tmp_result != '':
                            i = tmp_i
                            result += f"<{or_rule['value']}>{tmp_result}</{or_rule['value']}>"
                            or_success = True
                            break
            if not or_success:
                return ('', i)
        return (result, i)