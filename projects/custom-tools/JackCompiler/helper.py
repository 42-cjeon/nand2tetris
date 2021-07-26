import json
import re
a = [r'[a-zA-Z_]\w*$']

l = [[{"isTerminal": True, "repeat": None, "value": v}] for v in a]
f = open('tmp.json', 'w')

json.dump({"identifier": l}, f, indent=4)
f.close()