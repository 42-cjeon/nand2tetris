from Errors import MomoryError

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
    def add(self, key):
        if key not in self.symbols.keys():
            if self.cursor < 16384:
                current_cursor = self.cursor
                self.symbols[key] = current_cursor
                self.cursor += 1
                return current_cursor

            else:
                raise MomoryError('Maximum Hack memory exceded [16383]')
    def get(self, key):
        try:
            return self.symbols['key']
        except KeyError:
            return self.add(key)