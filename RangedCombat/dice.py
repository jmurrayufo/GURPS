import random
import re
import numpy
import time
import optparse
import os
if ( os.name == 'posix' ):
   # We only want this on OSX
   import readline

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

def ParenEval( expression ):

   # Run Cleanup of expression for evaluation
   while True:
      # Append '6' onto hanging d's
      matchStr = "(\d+d)([^0-9]|$)"
      if( re.search( matchStr, expression ) ): 
         if(_DEBUG): print " Nd Fix:",re.search( matchStr, expression ).group(1)
         replStr = re.search( matchStr, expression ).group(1)
         expression = re.sub( replStr, replStr+'6', expression, count=1 )
         continue

      # Prepend '1' infront of hanging d's
      matchStr = "[^\d](d\d+)"
      if( re.search( matchStr, expression ) ): 
         if(_DEBUG): print " dN Fix:",re.search( matchStr, expression ).group(1)
         replStr = re.search( matchStr, expression ).group(1)
         print expression
         expression = re.sub( replStr, '1'+replStr, expression, count=1 )
         print expression
         continue

      # XFixer
      matchStr = "\d+[xX]\d+"
      if( re.search( matchStr, expression ) ):
         if(_DEBUG): print " x-Fix:",re.search( matchStr, expression ).group(0)
         expression = re.sub( "[xX]", "*", expression, count=1 )
         continue 

      matchStr = '([\d\)])(\()'
      if( re.search( matchStr, expression ) ):         
         if(_DEBUG): print " ParenFix:",re.search( matchStr, expression ).groups()
         matches = re.search( matchStr, expression ).groups()
         replStr = matches[0]+'*'+matches[1]
         expression = re.sub( matchStr, replStr, expression, count = 1 )
         continue

      break

  

   parenDepth = 0
   subStr = ''

   for idx,val in enumerate( expression ):

      if( val == '(' ):
         parenDepth += 1
      elif( val == ')' ):
         parenDepth -= 1

      if( parenDepth and 
         not ( val == '(' and parenDepth == 1 ) 
         ):
         subStr += val
      elif( len( subStr ) ):
         replStr = ParenEval( subStr )
         subStr = '('+subStr+')'
         if(_DEBUG): print "Replace: "+subStr + " => " + replStr
         expression = expression.replace( subStr, replStr, 1)
         subStr = ''

   return DieEvaluator( expression )

