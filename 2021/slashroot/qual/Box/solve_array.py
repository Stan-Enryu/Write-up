def create(pam1):
	local_28 = pam1
	if ((local_28 & 0xff) == 0):
		local_28 = 105
	for i in range(255):
		local_28 = local_28 ^ (local_28 & 7) << 5
		local_28 = local_28 ^ local_28 >> 3
		local_28 = local_28 ^ (local_28 & 3) << 6
		keys.append(local_28)

def secret(param_1):
	return keys[(param_1 ^ (param_1 >> 6 | param_1 * 4) & 0xff ^
	(param_1 << 6 | param_1 >> 2) & 0xff)]
# 0x19 S
# 0xa2 l
for i in range(0xff):
	keys = []
	create(i)
	if secret(0 ^ ord("S")) == 0x19:
		print "key :", i
		print keys
		break
for i in range(0xff):
	keys = []
	create(i)
	if secret(1 ^ ord("l")) == 0xa2:
		print "key :", i
		print keys
		break