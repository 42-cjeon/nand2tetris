from lib.CommandType import COMMANDTYPE

class Code:
    def __init__(self):
        self.dest_table = {
            "null0": "000",
            "M"    : "001",
            "D"    : "010",
            "DM"   : "011",
            "A"    : "100",
            "AM"   : "101",
            "AD"   : "110",
            "ADM"  : "111"
        }
        self.jump_table = {
            "null": "000",
            "JGT" : "001",
            "JEQ" : "010",
            "JGE" : "011",
            "JLT" : "100",
            "JNE" : "101",
            "JLE" : "110",
            "JMP" : "111",
        }
        self.comp_table = {
            "0"  : "101010",
            "1"  : "111111", 
            "-1" : "111010", 
            "D"  : "001100", 
            "A"  : "110000", 
            "!D" : "001101", 
            "!A" : "110001", 
            "-D" : "001111", 
            "-A" : "110011", 
            "D+1": "011111",
            "1+D": "011111", 
            "A+1": "110111",
            "1+A": "110111", 
            "D-1": "001110", 
            "A-1": "110010", 
            "D+A": "000010",
            "A+D": "000010", 
            "D-A": "010011", 
            "A-D": "000111", 
            "D&A": "000000",
            "A&D": "000000", 
            "D|A": "010101",
            "A|D": "010101"
        }
    def convert(self, text: dict) -> str:
        command_type = text['type']
        if command_type == COMMANDTYPE.A:
            return f"0{int(text['symbol']):015b}"
        elif command_type == COMMANDTYPE.C:
            a_field = 0
            if "M" in text["comp"]:
                a_field = 1
                text["comp"] = text["comp"].replace("M", "A")
            comp = f'{a_field}{self.comp_table[text["comp"]]}'
            jump = self.jump_table[text["jump"]]
            dest = self.dest_table[text["dest"]]

            return f"111{comp}{dest}{jump}"