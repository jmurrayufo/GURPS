import json
import re
import types
import time
import glob
import os


class Weapon( ):

   # Parse and generator
   def __init__( self, jsonFile ):
      with open( jsonFile, 'r' ) as fp:
         jsonTable = json.load(fp)   

      self.TL     = jsonTable['TL']
      self.Name   = jsonTable['Name']
      self.Damage = self.ParseDamage( jsonTable['Damage'] )
      self.Acc    = jsonTable['Acc']
      self.Range  = self.ParseRange( jsonTable['Range'] )
      self.Weight = self.ParseWeight( jsonTable['Weight'] )
      self.Rof    = jsonTable['RoF']
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
            raise
      return retVal



   def ParseDamage( self, inputStr ):
      matchStr = "^(?:((?:\d+d|HT)(?:[x+-]\d+)?)(?:\((\d+(?:\.\d+)?|inf)\))?)(?: (.+))?"
      tmp = re.search( matchStr, inputStr )
      tmp = self.GenericToCleanList( tmp.groups() )
      return tmp

   def ParseRange( self, inputStr ):
      matchStr = "^(\d+)/?(\d+)?"
      tmp = re.search( matchStr, inputStr )
      tmp = self.GenericToCleanList( tmp.groups() )
      return tmp

   def ParseWeight( self, inputStr ):
      matchStr = "^(\d+)/?(\w+)?"
      tmp = re.search( matchStr, inputStr )
      tmp = self.GenericToCleanList( tmp.groups() )
      return tmp

   def ParseShots( self, inputStr ):
      matchStr = "^(\d+)(?:\((\d+\.?\d*)\))?"
      tmp = re.search( matchStr, inputStr )
      tmp = self.GenericToCleanList( tmp.groups() )
      return tmp

   # Output and access functions
   def PrintDetailed( self ):
      print "  Name:",       self.Name
      print "    TL:",       self.TL
      print "Damage:",       self.Damage
      print "   Acc:",       self.Acc
      print "Range :",       self.Range
      print "Weight:",       self.Weight
      print "   Rof:",       self.Rof
      print " Shots:",       self.Shots
      print "    ST:",       self.ST
      print "  Bulk:",       self.Bulk
      print "Recoil:",       self.Recoil
      print "  Cost:",       self.Cost
      print "    LC:",       self.LC
      print " Notes:",       self.Notes

