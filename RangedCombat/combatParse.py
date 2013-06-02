import glob
import json
import logging
import os
import re
import time
import types
import atexit

version = '0.0.3'

"""
GURPS is a trademark of Steve Jackson Games, and its rules and art are copyrighted 
by Steve Jackson Games. All rights are reserved by Steve Jackson Games. This game aid is 
the original creation of John Murray and is released for free distribution, and not for 
resale, under the permissions granted in the 
<a href="http://www.sjgames.com/general/online_policy.html">Steve Jackson Games Online 
Policy</a>.
"""

class Weapon( ):

   # Parse and generator
   def __init__( self, jsonFile ):
      logger.debug('Ceated new Weapon instance')
      with open( jsonFile, 'r' ) as fp:
         jsonTable = json.load(fp)

      self.TL     = jsonTable['TL']
      self.Name   = jsonTable['Name']
      self.Damage = self.ParseDamage( jsonTable['Damage'] )
      self.Acc    = jsonTable['Acc']
      self.Range  = self.ParseRange( jsonTable['Range'] )
      self.Weight = self.ParseWeight( jsonTable['Weight'] )
      self.RoF    = jsonTable['RoF']
      self.Shots  = self.ParseShots( jsonTable['Shots'] )
      self.ST     = jsonTable['ST']
      self.Bulk   = jsonTable['Bulk']
      self.Recoil = jsonTable['Rcl']
      self.Cost   = jsonTable['Cost']
      self.LC     = jsonTable['LC']
      self.Notes  = jsonTable['Notes']

   def __str__( self ):
      return self.Name

   # Data Process
   def GenericToCleanList( self, inputTuple ):
      """
      Convert any generic object, tuple or list into a clean list.
      """
      retVal = list()
      for i in inputTuple:
         try:
            retVal.append(int(i))
            continue
         except (TypeError, ValueError):
            pass
         try:
            retVal.append(float(i))
            continue
         except (TypeError, ValueError):
            pass
         try:
            if( i != None ):
               retVal.append(str(i))
            else:
               retVal.append(i)
         except:
            logger.critical('Unable to append items to list')
            raise
      return retVal



   def ParseDamage( self, inputStr ):
      return ( inputStr['Base'], inputStr['Divisor'], inputStr['Type'] )

   def ParseRange( self, inputStr ):
      return ( inputStr['Min'], inputStr['Max'] )

   def ParseWeight( self, inputStr ):
      return ( inputStr['Base'], inputStr['Misc'] ) 

   def ParseShots( self, inputStr ):
      return ( inputStr['Base'], inputStr['Reload'] )

   # Output and access functions
   def PrintDetailed( self ):
      print "  Name:",       self.Name
      print "    TL:",       self.TL
      print "Damage: %s (%.1f) %s"%( self.Damage[0], self.Damage[1], self.Damage[2] )
      print "   Acc:",       self.Acc
      print "Range : %d/%d"%( self.Range[0], self.Range[1] )
      print "Weight: %.1f/%s"%( self.Weight[0], self.Weight[1] )
      print "   RoF:",       self.RoF
      print " Shots: %d(%d)"%( self.Shots[0], self.Shots[1] )
      print "    ST:",       self.ST
      print "  Bulk:",       self.Bulk
      print "Recoil:",       self.Recoil
      print "  Cost:",       self.Cost
      print "    LC:",       self.LC
      print " Notes:",       self.Notes

