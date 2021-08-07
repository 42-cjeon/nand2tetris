import re

class Tokenizer:
    def __init__(self, input_file_path) -> None:
        self.__input_file = open(input_file_path, 'r')
        self.__token_generator = self.__get_token_generator()
        self.current_line = 0
        self.__look_aheaded = False
        self.__prev_token = ''
        self.symbols = ['{', '}', '[', ']', '(', ')', ',', '.', ';', '=', '+', '-', '*', '/', '&', '|', '~', '<', '>']

    def close(self):
        self.__input_file.close()

    def __get_token_generator(self):
        multiline_comment = False
        while True:
            line = self.__input_file.readline()
            self.current_line += 1
            if line == '':
                yield "$END"
                break
            line = line.strip()
            # remove single line comment
            line = re.sub(r"//.*", "", line, 1)
            # remove start of multiline comment (/*) 
            if not multiline_comment:
                line, start_of_multiline_comment_count = re.subn(r"/[*].*", "", line, 1)
                multiline_comment = bool(start_of_multiline_comment_count)
            # remove end of multiline comment (*/)
            if multiline_comment:
                line, end_of_multiline_comment_count = re.subn(r".*?[*]/", "", line, 1)
                multiline_comment = not bool(end_of_multiline_comment_count)
            if line == '' or multiline_comment:
                continue
            else:
                tmp = ''
                is_string_constant = False
                for char in line:
                    if char in self.symbols:
                        if tmp != '':
                            yield tmp
                        yield char
                        tmp = ''
                    elif char == '"':
                        tmp += '"'
                        is_string_constant = not is_string_constant
                    elif re.match(r'\s+', char) and not is_string_constant:
                        if tmp != '':
                            yield tmp
                        tmp = ''
                    else:
                        tmp += char

    def get_token(self, is_look_ahead=False):
        if self.__look_aheaded:
            return self.__prev_token
        elif is_look_ahead:
            self.__look_aheaded = True
            self.__prev_token = next(self.__token_generator)
            return self.__prev_token
        else:
            return next(self.__token_generator)