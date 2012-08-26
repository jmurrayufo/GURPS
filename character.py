import random


class CharSheet():
    
    def __init__(self):
        self.name="DEFAULT"
        self.ST=10
        self.DX=10
        self.IQ=10
        self.HT=10
        self.HP=10
        self.WILL=10
        self.PER=10
        self.FP=10
        self.Skills=dict()

        self.Height=0
        self.Weight=0
        self.Points=0
    
    def roll(self,points):
        self.Height = random.gauss(1.778,0.15)

        while(self.Points < points):
            # Spend points on stuff!
            selection = random.randint(1,8)

            if(selection == 1):
                self.ST+=1
                self.HP+=1
                self.Points+=10

            elif(selection == 2):
                self.DX+=1
                self.Points+=20

            elif(selection == 3):
                self.IQ+=1
                self.WILL+=1
                self.PER+=1
                self.Points+=20

            elif(selection == 4):
                self.HT+=1
                self.FP+=1
                self.Points+=10

            elif(selection == 5):
                self.HP+=1
                self.Points+=2

            elif(selection == 6):
                self.WILL+=1
                self.Points+=5

            elif(selection == 7):
                self.PER+=1
                self.Points+=5

            elif(selection == 8):
                self.FP+=1
                self.Points+=3

    def __str__(self):
        return self.name

    def printStats(self):
        print "Name:",self.name
        print " ST:",self.ST
        print " DX:",self.DX
        print " IQ:",self.IQ
        print " HT:",self.HT
        print " HP:",self.HP
        print " WILL:",self.WILL
        print " PER:",self.PER
        print " FP:",self.FP
        print " Points:",self.Points

            
x=CharSheet()

print x
x.printStats()
x.roll(200)
x.printStats()