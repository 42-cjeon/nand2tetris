from lib.DataIdentifier import DATAIDENTIFIER
from lib.SymbolTable import SymbolTable

class CompileEngine:
    def __init__(self, parsed_code) -> None:
        self.parsed_code = parsed_code
        self.class_name = parsed_code["name"]
        self.symbol_table = SymbolTable()

    def compile_class(self, code_snippet):
        reusult = ""
        for element in code_snippet:
            if element["name"] == "classVarDec":
                result += self.compile_class_var_dec(element)
            elif element["name"] == "subroutineDec":
                result += self.compile_subroutine_dec(element)
        return result

    def compile_class_var_dec(self, code_snippet):
        if code_snippet[0] == DATAIDENTIFIER.STATIC:
            kind = DATAIDENTIFIER.STATIC
        elif code_snippet[0] == DATAIDENTIFIER.FIELD:
            kind = DATAIDENTIFIER.FIELD
        var_type = code_snippet[1]["value"][0]["value"]
        if isinstance(var_type, list):
            var_type = var_type[0]["value"]

        result = ""
        for element in code_snippet[2:]:
            if element["name"] == "varName":
                name = element["value"][0]["value"]
            elif element["name"] == "varNameRepeat":
                name = element["value"][1]["value"][0]["value"]
            else:
                raise SyntaxError()
            index = self.symbol_table.define(name, var_type, kind)
            result += f"push static {index}"

        return result


    def compile_subroutine_dec(self, code_snippet):
        pass

    def compile_parameter_list(self, code_snippet):
        pass

    def compile_statements(self, code_snippet):
        pass
    def compile_expression_list(self, code_snippet):
        pass
    
    def compile_var_dec(self, code_snippet):
        pass
   
    def compile_do(self, code_snippet):
        pass
    def compile_let(self, code_snippet):
        pass
    def compile_while(self, code_snippet):
        pass
    def compile_if(self, code_snippet):
        pass
    def compile_return(self, code_snippet):
        pass
    def compile_term(self, code_snippet):
        pass
    def compile_expression(self, code_snippet):
        pass

    '''
    def compile(self, code_snippet):
        stack = deque([self.parsed_code])
        result = ""
        elements = stack.pop()["value"]

        for element in elements:
            if element["name"] == "classVarDec":
                result += self.compile_class_var_dec(element["value"])
            elif element["name"] == "varDec":
                result += self.compile_var_dec(element["value"])
            elif element["name"] == "subroutineDec":
                result += self.compile_subroutine_dec(element["value"])
            elif element["name"] == "doStatement":
                result += self.compile_do(element["value"])
            elif element["name"] == "letStatement":
                result += self.compile_let(element["value"])
            elif element["name"] == "whileStatement":
                result += self.compile_while(element["value"])
            elif element["name"] == "ifStatement":
                result += self.compile_if(element["value"])
            elif element["name"] == "returnStatement":
                result += self.compile_return(element["value"])
            elif element["name"] == "term":
                result += self.compile_term(element["value"])
            elif element["name"] == "expression":
                result += self.compile_expression(element["value"])
            else:
                stack.push()
    '''