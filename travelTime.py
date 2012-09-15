from math import *

# G's of Acceleration
Accel = 0.1

# Measured in light years
Distance = 1

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

Distance_Total = Distance * metersInALightYear
dDistance = 0
dTime = 0
V = Vi

while(dDistance <= Distance_Total/2):
    # Calculate Acceleration
    V_Old = V
    V += Accel * timeStep * LorenzFactor(V)
    # If Speed of light reached...
    if( V >= 299792458):
        print "Illegal V Reached!"
        print "Vel Change:",Accel * timeStep * LorenzFactor(V_Old)
        print "Vel Change(Newton):",Accel * timeStep
        V = 299792458
    # Calculate Disance Traveled
    dDistance += V * LorenzFactor(V)
    dTime += timeStep * LorenzFactor(V)

print "Distance Traveled:",dDistance
print "Time Taken(h):",dTime/60./60.
print "Final Velocity(m/s):",V

