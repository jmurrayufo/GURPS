from math import *
import time
import datetime

######################
### BASE FUNCTIONS ###
######################

def lorenz_factor( vel ):
        return sqrt(1-(vel**2) / (299792458.0**2))

def g2ms( gs ):
    return gs * 9.80665

def m2ly( m ):
    return m / 9460730472580800.0 # 9,460,730,472,580,800 (http://en.wikipedia.org/wiki/Lightyear)

def ly2m( ly ):
    return ly * 9460730472580800.0 # 9,460,730,472,580,800 (http://en.wikipedia.org/wiki/Lightyear)

def sol2ms( sol ):
    return sol * 299792458.0

#########################
### COMPLEX FUNCTIONS ###
#########################

def calcSpeedUpTime( accel, v_coast, v_i, t_step ):
    dDistance = 0
    dTime = 0
    V = v_i
    update = time.time()

    while(V <= v_coast):
        # Calculate Acceleration
        V_Old = V
        V += accel * t_step * lorenz_factor(V)
        while(V >= 299792458.0):
            print "Reduce Time Steps!"
            print "New Time Step:",t_step
            print "    V:",V
            print "V_Old:",V_Old
            time.sleep(0.1)
            t_step/=2.0
            V=V_Old
            V += Accel * t_step * lorenz_factor(V)

        # Calculate Disance Traveled
        dDistance += V * t_step * lorenz_factor(V)
        dTime += t_step * lorenz_factor(V)

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
    print "Final Lorenz Factor:",lorenz_factor(V)
    print "%% C: %0.2f%%" % (V/299792458.0*100)

def calcTravelTime( accel = 9.8, distance = 1, v_max= 1.0, v_i=0, v_f=0 ):
    """
    Calculate the amount of time it takes to travel a given distance, at a max accel and speed. 
    All Units are expected in m, s, m/s and m/(s^2)
    """
    # time
    dT = 0
    # Subjective time
    dTs = 0 

    # Calculate the required slow down time from max speed



if __name__ == '__main__':
    print lorenz_factor( sol2ms( 0.999999999 ) )
    # # Initial Speed
    # Vi = 0

    # # Time Step (seconds)
    # timeStep = 1*60*60

    # calcSpeedUpTime( 
    #     g2ms( 0.01 ),
    #     sol2ms( .99999999999 ),
    #     Vi,
    #     timeStep  )