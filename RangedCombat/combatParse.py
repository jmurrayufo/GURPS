import json
import re
import types
import time


class Weapon( ):

   # Parse and generator
   def __init__( self, jsonTable ):
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
   def __init__( self, WeaponObj ):
      # User input Fields
      self.DX = 0
      self.Skill = 0
      self.SM = 2
      self.Range = 0
      self.Speed = 0
      self.HitLoc = None
      self.DarkFog = 0
      self.CanSee = True
      self.KnowLoc = True
      self.Concealment = False
      self.Weapon = WeaponObj
      self.RoundsAiming = 0
      self.ShotsFired = 1
      self.Bracing = False
      self.Shock = 0
      self.AllOutAttack = False
      self.MoveAndAttack = False
      self.PopUpAttack = False
      self.MiscBonus = 0

      # Object Fields
      self.Mod = None

   # User Interaction
   def Main( self ):
      menu = [
         ("Quit",exit),
         ("Change Attribute",self.PromptSelectAttribute ),
         ("Enter ALL Attributes",self.PromptEnterAttributes )
         ]
      while True:
         # Print out the current stats and such
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

   def PromptEnterAttributes( self ):
      print "\n\nPromptEnterAttributes() needs to be writen!"
      print "Press enter to continue"
      raw_input()

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

   def PromptChangeWeapon( self, dummyVar ):
      print "\n\nPromptChangeWeapon needs to be writen!"
      print "Press enter to continue"
      raw_input()


   # Attribute Modification Prompts
   def PromptSelectAttribute( self ):
      menu = [
         ("DX", self.PromptChangeGenericInt, "DX", None),
         ("Skill", self.PromptChangeGenericInt, "Skill", None),
         ("SM", self.PromptChangeGenericFloat, "SM", None),
         ("Range", self.PromptChangeGenericFloat, "Range", None),
         ("Speed", self.PromptChangeGenericFloat, "Speed", None),
         ("DarkFog", self.PromptChangeGenericInt, "DarkFog", None),
         ("CanSee", self.PromptChangeGenericBool, "CanSee", None),
         ("KnowLoc", self.PromptChangeGenericBool, "KnowLoc", None),
         ("Concealment", self.PromptChangeGenericBool, "Concealment", None),
         ("HitLoc", None, None),
         ("Weapon", None, None),
         ("RoundsAiming", self.PromptChangeGenericInt, "RoundsAiming", None),
         ("ShotsFired", self.PromptChangeGenericInt, "ShotsFired", None),
         ("Bracing", self.PromptChangeGenericBool, "Bracing", None),
         ("Shock", self.PromptChangeGenericInt, "Shock", None),
         ("AllOutAttack", self.PromptChangeGenericBool, "AllOutAttack", None),
         ("MoveAndAttack", self.PromptChangeGenericBool, "MoveAndAttack", None),
         ("PopUpAttack", self.PromptChangeGenericBool, "PopUpAttack", None),
         ("MiscBonus", self.PromptChangeGenericInt, "MiscBonus", None)
         ]
      while True:   
         print "\n\n\n=== Attributes ==="
         for idx,val in enumerate( menu ):
            print "[%2d] %s"% ( idx, val[0] )
         # Get User Input

         try:
            selection = input(">")
         except SyntaxError:
            return

         try:
            funcCall = menu[selection][1]
         except IndexError:
            continue

         if( type( funcCall ) == types.FunctionType 
            or type(funcCall ) == types.InstanceType 
            or type( funcCall ) == types.MethodType ):
            funcCall(menu[selection][2])
            break
         if( funcCall == None ):
            print "\n\nPromptChange%s() needs to be writen!"%( menu[selection][0] )
            print "Press enter to continue"
            raw_input()

   def PrintOptions( self ):
      print "\n\n\n   ===Selected Options==="
      print "      ===Base Stats==="
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
      print "MoveAndAttack:  %5s    PopUpAttack: %s"%( self.MoveAndAttack, self.PopUpAttack )
      print "       ===GM Choices==="
      print "MiscBonus:",  self.MiscBonus
      print "       ===Result==="
      print "FINAL RESULT:",  self.Mod


files = ["laserrifle.json"]

with open( files[0], 'r' ) as fp:
    tmp = json.load(fp)

tmp = Weapon(tmp)

UI = RangedAttackCalculator( tmp )

UI.Main()