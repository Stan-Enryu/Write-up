import re
file = open('dotbat')
data = file.read()
file.close()
r = "jgigtgxzswbhmushio"
capturere = re.compile('%r:~(?P<index>[0-9]+),(?P<count>[0-9]+)%')
nocapturere = re.compile('%r:~[0-9]+,[0-9]+%')
indices = capturere.findall(data)
data = nocapturere.split(data)
out = data[0]
for i in range(1, len(data)):
    try:
        con = r[int(indices[i-1][0]):int(indices[i-1][1])+int(indices[i-1][0])]
        out += con + data[i]
    except:
        print(i, indices[i])
file2 = open('dotbat.bat', 'r+')
file2.write(out)
file2.close()