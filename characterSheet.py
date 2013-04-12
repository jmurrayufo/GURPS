import atexit
import json
import operator
import random
import sys
import time

"""
GURPS is a trademark of Steve Jackson Games, and its rules and art are copyrighted 
by Steve Jackson Games. All rights are reserved by Steve Jackson Games. This game aid is 
the original creation of John Murray and is released for free distribution, and not for 
resale, under the permissions granted in the 
<a href="http://www.sjgames.com/general/online_policy.html">Steve Jackson Games Online 
Policy</a>.
"""

class Skill():
    def __init__( self, name, atributeStr, atributeVal,  difficulty=0, points=1 ):
        """
            Default to 0 (easy) and 1 point spent
        """

        # Type Error checking
        assert( type( atributeStr ) == type( str( ) ) )
        assert( type( atributeVal ) == type( int( ) ) )
        assert( type( points ) == type( int( ) ) )
        assert( points > 0)

        self.Name=name
        self.AtributeString = atributeStr
        self.AtributeValue = atributeVal

        if( type( difficulty ) == type( int( ) ) ):
            self.Difficulty = difficulty
        else:
            if(difficulty=="E"):
                self.Difficulty=0
            elif(difficulty=="A"):
                self.Difficulty=1
            elif(difficulty=="H"):
                self.Difficulty=2
            elif(difficulty=="VH"):
                self.Difficulty=3
            else:
                assert(0),"Difficulty was set outside of accepted ranges!"



        self.Points = points
        self.CalcSkillMod( )


    def CalcSkillMod( self ):
        assert( self.Points > 0 )
        # Calculate base value
        if( self.Points < 4 ):
            self.SkillMod = int( self.Points / 2 ) 
        else:
            self.SkillMod = int( self.Points / 4 ) + 1
        # Adjust value based on Difficulty
        if( self.Difficulty == 0 ):
             pass
        elif( self.Difficulty == 1 ):
             self.SkillMod -= 1
        elif( self.Difficulty == 2 ):
             self.SkillMod -= 2
        elif( self.Difficulty == 3 ):
             self.SkillMod -= 3
        else:
            print "INVALID DIFFiCULTY!"
            assert(False)

    def SetAtrib(self, atributeStr, atributeVal):
        self.AtributeString = atributeStr
        self.AtributeValue = atributeVal

    def ModPoints(self, deltaPoints):
        self.Points += deltaPoints
        self.CalcSkillMod()
    
    def SetPoints(self, newPoints):
        self.Points = newPoints
        self.CalcSkillMod()

    def Check(self, mods=0):
        dieRoll = list()
        for i in range(3):
            dieRoll.append(random.randint(1,6))
        return  (self.SkillMod + self.AtributeValue) - sum(dieRoll) + mods

    def Check( self, mods=0, caller=None ):
        pass

    def Print(self):
        print "%s-%d (%+d)" %(self.Name, self.SkillMod + self.AtributeValue, self.SkillMod)

    def GetPrint(self):
        return "%s-%d (%+d)" %(self.Name, self.SkillMod + self.AtributeValue, self.SkillMod)


class CharSheet( ):
    
    def __init__( self, default = 10 ):
        self.Name   = "DEFAULT"
        self.ST     = default
        self.DX     = default
        self.IQ     = default
        self.HT     = default
        self.HP     = self.ST
        self.WILL   = self.IQ
        self.PER    = self.IQ
        self.FP     = self.HT
        self.Skills = dict( )
        self.Advantages = dict( )
        self.Disadvantages = dict( )

        # Unimplemented
        self.Languages = dict( )

        # Unimplemented
        self.Cultures = dict( )

        # Unimplemented
        self.ReactionMods = list( )

        # Unimplemented
        self.Height = 0
        self.Weight = 0
        self.Age    = 0

        # Unimplemented
        self.PointsTotal   = 0
        self.PointsUnspent = 0

    def __str__(self):
        return self.Name

    def __repr__(self):
        return {"name":self.Name}

    def GetAtributeValue( self, attribStr ):
        assert( type( attribStr ) == type( str( ) ) )

        # Assume we got the exact match first
        try:
            return getattr( self, attribStr )
        except AttributeError:
            pass

        # Try to match all caps (these are most of the raw attributes)
        try:
            return getattr( self, attribStr.upper( ) )
        except AttributeError:
            pass
            
        # Try to match proper name (few attributes and methods)
        try:
            return getattr( self, attribStr.capitalize( ) )
        except AttributeError:
            return None

    def Print(self):
        print "Name:",self.Name
        print "     ST: %3d" % (self.ST)
        print "     DX: %3d" % (self.DX)
        print "     IQ: %3d" % (self.IQ)
        print "     HT: %3d" % (self.HT)
        print "     HP: %3d" % (self.HP)
        print "   WILL: %3d" % (self.WILL)
        print "    PER: %3d" % (self.PER)
        print "     FP: %3d" % (self.FP)
        print " Skills:"      
        sortedSkills = sorted(self.Skills.iteritems(), key=operator.itemgetter(0))
        for i in sortedSkills:
            print " ",i[1].GetPrint()

class CharSheetEncoder(json.JSONEncoder):
    # Much work to be done here!
    def default(self,obj):
        assert( type( obj ) == type( CharSheet( ) ) )
        return obj.__dict__

# Register out exit routine so that the function holds for user input at the end. This
#   makes for cleaner debugging. 
def ExitPrompt():
    try:
        raw_input("Hit enter to exit!")
    except EOFError:
        print "\nEOFError, just quit...."
atexit.register(ExitPrompt)

# main() more or less...
player = CharSheet()
print player.GetAtributeValue("name")

fp = open("output.json","w")
json.dump( player, fp, cls=CharSheetEncoder, indent=1)
fp.close()

print "It works!"