class RangedAttackCalculator():

   def __init__( self ):
      logger.debug('Begin')

      # (Name,Type,Default,PrettyName,HelpString)
      self.CalcAttributes = [
         ("DX",            int,     10,      "DX",                None),
         ("Skill",         int,     1,       "Skill",             "Skill = Base skill, NOT effective"),
         ("SM",            float,   2.0,     "SM",                "SM = Size of target in yards"),
         ("Range",         float,   1.0,     "Range",             "Range = Distance to target, in yards"),
         ("Speed",         float,   0.0,     "Speed",             "Speed = Relative speed of target in yards/s"),
         ("DarkFog",       int,     0,       "Darkness and Fog", "Darkness and Fog = Negative modifier due to light and fog condition \nDarkness and Fog must be between -9 and 0"),
         ("CanSee",        bool,    True,    "Can See",           "Can See = Can you see the target?"),
         ("KnowLoc",       bool,    True,    "Know Location",     "Know Location = Do you know EXACTLY where the target is?"),
         ("Concealment",   bool,    False,   "Concealment",       "Concealment = Does the target have partial concealment?"),
         ("RoundsAiming",  int,     0,       "Rounds Aiming",     "Rounds Aiming = How many previous rounds have you spend aiming?"),
         ("ShotsFired",    int,     1,       "Shots Fired",       "Shots Fired = How many shots do you plan to fire?"),
         ("Bracing",       bool,    False,   "Bracing",           "Bracing = Are you currently bracing your weapon?"),
         ("Shock",         int,     0,       "Shock",             "Shock = Modifier if you took damage sense your last turn."),
         ("AllOutAttack",  bool,    False,   "All-Out Attack",    "All-Out Attack = Are you attacking without regard to defense?" ),
         ("MoveAndAttack", int,     0,       "Move And Attack",   "Move and Attack = Are you moving and attacking in the same round?"),
         ("ChangeFacing",  bool,    False,   "Change Facing",     "Have you changes the direction you are facing by more then one hex diretion?"),
         ("PopUpAttack",   bool,    False,   "Pop-Up Attack",     "Pop-Up Attack = Are you doing a Pop-Up Attack?"),
         ("MiscBonus",     int,     0,       "Misc Bonus",        "Misc Bonus = Has you DM given you any other +/- modifiers?"),
         ("HitLoc",        self.PromptChangeHitLoc,  "Torso",     "Hit Location",   None),
         ("Weapon",        self.PromptChangeWeapon,  None,        "Weapon",         "Weapon Help String default"),
         ("Advantages",    dict,    {},      "Advantages",        "List of Advantages that your character has that effect ranged comba")
      ]  

      for i in self.CalcAttributes:
         setattr( self, i[0], i[2] )

      # Object Fields
      self.Mod = None
      self.Weapon = None

      self.UpdateWeaponsList()

      logger.debug('Completed')

   # ********************************
   # ******* User Interaction *******
   # ********************************
   def Main( self ):
      menu = [
         ("Quit",exit),
         ("Change Attribute",self.PromptSelectAttribute ),
         ("Enter ALL Attributes",self.PromptEnterAttributes ),
         ("Walk Through Math",self.HelpUserWithMath),
         ("Check me for errors",self.PrintErrorGuide),
         ("Change Weapon",self.PromptChangeWeapon ),
         ("Print Gun Details",self.PrintGunDetails),
         ("Save",self.PromptSaveSettings),
         ("Load",self.PromptLoadSettings)
         ]
      while True:
         logger.debug('Printed main menu')
         # Print out the current stats and such
         self.CalculateBaseScore()
         self.PrintOptions()

         # Get User Input
         print "\n<<<MAIN MENU>>>"
         for idx,val in enumerate( menu ):
            print "[%2d] %s"%(idx,val[0])

         try:
            selection = input(">")
         except (SyntaxError, NameError):
            continue

         try:
            selection = menu[selection][1]
         except IndexError:
            logger.warning('User entered value that exceeds menu size')
            continue

         if(selection == exit):
            logger.info('******* Leaving Main loop on user selected exit *******')
            break

         if( type( selection ) == types.FunctionType or types.InstanceType):
            selection()


   def PromptSaveSettings( self ):

      logger.debug('Begin attempt to save file.')
      # Get user input for where to save the file
      print "\nEnter file name to save as."
      fileName = raw_input(">")
      fileName = "Save/"+fileName + ".json"

      # Do we have a save directory?
      if( not os.path.exists('Save') ):
         logger.warning('Save directory did not exist, attempt to create it')
         os.mkdir("Save")

      # Is it just a file?
      if( not os.path.isdir('Save') ):
         logger.critical('Save was a file, and cannot be a directory!')
         print "Error! Cannot save as \"./Save\" isn't a directory!"
         input_pause( "Press enter to continue..." )
         return

      # Prepare object for saving. 
      saveData = dict()

      # (Name,Type,Default,PrettyName,HelpString)
      # self.CalcAttributes = [
      for i in self.CalcAttributes:
         if( i[0] == 'Weapon' ):
            print "skip!"
            continue
         saveData[ i[0] ] = getattr( self, i[0], i[2] )

      print saveData

      with open( fileName, 'w' ) as fp:
         logger.debug('File Saving...')
         saveJson = json.dump( saveData, fp )
         print saveJson
      logger.debug('File Saved')

   def PromptLoadSettings( self ):
      def SafeLoad( savedData, attribute, default=None ):
         try:
            return saveData[attribute]
         except KeyError:
            logger.error('Tried to load attribute %s from file, no such attribute found'%(attribute))
            return default

      logger.debug('Begin attempt to load file.')
      savedFileList = glob.glob("./Save/*.json")
      if( len( savedFileList ) == 0 ):
         logger.error('No files found in the save directory from the glob.glob')
         print "No files in the Save directory!"
         input_pause( "Press enter to continue..." )
         return

      while True:
         print "\n\n\n   ===Select a File==="
         for idx,val in enumerate( savedFileList ):
            print "[%d] %s"%( idx, val.__str__( ) )

         try:
            tmp = input(">")
         # Non-Int entry
         except NameError:
            print "NameError: File Selection must be an int"
            continue
         # Blank entry
         except SyntaxError:
            logger.debug('File was not loaded')
            return
         try:
            savedFile = savedFileList[tmp]
         except IndexError:
            print "IndexError: Select a valid entry!"
            continue
         break

      with open( savedFile, 'r' ) as fp:
         saveData = json.load(fp)
      for i in self.CalcAttributes:
         setattr( self, i[0], SafeLoad( saveData, i[0], i[2] ) )
      
      logger.debug('File loading complete')
      print "\nLoaded settings from file",savedFile
      print "WARNING: Weapon select is NOT saved or loaded. Please reselect your weapon!"
      input_pause( "Press enter to continue..." )
      

   def PromptSelectAttribute( self ):
      while True:   
         print "\n\n\nPress enter w/o selecting a value to return to main menu"
         print "=== Attributes ==="
         for idx,val in enumerate( self.CalcAttributes ):
            print "[%2d] %s"% ( idx, val[3] )
         # Get User Input
         try:
            selection = input(">")
         except SyntaxError:
            return

         # (Name,Type,Default,PrettyName,HelpString)
         # PromptChangeGenericType( self, attribName, attrType, prettyName = None, helpStr = None ):
         try:
            tableLine = self.CalcAttributes[selection]
         except IndexError:
            continue

         self.PromptChangeGenericType( tableLine[0], tableLine[1], tableLine[3], tableLine[4] )

   def PromptEnterAttributes( self ):      
      print "\n\n\nAnswer the prompts!"
      print "Pressing enter will skip the step and leave the current value in place!"

      logger.debug('Entering ALL attributes')

      # (Name,Type,Default,PrettyName,HelpString)
      for i in self.CalcAttributes:
         self.PromptChangeGenericType( i[0], i[1], i[3], i[4] )

      logger.debug('Attributes completed')

   def PromptChangeGenericType( self, attribName, attrType, prettyName = None, helpStr = None ):
      if( prettyName == None ):
         prettyName = attribName


      if( type(attrType) == types.MethodType ):
         attrType( prettyName, helpStr )
         return

      reTrueStr = "^[yYtT1]"
      reFalseStr = "^[nNfF0]"
      while True:
         print "\n%s = %s"%( attribName, getattr( self, attribName ) )
         if( helpStr ):
            print helpStr
         print "Enter New %s"%( attribName )
         tmp = raw_input(">")
         # Empty Lines Break
         if( len( tmp ) == 0 ):
            break

         if( attrType == int or attrType == float):
            try:
               # Case the value into the correct type!
               tmp = attrType(tmp)
            except ValueError:
               continue
            setattr( self, attribName, tmp )
            break

         if( attrType == bool):
            if( re.search( reTrueStr, tmp ) ):
               setattr( self, attribName, True )
            elif( re.search( reFalseStr, tmp ) ):
               setattr( self, attribName, False )
            else:
               print "InputError: Invalid entry"
               continue
         break

   def PromptChangeHitLoc( self, attribName, attrType, prettyName = None, helpStr = None ):
      attribName = "HitLoc"
      menu = [ "Arm","Eye","Face","Foot","Groin","Hand","Leg",
         "Neck","Skull","Torso","Vitals" ]
      while True:
         print "\n%s = %s"%( attribName, getattr( self, attribName ) )
         print "Enter New %s"%( attribName )
         for idx,val in enumerate( menu ):
            print "[%2d] %s"% ( idx, val )
         try:
            selection = input(">")
         except NameError:
            continue
         except SyntaxError:
            break

         try:
            self.HitLoc = menu[selection]
         except IndexError:
            continue
         break

   def PromptChangeWeapon( self, *pargs ):
      while True:
         self.UpdateWeaponsList()
         if( len( self.WeaponList ) == 0 ):
            logger.error('Attempted to load weapons w/o a populated list')
            print "Error: No weapons found in Weapons directory!"
            input_pause( "Press enter to continue" )
            break
         print "\n\n\n   ===Select a Weapon==="
         print "Note: Weapons list has been reloaded from HDD. Reselect weapon to refresh"
         for idx,val in enumerate( self.WeaponList ):
            print "[%d] %s"%( idx, val.__str__( ) )

         try:
            tmp = input(">")
         except NameError:
            print "NameError: Weapon Selection must be an int"
            continue
         except SyntaxError:
            break
         if( type( tmp ) != types.IntType ):
            print "TypeError: Weapon Selection must be an int"
            continue
         try:
            self.Weapon = self.WeaponList[tmp]
         except IndexError:
            print "IndexError: Select a valid entry!"
            continue
         break

   def PrintOptions( self ):
      print "\n\n\n   ===Selected Options==="
      print "       ===Base Stats==="
      print "    DX:    %2d         Skill:    %2d"%( self.DX, self.Skill )
      print "       ===Situation==="
      print "    SM:  %4.1f         Range:  %4.1f"%( self.SM, self.Range )
      print " Speed:  %4.1f   Darkess/Fog:   %3d"%( self.Speed, self.DarkFog )
      print "CanSee: %5s  KnowLocation: %5s"%( self.CanSee, self.KnowLoc )
      print " Shock:    %2d   Concealment: %s"%(self.Shock,   self.Concealment )
      print "       ===Player Choices==="
      print "       HitLoc: %6s         Weapon: %s"%( self.HitLoc, self.Weapon )
      print " RoundsAiming:     %2d     ShotsFired: %d"%( self.RoundsAiming, self.ShotsFired )
      print "      Bracing:  %5s   AllOutAttack: %5s"%( self.Bracing, self.AllOutAttack )
      print "MoveAndAttack:     %2d    PopUpAttack: %s"%( self.MoveAndAttack, self.PopUpAttack )
      print "Change Facing:  %5s"%( self.ChangeFacing )
      print "       ===GM Choices==="
      print "MiscBonus:",  self.MiscBonus
      print "       ===Result==="
      print "FINAL RESULT: >>> %d <<<"%( self.Mod )

   def HelpUserWithMath( self ):
      """
      Walk the user through math choices step by step
      """

      logger.debug('Starting to assist user with math')
      print "This section has yet to be done"
      input_pause( "Press enter to continue" )

      logger.debug('Finished assisting user with math')

   def PrintErrorGuide( self ):
      """
      Try to find errors in the users numbers and display them!
      """
      def ErrorPrint( check, errorStr):
         if( check ):
            print "\nERROR:",errorStr
            input_pause( "Press enter to continue" )

      def WarningPrint( check, errorStr ):
         if( check ):
            print "\nWARNING:",errorStr


      logger.debug('Starting Error Check')

      print "\n\n\n   ===Begin Error Checking==="
      print "WARNINGs will not block, and will only be displayed."
      print "ERRORs will block and force you to hit enter to move on."

      ErrorPrint( self.DX < 1, "DX < 1" )
      WarningPrint( self.DX > 18, "DX > 18, this is a LOT of DX")

      WarningPrint( self.Skill >= 10, "Skill is > 10, did you enter effective skill rather then base?")

      ErrorPrint( self.SM <= 0, "SM <=0, SM is a measure of size, NOT the modifier itself.")

      WarningPrint( self.Range == 0.0, "Range = 0, Are you standing on your target? Adjacent targets are range 1")
      ErrorPrint( self.Range < 0.0, "Range < 0, Negative length implies non-euclidean space. Go Play Call Of Cthulhu....")

      ErrorPrint( self.Speed < 0.0, "Speed < 0, Use speed NOT velocity")

      ErrorPrint( self.DarkFog > 0, "DarkFod > 0. These are negative modifiers only! You cannot have positive values.")
      ErrorPrint( self.DarkFog < -9, "DarkFog < -9, TOTAL Darkness/Fog is a -9, you cannot be worse!")

      WarningPrint( self.CanSee and not self.KnowLoc, "You can see you target but you don't know their location? \n  Fix \"Can See\" or \"Know Location\"" )
      WarningPrint( not self.CanSee and self.Concealment, "Not being able to see a target will ignore Concealment condition.")

      ErrorPrint( self.RoundsAiming < 0, "You cannot spend negative rounds aiming")
      # TODO: This warning is not REALLY true. Sniper rifles need to aim for many rounds to get their bonus (per page 412). We need to handle scopes...
      WarningPrint( self.RoundsAiming > 3, "Spending more then 3 rounds aiming gives no further benefit...")

      ErrorPrint( self.Weapon == None, "You need to select a weapon!")

      if( self.Weapon ):
         ErrorPrint(  self.ShotsFired > self.Weapon.Shots[0], "Shots fired is more then max ammo of your weapon.")
         ErrorPrint(  self.ShotsFired > self.Weapon.RoF, "Shots fired exceeds Rate of Fire of your weapon.")
         ErrorPrint(  self.ShotsFired < 1, "Shots fired < 1" )
      else:
         logger.debug('No weapon selected')
      WarningPrint( self.ShotsFired > 9000, "THATS OVER 9000!!!!!!!!")

      ErrorPrint( self.Bracing and ( self.MoveAndAttack or self.PopUpAttack ), "You cannot brace while Moving or Popping up!" )

      ErrorPrint( self.ChangeFacing and self.MoveAndAttack , "Moving gives you a free change of facing!" )

      ErrorPrint( self.Shock > 0, "Shock > 0, this cannot be a bonus!")
      ErrorPrint( self.Shock < -4, "Shock < -4, this is the worst case effect of shock damage")

      WarningPrint( self.AllOutAttack and self.MoveAndAttack, "You can only move half your movement when All Out Attacking AND moving.")

      ErrorPrint( self.MoveAndAttack < 0, "Move and Attack < 0, Negative distance implies non-euclidean space. Go Play Call Of Cthulhu....")      

      ErrorPrint( self.PopUpAttack and self.RoundsAiming, "You cannot Pop Up Attack AND aim.")

      print "\nError checks complete!"
      input_pause( "Press enter to continue..." )
      logger.debug('Finished Error Check')

   def PrintGunDetails( self ):
      print 
      try:
         self.Weapon.PrintDetailed()
      except AttributeError:
         logger.error('Attmepted to print a gun w/o selecting one first!')
         print "You need to select a gun first!"

      input_pause( "Press enter to return to main menu..." )


   def UpdateWeaponsList( self ):

      logger.debug('Start updating the weapons list')
      # Object Fields
      self.WeaponList = list()

      files = glob.glob('./Weapons/*.json')
      print "files=",files

      # Init functionality
      for i in files:
         try:
            self.WeaponList.append(Weapon(i))
         except:
            logger.warning('Failed to create a Weapon() instance out of file %s'%(i))
            print "\nError, file \"%s\" was not parsed."%(i)
            input_pause( "Press enter to continue..." )

      if( len(self.WeaponList ) == 0 ):
         logger.error('No weapons loaded')

      logger.debug('Finished updating the weapons list')



   # ************************************
   # ******* Calculator Functions *******
   # ************************************

   def CalculateBaseScore( self ):

      logger.debug('Started to calculate the base score')

      self.Mod = 0
      self.Mod += self.DX
      self.Mod += self.Skill
      self.Mod += self.CalcSizeModifier( self.SM )
      self.Mod += self.CalcSpeedAndRange( self.Range, self.Speed )
      self.Mod += self.CalcHitLocation( self.HitLoc )
      self.Mod += self.CalcVisionEffects( self.CanSee,       self.KnowLoc, 
                                          self.DarkFog, self.Concealment )
      self.Mod += self.CalcWeaponMods( self.RoundsAiming, self.PopUpAttack, 
                                       self.MoveAndAttack, self.ChangeFacing )
      if( self.Bracing ):
         self.Mod += 1
      self.Mod += self.Shock
      if( self.AllOutAttack ):
         # TODO: This only includes the Determinded attack from page 365, the suppression attack is different...
         self.Mod += 1
      self.Mod += self.MiscBonus
      self.Mod += self.CalcRateOfFireBonus( self.ShotsFired )
      # TODO:
         # Calculate Rate of Fire table for the player

      logger.debug('Finished calculating the base score')

   def CalcSpeedAndRange( self, distance, speed ):
      ranges = (
         (2, 0 ),(3, -1 ),(5, -2 ),(7, -3 ),(10, -4 ),
         (15, -5 ),(20, -6 ),(30, -7 ),(50, -8 ),(70, -9 ),
         (100, -10 ),(150, -11 ),(200, -12 ),(300, -13 ),
         (500, -14 ),(700, -15 ),(1000, -16 ),(1500, -17 ),
         (2000, -18 ),(3000, -19 ),(5000, -20 ),(7000, -21 ),
         (10000, -22 ),(15000, -23 ),(20000, -24 ),(30000, -25 ),
         (50000, -26 ),(70000, -27 ),(100000, -28 ),(150000, -29 ),
         (200000, -30 )
         )

      if( speed < 0 or distance < 0 ):
         logger.error('Negative distance or speed')
         logger.error('Speed: %f'%(speed))
         logger.error('Distance: %f'%(distance))
         return -9000


      for i in ranges:
         if distance + speed < i[0]:
            return i[1]

      logger.warning('Speed: %f Range: %f exdeed legal values'%(speed,distance))

      print "WARNING! Speed and Range are outside of legal values!"
      print "Value will default to -9000"
      input_pause( "Press enter to continue..." )
      return -9000

   def CalcSizeModifier( self, size ):
      sizeTbl = (
         (0.006, -15),(0.009, -14),(0.014, -13),(0.019, -12),(0.028, -11),(0.042, -10),
         (0.056, -9),(0.083, -8),(0.139, -7),(0.222, -6),(0.333, -5),(0.500, -4),
         (0.667, -3),(1, -2),(1.5, -1),(2, 0),(3, 1),(5, 2),(7, 3),(10, 4),(15, 5),
         (20, 6),(30, 7),(50, 8),(70, 9),(100, 10),(150, 11),(200, 12),(300, 13),
         (500, 14),(700, 15),(1000,  16),(1500,  17),(2000,  18),(3000,  19),(5000,  20),
         (7000,  21),(10000, 22),(15000, 23),(20000, 24),(30000, 25),(50000, 26),
         (70000, 27),(100000, 28),(150000, 29),(200000, 30)
         )

      if( size <= 0 ):
         logger.error('Zero or Negative size')
         logger.error('Size: %f'%(size))
         return -9000

      for i in sizeTbl:
         if size < i[0]:
            return i[1]
      print "WARNING! Size is outside of legal values!"
      print "Value will default to 30"
      input_pause( "Press enter to continue..." )
      return 30

   def CalcHitLocation( self, location ):
      hitLocDict = {
         "Arm":-2,
         "Eye":-9,
         "Face":-5,
         "Foot":-4,
         "Groin":-3,
         "Hand":-4,
         "Leg":-2,
         "Neck":-5,
         "Skull":-7,
         "Torso":0,
         "Vitals":-3,
         }
      try:
         return hitLocDict[location]
      except KeyError:
         logger.critical('HitLocation is outside of hitLocDict bounds!')
         print "WARNING! Hit location has an invalid key!"
         print "Value will default to -10"
         input_pause( "Press enter to continue..." )
         return -10

   def CalcVisionEffects( self, argCanSee, argKnowLoc, argDarkFog, argConcealment ):
      tmp = 0
      if( not argCanSee and not argKnowLoc ):
         tmp = -6
      elif( not argCanSee and argKnowLoc ):
         tmp = -4
      elif( argConcealment ):
         tmp = -2

      if( argDarkFog < -9 ):
         logger.error('Darkness/Fog value bellow minimums')
         logger.error('argDarkFog: %f'%(argDarkFog))

      return max(-10,tmp + argDarkFog)

   def CalcWeaponMods( self, argAcc, argPopup, argMoveAndAttack, argChangeFacing ):
      if( self.Weapon == None ):
         logger.error('Cannot calculate with a Weapon of None')
         return 0
      retVal = 0
      
      if( argAcc ):
         if( argAcc >= 1 ):
            retVal += self.Weapon.Acc
         if( argAcc >= 2 ):
            retVal += 1
         if( argAcc >= 3 ):
            retVal += 1
      
      if( argPopup ):
         retVal += -2
      
      if( argMoveAndAttack or argChangeFacing ):
         retVal += self.Weapon.Bulk
      
      return retVal

   def CalcRateOfFireBonus( self, argShotsFired ):
      shotsTbl = (
         (4,0),
         (8,1),
         (12,2),
         (16,3),
         (24,4),
         (49,5),
         (99,6)
         )

      for i in shotsTbl:
         if argShotsFired <= i[0]:
            return i[1]

      print "WARNING! Shots Fired exceeds legal limits!"
      print "Value will default to 0"
      input_pause( "Press enter to continue..." )
      return 0

