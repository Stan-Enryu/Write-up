from z3 import *

a1 = [BitVec(i, 8) for i in range(3)]

s=Solver()
s.add(a1[0] + a1[1] == a1[0] * a1[2])
s.add(a1[1] / a1[2] == 20) 
s.add(a1[1] / a1[0] == 3)

s.check()
s.model()

l = [a1[i] for i in range(3)]

flag = ' '.join([str(s.model()[i].as_long()) for i in l ])
print flag
