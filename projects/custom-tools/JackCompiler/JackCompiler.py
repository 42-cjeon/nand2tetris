import sys
import re

from lib.Parser import Parser

input_path = sys.argv[1]
output_path = re.match(r"(.*)[.]jack$", input_path).group(1)
p = Parser(input_path)
p.tokenize()
print(p.input_token)
k = p.parse()
print(k)
with open(output_path + '.xml', 'w') as f:
    f.write(k)