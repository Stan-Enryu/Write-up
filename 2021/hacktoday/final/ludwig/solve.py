from Crypto.Util.number import bytes_to_long
from string import ascii_uppercase, digits
def convert(v):
    for _ in range(1337):
        v = ~(~v >> 1 ^ v)
    return v
 
v = bytes_to_long(b"VERY1234")
assert convert(v) == 9014765630940167186
 
target = [9013365925341683735,3208797737010034330,2619883148120664450]
# target = [9013365925341683735]
serialKey = b""
for t in target:
    template = b""
    for i in range(8):
        minimal = t
        hasil = {}
        for c in digits+ascii_uppercase:
            tmp = template
            tmp += c.encode()
            hasil[c] = convert(bytes_to_long(tmp.ljust(8, b'0')))
        for c in hasil:
            if minimal >= abs(t-hasil[c]):
                minimal = abs(t-hasil[c])
                curr = c
        template += curr.encode()
 
    if convert(bytes_to_long(template)) == t:
        serialKey = serialKey + template + b"-"

serialKey = serialKey[:-1]
print(serialKey)