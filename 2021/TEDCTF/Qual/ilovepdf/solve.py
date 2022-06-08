from z3 import *

# 1597956
from hashlib import md5
a1 = [BitVec(i, 32) for i in range(21)]

s=Solver()

s.add(a1[16] - a1[8] - a1[19] - (a1[9] * a1[1])  == -5796)
# s.add( - (a1[9] * a1[1])  == -5796 + a1[19] - a1[16] + a1[8])
s.add( (a1[9] * a1[1])  == 5796 + a1[16] - a1[19] - a1[8])

s.add(a1[19] + a1[8] - a1[13] + a1[9] == 242)

s.add(a1[14] * a1[15] == 13221)
s.add(a1[2] * a1[13] + a1[6] == 11716)
s.add(a1[7] + a1[4] * a1[7] * a1[2] == 1179995)
s.add(a1[15] * (a1[12] + 1) + a1[14] == 11345)
s.add(a1[19] * a1[18] - a1[20] * a1[4] - a1[13] == -326)

s.add(a1[3] * a1[9] - a1[8] == 12200)
s.add(a1[1] - a1[5] * a1[9] - a1[5] + a1[1] == -13114)

s.add(a1[14] * a1[19] + a1[3] == 12654)
s.add(a1[16] * a1[0] * a1[4] * a1[18] == 134197560)
s.add(a1[17] + a1[16] * a1[19] + a1[13] * a1[7] == 20478)
s.add(a1[14] + a1[4] * a1[7] - a1[8] == 10252)
s.add(a1[17] + a1[0] * a1[10] * a1[11] == 1627352)
# s.add(1627352 - a1[17] == a1[0] * a1[10] * a1[11])

s.add(a1[17] + a1[16] - a1[15] + a1[12] == 191)
s.add(a1[8] + a1[5] * a1[14] == 13455)
s.add(a1[5] * a1[2] == 13570)
s.add(a1[20] - a1[8] + a1[1] * a1[12] - a1[12] == 4739)
s.add(a1[5] + a1[6] + a1[9] == 330)




s.add(a1[3] * a1[0] * a1[5] == 1597956)
s.add(a1[11] * a1[4] + a1[9] == 12423)
# s.add(md5([s.model()[i].as_long() for i in a1 ]).hexdigest() == 'bfe0f7cd0a926ec05cee3717bd9bce20')


s.check()

l = [a1[i] for i in range(21)]

helo = [str(s.model()[i].as_long()) for i in l ]
flag = ' , '.join(helo)
result = 'dee6266bdfff =  ['+flag+']'
print (result)
# with open("secret.py", 'wb') as f:

# 	f.write(result)

print md5([123,123]).hexdigest()