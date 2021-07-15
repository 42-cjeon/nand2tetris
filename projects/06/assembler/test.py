from Parser import Parser
from Code import Code
from command_type import COMMANDTYPE

p = Parser('C:\\Users\\anduuin\\Projects\\nand2tetris\\projects\\06\\pong\\PongL.asm')
c = Code()
f = open("C:\\Users\\anduuin\\Projects\\nand2tetris\\projects\\06\\pong\\PongL.hack", 'w')
while p.advance():
    c_type = p.command_type()
    if c_type == COMMANDTYPE.COMMENT:
        continue
    elif c_type == COMMANDTYPE.L_COMMAND:
        raise NotImplementedError
    elif c_type == COMMANDTYPE.A_COMMAND:
        text = p.symbol()
    elif c_type == COMMANDTYPE.C_COMMAND:
        text = {
            'jump': p.jump(),
            'dest': p.dest(),
            'comp': p.comp()
        }
    f.write(c.convert(text, c_type) + '\n')
f.close()