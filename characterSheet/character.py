import collections
import glob
import json
import math
import os
import random
import re
import skill
import types


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
      self.Skills.append( skill.Skill( csvLine, points ) )


   def AddSkillTXT( self, newSkill ):
      if( self.HasSkill( newSkill, regex = True ) ):
         return
      tmp = skill.Skill( newSkill, format='text')
      if( hasattr( tmp, 'Name' ) ):
         self.Skills.append( tmp )
      else:
         print "Attemped to add:",newSkill
         print "Current Skills:",self.Skills
         print "Skill failed to generate!"
         print "Press enter to continue"
         raw_input()



   def AddSkill( self, newSkill ):
      if( self.HasSkill( newSkill.Name ) ):
         return
      self.Skills.append( newSkill )


   def HasSkill( self, skillName, regex=False ):
      """
      Check if the named skill is the in skill list
      """
      assert( type( skillName ) == str or type( skillName ) == unicode ),type( skillName )
      for i in self.Skills:
         if( i.Name == skillName ):
            return True
         if( regex and re.search( skillName, i.Name, re.IGNORECASE ) ):
            return True
      return False


   def GetAttrValue( self, attribute ):
      """
      Return the true value of a given attribute.
         attribute: String of attribute to be returned. Can be..
            ST, DX, IQ, HT, HP, WILL, PER, FP
      """
      def Point( points, div ):
         if( math.copysign( 1, points ) == -1.0 ):
            return int( -math.floor( abs( points ) / div ) )
         return int( math.floor( points / div ) ) 

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
      print "Stat Total: [%3d]" %( self.CalcPointsStats( ) )
      if( len( self.Skills ) ):
         print "\nSkills:"      
         sortedSkills = sorted(self.Skills, key=lambda x: x.Name)
         for i in sortedSkills:
            print " ",i.Print( self )
         print "Skill Total: [%3d]" %( self.CalcPointsSkills( ) )
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
         ( "Save", self.PromptSave ),
         ( "Load", self.PromptLoad ),
         ( "Help", self.PromptHelp ),
         ( "NPC",  self.PromptNPC ),
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
         ( "Find Default",       self.PromptSkillFindDefault ),
         ( "Remove Skill",       self.PromptSkillDelete)
         ) 

      while True:
         print "\n\nSelection option"
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
         skillList = skill.Re2SkilTuple( matchStr )

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
      # Prompt user for regex to skill to find
      def DefaultLister( matchStr ):
         retVal = list()
         skillList = skill.Re2SkilTuple( matchStr ) 
         for i in skillList:
            for x in self.Skills:
               if( i.Name == x.Name ):
                  i.SetPoints( x.Points )
                  break
            retVal.append( i )
         return retVal


      while True:
         print "\n\nDefault Calculator"
         print "Enter a valid regex to find as a default"
         print "Enter ? for help"
         print "Leave blank to close"
         matchStr = raw_input(">")
         if( len ( matchStr ) == 0 ):
            break
         if( matchStr == '?' ):
            print "This screen will attempt to help you find defaults for"
            continue
         try:
            matchRe = re.compile( matchStr, re.IGNORECASE )
         except( re.error ):
            print "ERROR: \'%s\'' is not a valid regex. Try again!"%( matchStr )
            continue

         # Parse through matches, and defaults. Print the results
         matchStrBase = "([^\(\-]+)"
         matchStrNum  = "(\d+)"
         for i in DefaultLister( matchStr ):
            print "\n"+i.Print( self )
            # Print through just the defaults
            for default in i.Defaults.split(';'):
               base = re.search( matchStrBase, default )
               num  = re.search( matchStrNum , default )
               # Make sure we got match objects for both searches
               if( base and num ):
                  base = base.group( 1 )
                  num = num.group( 1 )
                  print "  %s"%( default )
                  # Dont look for base stats, they are clear as it is
                  if( base in  ['ST','DX','IQ','HT','HP','WILL','PER','FP']):
                     continue
                  # Get the skill we are looking for
                  tmp = skill.Re2SkillSingle( base )
                  for x in self.Skills:
                     if( tmp.Name == x.Name ):
                        tmp.SetPoints( x.Points )
                        break
                  # Print the result modified for this character
                  print "   ->%s"%( tmp.Print( self, mod = -eval(num) ) )


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


   def PromptSave( self ):
      print "\n\nEnter file name"
      print "Leave blank to cancel"
      fileName = raw_input(">")

      if( len( fileName ) == 0 ):
         return

      if( not fileName.endswith('.json') ):
         fileName = fileName + '.json'

      if( fileName in glob.glob('*.json') ):
         print "***WARNING***"
         print "File",fileName,"already exists, overwrite? (y/n)"
         if( not raw_input(">") in ['y','Y','Yes','yes','1'] ):
            return

      with open( fileName, 'w' ) as fp:
         mule = collections.OrderedDict()
         mule['Name'] = self.Name
         muleStats = collections.OrderedDict()
         muleStats['STp'] = self.STp
         muleStats['DXp'] = self.DXp
         muleStats['IQp'] = self.IQp
         muleStats['HTp'] = self.HTp
         muleStats['HPp'] = self.HPp
         muleStats['WILLp'] = self.WILLp
         muleStats['PERp'] = self.PERp
         muleStats['FPp'] = self.FPp
         mule['Stats'] = muleStats

         # Process Skills
         muleSkills = list()
         for i in self.Skills:
            muleSkills.append( i.Save( ) )
         mule['Skills'] = muleSkills
         mule['Advantages'] = list( )
         mule['Disadvantages'] = list( )
         mule['Languages'] = list( )
         mule['Cultures'] = list( )
         mule['ReactionMods'] = list( )
         mule['Height'] = self.Height
         mule['Weight'] = self.Weight
         mule['Age'] = self.Age
         mule['PointsTotal'] = self.PointsTotal
         mule['PointsUnspent'] = self.PointsUnspent
         json.dump( mule, fp, indent=3 )


   def PromptLoad( self ):
      files = glob.glob("*.json")
      print "\n\nSelect file to load\n"
      for idx,val in enumerate(files):
         print "[%d] %s"%(idx + 1,val)
      print "\nEnter index to load, or blank to cancel"
      try:
         selection = input(">") - 1
      except ( NameError, SyntaxError ):
         return

      print "\n***WARNING***"
      print "Loading this file will delete all unsaved data!"
      print "Continue? (y/n)"
      if( not raw_input(">") in ['y','Y','Yes','yes','1'] ):
         print "Did not get a yes, exit load!"
         print "Press enter to continue"
         raw_input()
         return


      with open( files[selection], 'r' ) as fp:
         data = json.load( fp )
         self.STp = data['Stats']['STp']
         self.DXp = data['Stats']['DXp']
         self.IQp = data['Stats']['IQp']
         self.HTp = data['Stats']['HTp']
         self.HPp = data['Stats']['HPp']
         self.WILLp = data['Stats']['WILLp']
         self.PERp = data['Stats']['PERp']
         self.FPp = data['Stats']['FPp']

         # Process Skills
         self.Skills = list()
         for i in data['Skills']:
            self.Skills.append( skill.Skill( i, format='json' ) )

         self.Advantages = data['Advantages']
         self.Disadvantages = data['Disadvantages']
         self.Languages = data['Languages']
         self.Cultures = data['Cultures']
         self.ReactionMods = data['ReactionMods']
         self.Height = data['Height']
         self.Weight = data['Weight']
         self.Age = data['Age']
         self.PointsTotal = data['PointsTotal']
         self.PointsUnspent = data['PointsUnspent']


   def PromptHelp( self ):
      print "\n\nHelp Screen"
      print (
            "TODO List:"
            "\n   Rename Character"
            "\n   Dis/Advantages"
            "\n   Languages/Cultures"
            "\n   Weight/Height"
            "\n   Item Management"
            )
      print "\nPress enter to continue..."
      raw_input()


   def PromptNPC( self ):
      print "\n\nNPC Screen"
      print "***WARNING***"
      print "This function will overwrite the current player character, and roll an NPC"
      print "***WARNING***"
      print "Are you sure you want to continue?"
      if( not raw_input(">") in ['y','Y','Yes','yes','1'] ):
         return

      # Blank out character
      self.__init__()

      # Show Avaliable Templates
      templateFiles = os.path.dirname( os.path.abspath( __file__ ) ) + "\\..\\data\\Templates\\*.json"
      templateFiles = glob.glob( templateFiles )
      
      while True:
         print "\n"
         for idx,val in enumerate( templateFiles ):
            print "[%d] %s"%( idx + 1, val.split( "\\" )[-1] )

         try:
            selection = input(">") - 1
         except ( NameError ):
            continue
         except ( SyntaxError ):
            return

         try:
            selection = templateFiles[ selection ]
         except ( IndexError ):
            continue
         break

      with open( selection, 'r' ) as fp:
         data = json.load( fp )

      dataAttr = data['Attributes']
      self.STp = int( random.gauss( dataAttr['STp']['mean'], dataAttr['STp']['std'] ) )
      self.DXp = int( random.gauss( dataAttr['DXp']['mean'], dataAttr['DXp']['std'] ) )
      self.IQp = int( random.gauss( dataAttr['IQp']['mean'], dataAttr['IQp']['std'] ) )
      self.HTp = int( random.gauss( dataAttr['HTp']['mean'], dataAttr['HTp']['std'] ) )
      self.HPp = int( random.gauss( dataAttr['HPp']['mean'], dataAttr['HPp']['std'] ) )
      self.WILLp = int( random.gauss( dataAttr['WILLp']['mean'], dataAttr['WILLp']['std'] ) )
      self.PERp = int( random.gauss( dataAttr['PERp']['mean'], dataAttr['PERp']['std'] ) )
      self.FPp = int( random.gauss( dataAttr['FPp']['mean'], dataAttr['FPp']['std'] ) )

      # Adjust points to legal values
      attrList = ['ST','DX','IQ','HT','HP','WILL','PER','FP']
      for i in attrList:
         while( self.GetAttrValue( i ) <= 0 ):
            setattr( self, i+'p', getattr( self, i+'p' )+1 )

      self.PointsUnspent -= self.STp
      self.PointsUnspent -= self.DXp 
      self.PointsUnspent -= self.IQp 
      self.PointsUnspent -= self.HTp 
      self.PointsUnspent -= self.HPp 
      self.PointsUnspent -= self.WILLp
      self.PointsUnspent -= self.PERp
      self.PointsUnspent -= self.FPp 


      self.CalcUpdatePointsTotals()
      print self.PointsTotal
      print self.PointsUnspent

      #### Handle Skills ####
      """
      This section will attempt to load up skills as dictated from the data sheet
      """

      dataSkill = data['Skills']

      if( len( data['Skills'].keys( ) ) ):

         while True:
            try:
               print "\nEnter the amount of points for skills"
               dPoints = input(">")
            except ( NameError ):
               print "ERROR, Not a valid number!"
               continue
            except ( SyntaxError ):
               dPoints = 0 # Default value of most humans?
            break

         # Build list of weighted skill tuples
         tmpSkillList = list()
         tmpTotal = 0
         for i in data['Skills'].keys():
            tmpSkillList.append( ( i, dataSkill[i] + tmpTotal ) )
            tmpTotal += dataSkill[i]

         # Loop through skills, add them to the character

         for idx,val in enumerate( tmpSkillList ):
            self.AddSkillTXT( val[0] )

         skillPointsTotal = 0
         while skillPointsTotal < dPoints:
            # Pick a random skill
            choice = random.randint( 0, tmpTotal-1 ) # -1 handles max value error
            for idx,val in enumerate( tmpSkillList ):
               if( choice < val[1] ):
                  break
            # Find that skill, add points
            for i in self.Skills:
               if( re.search( val[0], i.Name, re.IGNORECASE ) ):
                  i.ModPoints(1)
                  self.PointsUnspent -= 1
                  skillPointsTotal += 1
                  break

      """
      TODO:
         Advantages
         Disadvantages
         Languages
      """

      # Last update before we are done
      self.CalcUpdatePointsTotals()


   def CalcPointsStats( self ):
      """
      Return the total points currently allocated to stats
      """
      attrList = ['STp','DXp','IQp','HTp','HPp','WILLp','PERp','FPp']
      retVal = 0
      for i in attrList:
         retVal += getattr( self, i )
      return retVal


   def CalcPointsSkills( self ):
      """
      Return the total points currently allocated to skills
      """
      retVal = 0
      for i in self.Skills:
         retVal += i.Points
      return retVal


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