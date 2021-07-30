import sys
import re
import json
from lib.Parser import Parser

input_path = sys.argv[1]

#input_path = "lib/Seven.jack"
output_path = re.match(r"(.*)[.]jack$", input_path).group(1)
p = Parser(input_path)
p.tokenize()
print(p.input_token)
k = p.parse()
print(k)
with open(output_path + '.json', 'w') as f:
    json.dump(k, f, indent=4)