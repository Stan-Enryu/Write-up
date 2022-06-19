
# 82174e d8dbeb cee3bd d38bd6 5e44f5 c6490d
# enc ="82174e d8dbeb cee3bd d38bd6 5e44f5 c6490d"
enc = ["82174e", "d8dbeb","cee3bd","d38bd6","5e44f5","c6490d"]
valid = []

for i in range(96,123):
    valid.append(i)
for i in range(47,58):
    valid.append(i)
for i in range(95,96):
    valid.append(i)


flag =""
for enc_flag in enc:
    for i in valid:
        for j in valid:
            for k in valid:
                for l in valid:

                    temp = i ^ j

                    temp *= k

                    temp += l

                    temp = temp ^ (i * i * i)

                    temp *= i

                    temp -= k

                    temp = temp % 0xffffff

                    if enc_flag == str(hex(temp)[2:]):
                        flag += chr(i)
                        flag += chr(j)
                        flag += chr(k)
                        flag += chr(l)

print len(flag)
print flag
