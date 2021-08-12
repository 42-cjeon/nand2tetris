class VmWriter:
    def __init__(self, output_file_path) -> None:
        self.output_file = open(output_file_path, 'w')
        self.arithmetic_command = {'+': 'add', '-': 'sub', '$-': 'neg', '=': 'eq', '>': 'gt', '<': 'lt', '&': 'and', '|': 'or', '~': 'not', '*': self.__write_multiply, '/': self.__write_divide}
        self.memory_command = ['push', 'pop']
        self.memory_segment = ['argument', 'local', 'static', 'this', 'that', 'pointer', 'temp', 'constant']
        self.control_flow_command = ['label', 'goto', 'if-goto']

    def close(self):
        self.output_file.close()

    def __write(self, *command):
        self.output_file.write(' '.join(command) + '\n')

    def write_arithmetic(self, operator: str):
        command = self.arithmetic_command.get(operator)
        if command:
            if callable(command):
                command()
            else:
                self.__write(command)
    
    def write_memory_access(self, command: str, segment: str, index: str):
        if command in self.memory_command and segment in self.memory_segment:
            self.__write(command, segment, index)

    def write_function(self, command: str, arg1: str=None, arg2: str=None):
        if command == "function" or command == "call":
            if arg1 and arg2:
                self.__write(command, arg1, arg2)
        elif command == "return":
            self.__write(command)
    
    def write_control_flow(self, command: str, label: str):
        if command in self.control_flow_command and label:
            self.__write(command, label)

    def __write_multiply(self):
        self.write_function('call', 'Math.multiply', '2')
    def __write_divide(self):
        self.write_function('call', 'Math.divide', '2')