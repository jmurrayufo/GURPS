import random

Colonists = 240 + 60 - 54

print Colonists

for i in range(Colonists-5):
    tmp = random.gauss(50000,6000)
    # print "$%0.2f" % tmp
    if(tmp > 50000):
        print "%d,$%0.2f" % (i,tmp-50000)