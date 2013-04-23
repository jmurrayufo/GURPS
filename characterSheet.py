import atexit
import csv
import json
import operator
import random

"""
GURPS is a trademark of Steve Jackson Games, and its rules and art are copyrighted 
by Steve Jackson Games. All rights are reserved by Steve Jackson Games. This game aid is 
the original creation of John Murray and is released for free distribution, and not for 
resale, under the permissions granted in the 
<a href="http://www.sjgames.com/general/online_policy.html">Steve Jackson Games Online 
Policy</a>.
"""

class Skill():

    # Need to rework to allow a different style of input (a csv file line). And to understand defaults
    def __init__( self, csvLine=None, points=0):
        """
            Default to 0 (easy) and 1 point spent
        """

        # Skill, Attribute, Difficulty, Defaults(; sep), page

        # Type Error checking
        assert( points >= 0)

        self.Name = csvLine[0]
        self.AtributeString = csvLine[1]

        # Temporay string to parse out value
        self.Difficulty = csvLine[2]

        self.Points = points
        self.SkillMod = None
        self.CalcSkillMod( )


    def __str__( self ):
        return "%s-%d (%+d) [%d]" %(self.Name, self.SkillMod, self.SkillMod, self.Points)

    def __repr__( self ):
        return self.__str__()


    def CalcSkillMod( self ):
        assert( self.Points >= 0 )

        # Calculate base value
        if( self.Points < 4 ):
            self.SkillMod = int( self.Points / 2 ) 
        else:
            self.SkillMod = int( self.Points / 4 ) + 1

        # Adjust value based on Difficulty
        if( self.Difficulty == 'E' ):
             pass
        elif( self.Difficulty == 'A' ):
             self.SkillMod -= 1
        elif( self.Difficulty == 'H' ):
             self.SkillMod -= 2
        elif( self.Difficulty == 'VH' ):
             self.SkillMod -= 3
        else:
            print "INVALID DIFFiCULTY!"
            raise ValueError


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


    def Print( self, caller):
        if( caller == None ):
           return self.__str__() + " NO CALLER"
        else:
            return "%s-%d (%s%+d) [%d]" %(self.Name, self.SkillMod + caller.GetAtributeValue( self.AtributeString ), self.AtributeString, self.SkillMod, self.Points)
            pass


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
        self.Skills = list( )
        self.Advantages = list( )
        self.Disadvantages = list( )

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


    def AddSkill( self, csvLine, points=0 ):
        """
        Attempt to add a skill from the CSV format
        """
        if( self.HasSkill( csvLine[0] ) ):
            return
        self.Skills.append( Skill( csvLine, points ) )


    def HasSkill( self, skillName ):
        """
        Check if the named skill is the in skill list
        """
        for i in self.Skills:
            if( i.Name == skillName ):
                return True
        return False


    def GetAtributeValue( self, attribStr ):
        assert( type( attribStr ) == type( str( ) ) )

        # Assume we got the exact match first
        if( hasattr( self, attribStr ) ):
            return getattr( self, attribStr )

        # Try to match all caps (these are most of the raw attributes)
        if( hasattr( self, attribStr.upper( ) ) ):
            return getattr( self, attribStr.upper( ) )
            
        # Try to match proper name (few attributes and methods)
        if( hasattr( self, attribStr.capitalize( ) ) ):
            return getattr( self, attribStr.capitalize( ) )

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
        sortedSkills = sorted(self.Skills, key=lambda x: x.Name)
        for i in sortedSkills:
            print " ",i.Print( self )




class CharSheetEncoder(json.JSONEncoder):
    # Much work to be done here!
    def default(self,obj):
        assert( type( obj ) == type( CharSheet( ) ) )
        return obj.__dict__
    """
# main() more or less...
player = CharSheet()
print player.GetAtributeValue("name")

fp = open("output.json","w")
json.dump( player, fp, cls=CharSheetEncoder, indent=1)
fp.close()
    """




# Register out exit routine so that the function holds for user input at the end. This
#   makes for cleaner debugging. 
def ExitPrompt():
    try:
        raw_input("Hit enter to exit!")
    except EOFError:
        print "\nEOFError, just quit...."
atexit.register(ExitPrompt)

if __name__ == '__main__':

    john = CharSheet()
    john.Name = 'John'


    with open("data/gameref/skills.csv",'r') as fp:
        skillreader = csv.reader( fp, delimiter=',')
        # Gobble header
        header = skillreader.next()
        for idx,val in enumerate( skillreader ):
            if( len( val ) == 5):
                john.AddSkill( val )
            else:
                pass

    print john
    john.Print()
