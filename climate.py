from datetime import *
from math import *
import random

### CONFIGURATION ###

dateLandFall = datetime(2075,9,9)

dateMissionEnd = datetime(2080,5,26)

offsetDays = timedelta(1)

timeToday = timedelta(hours=20,minutes=1,seconds=0)

# Days for one cycle
moon1Period = 17.974322903911

# Days for one cycle
moon2Period = 65.642457479688


### POST CONFIG MATH ###

timeToday = (dateLandFall + offsetDays).replace(hour=0,minute=0,second=0) + timeToday

missionElapsed = (timeToday - dateLandFall).total_seconds()

def Weather(date,wtype=0):
    """
    Enter a datetime and the type of weather as an int. 
    Wtype:
        0: General Weather
        1: Wind Speed
        2: Temperature
        TODO: All of this junk....
    """
    assert type(date) == type(datetime(1,1,1)),"Date must be of type Datetime. Is of type %s" %(type(date))
    assert type(wtype) == type(int()),"Wtype MUST be of type int, is of type %s."%(type(wtype))

    hourProgress = date.time().minute*60 + date.time().second
    hourProgress /= 60.*60.

    if(wtype==0):
        jumpValue=0
    elif(wtype==1):
        jumpValue = 617147


    random.seed(date.replace(minute=0,second=0))
    random.jumpahead(jumpValue)
    a=random.random()
    random.seed(date.replace(minute=0,second=0) + timedelta(hours=1))
    random.jumpahead(jumpValue)
    b=random.random()
    print "Weather(date):",Cosine_Interpolate(a,b,hourProgress)

def Cosine_Interpolate(a, b, x):
    ft = x * 3.1415927
    f = (1 - cos(ft)) * 0.5
    return  a*(1-f) + b*f


### Output ###

print "Arrived:", dateLandFall.date()
print "  Today:", (dateLandFall + offsetDays).date()
print "    Now:", timeToday
print "Mission Timer:",missionElapsed
print "Days Remaining:",(dateMissionEnd - dateLandFall).days

# print "Moon 1 Phase",sin(2*pi*missionElapsed/(moon1Period * 24 * 60 * 60))

# print "Moon 1 Phase",sin(2*pi*missionElapsed/(moon2Period * 24 * 60 * 60))

print Weather(timeToday)
print Weather(timeToday,1)
