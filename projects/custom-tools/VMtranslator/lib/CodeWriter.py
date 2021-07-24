class CodeWriter:
    def __init__(self, output_file_path: str) -> None:
        self.output_file = open(output_file_path, 'w')
        self.arithmetic_commands = {
            "add": "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D+M",
            "sub": "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M-D",
            "and": "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D&M",
            "eq": "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@$HERE+5\nD;JEQ\nD=0\n@$HERE+3\n0;JMP\nD=-1\n@SP\nA=M-1\nM=D",
            "gt": "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@$HERE+5\nD;JGT\nD=0\n@$HERE+3\n0;JMP\nD=-1\n@SP\nA=M-1\nM=D",
            "lt": "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@$HERE+5\nD;JLT\nD=0\n@$HERE+3\n0;JMP\nD=-1\n@SP\nA=M-1\nM=D",
            "or": "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=D|M",
            "neg": "@SP\nA=M-1\nM=-M",
            "not": "@SP\nA=M-1\nM=!M"
        }
        self.memory_commands = {
            "push": "@{OFFSET}\nD=A\n@{BASE}\nA=D+{TYPE}\nD=M\n@SP\nM=M+1\nA=M-1\nM=D",
            "pop": "@{OFFSET}\nD=A\n@{BASE}\nD=D+{TYPE}\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D"
        }
        self.memory_arg1 = {
            "argument": {"BASE": "ARG", "TYPE": "M"},
            "local": {"BASE": "LCL", "TYPE": "M"},
            "this": {"BASE": "THIS", "TYPE": "M"},
            "that": {"BASE": "THAT", "TYPE": "M"},
            "pointer": {"BASE": "3", "TYPE": "A"},
            "temp": {"BASE": "5", "TYPE": "A"}
        }
        self.context = {"file": "Sys", "function": "Sys.init"}
        self.label_constant = 0

    def close(self) -> None:
        self.output_file.write("@ENDINFINITYLOOP\n(ENDINFINITYLOOP)\n0;JMP")
        self.output_file.close()

    def write_arithmetic(self, command: list) -> None:
        assembly = self.arithmetic_commands[command[0]]
        self.output_file.write(assembly + '\n')

    def write_memory(self, command: list) -> None:
        assembly = ''
        if command[1] == 'constant':
            assembly = f"@{command[2]}\nD=A\n@SP\nM=M+1\nA=M-1\nM=D"
        elif command[1] == 'static':
            if command[0] == 'push':
                assembly = f"@{'.'.join([self.context['file'],command[2]])}\nD=M\n@SP\nM=M+1\nA=M-1\nM=D"
            else: 
                assembly = f"@SP\nAM=M-1\nD=M\n@{'.'.join([self.context['file'],command[2]])}\nM=D"
        else:
            assembly = self.memory_commands[command[0]]
            assembly = assembly.format(**self.memory_arg1[command[1]], OFFSET=command[2])
        self.output_file.write(assembly + '\n')
    
    def write_label(self, command: list) -> None:
        assembly = f"({'$'.join([self.context['function'], command[1]])})"
        self.output_file.write(assembly + '\n')
    
    def write_goto(self, command: list) -> None:
        assembly = f"@{'$'.join([self.context['function'], command[1]])}\n0;JMP"
        self.output_file.write(assembly + '\n')

    def write_if(self, command: list) -> None:
        assembly = f"@SP\nM=M-1\nA=M\nD=M\n@{'$'.join([self.context['function'], command[1]])}\nD;JNE"
        self.output_file.write(assembly + '\n')

    def write_function(self, command: list) -> None:
        self.context["function"] = command[1]
        assembly = f"({command[1]})\n@SP\nA=M\n" + ("M=0\nA=A+1\n" * int(command[2])) + "D=A\n@SP\nM=D"
        self.output_file.write(assembly + '\n')

    def write_call(self, command: list) -> None:
        return_address = f'RETURN_ADDRESS_{self.label_constant}'
        push_command = '@{POINTER}\nD=M\n@SP\nM=M+1\nA=M-1\nM=D'
        self.write_memory(['push', 'constant', return_address])
        self.output_file.write(push_command.format(POINTER='LCL') + '\n')
        self.output_file.write(push_command.format(POINTER='ARG') + '\n')
        self.output_file.write(push_command.format(POINTER='THIS') + '\n')
        self.output_file.write(push_command.format(POINTER='THAT') + '\n')
        self.output_file.write(f'@{command[2]}\nD=A\n@5\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D' + '\n')
        self.output_file.write(f'@SP\nD=M\n@LCL\nM=D\n@{command[1]}\n0;JMP' + '\n')
        self.output_file.write(f"({return_address})"+ '\n')
        self.label_constant += 1

    def write_return(self) -> None:
        self.output_file.write('@LCL\nD=M\n@R13\nM=D\n@5\nA=D-A\nD=M\n@R14\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\nD=A\n@SP\nM=D+1\n@R13\nAM=M-1\nD=M\n@THAT\nM=D\n@R13\nAM=M-1\nD=M\n@THIS\nM=D\n@R13\nAM=M-1\nD=M\n@ARG\nM=D\n@R13\nAM=M-1\nD=M\n@LCL\nM=D\n@R14\nA=M\n0;JMP' + '\n')

    def write_init(self) -> None:
        self.output_file.write('@256\nD=A\n@SP\nM=D' + '\n')
        self.write_call(['call', 'Sys.init', '0'])