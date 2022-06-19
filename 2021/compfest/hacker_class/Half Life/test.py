flag = zip([93, 380, 529, 808, 1028, 1307], [361, 1346, 1891, 2819, 3641, 4830])

f=(lambda x: lambda y: x(x, y)) ( 
		lambda f, x: x if (lambda x: False if x == 1 else 
			( 
			 	lambda x: False if x == 1 else 
			 	(lambda x: True if x == 1 else False)
			 		( 
			 			x//( lambda x: [i for i in range(1, x+1) 
			 			if (lambda x, y, z: z(x, y, z))(x, i, lambda x, y,z: x if x < y else z(x - y, y, z)) == 0] [1] )
			 			(x) 
			 		) 
			)

			( x//
			 ( lambda x: [i for i in range(2, x+1) 
			 	if not (lambda x, y, z: x(z, y, x))
			 	(lambda x, y, z: x + y if x < 0 else z(x - y, y, z), i, x)][0] )(x) 
			) 
			 )(x) else f(f, x+1) 
		)
idx =1
for i,j in flag:
	print (i,j)
	y = 1
	# print (idx)
	if idx == 1 :
		temp = [y-1 for i in range(i) if (y := f(y)+1)]
		idx =

# for i in range(len(x)):
# 	print (x[i+1]-x[i], end=' ')
