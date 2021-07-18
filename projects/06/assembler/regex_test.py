import re
from itertools import permutations

base_char = ['-', '&', '|', '+', 'A', 'M', 'D']

print(list(permutations(base_char, 3)))


r = re.compile(r'D[+-|&][AM]|A[+-|&]D|M[+-|&]D|[AMD][-+]1|[-!]?[AMD]|-?1|0')
while True:
    print(bool(r.fullmatch(input("text : "))))