class RangedAttackCalculator():

   def __init__( self ):
      # User input Fields
      self.DX = 0
      self.Skill = 0
      self.SM = 2
      self.Range = 0
      self.Speed = 0
      self.HitLoc = "Torso"
      self.DarkFog = 0
      self.CanSee = True
      self.KnowLoc = True
      self.Concealment = False
      self.Weapon = None
      self.RoundsAiming = 0
      self.ShotsFired = 1
      self.Bracing = False
      self.Shock = 0
      self.AllOutAttack = False
      self.MoveAndAttack = 0
      self.PopUpAttack = False
      self.MiscBonus = 0

      # Object Fields
      self.Mod = None

      # (GetAttr name, function to use, name to print, help for user)
      self.PromptMenu = [
         ("DX", self.PromptChangeGenericInt, "DX", None),
         ("Skill", self.PromptChangeGenericInt, "Skill", None),
         ("SM", self.PromptChangeGenericFloat, "SM", "SM = Size of target in yards"),
         ("Range", self.PromptChangeGenericFloat, "Range", None),
         ("Speed", self.PromptChangeGenericFloat, "Speed", None),
         ("DarkFog", self.PromptChangeGenericInt, "DarkFog", None),
         ("CanSee", self.PromptChangeGenericBool, "CanSee", None),
         ("KnowLoc", self.PromptChangeGenericBool, "KnowLoc", None),
         ("Concealment", self.PromptChangeGenericBool, "Concealment", None),
         ("HitLoc", self.PromptChangeHitLoc, None, None),
         ("RoundsAiming", self.PromptChangeGenericInt, "RoundsAiming", None),
         ("ShotsFired", self.PromptChangeGenericInt, "ShotsFired", None),
         ("Bracing", self.PromptChangeGenericBool, "Bracing", None),
         ("Shock", self.PromptChangeGenericInt, "Shock", None),
         ("AllOutAttack", self.PromptChangeGenericBool, "AllOutAttack", None),
         ("MoveAndAttack", self.PromptChangeGenericInt, "MoveAndAttack", None),
         ("PopUpAttack", self.PromptChangeGenericBool, "PopUpAttack", None),
         ("MiscBonus", self.PromptChangeGenericInt, "MiscBonus", None)
         ]

      self.UpdateWeaponsList()

   # ********************************
   # ******* User Interaction *******
   # ********************************
   def Main( self ):
      menu = [
         ("Quit",exit),
         ("Change Attribute",self.PromptSelectAttribute ),
         ("Enter ALL Attributes",self.PromptEnterAttributes ),
         ("Change Weapon",self.PromptChangeWeapon ),
         ("Walk Through Math",self.HelpUserWithMath),
         ("Print Gun Details",self.PrintGunDetails),
         ("Save",self.PromptSaveSettings),
         ("Load",self.PromptLoadSettings)
         ]
      while True:
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
            continue

         if(selection == exit):
            break

         if( type( selection ) == types.FunctionType or types.InstanceType):
            selection()


   def PromptSaveSettings( self ):
      # Get user input for where to save the file
      print "\nEnter file name to save as."
      fileName = raw_input(">")
      fileName = "Save/"+fileName + ".json"

      # Do we have a save directory?
      if( not os.path.exists('Save') ):
         os.mkdir("Save")

      # Is it just a file?
      if( not os.path.isdir('Save') ):
         print "Error! Cannot save as \"./Save\" isn't a directory!"
         print "Press enter to continue"
         raw_input()
         return

      # Prepare object for saving. 
      saveData = dict()
      saveData['DX'] = self.DX
      saveData['Skill '] = self.Skill
      saveData['SM '] = self.SM
      saveData['Range'] = self.Range
      saveData['Speed'] = self.Speed 
      saveData['HitLoc'] = self.HitLoc
      saveData['DarkFog'] = self.DarkFog
      saveData['CanSee'] = self.CanSee
      saveData['KnowLoc'] = self.KnowLoc
      saveData['Concealment'] = self.Concealment 
      saveData['RoundsAiming'] = self.RoundsAiming
      saveData['ShotsFired'] = self.ShotsFired
      saveData['Bracing'] = self.Bracing
      saveData['Shock'] = self.Shock
      saveData['AllOutAttack'] = self.AllOutAttack
      saveData['MoveAndAttack'] = self.MoveAndAttack
      saveData['PopUpAttack'] = self.PopUpAttack
      saveData['MiscBonus'] = self.MiscBonus

      print saveData

      with open( fileName, 'w' ) as fp:
         saveJson = json.dump( saveData, fp )
         print saveJson

   def PromptLoadSettings( self ):
      savedFileList = glob.glob(".\\Save\\*.json")
      print savedFileList

      while True:
         print "\n\n\n   ===Select a File==="
         for idx,val in enumerate( savedFileList ):
            print "[%d] %s"%( idx, val.__str__( ) )

         try:
            tmp = input(">")
         except NameError:
            print "NameError: File Selection must be an int"
            continue
         except SyntaxError:
            return
         if( type( tmp ) != types.IntType ):
            print "TypeError: File Selection must be an int"
            continue
         try:
            savedFile = savedFileList[tmp]
         except IndexError:
            print "IndexError: Select a valid entry!"
            continue
         break

      with open( savedFile, 'r' ) as fp:
         saveData = json.load(fp)
      self.DX = saveData['DX']
      self.Skill = saveData['Skill ']
      self.SM = saveData['SM ']
      self.Range = saveData['Range']
      self.Speed  = saveData['Speed']
      self.HitLoc = saveData['HitLoc']
      self.DarkFog = saveData['DarkFog']
      self.CanSee = saveData['CanSee']
      self.KnowLoc = saveData['KnowLoc']
      self.Concealment  = saveData['Concealment']
      self.RoundsAiming = saveData['RoundsAiming']
      self.ShotsFired = saveData['ShotsFired']
      self.Bracing = saveData['Bracing']
      self.Shock = saveData['Shock']
      self.AllOutAttack = saveData['AllOutAttack']
      self.MoveAndAttack = saveData['MoveAndAttack']
      self.PopUpAttack = saveData['PopUpAttack']
      self.MiscBonus = saveData['MiscBonus']

      print "\nLoaded settings from file",savedFile
      print "WARNING: Weapon select is NOT saved or loaded. Please reselect your weapon!"
      print "Press enter to continue"
      raw_input()



   def PromptEnterAttributes( self ):      
      print "Answer the prompts!"
      print "Pressing enter will skip the step and leave the current value in place!"

      for i in self.PromptMenu:
         i[1]( i[2], i[3] )

   def PromptChangeGenericInt( self, attribName, prettyName = None ):
      if( prettyName == None ):
         prettyName = attribName
      while True:
         print "\n%s = %d"%( attribName, getattr( self, attribName ) )
         print "Enter New %s"%( attribName )
         try:
            tmp = input(">")
         except NameError:
            print "NameError: %s must be an int"%( attribName )
            continue
         except SyntaxError:
            break
         if( type( tmp ) != types.IntType ):
            print "TypeError: %s must be an int"%( attribName )
            continue
         setattr( self, attribName, tmp )
         break

   def PromptChangeGenericFloat( self, attribName, prettyName = None ):
      if( prettyName == None ):
         prettyName = attribName
      while True:
         print "\n%s = %.1f"%( attribName, getattr( self, attribName ) )
         print "Enter New %s"%( attribName )
         try:
            tmp = input(">")
         except NameError:
            print "NameError: %s must be a float"%( attribName )
            continue
         except SyntaxError:
            break
         if( type( tmp ) != types.FloatType ):
            try: 
               tmp = float( tmp )
            except:
               print "TypeError: %s must be an float"%( attribName )
               continue
         setattr( self, attribName, tmp )
         break

   def PromptChangeGenericBool( self, attribName, prettyName = None ):
      if( prettyName == None ):
         prettyName = attribName
      reTrueStr = "^[yYtT1]"
      reFalseStr = "^[nNfF0]"
      while True:
         print "\n%s = %s"%( attribName, getattr( self, attribName ) )
         print "Enter New %s"%( attribName )
         tmp = raw_input(">")
         if( len( tmp ) == 0 ):
            break
         if( re.search( reTrueStr, tmp ) ):
            setattr( self, attribName, True )
         elif( re.search( reFalseStr, tmp ) ):
            setattr( self, attribName, False )
         else:
            print "InputError: Invalid entry"
            continue
         break

   def PromptChangeHitLoc( self, *dummyArgs1, **dummyArgs2):
      attribName = "HitLoc"
      menu = [ "Arm","Eye","Face","Foot","Groin","Hand","Leg",
         "Neck","None","Skull","Torso","Vitals" ]
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

   def PromptChangeWeapon( self ):
      while True:
         self.UpdateWeaponsList()
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

   def PromptSelectAttribute( self ):
      while True:   
         print "\n\n\n=== Attributes ==="
         for idx,val in enumerate( self.PromptMenu ):
            print "[%2d] %s"% ( idx, val[0] )
         # Get User Input

         try:
            selection = input(">")
         except SyntaxError:
            return

         try:
            funcCall = self.PromptMenu[selection][1]
         except IndexError:
            continue

         if( type( funcCall ) == types.FunctionType 
            or type(funcCall ) == types.InstanceType 
            or type( funcCall ) == types.MethodType ):
            funcCall(self.PromptMenu[selection][2])
            break
         if( funcCall == None ):
            print "\n\nPromptChange%s() needs to be writen!"%( self.PromptMenu[selection][0] )
            print "Press enter to continue"
            raw_input()

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
      print "       ===GM Choices==="
      print "MiscBonus:",  self.MiscBonus
      print "       ===Result==="
      print "FINAL RESULT: >>> %d <<<"%( self.Mod )

   def HelpUserWithMath( self ):
      print "This section has yet to be done"

   def PrintErrorGuide( self ):
      """
      Try to find errors in the users numbers and display them!
      """
      # Known issues:
         # Shots fired can exceed the RoF of the Weapon AND the Shots in the weapon

   def PrintGunDetails( self ):
      print 
      try:
         self.Weapon.PrintDetailed()
      except AttributeError:
         print "You need to select a gun first!"

      print "Hit enter to return to main menu..."
      raw_input()


   def UpdateWeaponsList( self ):
      # Object Fields
      self.WeaponList = list()

      files = glob.glob('*.json')

      # Init functionality
      for i in files:
         try:
            self.WeaponList.append(Weapon(i))
         except:
            print "\nError, file \"%s\" was not parsed."%(i)
            print "Hit enter to continue parsing other files"
            raw_input()



   # ************************************
   # ******* Calculator Functions *******
   # ************************************

   def CalculateBaseScore( self ):
      self.Mod = 0
      self.Mod += self.DX
      self.Mod += self.Skill
      self.Mod += self.CalcSizeModifier( self.SM )
      self.Mod += self.CalcSpeedAndRange( self.Range, self.Speed )
      self.Mod += self.CalcHitLocation( self.HitLoc )
      self.Mod += self.CalcVisionEffects( self.CanSee,       self.KnowLoc, 
                                          self.DarkFog, self.Concealment )
      self.Mod += self.CalcWeaponMods( self.RoundsAiming, self.PopUpAttack, 
                                       self.MoveAndAttack )
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
      for i in ranges:
         if distance + speed < i[0]:
            return i[1]
      print "WARNING! Speed and Range are outside of legal values!"
      print "Press enter to accept and use a score of -30"
      raw_input()
      return -30

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
      for i in sizeTbl:
         if size < i[0]:
            return i[1]
      print "WARNING! Size is outside of legal values!"
      print "Press enter to accept and use a score of -15"
      raw_input()
      return -15

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
         "None":0,
         "Skull":-7,
         "Torso":0,
         "Vitals":-3,
         }
      try:
         return hitLocDict[location]
      except KeyError:
         print "WARNING! Hit location has an invalid key!"
         print "Press enter to accept and use a score of -10"
         raw_input()
         return -10

   def CalcVisionEffects( self, argCanSee, argKnowLoc, argDarkFog, argConcealment ):
      tmp = 0
      if( not argCanSee and not argKnowLoc ):
       tmp = -6
      elif( not argCanSee and argKnowLoc ):
       tmp = -4
      elif( argConcealment ):
       tmp = -2

      return max(-10,tmp + argDarkFog)

   def CalcWeaponMods( self, argAcc, argPopup, argMoveAndAttack ):
      if( self.Weapon == None ):
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
      
      retVal += self.Weapon.Bulk * argMoveAndAttack
      
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
      print "Press enter to accept and use a score of 0"
      raw_input()
      return 0

os.system('cls')

print "Welcome to the Ranged Combat Calculator!"
print "There is no load/save functionality at the moment (sorry!)"
print "This program uses a lot of screen space, so I suggest you expand your window"
print " before you continue."
print "Press Enter to continue..."
raw_input()

os.system('cls')

UI = RangedAttackCalculator()

UI.Main()