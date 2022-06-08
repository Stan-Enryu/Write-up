# uncompyle6 version 2.11.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Apr 20 2020, 20:30:41) 
# [GCC 9.3.0]
# Embedded file name: ransom.py
# Compiled at: 2021-11-20 13:50:14
import os
import random
import string
import subprocess
from pwn import xor
from hashlib import md5

def ba134bc34ef1(dee6266bdfff):
    assert dee6266bdfff[19] + dee6266bdfff[8] - dee6266bdfff[13] + dee6266bdfff[9] == 242
    assert dee6266bdfff[16] - dee6266bdfff[8] - dee6266bdfff[9] * dee6266bdfff[1] - dee6266bdfff[19] == -5796
    assert dee6266bdfff[14] * dee6266bdfff[15] == 13221
    assert dee6266bdfff[2] * dee6266bdfff[13] + dee6266bdfff[6] == 11716
    assert dee6266bdfff[7] + dee6266bdfff[4] * dee6266bdfff[7] * dee6266bdfff[2] == 1179995
    assert dee6266bdfff[15] * (dee6266bdfff[12] + 1) + dee6266bdfff[14] == 11345
    assert dee6266bdfff[19] * dee6266bdfff[18] - dee6266bdfff[20] * dee6266bdfff[4] - dee6266bdfff[13] == -326


def ba134bc34ef2(dee6266bdfff):
    assert dee6266bdfff[3] * dee6266bdfff[0] * dee6266bdfff[5] == 1597956
    assert dee6266bdfff[3] * dee6266bdfff[9] - dee6266bdfff[8] == 12200
    assert dee6266bdfff[1] - dee6266bdfff[5] * dee6266bdfff[9] - dee6266bdfff[5] + dee6266bdfff[1] == -13114
    assert dee6266bdfff[11] * dee6266bdfff[4] + dee6266bdfff[9] == 12423
    assert dee6266bdfff[14] * dee6266bdfff[19] + dee6266bdfff[3] == 12654
    assert dee6266bdfff[16] * dee6266bdfff[0] * dee6266bdfff[4] * dee6266bdfff[18] == 134197560
    assert dee6266bdfff[17] + dee6266bdfff[16] * dee6266bdfff[19] + dee6266bdfff[13] * dee6266bdfff[7] == 20478
    assert dee6266bdfff[14] + dee6266bdfff[4] * dee6266bdfff[7] - dee6266bdfff[8] == 10252


def ba134bc34ef3(dee6266bdfff):
    assert dee6266bdfff[17] + dee6266bdfff[0] * dee6266bdfff[10] * dee6266bdfff[11] == 1627352
    assert dee6266bdfff[17] + dee6266bdfff[16] - dee6266bdfff[15] + dee6266bdfff[12] == 191
    assert dee6266bdfff[8] + dee6266bdfff[5] * dee6266bdfff[14] == 13455
    assert dee6266bdfff[5] * dee6266bdfff[2] == 13570
    assert dee6266bdfff[20] - dee6266bdfff[8] + dee6266bdfff[1] * dee6266bdfff[12] - dee6266bdfff[12] == 4739
    assert dee6266bdfff[5] + dee6266bdfff[6] + dee6266bdfff[9] == 330
    # assert md5(dee6266bdfff).hexdigest() == 'bfe0f7cd0a926ec05cee3717bd9bce20'


def generatedee6266bdfff():
    from secret import dee6266bdfff
    print dee6266bdfff
    print dee6266bdfff[16] - dee6266bdfff[8] - dee6266bdfff[9] * dee6266bdfff[1] - dee6266bdfff[19]
    ba134bc34ef1(dee6266bdfff)
    ba134bc34ef2(dee6266bdfff)
    ba134bc34ef3(dee6266bdfff)
    dee6266bdfff_int = int.from_bytes(dee6266bdfff, byteorder='big')
    for i in range(4):
        dee6266bdfff_int >>= dee6266bdfff[i * 4]
        dee6266bdfff_int <<= dee6266bdfff[i * 4]

    dee6266bdfff = dee6266bdfff_int.to_bytes(len(dee6266bdfff), 'big')
    return dee6266bdfff


def ransom(c651bca63aaas, dee6266bdfff):
    c651bca63aaa = open(c651bca63aaas, 'rb').read()
    rdee6266bdfff = os.urandom(len(dee6266bdfff))
    dee6266bdfff2 = xor(rdee6266bdfff, dee6266bdfff)
    a622337 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)).encode()
    w = open('ransom/broke_' + a622337 + '.pdf', 'wb+')
    w.write(os.urandom(1337))
    w.write(xor(c651bca63aaa[:5] * 5, dee6266bdfff2))
    w.write(xor(c651bca63aaa[5:], rdee6266bdfff))
    w.write(os.urandom(1337))


dee6266bdfff = generatedee6266bdfff()
print (dee6266bdfff)
baab3636 = subprocess.check_output('ls | grep .text', shell=True).split('\n')[:-1]
for _ in baab3636:
    ransom(_, dee6266bdfff)
# okay decompiling ./ransom.pyc
