import atexit
import csv
import json
import operator
import random
import math
import types

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
         return "%s-%d (%s%+d) [%d]" %(self.Name, self.SkillMod + caller.GetAttrValue( self.AtributeString ), self.AtributeString, self.SkillMod, self.Points)
         pass


class CharSheet( ):
    

   def __init__( self ):
      self.Name   = "DEFAULT"
      self.STp     = 10
      self.DXp     = -20
      self.IQp     = 20
      self.HTp     = 0
      self.HPp     = 0
      self.WILLp   = 0
      self.PERp    = 0
      self.FPp     = 20
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

      self.CalcUpdatePointsTotals( )

      # Menus


   def __str__(self):
      return self.Name


   def __repr__(self):
      return {"name":self.Name}


   def AddSkillCSV( self, csvLine, points=0 ):
      """
      Attempt to add a skill from the CSV format
      """
      if( self.HasSkill( csvLine[0] ) ):
         return
      self.Skills.append( Skill( csvLine, points ) )


   def AddSkill( self, newSkill ):
      if( self.HasSkill( newSkill.Name ) ):
         return
      self.Skills.append( newSkill )


   def HasSkill( self, skillName ):
      """
      Check if the named skill is the in skill list
      """
      assert( type( skillName ) == str )
      for i in self.Skills:
         if( i.Name == skillName ):
            return True
      return False


   def GetAttrValue( self, attribute ):
      def Point( points, div ):
         if( math.copysign( 1, points ) == -1.0 ):
            return int( -math.floor( abs( points ) / div ) )
         return int( math.floor( points / div ) )    
      """
      Return the true value of a given attribute.
         attribute: String of attribute to be returned. Can be..
            ST, DX, IQ, HT, HP, WILL, PER, FP
      """
      # Modify input to uppercase
      attribute = attribute.upper()
      # Determine which attribute needs to be calculated,and return
      if( attribute == "ST" ):
         return Point( self.STp, 10 ) + 10
      if( attribute == "DX" ):
         return Point( self.DXp, 20 ) + 10
      if( attribute == "IQ" ):
         return Point( self.IQp, 20 ) + 10
      if( attribute == "HT" ):
         return Point( self.HTp, 10 ) + 10
      if( attribute == "HP" ):
         return Point( self.HPp,  2 ) + self.GetAttrValue( 'ST' )
      if( attribute == "WILL" ):
         return Point( self.WILLp, 5 ) + self.GetAttrValue( 'IQ' )
      if( attribute == "PER" ):
         return Point( self.PERp, 5 ) + self.GetAttrValue( 'IQ' )
      if( attribute == "FP" ):
         return Point( self.FPp, 3 ) + self.GetAttrValue( 'HT' )


   def Print(self):
      print "Name:",self.Name
      print "     ST: %2d [%3d]" % ( self.GetAttrValue( 'ST'), self.STp )
      print "     DX: %2d [%3d]" % ( self.GetAttrValue( 'DX' ), self.DXp )
      print "     IQ: %2d [%3d]" % ( self.GetAttrValue( 'IQ' ), self.IQp )
      print "     HT: %2d [%3d]" % ( self.GetAttrValue( 'HT' ), self.HTp )
      print "     HP: %2d [%3d]" % ( self.GetAttrValue( 'HP' ), self.HPp )
      print "   WILL: %2d [%3d]" % ( self.GetAttrValue( 'WILL' ), self.WILLp )
      print "    PER: %2d [%3d]" % ( self.GetAttrValue( 'PER' ), self.PERp )
      print "     FP: %2d [%3d]" % ( self.GetAttrValue( 'FP' ), self.FPp )
      if( len( self.Skills ) ):
         print " Skills:"      
         sortedSkills = sorted(self.Skills, key=lambda x: x.Name)
         for i in sortedSkills:
            print " ",i.Print( self )
      print "   Total Points: %3d"%( self.PointsTotal )
      print " Unspent Points: %3d"%( self.PointsUnspent )


   def Main( self ):
      """
      Main loop of application if used as such
      """
      mainMenu = (
         ( "Attributes", self.PormptAttributes ),
         ( "Skills", self.PromptSkills ),
         ( "Save", None ),
         (" Load", None ),
         ( "Quit", None )
         )

      while True:
         self.Print()
         for idx,val in enumerate( mainMenu ):
            print "[%d] %s"%( idx + 1, val[0] )
            # print val[0]

         try:
            selection = input(">")
         except ( NameError, SyntaxError ):
            continue

         try:
            # Map selection back to true index
            selection = mainMenu[selection - 1][1]
         except IndexError:
            continue

         if( type( selection ) == types.FunctionType 
            or type( selection ) == types.InstanceType 
            or type( selection ) == types.MethodType
            ):
            selection()
            continue
         if( selection == None ):
            break

   def PormptAttributes( self ):
      attrMenu = (
         ( "ST",   "STp",   "Strength"       ),
         ( "DX",   "DXp",   "Dexterity"      ),
         ( "IQ",   "IQp",   "Intelligence"   ),
         ( "HT",   "HTp",   "Health"         ),
         ( "HP",   "HPp",   "Hit Points"     ),
         ( "Will", "Willp", "Will"           ),
         ( "PER",  "PERp",  "Perception"     ),
         ( "FP",   "FPp",   "Fatigue Points" )
         )

      while True:
         for idx,val in enumerate( attrMenu ):
            print "[%d] %s"%( idx + 1, val[2] )

         try:
            # Map selection back to true index
            selection = input(">") - 1
         except (NameError):
            continue
         except (SyntaxError):
            break

         try:
            selection = attrMenu[selection]
         except IndexError:
            continue

         # We have a valid entry, print out the current value and then modify the points
         print "Selected %s %d [%d]"%(
            selection[0], 
            self.GetAttrValue( selection[0] ),
            getattr( self, selection[1])
             )

         print "Enter the change in points..."
         dPoints = input(">")
         setattr( self, selection[1], getattr( self, selection[1] ) + dPoints )
         self.PointsUnspent -= dPoints
         break


   def PromptSkills( self ):
      skillMenu = (
         ( "Add Skill From HDD", None ),
         ( "Add Skill Manually", None ),
         ( "Find Default",       None )
         ( "Remove Skill",       None )
         ) 

      while True:
         for idx,val in enumerate( skillMenu ):
            print "[%d] %s"%( idx + 1, val[0] )

         try:
            # Map selection back to true index
            selection = input(">") - 1
         except (NameError):
            continue
         except (SyntaxError):
            break

         try:
            selection = skillMenu[selection]
         except IndexError:
            continue
         break


   def CalcUpdatePointsTotals( self ):
      """
      Update the total points spent across all aspects of the character sheet. 
      """
      self.PointsTotal = 0
      self.PointsTotal += self.STp
      self.PointsTotal += self.DXp
      self.PointsTotal += self.IQp
      self.PointsTotal += self.HTp
      self.PointsTotal += self.HPp
      self.PointsTotal += self.WILLp
      self.PointsTotal += self.PERp
      self.PointsTotal += self.FPp



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


if __name__ == '__main__':
   john = CharSheet()
   john.Name = 'John'

   # with open("data/gameref/skills.csv",'r') as fp:
   #     skillreader = csv.reader( fp, delimiter=',')
   #     # Gobble header
   #     header = skillreader.next()
   #     for idx,val in enumerate( skillreader ):
   #         if( len( val ) == 5):
   #             john.AddSkill( val )
   #         else:
   #             pass

   # print john


   john.Main()