def input_pause( inputStr="Press enter to continue..." ):
   print inputStr
   raw_input()

def GlobalCleanup():
   logger.info('***** Logging Terminated *****')

if __name__ == '__main__':
   # Setup and format the logging for the application
   logger = logging.getLogger('Test')
   logger.setLevel( logging.DEBUG )
   fh = logging.FileHandler('debug.log')
   fh.setLevel( logging.DEBUG )
   formatter = logging.Formatter('%(asctime)s - %(levelname)7s - %(funcName)s@%(lineno)d: %(message)s')
   fh.setFormatter(formatter)
   logger.addHandler(fh)

   # Legal logging levels are: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'

   logger.info('***** Logging Initiated  *****')
   logger.info('******************************')
   logger.info('******************************')
   logger.info('******************************')
   logger.info('******************************')
   logger.info('******************************')
   logger.info('Logging started on version: %s'%(version))

   atexit.register(GlobalCleanup)

   logger.info('OS: %s'%(os.name))

   # TODO: This doesn't work on OSx
   if( os.name == 'nt'):
      os.system('cls')

   print "/\\"
   for i in range(24):
      print "||"
   print "\\/"
   print "This program uses a lot of screen space, so I suggest you expand your window"
   print " before you continue. Expand to see the complete ruler above for best results. "
   input_pause( "Press enter to continue..." )

   if( os.name == 'nt'):
      os.system('cls')

   UI = RangedAttackCalculator()
   
   try:
      UI.Main()
   except BaseException,e:
       logger.exception(e)
       raise