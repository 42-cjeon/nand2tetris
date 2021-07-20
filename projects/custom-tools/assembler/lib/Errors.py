class ParseError(Exception):
    def __init__(self, file_name, line, message) -> None:
        self.file_name = file_name
        self.line = line
        self.message = message

class MemoryError(Exception):
    def __init__(self, message) -> None:
        self.message = message