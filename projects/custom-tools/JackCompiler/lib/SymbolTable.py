from lib.Enums import DATAIDENTIFIER
from lib.Errors import ParseError

class SymbolTable:
    def __init__(self) -> None:
        self.class_scope_table = {}
        self.function_scope_table = {}
        self._var_count = [0, 0, 0, 0]
        self.current_scope = "unknown"

    def start_subroutine(self, scope: str):
        self.function_scope_table = {}
        self.current_scope = scope
        self._var_count[2] = 0
        self._var_count[3] = 0
    
    # _scope_table : dict {name: {"type": var_type: str, kind: kind: DATAIDENTIFIER, index: k: int}}
    def define(self, name: str, var_type: str, kind: DATAIDENTIFIER) -> int:
        if kind == DATAIDENTIFIER.STATIC or kind == DATAIDENTIFIER.FIELD:
            target_table = self.class_scope_table
        elif kind == DATAIDENTIFIER.VAR or DATAIDENTIFIER.ARG:
            target_table = self.function_scope_table
        else:
            raise SyntaxError()
        
        var_count = self._var_count[kind.value]
        
        target_table[name] = {
            "type": var_type,
            "kind": kind,
            "index": str(var_count)
        }
        self._var_count[kind.value] += 1
        return var_count

    def get_var_info(self, name):
        # search from function scope first
        if name in self.function_scope_table.keys():
            return self.function_scope_table[name]
        # then class scope
        elif name in self.class_scope_table.keys():
            return self.class_scope_table[name]
        else:
            return None
    
    def get_field_var_count(self):
        return self._var_count[DATAIDENTIFIER.FIELD.value]