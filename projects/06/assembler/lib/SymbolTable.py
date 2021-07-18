from lib.Errors import MomoryError

class SymbolTable:
    def __init__(self) -> None:
        self.symbols = {
            **{f'R{i}': i for i in range(16)},
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'SCREEN': 16384,
            'KBD': 24576
        }
        self.cursor = 16
    def add(self, key:str, value:int=None) -> int:
        if value != None:
            if 0 <= value < 2 ** 16:
                self.symbols[key] = value
                return value
            else:
                raise MomoryError('invalid memory address (ROM)')
        elif self.cursor < 16384:
            current_cursor = self.cursor
            self.symbols[key] = current_cursor
            self.cursor += 1
            return current_cursor
        else:
            raise MomoryError('Maximum memory address (RAM) exceded [16383]')
    def get(self, key:str, value:int=None) -> int:
        try:
            return self.symbols[key]
        except KeyError:
            return self.add(key, value)