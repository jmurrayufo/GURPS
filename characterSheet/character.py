import math
import types
import skill
import os

class Character( ):
    

   def __init__( self, defaults = None ):
      self.Name   = "DEFAULT"
      self.STp     = 0
      self.DXp     = 0
      self.IQp     = 0
      self.HTp     = 0
      self.HPp     = 0
      self.WILLp   = 0
      self.PERp    = 0
      self.FPp     = 0
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
      self.PointsUnspent = 50

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
      self.Skills.append( skill.Skill( csvLine, points ) )


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
      print "\nName:",self.Name
      print "     ST: %2d [%3d]" % ( self.GetAttrValue( 'ST'), self.STp )
      print "     DX: %2d [%3d]" % ( self.GetAttrValue( 'DX' ), self.DXp )
      print "     IQ: %2d [%3d]" % ( self.GetAttrValue( 'IQ' ), self.IQp )
      print "     HT: %2d [%3d]" % ( self.GetAttrValue( 'HT' ), self.HTp )
      print "     HP: %2d [%3d]" % ( self.GetAttrValue( 'HP' ), self.HPp )
      print "   WILL: %2d [%3d]" % ( self.GetAttrValue( 'WILL' ), self.WILLp )
      print "    PER: %2d [%3d]" % ( self.GetAttrValue( 'PER' ), self.PERp )
      print "     FP: %2d [%3d]" % ( self.GetAttrValue( 'FP' ), self.FPp )
      if( len( self.Skills ) ):
         print "\nSkills:"      
         sortedSkills = sorted(self.Skills, key=lambda x: x.Name)
         for i in sortedSkills:
            print " ",i.Print( self )
      print "\nPoint Stats:"
      print "   Total Points: %3d"%( self.PointsTotal )
      print " Unspent Points: %3d"%( self.PointsUnspent )


   def Main( self ):
      """
      Main loop of application if used as such
      """
      mainMenu = (
         ( "Attributes", self.PormptAttributes ),
         ( "Skills", self.PromptSkills ),
         ( "Points", self.PromptPoints ),
         ( "Save", None ),
         ( "Load", None ),
         ( "Quit", None )
         )

      while True:
         self.Print()
         print "\nEnter menu selection"
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
         ( "Will", "WILLp", "Will"           ),
         ( "PER",  "PERp",  "Perception"     ),
         ( "FP",   "FPp",   "Fatigue Points" )
         )

      while True:
         print "\n\n\nAttributes:"
         for idx,val in enumerate( attrMenu ):
            print "[%d] %s"%( idx + 1, val[2] )

         try:
            # Map selection back to true index
            print "\nEnter attribute to modify"
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
         try:
            dPoints = input(">")
         except ( SyntaxError, NameError ):
            continue
         setattr( self, selection[1], getattr( self, selection[1] ) + dPoints )
         self.PointsUnspent -= dPoints
         break


   def PromptSkills( self ):
      skillMenu = (
         ( "Add Skill From HDD", self.PromptSkillAddHDD ),
         ( "Modify Skill Points",self.PromptSkillModifyPoints ),
         ( "Find Default",       None ),
         ( "Remove Skill",       self.PromptSkillDelete)
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
            selection = skillMenu[selection][1]
         except IndexError:
            continue

         if( selection != None ):
            selection()
            continue
         break
   
   def PromptSkillAddHDD( self ):
      matchStr = ""
      skillList = list()
      while True:
         # Get User filter
         print "\n\n"
         print "Current Skills"
         if( len( self.Skills ) ):
            for i in self.Skills:
               print " "+i.Print( self )
         else: 
            print " None"
         print "\nEnter a valid regex filter for the skill to add"
         print "A filter of \".\" will match everything"
         matchStr = raw_input(">")
         if( len( matchStr ) == 0 ):
            break

         # Get List from Selection
         skillFile = os.path.dirname(os.path.abspath(__file__))+"\\..\\data\\gameref\\skills.csv"
         skillList = skill.Re2SkilTuple( skillFile, matchStr )

         if( len( skillList ) == 0 ):
            continue

         # Filter vs Current Skills
         for cur in self.Skills:
            for idx,val in enumerate( skillList ):
               if( val.Name == cur.Name ):
                  del skillList[idx]
                  break

         # Display for selection
         for idx,val in enumerate( skillList ):
            print "[%d] %s"%( idx + 1, val )

         print "\nSelect new skill"
         try:
            # Map selection back to true index
            selection = input(">") - 1
         except ( NameError, SyntaxError ):
            continue

         try:
            selection = skillList[selection]
         except IndexError:
            continue


         # Add what the user selects or exit
         self.Skills.append( selection )


   def PromptSkillModifyPoints( self ):
      while True:
         # Print out list of skills
         print "\n\nCurrent Skills"
         for idx,val in enumerate( self.Skills ):
            print "[%d] %s"%( idx + 1, val.Print( self ) )

         # Select Skill to Modify
         print "\nSelect skill to modify points spent"
         try:
            # Map selection back to true index
            selection = input(">") - 1
         except ( NameError ):
            continue
         except ( SyntaxError ):
            break

         try:
            print "Selection:",self.Skills[selection].Print(self)
         except IndexError:
            continue

         print "\nEnter the delta of points"
         try:
            dPoints = input(">")
         except ( NameError, SyntaxError ):
            continue

         if( type( dPoints ) != int ):
            continue

         self.PointsUnspent -= dPoints
         self.Skills[selection].ModPoints( dPoints )


   def PromptSkillFindDefault( self ):
      print "Not implemented"


   def PromptSkillDelete( self ):

      if( len( self.Skills ) == 0 ):
         print "No skills to delete!"
         return
      
      while True:
         print "\n"

         # Print out list
         for idx,val in enumerate( self.Skills ):
            print "[%d] %s"%( idx + 1, val )

         # Get user input         
         print "\nEnter desired skill to delete"
         print "Leave blank to exit"
         try:
            # Map selection back to true index
            selection = input(">") - 1
         except ( NameError ):
            continue
         except ( SyntaxError ):
            break

         # Get Selection
         # Refund points
         try:
            self.PointsUnspent += self.Skills[selection].Points
         except IndexError :
            continue

         # Delete
         del self.Skills[selection]


   def PromptPoints( self ):
      while True:
         print "\n\nCurrent Unspent Points:",self.PointsUnspent
         print "Enter delta for unspent points"
         try:
            dPoints = input(">")
         except ( NameError ):
            continue
         except ( SyntaxError ):
            break
         self.PointsUnspent += dPoints



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

      for i in self.Skills:
         self.PointsTotal += i.Points