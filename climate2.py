from datetime import *
from math import *
from scipy import interpolate
import json
import matplotlib.pyplot as plt
import numpy as np
import random
import time

### CONFIGURATION ###

dateLandFall = datetime(2075,9,9)

dateMissionEnd = datetime(2080,5,26)

offsetDays = timedelta(7)

timeToday = timedelta(hours=12,minutes=0,seconds=1)

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

    hourProgress = date.minute*60 + date.second
    hourProgress /= 60.*60.

    yearProgress = date-date.replace(month=1,day=1,hour=0,minute=0,second=0)
    yearProgress = yearProgress.total_seconds()/31557600.0

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
    print "Weather(date):",date
    print Cosine_Interpolate(a,b,hourProgress)
    print "yearProgress",yearProgress

def GenTemperature(date,confFile):
    assert type(date) == type(datetime(1,1,1)),"Date must be of type Datetime. Is of type %s" %(type(date))
    assert type(confFile) == type(str()),"confFile must be of type str(). Is of type %s" %(type(confFile))

    with open(confFile,"rb") as f:
        data = json.load(f)
    
    x=list()
    y=list()
    for i in range(1,14):
        x.append(i)
        y.append(data["Temperature"]["Map"][str(i)])
    interpFunc = interpolate.interp1d(x, y,'cubic')

    timeOfDayOffset = sin((date.hour+date.minute/60.+date.second/60./60.-6.)*2.*pi/24.)*data["Temperature"]["Variance"]

    dayOffset=list()

    dateToday = date.replace(hour=0,minute=0,second=0,microsecond=0)

    random.seed(YearProgress(dateToday) + DayProgress(dateToday))
    dayOffset.append( random.gauss(0,data["Temperature"]["Variance"]) ) 

    random.seed(YearProgress(dateToday + timedelta(days=1)) + DayProgress(dateToday))
    dayOffset.append( random.gauss(0,data["Temperature"]["Variance"]) )

    dayOffset = Cosine_Interpolate(dayOffset[0],dayOffset[1],DayProgress(date))

    return float(interpFunc(YearProgress(date)*12+1)) + timeOfDayOffset + dayOffset


def Cosine_Interpolate(a, b, x):
    ft = x * 3.1415927
    f = (1 - cos(ft)) * 0.5
    return  a*(1-f) + b*f

def DayProgress(date):
    return (date - date.replace(hour=0,minute=0,second=0)).total_seconds()/(24.*60.*60.)

def YearProgress(date):
    return (date-date.replace(month=1,day=1,hour=0,minute=0,second=0)).total_seconds()/31643136.0

def LunarInfo(date,period):
    offset = (date-dateLandFall).total_seconds()/(24.*60.*60.)
    return (sin(2*pi*offset/period)+1)/2.

### Output ###

# print "Arrived:", dateLandFall.date()
# print "  Today:", (dateLandFall + offsetDays).date()
# print "    Now:", timeToday
# print "Mission Timer:",missionElapsed
# print "Days Remaining:",(dateMissionEnd - dateLandFall).days

# print "Moon 1 Phase",sin(2*pi*missionElapsed/(moon1Period * 24 * 60 * 60))

# print "Moon 1 Phase",sin(2*pi*missionElapsed/(moon2Period * 24 * 60 * 60))
print GenTemperature(datetime(2075,12,31,12,59,59),"data/weatherHome.json")
print "Lunar Intensity: %.02f%%" % (LunarInfo(timeToday,moon1Period)*100)
print "Lunar Intensity: %.02f%%" % (LunarInfo(timeToday,moon2Period)*100)

x=list()
y1=list()
y2=list()
for i in np.linspace(0,365*5,24*365):
    x.append(i)
    y1.append(LunarInfo(timeToday+timedelta(days=i),moon1Period)*100)
    y2.append(LunarInfo(timeToday+timedelta(days=i),moon2Period)*100)

plt.plot(x,y1,x,y2)
plt.show()