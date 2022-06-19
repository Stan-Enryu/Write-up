HOUSE of lore or Tcache statshing unlink

fake1 
fd : real 
bk : fake2 

fake2 
fd : fake1
bk :

real / small-bin
fd : 
bk : fake1


fake1 = heap + 0x80
fd : real / small-bin = 0x10
bk : fake2 = 0x20

fake2 = 0x20
fd : fake1
bk :

real / small-bin = 0x10
fd : 
bk : fake1