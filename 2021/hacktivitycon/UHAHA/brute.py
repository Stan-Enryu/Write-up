import subprocess
import sys
import os
import string

def main():
	i=1
	archive = '.\\uhaha.uha'
	f = open(".\\rockyou.txt","r")
	word = f.read().split("\n")
	# print (word[1])
	for i in range(100):
		for w in word:
			print (w)
			stdout = subprocess.call("uharc.exe e -pw{} {}".format(w,archive), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, shell=True)
			if stdout == 0:
				print("Password found: " + w)
				os.system("move uhaha.uha uhaha_{}.uha{}".format(w,i))
				os.system("move uhaha uhaha.uha")
				break
	
	print("Password not found.")

if __name__ == "__main__":
	if len(sys.argv) == 1:
		main()
		# stdout = subprocess.call("uharc.exe e -pwabc1234 .\\uhaha.uha", stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
		# # stdout = os.system("uharc.exe e -pwabc1234 .\\uhaha.uha")
		# if stdout==0:
		# 	break
		# print (stdout)
	else:
		print("missing args")

# flag{ec8753d9932766b1724618b5ad12de13}