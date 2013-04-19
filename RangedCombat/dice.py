import random
import re
import numpy

class Dice():
   def __init__( self, n=1, s=6 ):
      self.Sides = None
      self.Number = None
      self.MathOp = None
      self.MathVal = None
      self.InputStr = None
      self.DiceInError = True
      if( type(n) == str ):
         self.InputStr = n
         matchStr = "^(\d+)d(\d+)?(?:([+-/*//])(\d+))?"
         results = re.search( matchStr, n )
         if( results ):
            results = results.groups()
            if( results[1] ):
               self.Sides = int( results[1] )
            else:
               self.Sides = 6
            self.Number = int( results[0] )
            if( results[2] and results[3] ):
               self.MathOp = results[2]
               self.MathVal = int( results[3] )
            self.DiceInError = False

      else:
         self.DiceInError = False
         self.Sides = int( s )
         self.Number = int ( n )
      self.History = list()

   def __str__( self ):
      if( self.DiceInError ):
         return "Dice(%s)(Err)"%( self.InputStr )
      if( self.MathOp and self.MathVal ):
         return "Dice(%dd%d %s %d)"%( self.Number, self.Sides, self.MathOp, self.MathVal )
      else:
         return "Dice(%dd%d)"%( self.Number, self.Sides )

   def Roll( self ):
      retval = 0
      for i in range(self.Number):
         retval += random.randint(1,self.Sides)
      if( self.MathOp and self.MathVal ):
         retval = eval( '%d %s %d'%( retval, self.MathOp, self.MathVal ) )
      self.History.append( retval )
      return retval

   def Check( self, checkVal, verbose=False):
      """
      GURPs style skill check, will return a 3 part tuple
      ( pass, roll, margin )
         Pass: True/False if the check was passed
         Roll: Amount rolled on the dice
         Margin: Margin of Success or Failure
      """
      result = self.Roll()
      passVal = result <= checkVal
      passMargin = checkVal - result
      if( verbose ):
         return ( passVal, result, passMargin )
      else:
         return passMargin

   def DC( self, DCval, mods=0, verbose=False ):
      """
      DnD Style DC checks
      ( pass, roll, margin )
         Pass: True/False if the check was passed
         Roll: Amount rolled on the dice
         Margin: Margin of Success or Failure
      """
      result = self.Roll()
      passVal = result >= checkVal
      passMargin = checkVal - result
      if( verbose ):
         return ( passVal, result, passMargin )
      else:
         return passMargin
class Dice2():
   """
   Dice2 is a more advanced version of Dice. This takes only one argument on
      on creation. A string that describes any basic math formula and basic dice 
      expression.
   """
   def __init__( self, diceExpression='1d20' ):
      self.DieStr = diceExpression
      self.History=numpy.zeros(0)

   def __str__( self ):
      return self.DieStr

   def Roll( self ):
      retVal = DieEvaluator( self.DieStr )
      try:
         self.History = numpy.append( self.History, int(retVal) )
         return int(retVal)
      except ValueError:
         print "Error: Invalid Dice String:",self.DieStr
         print "   Final return of:", retVal
         return None

   def PrintStats( self ):
      if( len( self.History ) < 1 ):
         return
      print "===Stats==="
      print "  History:",self.History
      print "    Range:",numpy.ptp( self.History )
      print "     Mean:",numpy.mean( self.History )
      print "   Median:",numpy.median( self.History )
      print "      std:",numpy.std( self.History )
      print "      var:",numpy.var( self.History )

      tmp = list( self.History )
      tmp.reverse()
      try:
         print "Last Crit:",tmp.index(20)
      except ValueError:
         print "Never"

      try:
         print "Last Fail:",tmp.index(1)
      except ValueError:
         print "Never"





def DieEvaluator( diceExpression ):   
   def funcRoll( matchobj ):
      n=int( matchobj.group( 1 ) )
      s=int( matchobj.group( 2 ) )
      retval = 0
      for i in range(n):
         retval += random.randint(1,s)
      return str(retval)

   # print "\nBegin eval"
   while True:
      # print "Loop on:",diceExpression

      # Remove parenthesis with only numbers inside of them
      matchStr = "\(\d+\)"
      if( re.search( matchStr, diceExpression ) ):
         #print "Peren:",re.search( matchStr, diceExpression ).group(0)
         replStr = eval( re.search( matchStr, diceExpression ).group(0) )
         replStr = str( replStr )
         diceExpression = re.sub( matchStr, replStr, diceExpression, count=1 )
         continue

      # Evaluate correct dice stings
      matchStr = "(\d+)d(\d+)"
      if( re.search( matchStr, diceExpression ) ):
         # print "Dice:",re.search( matchStr, diceExpression ).group(0)
         diceExpression = re.sub( matchStr, funcRoll, diceExpression, count=1 )
         continue

      # Append '6' onto hanging d's
      matchStr = "\d+d"
      if( re.search( matchStr, diceExpression ) ): 
         # print "d Fix:",re.search( matchStr, diceExpression ).group(0)
         replStr = re.search( matchStr, diceExpression ).group(0)
         diceExpression = re.sub( matchStr, replStr+'6' , diceExpression, count=1 )
         continue     

      # Exponents
      matchStr = "\d+\^\d+"
      if( re.search( matchStr, diceExpression ) ):
         #print "Exponent:",re.search( matchStr, diceExpression ).group(0)
         replStr = re.sub( "\^", "**", re.search( matchStr, diceExpression ).group(0) )
         replStr = eval( replStr )
         replStr = str( replStr )
         diceExpression = re.sub( matchStr, replStr, diceExpression, count=1 )
         continue

      # Multiplication
      matchStr = "\d+[*xX]\d+"
      if( re.search( matchStr, diceExpression ) ):
         #print "Multi:",re.search( matchStr, diceExpression ).group(0)
         replStr = re.sub( "x", "*", re.search( matchStr, diceExpression ).group(0) )
         replStr = re.sub( "X", "*", re.search( matchStr, diceExpression ).group(0) )
         replStr = eval( replStr )
         replStr = str( replStr )
         diceExpression = re.sub( matchStr, replStr, diceExpression, count=1 )
         continue      

      # Dor-vision
      matchStr = "\d+\/\d+"
      if( re.search( matchStr, diceExpression ) ):
         #print "Divide:",re.search( matchStr, diceExpression ).group(0)
         replStr = eval( re.search( matchStr, diceExpression ).group(0) )
         replStr = str( replStr )
         diceExpression = re.sub( matchStr, replStr, diceExpression, count=1 )
         continue      

      # Addition
      matchStr = "\d+\+\d+"
      if( re.search( matchStr, diceExpression ) ):
         #print "Add:",re.search( matchStr, diceExpression ).group(0)
         replStr = eval( re.search( matchStr, diceExpression ).group(0) )
         replStr = str( replStr )
         diceExpression = re.sub( matchStr, replStr, diceExpression, count=1 )
         continue    

      # Surb-Traction
      matchStr = "\d+\-\d+"
      if( re.search( matchStr, diceExpression ) ):
         #print "Sub:",re.search( matchStr, diceExpression ).group(0)
         replStr = eval( re.search( matchStr, diceExpression ).group(0) )
         replStr = str( replStr )
         diceExpression = re.sub( matchStr, replStr, diceExpression, count=1 )
         continue
      # We only get here when we have nothing left to parse!
      break

   return diceExpression





if __name__ == '__main__':
   print "Testing the dice roller!"
   d=Dice2('1d20')
   # print d
   for i in range(1000):
      d.Roll()
   d.PrintStats()
