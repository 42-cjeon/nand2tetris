import re

from lib.Tokenizer import Tokenizer
from lib.VmWriter import VmWriter
from lib.SymbolTable import SymbolTable
from lib.Enums import DATAIDENTIFIER
from lib.Errors import ParseError

class CompileEngine:
    def __init__(self, input_file_path) -> None:
        self.input_file_name = re.match(r"(.*)[.]", input_file_path).group(1)
        self.__vm_writer = VmWriter(self.input_file_name + '.vm')
        self.__tokenizer = Tokenizer(input_file_path)
        self.__symbol_table = SymbolTable()
        self.class_name = ''
        self.while_count = 0
        self.if_count = 0

    def close(self):
        self.__tokenizer.close()
        self.__vm_writer.close()

    def is_identifier(self, token):
        if re.match(r"[a-zA-Z_]\w*$", token):
            return True
        return False
    
    def is_type(self, token):
        valid_type = ['int', 'char', 'boolean']
        if token in valid_type:
            return True
        return self.is_identifier(token)

    def is_op(self, token):
        valid_op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
        if token in valid_op:
            return True
        return False

    def is_unary_op(self, token):
        valid_unary_op = ['-', '~']
        if token in valid_unary_op:
            return True
        return False

    def is_integer_constant(self, token):
        if re.match(r"\d+$", token):
            return True
        return False

    def is_string_constant(self, token):
        if re.match(r'".+"$', token):
            return True
        return False

    def is_keyword_constant(self, token):
        valid_keyword_constant = ['true', 'false', 'null', 'this']
        if token in valid_keyword_constant:
            return True
        return False

    def compile_class(self):
        keyword_class = self.__tokenizer.get_token()
        if keyword_class != "class":
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'class: keyword' not '{keyword_class}'")
        
        class_name = self.__tokenizer.get_token()
        if not self.is_identifier(class_name):
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'className: identifier' not '{class_name}'")
        self.class_name = class_name

        start_curly_brace = self.__tokenizer.get_token()
        if start_curly_brace != '{':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '{{: symbol' not '{start_curly_brace}'")

        next_token_preview = self.__tokenizer.get_token(True)
        if next_token_preview == 'field' or next_token_preview == 'static':
            self.compile_class_var_dec()

        next_token_preview = self.__tokenizer.get_token(True)
        if next_token_preview == 'constructor' or next_token_preview == 'function' or next_token_preview == 'method':
            self.compile_subroutine_dec()

        end_curly_brace = self.__tokenizer.get_token()
        if end_curly_brace != '}':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '}}: symbol' not '{end_curly_brace}'")

        end_token = self.__tokenizer.get_token()
        if end_token != '$END':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '$END: EOF' not '{end_token}'")

    def compile_class_var_dec(self):
        while True:
            class_var_type = self.__tokenizer.get_token()
            if class_var_type != 'field' and class_var_type != 'static':
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'static or field: keyword' not '{class_var_type}'")
            class_var_type = DATAIDENTIFIER.FIELD if class_var_type == 'field' else DATAIDENTIFIER.STATIC

            var_type = self.__tokenizer.get_token()
            if not self.is_type(var_type):
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'type: keyword | identifier' not '{var_type}'")
            
            var_name = self.__tokenizer.get_token()
            if not self.is_identifier(var_name):
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'varName: identifier' not '{var_name}'")
            
            self.__symbol_table.define(var_name, var_type, class_var_type)
            while True:
                class_var_dec_repeat = self.__tokenizer.get_token()
                if class_var_dec_repeat == ',':
                    var_name = self.__tokenizer.get_token()
                    if not self.is_identifier(var_name):
                        raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'varName: identifier' not '{var_name}'")
                    self.__symbol_table.define(var_name, var_type, class_var_type)
                elif class_var_dec_repeat == ';':
                    break
                else:
                    raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected ', varName | ;: symbol' not '{class_var_dec_repeat}'")
            next_token_preview = self.__tokenizer.get_token(True)
            if next_token_preview != 'field' and next_token_preview != 'static':
                break

    def compile_subroutine_dec(self):
        while True:
            subroutine_type = self.__tokenizer.get_token()
            if subroutine_type != 'constructor' and subroutine_type != 'function' and subroutine_type != 'method':
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'constructor | function | method: keyword' not '{subroutine_type}'")
            
            subroutine_return_type = self.__tokenizer.get_token()
            if (not self.is_type(subroutine_return_type)) and subroutine_return_type != 'void':
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'type | void: keyword' not '{subroutine_return_type}'")

            subroutine_name = self.__tokenizer.get_token()
            if not self.is_identifier(subroutine_name):
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'subroutineName: identifier' not '{subroutine_name}'")
            
            self.__symbol_table.start_subroutine(f"{self.class_name}.{subroutine_name}")
            if subroutine_type == 'method':
                self.__symbol_table.define('this', self.class_name, DATAIDENTIFIER.ARG) 

            start_parentheses = self.__tokenizer.get_token()
            if start_parentheses != '(':
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '(: symbol' not '{start_parentheses}'")
            
            next_token_preview = self.__tokenizer.get_token(True)
            if next_token_preview != ')':
                self.compile_parameter_list()

            end_parentheses = self.__tokenizer.get_token()
            if end_parentheses != ')':
               raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '): symbol' not '{end_parentheses}'")

            start_curly_brace = self.__tokenizer.get_token()
            if start_curly_brace != '{':
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '{{: symbol' not '{start_curly_brace}'")
            
            next_token_preview = self.__tokenizer.get_token(True)
            local_var_count = 0
            if next_token_preview == 'var':
                local_var_count += self.compile_var_dec()
            
            self.__vm_writer.write_function('function', f"{self.class_name}.{subroutine_name}", str(local_var_count))
            if subroutine_type == 'constructor':
                self.__vm_writer.write_memory_access('push', 'constant', str(self.__symbol_table.get_field_var_count()))
                self.__vm_writer.write_function('call', 'Memory.alloc', '1')
                self.__vm_writer.write_memory_access('pop', 'pointer', '0')

            elif subroutine_type == 'method':
                self.__vm_writer.write_memory_access('push', 'argument', '0')
                self.__vm_writer.write_memory_access('pop', 'pointer', '0')
            self.compile_statements()

            end_curly_brace = self.__tokenizer.get_token()
            if end_curly_brace != '}':
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '}}: symbol' not '{end_curly_brace}'")

            next_token_preview = self.__tokenizer.get_token(True)
            if next_token_preview != 'constructor' and next_token_preview != 'function' and next_token_preview != 'method':
                break
    
    def compile_subroutine_call(self, first_token=None):
        if first_token == None:
            first_token = self.__tokenizer.get_token()

        if not self.is_identifier(first_token):
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'subroutineName | varName | className: identifier' not '{first_token}'")
        symbol = self.__tokenizer.get_token()

        parameter_count = 0
        if symbol == '.':
            
            # subroutine is method -> push this
            class_info = self.__symbol_table.get_var_info(first_token)
            if class_info: 
                first_token = class_info['type']
                if class_info["kind"] == DATAIDENTIFIER.FIELD:
                    self.__vm_writer.write_memory_access('push', 'this', class_info["index"])
                elif class_info["kind"] == DATAIDENTIFIER.VAR:
                    self.__vm_writer.write_memory_access('push', 'local', '0')
                parameter_count += 1

            subroutine_name = self.__tokenizer.get_token()
            if not self.is_identifier(subroutine_name):
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'subroutineName: identifier' not '{subroutine_name}'")
            
            start_parentheses = self.__tokenizer.get_token()
            if start_parentheses != '(':
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '(: symbol' not '{start_parentheses}'")
            
            if self.__tokenizer.get_token(True) != ')':
                parameter_count += self.compile_expression_list()
            end_parentheses = self.__tokenizer.get_token()
            if end_parentheses != ')':
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '(: symbol' not '{end_parentheses}'")

            self.__vm_writer.write_function('call', f'{first_token}.{subroutine_name}', str(parameter_count))

        # subroutine is method
        elif symbol == '(':
            self.__vm_writer.write_memory_access('push', 'pointer', '0')
            parameter_count += 1
            if self.__tokenizer.get_token(True) != ')':
                parameter_count += self.compile_expression_list()
            end_parenthses = self.__tokenizer.get_token()
            if end_parenthses != ')':
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '): symbol' not '{end_parenthses}'")
            self.__vm_writer.write_function('call', f'{self.class_name}.{first_token}', str(parameter_count))
        else:
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '( | .: symbol' not '{symbol}'")

    def compile_parameter_list(self):
        while True:
            parameter_type = self.__tokenizer.get_token()
            if not self.is_type(parameter_type):
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'type: keyword' not '{parameter_type}'")

            parameter_name = self.__tokenizer.get_token()
            if not self.is_identifier(parameter_name):
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'varName: identifier' not '{parameter_name}'")

            self.__symbol_table.define(parameter_name, parameter_type, DATAIDENTIFIER.ARG)
            
            next_token_preview = self.__tokenizer.get_token(True)
            if next_token_preview != ',':
                break

            # ignore token ','
            self.__tokenizer.get_token()
            
    def compile_var_dec(self):
        local_var_count = 0
        while True:
            keyword_var = self.__tokenizer.get_token()
            if keyword_var != 'var':
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'var: keyword' not '{keyword_var}'")
            
            var_type = self.__tokenizer.get_token()
            if not self.is_type(var_type):
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'type: keyword' not '{var_type}'")

            var_name = self.__tokenizer.get_token()
            if not self.is_identifier(var_name):
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'varName: identifier' not '{var_name}'")
            
            self.__symbol_table.define(var_name, var_type, DATAIDENTIFIER.VAR)
            local_var_count += 1

            while True:
                var_dec_repeat = self.__tokenizer.get_token()
                if var_dec_repeat == ',':
                    var_name = self.__tokenizer.get_token()
                    if not self.is_identifier(var_name):
                        raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'varName: identifier' not '{var_name}'")
                    self.__symbol_table.define(var_name, var_type, DATAIDENTIFIER.VAR)
                    local_var_count += 1
                elif var_dec_repeat == ';':
                    break
                else:
                    raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected ', varName | ;: symbol' not '{var_dec_repeat}'")

            next_token_preview = self.__tokenizer.get_token(True)
            if next_token_preview != 'var':
                break
        return local_var_count
        
    def compile_statements(self):
        while True:
            statement_type = self.__tokenizer.get_token(True)
            if statement_type == 'let':
                self.compile_let()
            elif statement_type == 'if':
                self.compile_if()
            elif statement_type == 'while':
                self.compile_while()
            elif statement_type == 'do':
                self.compile_do()
            elif statement_type == 'return':
                self.compile_return()
            else:
                break
            
    def compile_do(self):
        keyword_do = self.__tokenizer.get_token()
        if keyword_do != 'do':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'do: keyword' not '{keyword_do}'")
        
        self.compile_subroutine_call()

        semicolon = self.__tokenizer.get_token()
        if semicolon != ';':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected ';: symbol' not '{semicolon}'")
        # ignore return value
        self.__vm_writer.write_memory_access('pop', 'temp', '0')

    def compile_let(self):
        keyword_let = self.__tokenizer.get_token()
        if keyword_let != 'let':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'let: keyword' not '{keyword_let}'")

        var_name = self.__tokenizer.get_token()
        identifier_info = self.__symbol_table.get_var_info(var_name)
        if identifier_info:
            if identifier_info['kind'] == DATAIDENTIFIER.VAR:
                segment = 'local'
            elif identifier_info['kind'] == DATAIDENTIFIER.ARG:
                segment = 'argument'
            elif identifier_info['kind'] == DATAIDENTIFIER.FIELD:
                segment = 'this'
            elif identifier_info['kind'] == DATAIDENTIFIER.STATIC:
                segment = 'static'
        else:
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Identifier '{var_name}' not defined")

        symbol = self.__tokenizer.get_token()
        if symbol == '[':
            self.__vm_writer.write_memory_access('push', segment, identifier_info["index"])
            self.compile_expression()
            self.__vm_writer.write_arithmetic('+')
            end_bracket = self.__tokenizer.get_token()
            if end_bracket != ']':
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected ']: symbol' not '{end_bracket}'")
            
            symbol = self.__tokenizer.get_token()
            if symbol != '=':
                raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '=: symbol' not '{symbol}'")
            self.compile_expression()
            self.__vm_writer.write_memory_access('pop', 'temp', '0')
            self.__vm_writer.write_memory_access('pop', 'pointer', '1')
            self.__vm_writer.write_memory_access('push', 'temp', '0')
            self.__vm_writer.write_memory_access('pop', 'that', '0')

        elif symbol == '=':
            self.compile_expression()
            self.__vm_writer.write_memory_access('pop', segment, identifier_info["index"])
        else:
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '= | [: symbol' not '{symbol}'")
        semicolon = self.__tokenizer.get_token()
        if semicolon != ';':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected ';: symbol' not '{semicolon}'")

    def compile_while(self):
        while_count = self.while_count
        self.while_count += 1
        keyword_while = self.__tokenizer.get_token()
        if keyword_while != 'while':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'while: keyword' not '{keyword_while}'")

        start_parentheses = self.__tokenizer.get_token()
        if start_parentheses != '(':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '(: symbol' not '{start_parentheses}'")
        
        self.__vm_writer.write_control_flow('label', f'_START_WHILE{while_count}')
        self.compile_expression()
        self.__vm_writer.write_arithmetic('~')
        self.__vm_writer.write_control_flow('if-goto', f'_END_WHILE{while_count}')
        
        end_parentheses = self.__tokenizer.get_token()
        if end_parentheses != ')':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '): symbol' not '{end_parentheses}'")

        start_curly_brace = self.__tokenizer.get_token()
        if start_curly_brace != '{':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '{{: symbol' not '{start_curly_brace}'")

        self.compile_statements()
        self.__vm_writer.write_control_flow('goto', f'_START_WHILE{while_count}')
        self.__vm_writer.write_control_flow('label', f'_END_WHILE{while_count}')

        end_curly_brace = self.__tokenizer.get_token()
        if end_curly_brace != '}':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '}}: symbol' not '{end_curly_brace}'")
        

    def compile_return(self):
        keyword_return = self.__tokenizer.get_token()
        if keyword_return != 'return':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'return: keyword' not '{keyword_return}'")

        if self.__tokenizer.get_token(True) == ';':
            self.__vm_writer.write_memory_access('push', 'constant', '0')
        else:
            self.compile_expression()
        semicolon = self.__tokenizer.get_token()
        if semicolon != ';':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected ';: symbol' not '{semicolon}'")

        self.__vm_writer.write_function('return')

    def compile_if(self):
        if_count = self.if_count
        self.if_count += 1
        keyword_if = self.__tokenizer.get_token()
        if keyword_if != 'if':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'if: keyword' not '{keyword_if}'")

        start_parentheses = self.__tokenizer.get_token()
        if start_parentheses != '(':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '(: symbol' not '{start_parentheses}'")
        
        self.compile_expression()
        self.__vm_writer.write_control_flow('if-goto', f'_START_IF{if_count}')
        self.__vm_writer.write_control_flow('goto', f"_END_IF{if_count}")
        self.__vm_writer.write_control_flow('label', f"_START_IF{if_count}")
        
        
        end_parenthses = self.__tokenizer.get_token()
        if end_parenthses != ')':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '): symbol' not '{end_parenthses}'")

        start_curly_brace = self.__tokenizer.get_token()
        if start_curly_brace != '{':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '{{: symbol' not '{start_curly_brace}'")

        self.compile_statements()

        end_curly_brace = self.__tokenizer.get_token()
        if end_curly_brace != '}':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '}}: symbol' not '{end_curly_brace}'")

        if self.__tokenizer.get_token(True) == 'else':
            self.__vm_writer.write_control_flow('goto', f"_END_ELSE{if_count}")
            self.__vm_writer.write_control_flow('label', f"_END_IF{if_count}")
            self.compile_else()
            self.__vm_writer.write_control_flow('label', f"_END_ELSE{if_count}")
        else:
            self.__vm_writer.write_control_flow('label', f"_END_IF{if_count}")

    def compile_else(self):
        keyword_else = self.__tokenizer.get_token()
        if keyword_else != 'else':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'else: keyword' not '{keyword_else}'")

        start_curly_brace = self.__tokenizer.get_token()
        if start_curly_brace != '{':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '{{: symbol' not '{start_curly_brace}'")

        self.compile_statements()

        end_curly_brace = self.__tokenizer.get_token()
        if end_curly_brace != '}':
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected '}}: symbol' not '{end_curly_brace}'")

    def compile_expression(self, bracket=False, parentheses=False):
        operators = []
        self.compile_term()
        while True:
            op = self.__tokenizer.get_token(True)
            if parentheses and op == ')':
                for operator in reversed(operators):
                    self.__vm_writer.write_arithmetic(operator)
                self.__tokenizer.get_token()
                return
            elif bracket and op == ']':
                for operator in reversed(operators):
                    self.__vm_writer.write_arithmetic(operator)
                self.__vm_writer.write_arithmetic('+')
                self.__vm_writer.write_memory_access('pop', 'pointer', '1')
                self.__vm_writer.write_memory_access('push', 'that', '0')
                
                # ignore ']' token
                self.__tokenizer.get_token()
                return
            if not self.is_op(op):
                break
            operators.append(self.__tokenizer.get_token())
            self.compile_term()
        for operator in reversed(operators):
            self.__vm_writer.write_arithmetic(operator)

    def compile_term(self):
        term = self.__tokenizer.get_token()
        if self.is_integer_constant(term):
            self.__vm_writer.write_memory_access('push', 'constant', term)
        elif self.is_string_constant(term):
            term = term[1:-1]
            self.__vm_writer.write_memory_access('push', 'constant', str(len(term)))
            self.__vm_writer.write_function('call', 'String.new', '1')
            for char in term:
                self.__vm_writer.write_memory_access('push', 'constant', str(ord(char)))
                self.__vm_writer.write_function('call', 'String.appendChar', '2')
        elif self.is_keyword_constant(term):
            '''
            true (~0) | false (0) | null (0) | this ?
            '''
            if term == 'false' or term == 'null':
                self.__vm_writer.write_memory_access('push', 'constant', '0')
            elif term == 'true':
                self.__vm_writer.write_memory_access('push', 'constant', '0')
                self.__vm_writer.write_arithmetic('~')
            elif term == 'this':
                self.__vm_writer.write_memory_access('push', 'pointer', '0')

        elif self.is_identifier(term):
            next_token_preview = self.__tokenizer.get_token(True)
            identifier_info = self.__symbol_table.get_var_info(term)
            if identifier_info:
                if identifier_info['kind'] == DATAIDENTIFIER.VAR:
                    segment = 'local'
                elif identifier_info['kind'] == DATAIDENTIFIER.ARG:
                    segment = 'argument'
                elif identifier_info['kind'] == DATAIDENTIFIER.FIELD:
                    segment = 'this'
                elif identifier_info['kind'] == DATAIDENTIFIER.STATIC:
                    segment = 'static'
            if next_token_preview == '[':
                if not identifier_info:
                    raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Identifier '{term}' not defined")
                self.__tokenizer.get_token()
                self.__vm_writer.write_memory_access('push', segment, identifier_info['index'])
                self.compile_expression(bracket=True)
            elif next_token_preview == '(' or next_token_preview == '.':
                self.compile_subroutine_call(term)
            else:
                if not identifier_info:
                    raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Identifier '{term}' not defined")
                self.__vm_writer.write_memory_access('push', segment, identifier_info['index'])
        elif term == '(' or term == '[':
            parenthses, bracket = (term == '(', term == '[')
            self.compile_expression(bracket, parenthses)
        elif self.is_unary_op(term):
            self.compile_term()
            self.__vm_writer.write_arithmetic('$-' if term == '-' else term)
        else:
            raise ParseError(self.input_file_name, self.__tokenizer.current_line, f"Expected 'term: symbol | identifier' not '{term}'")

    def compile_expression_list(self) -> int:
        expression_count = 0
        while True:
            self.compile_expression()
            expression_count += 1
            next_token_preview = self.__tokenizer.get_token(True)
            if next_token_preview != ',':
                break
            #ignore symbol ','
            self.__tokenizer.get_token()
        return expression_count