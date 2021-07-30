from lib.DataIdentifier import DATAIDENTIFIER

class SymbolTable:
    def __init__(self) -> None:
        self.class_scope_table = {}
        self.function_scope_table = {}
        self._var_count = [0, 0, 0, 0]
        self.current_scope = "main"

    def start_subroutine(self, scope: str):
        if scope not in self.function_scope_table.keys():
            self.function_scope_table[scope] = {}
        self.current_scope = scope
    
    # _scope_table : dict {name: {"type": var_type: str, kind: kind: DATAIDENTIFIER, index: k: int}}
    def define(self, name: str, var_type: str, kind: DATAIDENTIFIER) -> int:
        if kind == DATAIDENTIFIER.STATIC or kind == DATAIDENTIFIER.FIELD:
            target_table = self.class_scope_table
        elif kind == DATAIDENTIFIER.VAR or DATAIDENTIFIER.ARG:
            target_table = self.function_scope_table[self.current_scope]
        else:
            raise SyntaxError()
        
        var_count = self._var_count[kind]
        target_table[name] = {
            "type": var_type,
            "kind": kind,
            "index": var_count 
        }
        self._var_count[kind] += 1
        return var_count

    def get_var_info(self, name):
        # search from function scope first
        if name in self.function_scope_table[self.current_scope].keys():
            return self.function_scope_table[self.current_scope][name]
        # then class scope
        elif name in self.class_scope_table.keys():
            return self.class_scope_table[name]
        else:
            raise SyntaxError()