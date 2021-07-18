a = open('Pong-A.hack', 'r')
b = open('Pong.hack', 'r')

l_a = True
l_b = True
l = 1
while l_a and l_b:
    l_a = a.readline()
    l_b = b.readline()
    try:
        assert(l_a == l_b)
    except AssertionError:
        print(l)
        raise AssertionError
    l += 1
print("success!")
a.close()
b.close()