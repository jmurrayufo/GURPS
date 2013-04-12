import json
import re


class Weapon( ):
    # Parse and generator
    def __init__( self, jsonTable ):

        self.TL     = jsonTable['TL']
        self.Name   = jsonTable['Name']
        self.Damage = self.ParseDamage( jsonTable['Damage'] )
        self.Acc    = jsonTable['Acc']
        self.Range  = self.ParseRange( jsonTable['Range'] )
        self.Weight = jsonTable['Weight']
        self.Rof    = jsonTable['RoF']
        self.Shots  = jsonTable['Shots']
        self.ST     = jsonTable['ST']
        self.Bulk   = jsonTable['Bulk']
        self.Recoil = jsonTable['Rcl']
        self.Cost   = jsonTable['Cost']
        self.LC     = jsonTable['LC']
        self.Notes  = jsonTable['Notes']
    
    # Data Process
    def ParseDamage( self, inputStr ):
        matchStr = "^(?:((?:\d+d|HT)(?:[x+-]\d+)?)(?:\((\d+(?:\.\d+)?|inf)\))?)(?: (.+))?"

        tmp = re.search( matchStr, inputStr )
        return tmp.groups()

    def ParseRange( self, inputStr ):
        matchStr = "^(\d+)/?(\d+)?"

        tmp = re.search( matchStr, inputStr )
        return tmp.groups()

    # Output and access functions        
    def PrintDetailed( self ):
        print "Name:"




files = ["laserrifle.json"]

with open( files[0], 'r' ) as fp:
    tmp = json.load(fp)

tmp = Weapon(tmp)

print tmp.Damage
print tmp.Range
