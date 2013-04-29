import re
import csv
import time

class Skill():

   # Need to rework to allow a different style of input (a csv file line). And to understand defaults
   def __init__( self, csvLine=None, points=0):
      """
      Default to 0 (easy) and 1 point spent
      """
      
      # Skill, Attribute, Difficulty, Defaults(; sep), page
      
      # Type Error checking
      assert( points >= 0)
      assert( csvLine[1] in ['IQ','HT','DX','Will','Per'] ), "Error on:"+csvLine[0]
      
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
      return "%s" %(self.Name)



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
         print self.Difficulty
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
         return "%s-%d (%s%+d) [%d]" %(self.Name, self.SkillMod + caller.GetAttrValue( self.AtributeString ), self.AtributeString, self.SkillMod, self.Points)
         pass

def Validator( csvLine=None ):

   if( csvLine == None ):
      # print "FAILIURE: No Line"
      return False

   if( len(csvLine) and len(csvLine[0]) and csvLine[0][0] == '#' ):
      # print "FAILIURE: Comment: ",csvLine
      return False

   if( len( csvLine ) != 5 ):
      # print "FAILIURE: Not Lne(5) ",csvLine
      return False

   if( not ( csvLine[1] in ['IQ','HT','DX','Will','Per'] ) ):
      # print "FAILIURE: Stat: ",csvLine
      return False

   if( not ( csvLine[2] in ['E','A','H','VH'] ) ):
      # print "FAILIURE: Diff: ",csvLine
      return False

   return True

def Re2SkilTuple( csvFile=None, matchStr="."):

   retVal = list()

   with open( csvFile, 'r' ) as fp:
      skillreader = csv.reader( fp, delimiter=',' )
      # Gobble header
      header = skillreader.next()
      for idx, val in enumerate( skillreader ):
         if( Validator( val  ) ):
            val = Skill( val )
            try:  
               if( re.search( matchStr, val.Name, re.IGNORECASE ) ):
                  retVal.append( val )
            except re.error:
               print "\nREGEX ERROR! \"%s\" is not a valid regex!"%( matchStr )
               print "Press enter to continue..."
               raw_input()
               return []

   return retVal