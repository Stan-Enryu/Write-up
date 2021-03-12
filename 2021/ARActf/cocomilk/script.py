a = input("Input: ")
b = ""
c = ""

for x, y in enumerate(a):
    print (x, y)
    if x % 2 == 0:
        b += y
    else :
        c += y


# print (b)
# print (c)
c = c[::-1]
d = ""
# print (c)
for y,z in enumerate(c):
    print(y)
    d += chr(ord(z)^y^ord(b[y]))

# print (d)
print(":".join("{:02x}".format(ord(c)) for c in d))
