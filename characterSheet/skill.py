import re
import csv
import time
import collections
import os

class Skill():

   # Need to rework to allow a different style of input (a csv file line). And to understand defaults
   def __init__( self, inputData=None, points=0, format = 'csv' ):
      """
      Skill class
         inputData:
            Default: None
            Either a csv line, or a json dict
         points:
            Default: 0
            Amount of points to allocate to this skill
         format:
            Default: 'csv'
            Either 'csv' or 'json' to take the given form of input
               'csv': inputData is a csv list
               'json': inputData is a json object with the inputData
               'text': inputData is the name of a skill from the file to load

      """
      
      # Skill, Attribute, Difficulty, Defaults(; sep), page
      
      # Type Error checking
      assert( points >= 0)
      if( format == 'csv' ):
         assert( inputData[1] in ['IQ','HT','DX','Will','Per'] ), "Error on:"+inputData[0]
         self.Name = inputData[0]
         self.AttributeString = inputData[1]
         self.Difficulty = inputData[2]
         self.Defaults = inputData[3]
         self.Page = inputData[4]
         self.Points = points

      elif( format == 'json' ):
         self.Name = inputData.keys()[0]
         self.AttributeString = inputData[self.Name]['Attr']
         self.Difficulty = inputData[self.Name]['Diff']
         self.Defaults = inputData[self.Name]['Defa']
         self.Page = inputData[self.Name]['Page']
         self.Points = inputData[self.Name]['Poin']

      elif( format == 'text' ):
         assert( type( inputData ) in [ str, unicode ] ), "Bad input type for Skill.__init__(), not a str"
         skillFile = os.path.dirname(os.path.abspath(__file__))+"\\..\\data\\gameref\\skills.csv"
         with open( skillFile, 'r' ) as fp:
            skillreader = csv.reader( fp, delimiter=',' )
            # Gobble header
            header = skillreader.next()
            for idx, val in enumerate( skillreader ):
               if( val[0] == inputData ):
                  break
            else:
               # Failed to find it exactly, try regex
               fp.seek(0)
               skillreader = csv.reader( fp, delimiter=',' )
               # Gobble header
               header = skillreader.next()
               for idx, val in enumerate( skillreader ):
                  if( re.search( inputData, val[0], re.IGNORECASE ) ):
                     break
               else:
                  return

            self.Name = val[0]
            self.AttributeString = val[1]
            self.Difficulty = val[2]
            self.Defaults = val[3]
            self.Page = val[4]
            self.Points = points

      else:
         assert(0),"Invalid format"


      self.SkillMod = None
      
      
      self.CalcSkillMod( )


   def __str__( self ):
      return "%s (%+d) [%d]" %(self.Name, self.SkillMod, self.Points)


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
      self.AttributeString = atributeStr
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


   def Print( self, caller=None, mod = 0 ):
      if( caller == None ):
         return self.__str__() + " NO CALLER"
      else:
         tmpBase = "%s-%d"%( self.Name, self.SkillMod + caller.GetAttrValue( self.AttributeString ) + mod )
         return "%-25s (%s%+d) [%d]" %(tmpBase, self.AttributeString, self.SkillMod + mod, self.Points)
         pass

   def Save( self ):
      retVal = collections.OrderedDict()

      retVal[self.Name] = collections.OrderedDict()
      retVal[self.Name]['Attr'] = self.AttributeString 
      retVal[self.Name]['Diff'] = self.Difficulty 
      retVal[self.Name]['Defa'] = self.Defaults
      retVal[self.Name]['Page'] = self.Page 
      retVal[self.Name]['Poin'] = self.Points 

      return retVal

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

def Re2SkillSingle( matchStr ):
   skillFile = os.path.dirname(os.path.abspath(__file__))+"\\..\\data\\gameref\\skills.csv"
   with open( skillFile, 'r' ) as fp:
      skillreader = csv.reader( fp, delimiter=',' )
      # Gobble header
      header = skillreader.next()
      for idx,val in enumerate( skillreader ):
         try:
            if( re.search( matchStr, val[0], re.IGNORECASE ) ):
               return Skill( val )
         except:
            print "Failed on:",matchStr
            print "Val of:",val
            raise
      else:
         return None

def Re2SkilTuple( matchStr="."):

   retVal = list()
   skillFile = os.path.dirname(os.path.abspath(__file__))+"\\..\\data\\gameref\\skills.csv"

   with open( skillFile, 'r' ) as fp:
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