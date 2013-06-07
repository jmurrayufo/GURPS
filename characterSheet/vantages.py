# import csv
import json

class Vantage( ):
   

   def __init__( self ):
      base = BaseVantageDict( )
      self.Name = base.keys()[0]
      subBase = base[ self.Name ]
      self.Type = subBase[ 'Type' ]
      self.BaseCost = subBase[ 'BaseCost' ]
      self.CostIsPerLevel = subBase[ 'CostIsPerLevel' ]
      self.Levels = subBase[ 'Levels' ]
      self.Summery = subBase[ 'Summery' ]
      self.Synopsis = subBase[ 'Synopsis' ]




def VantageValidator( item ):
   """
   Validate vantages have all required items, 
   Return True/False
   """

   if( not type( item ) == dict ):
      return False

   tmp = item[item.keys()[0]]

   if(   not 'Type' in tmp 
      or not 'BaseCost' in tmp
      or not 'CostIsPerLevel' in tmp
      or not 'Levels' in tmp
      or not 'Summery' in tmp
      or not 'Synopsis' in tmp
      ):
      return False

   return True


def BaseVantageDict():
   """
   Return the basic Vantage dict for use

   "Example":{
         "Type":["Men","Phy","Soc","Exo","Sup"],
         "BaseCost":25,
         "CostIsPerLevel":false,
         "Levels":[null],
         "Summery":"This is an example summery.",
         "Synopsis":"This is an example synopsis. It goes into great detail about the vantage."
      }
   """

   retVal = dict()

   retVal['Example'] = dict()
   retVal['Example']['Type'] = ["Men","Phy","Soc","Exo","Sup"]
   retVal['Example']['BaseCost'] = 0
   retVal['Example']['CostIsPerLevel'] = False
   retVal['Example']['Levels'] = [None]
   retVal['Example']['Summery'] = "Base Summery"
   retVal['Example']['Synopsis'] = "Base Synopsis"

   return retVal

def VantageGenerator( self ):
   pass


if __name__ == "__main__":
   # print VantageValidator( BaseVantageDict( ) )
   x = Vantage()