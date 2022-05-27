import numpy as np
import hashlib
from z3 import *

a = Int('a')
b = Int('b')
c = Int('c')
d = Int('d')
solve(	50*a+11*b+18*c+12*d==7681,
		18*a+12*b+23*c+2*d==4019,
		21*a+11*b+35*c+42*d==7160,
		47*a+2*b+12*c+40*d==8080	)

data = np.array([[50, 11, 18, 12], [18, 12, 23, 2], [21, 11, 35, 42], [47, 2, 12, 40]])
my_input = chr(110)+chr(33)+chr(67)+chr(51)
password = np.array(list(map(ord, list(my_input[:4].ljust(4, '\x00')))))
result = list(np.matmul(data, password))
print(result)
if result == [7681, 4019, 7160, 8080]:
	print("Congratz, here is your flag: COMPFEST12{" + hashlib.sha384(bytes(my_input.encode())).hexdigest() + "}")
