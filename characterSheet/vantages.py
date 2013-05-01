import csv

class Vantage( ):
   

   def __init__( self, dataFile = None, format = 'csv' ):
      self.Name = dataFile[0]


def VantageValidator( item ):
   """
   Validate vantages have all required items, 
   Return True/False
   """

   if( not type( item ) == dict ):
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

print VantageValidator( BaseVantageDict( ) )