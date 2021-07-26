import json
f = open('test.json', 'w')
json.dump({"a": r"[a-zA-Z_]\w*$"}, f)