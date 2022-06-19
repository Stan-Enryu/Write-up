import sys

sys.setrecursionlimit(10000)

flag = zip([93, 380, 529, 808, 1028, 1307, 1443, 1645, 1750, 2035, 2198, 2308, 2592, 5431, 7221, 9553, 11449, 13429, 15359, 18268, 20677, 22690, 24310, 26342, 28561, 53607, 65550, 90362, 112012, 124846, 149572, 167415, 179176, 192577, 202971, 226896, 238931, 238927, 400885, 400882, 400886, 400881, 400880, 400878, 400881, 400888, 400887, 400885, 400884, 400878, 400878], [361, 1346, 1891, 2819, 3641, 4830, 5354, 6038, 6491, 7678, 8258, 8597, 9926, 21419, 28968, 38992, 46992, 55790, 64359, 77179, 87908, 96952, 104085, 113381, 123382, 239010, 295104, 413285, 517955, 580204, 700856, 788889, 847166, 913771, 965098, 1084194, 1144811, 1144617, 1967166, 1967140, 1967123, 1967205, 1967177, 1967172, 1967189, 1967119, 1967109, 1967167, 1967136, 1967107, 1967179]) 

x = [93, 380, 529, 808, 1028, 1307, 1443, 1645, 1750, 2035, 2198, 2308, 2592, 5431, 7221, 9553, 11449, 13429, 15359, 18268, 20677, 22690, 24310, 26342, 28561, 53607, 65550, 90362, 112012, 124846, 149572, 167415, 179176, 192577, 202971, 226896, 238931, 238927, 400885, 400882, 400886, 400881, 400880, 400878, 400881, 400888, 400887, 400885, 400884, 400878, 400878]
for i in range(len(x)):
	if i == 1:
		print (x[i], end=' ')
	else:
		print (x[i]-x[i-1], end=' ')

# print (flag)
# temp = [y-1 for i in range(20) if (y := 1+1)]
# i 93 380 2819 1967179 j 361 
# print (temp)
# print( chr(
# 		361 ^  
# 		(lambda x, f=(lambda x: lambda y: x(x, y)) ( lambda f, x: x if (lambda x: False if x == 1 else ( 
# 			 	lambda x: False if x == 1 else 
# 			 	(lambda x: True if x == 1 else False )
# 			 		( 
# 			 			x//( lambda x: [i for i in range(1, x+1) 
# 			 			if (lambda x, y, z: z(x, y, z))(x, i, lambda x, y, z: x if x < y else z(x - y, y, z)) == 0][1] )(x) 
# 			 		) 
# 			 )( x//( lambda x: [i for i in range(2, x+1) 
# 			 	if not (lambda x, y, z: x(z, y, x))(lambda x, y, z: x + y if x < 0 else z(x - y, y, z), i, x)][0] )(x) ) 
# 			 )(x) else f(f, x+1) 
# 		), 
# 		y=1: [y-1 for i in range(x) if (y := f(y)+1)][-1] 

# 		)
# 		(93)

# 		), flush=True )

# print (
# 	(lambda x, f=(lambda x: lambda y: x(x, y)) ( 
# 		lambda f, x: x if (lambda x: False if x == 1 else 
# 			( 
# 			 	lambda x: False if x == 1 else 
# 			 	(lambda x: True if x == 1 else False)
# 			 		( 
# 			 			x//( lambda x: [i for i in range(1, x+1) 
# 			 			if (lambda x, y, z: z(x, y, z))(x, i, lambda x, y,z: x if x < y else z(x - y, y, z)) == 0] [1] )
# 			 			(x) 
# 			 		) 
# 			)

# 			( x//
# 			 ( lambda x: [i for i in range(2, x+1) 
# 			 	if not (lambda x, y, z: x(z, y, x))
# 			 	(lambda x, y, z: x + y if x < 0 else z(x - y, y, z), i, x)][0] )(x) 
# 			) 
# 			 )(x) else f(f, x+1) 
# 		), 
# 		y=1: [y-1 for i in range(x) if (y := f(y)+1)] 
# 		)
# 		(93))

# print ( ( lambda x: [i for i in range(1, x+1)(lambda x, y, z: z(x, y, z))(x, i, lambda x, y,z: x if x < y else z(x - y, y, z)) == 0][1] )(1))

# f=(lambda x: lambda y: x(x, y)) ( lambda f, x: x if (lambda x: False if x == 1 else ( 
# 			 	lambda x: False if x == 1 else 
# 			 	(lambda x: True if x == 1 else False )
# 			 		( 
# 			 			x//( lambda x: [i for i in range(1, x+1) 
# 			 			if (lambda x, y, z: z(x, y, z))(x, i, lambda x, y,z: x if x < y else z(x - y, y, z)) == 0][1] )(x) 
# 			 		) 
# 			 )  ( x//
# 			 ( lambda x: 
# 			 	[i for i in range(2, x+1) 
# 			 	if not (lambda x, y, z: x(z, y, x))
# 			 	(lambda x, y, z: x + y if x < 0 else z(x - y, y, z), i, x)][0] )(x) 
# 			 	) 
# 			 )(x) else f(f, x+1) 
# 		)

# print (x(380, 2))
# print (f(380))
# print (
# 	(lambda x, f=(lambda x: lambda y: x(x, y)) ( lambda f, x: x if (lambda x: False if x == 1 else ( 
# 			 	lambda x: False if x == 1 else 
# 			 	(lambda x: True if x == 1 else False )
# 			 		( 
# 			 			x//( lambda x: [i for i in range(1, x+1) 
# 			 			if (lambda x, y, z: z(x, y, z))(x, i, lambda x, y,z: x if x < y else z(x - y, y, z)) == 0][1] )(x) 
# 			 		) 
# 			 )  ( x//
# 			 ( lambda x: [i for i in range(2, x+1) 
# 			 	if not (lambda x, y, z: x(z, y, x))
# 			 	(lambda x, y, z: x + y if x < 0 else z(x - y, y, z), i, x)][0] )(x) 
# 			 	) 
# 			 )(x) else f(f, x+1) 
# 		), 
# 		y=1: [y-1 for i in range(x) if (y := f(y)+1)] 
# 		)
# 		(10394))
# for i,j in flag:
	
# 	print (i,j)
# 	print( chr(
# 		j ^  
# 		(lambda x, f=(lambda x: lambda y: x(x, y)) ( lambda f, x: x if (lambda x: False if x == 1 else ( 
# 			 	lambda x: False if x == 1 else 
# 			 	(lambda x: True if x == 1 else False )
# 			 		( 
# 			 			x//( lambda x: [i for i in range(1, x+1) 
# 			 			if (lambda x, y, z: z(x, y, z))(x, i, lambda x, y, z: x if x < y else z(x - y, y, z)) == 0][1] )(x) 
# 			 		) 
# 			 )( x//( lambda x: [i for i in range(2, x+1) 
# 			 	if not (lambda x, y, z: x(z, y, x))(lambda x, y, z: x + y if x < 0 else z(x - y, y, z), i, x)][0] )(x) ) 
# 			 )(x) else f(f, x+1) 
# 		), 
# 		y=1: [y-1 for i in range(x) if (y := f(y)+1)][-1] 

# 		)
# 		(i)

# 		), end='', flush=True )

		