def DieEvaluator( diceExpression ):   
   def funcRoll( matchobj ):
      n=int( matchobj.group( 1 ) )
      s=int( matchobj.group( 2 ) )
      retval = 0
      if(_DEBUG): print " Rolling..."
      for i in range(n):
         tmp = random.randint(1,s)
         if(_DEBUG): print "  %d"%(tmp)
         retval += tmp
      return str(retval)

   if(_DEBUG): print "\nBegin eval"
   while True:
      if(_DEBUG): 
         print "\nLoop on:",diceExpression
         time.sleep(1)


      # Remove parenthesis with only numbers inside of them
      matchStr = "\(\d+\)"
      if( re.search( matchStr, diceExpression ) ):
         if(_DEBUG): print " Peren:",re.search( matchStr, diceExpression ).group(0)
         replStr = eval( re.search( matchStr, diceExpression ).group(0) )
         replStr = str( replStr )
         diceExpression = re.sub( matchStr, replStr, diceExpression, count=1 )
         continue

      # Evaluate correct dice stings
      matchStr = "(\d+)d(\d+)"
      if( re.search( matchStr, diceExpression ) ):
         if(_DEBUG): print " Dice:",re.search( matchStr, diceExpression ).group(0)
         diceExpression = re.sub( matchStr, funcRoll, diceExpression, count=1 )
         continue

      # Exponents
      matchStr = "\d+\^\d+"
      if( re.search( matchStr, diceExpression ) ):
         if(_DEBUG): print " Exponent:",re.search( matchStr, diceExpression ).group(0)
         replStr = re.sub( "\^", "**", re.search( matchStr, diceExpression ).group(0) )
         replStr = eval( replStr )
         replStr = str( replStr )
         diceExpression = re.sub( matchStr, replStr, diceExpression, count=1 )
         continue 

      # Multiplication
      matchStr = "\d+[*]\d+"
      if( re.search( matchStr, diceExpression ) ):
         if(_DEBUG): print " Multi:",re.search( matchStr, diceExpression ).group(0)
         replStr = eval( re.search( matchStr, diceExpression ).group(0) )
         # replStr = eval( replStr ) 
         replStr = str( replStr )
         diceExpression = re.sub( matchStr, replStr, diceExpression, count=1 )
         continue      

      # Dor-vision
      matchStr = "\d+\/\d+"
      if( re.search( matchStr, diceExpression ) ):
         if(_DEBUG): print " Divide:",re.search( matchStr, diceExpression ).group(0)
         replStr = eval( re.search( matchStr, diceExpression ).group(0) )
         replStr = str( replStr )
         diceExpression = re.sub( matchStr, replStr, diceExpression, count=1 )
         continue      

      # Addition
      matchStr = "\d+\+\d+"
      if( re.search( matchStr, diceExpression ) ):
         if(_DEBUG): print " Add:",re.search( matchStr, diceExpression ).group(0)
         replStr = eval( re.search( matchStr, diceExpression ).group(0) )
         replStr = str( replStr )
         diceExpression = re.sub( matchStr, replStr, diceExpression, count=1 )
         continue    

      # Surb-Traction
      matchStr = "\d+\-\d+"
      if( re.search( matchStr, diceExpression ) ):
         if(_DEBUG): print " Sub:",re.search( matchStr, diceExpression ).group(0)
         replStr = eval( re.search( matchStr, diceExpression ).group(0) )
         replStr = str( replStr )
         diceExpression = re.sub( matchStr, replStr, diceExpression, count=1 )
         continue

      # Logical Results
      matchStr = "^(?:-|\+)?\d+(<|<=|>|>=|==)(?:-|\+)?\d+$"
      if( re.search( matchStr, diceExpression ) ):
         if(_DEBUG): print " Logic:",re.search( matchStr, diceExpression ).group(0)
         print " Logical Compareson:",diceExpression
         replStr = eval( re.search( matchStr, diceExpression ).group(0) )
         replStr = str( replStr )
         diceExpression = re.sub( matchStr, replStr, diceExpression, count=1 )
         # No continue here, we are DONE. This can only be run when the diceExpression is 
         #  out of new things for us to test!

      # We only get here when we have nothing left to parse!
      break

   if(_DEBUG): print "\nReturn:", diceExpression
   return diceExpression

def PromptDice():
   old_tmp = '1d20'
   print "?: help"
   print "q: quit"
   while True:
      tmp = raw_input("\n>")

      if( tmp in ['q','Q','quit','exit'] ):
         break
      if( tmp in ['h','H','-?','?'] ):
         print "Enter any valid dice expression to evaluate it."
         print "  Extra text is ignored, math is evaluated. Note that all dice"
         print "  expressions are evaluated before any math."
         print "Enter blank string to repeat last entry."
         print "Enter 'q' to quit."
         continue
         
      if( len( tmp ) == 0 ):
         print "r>"+old_tmp
         tmp = old_tmp
      old_tmp = tmp
      # print DieEvaluator( tmp )
      print ParenEval( tmp )

if __name__ == '__main__':

   parser = optparse.OptionParser()

   parser.add_option( 
      '-d',
      '--debug', 
      action = "store_true", 
      help = "Activate debug statements",
      dest = "DEBUG", 
      default = False 
      )

   (options, args) =  parser.parse_args()
   _DEBUG = options.DEBUG

   PromptDice()

