from math import *
import time
import datetime

# G's of Acceleration
Accel = 0.2

# % Speed of light to coast at
V_Coast = 0.25

# Conversion Factor
metersInALightYear = 9.461e15

# Initial Speed
Vi = 0

# Time Step (seconds)
timeStep = 1*60*60

###############
### Convert ###
###############

# G -> m/s
Accel *= 9.81

#################
### FUNCTIONS ###
#################

def LorenzFactor(vel):
    try:
        return sqrt(1-(vel**2) / (299792458.0**2))
    except:
        print "Illegal Value:",vel
        raise

###########
### RUN ###
###########

dDistance = 0
dTime = 0
V = Vi
V_Coast *= 299792458.0
update = time.time()

while(V <= V_Coast):
    # Calculate Acceleration
    V_Old = V
    V += Accel * timeStep * LorenzFactor(V)
    while(V >= 299792458.0):
        print "Reduce Time Steps!"
        print "New Time Step:",timeStep
        print "    V:",V
        print "V_Old:",V_Old
        time.sleep(0.1)
        timeStep/=2.0
        V=V_Old
        V += Accel * timeStep * LorenzFactor(V)

    # Calculate Disance Traveled
    dDistance += V * timeStep * LorenzFactor(V)
    dTime += timeStep * LorenzFactor(V)

    if(time.time() > update + 10):
        print "dDistance:",dDistance
        print "dTime:",dTime
        print "%% of trip:",dDistance/float(Distance_Total)*100
        update = time.time()

print "Distance Traveled(m):",dDistance
print "Distance Traveled(ly):",dDistance/9.461e15
print "Time Taken:",datetime.timedelta(seconds = dTime)
print "Time Taken(y): %0.1f" % (datetime.timedelta(seconds = dTime).days/365.24)
print "Final Velocity(m/s):",V
print "Final LorenzFactor:",LorenzFactor(V)
print "%% C: %0.2f%%" % (V/299792458.0*100)