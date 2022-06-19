#!/usr/bin/env python3
import sys

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
sys.stdout = Unbuffered(sys.stdout)

MEMORY = [None for i in range(10**6 + 1)]
EBP = 10**6
ESP = 10**6
EIP = 10**6

ADDRESS = dict()
FUNC = {
    "WINN": [
        "PUSH EBP",
        "EBP = ESP",
        "ESP = ESP - 100",
        "write_memory(ESP, open('flag.txt').read(), True)",
        "print('Congratz, you get what u want!')",
        "print(read_memory(ESP)[0])",
        "ESP = EBP",
        "POP EBP",
        "RETURN"
    ],
    "VULN": [
        "PUSH EBP",
        "EBP = ESP",
        "ESP = ESP - 150",
        "write_memory(ESP, input(), True)",
        "print(f'Welcome {read_memory(ESP, 50)[0]}!')",
        "ESP = EBP",
        "POP EBP",
        "RETURN"
    ],
    "MAIN": [
        "PUSH EBP",
        "EBP = ESP",
        "ESP = ESP - 50",
        "print('Enter your name plz!')",
        "ESP = EBP",
        "CALL VULN",
        "RETURN"
    ]
}

def write_memory(idx, val, addEndl = False):
    if addEndl == True: val = val + "\n"
    # print (val)
    for c in val:
        MEMORY[idx] = c
        idx += 1
    return idx
    
def read_memory(idx, size = 9999999999):
    ret = ""
    lim = idx + size
    while MEMORY[idx] != "\n" and idx < lim:
        ret += MEMORY[idx]
        idx += 1
    return ret, idx + 1

def EVAL(ins):
    global EBP, ESP, EIP
    if ins[:4] == "CALL":
        func_called = ins[5:]
        EIP_hex = hex(EIP)[2:].rjust(8,'0')
        ESP = ESP - 8
        write_memory(ESP, EIP_hex)
        EIP = ADDRESS[func_called]

    elif ins[:4] == "PUSH":
        var_name = ins[5:]
        var_hex = hex(eval(var_name))[2:].rjust(8,'0')
        ESP = ESP - 8
        write_memory(ESP, var_hex)
    elif ins[:3] == "POP":
        var_name = ins[4:]
        var_hex = read_memory(ESP, 8)[0]
        # print (var_name)
        # print (var_hex)
        exec(f"{var_name} = int('{var_hex}', 16)") 
        ESP = ESP + 8
    elif ins == "RETURN":
        EIP_hex = read_memory(ESP, 8)[0]
        EIP = int(EIP_hex, 16)
        ESP = ESP + 8
    else:
        exec(ins, globals())
    

def mount_code(idx_begin, func_name):
    ADDRESS[func_name] = idx_begin
    idx_now = idx_begin
    for ins in FUNC[func_name]:
        idx_now = write_memory(idx_now, ins + "\n")
    return idx_now

def run():
    global EIP, EBP, ESP
    cnt_idx = 48869
    for f_name in FUNC:
        cnt_idx = mount_code(cnt_idx + 10, f_name)

    EVAL("CALL MAIN")
    # EIP = 
    # print ('asdf', ADDRESS['WINN'])
    while(EIP != 10 ** 6):
        ins, EIP = read_memory(EIP)
        # print (ins,EIP)
        EVAL(ins)


if __name__ == "__main__":
    run()