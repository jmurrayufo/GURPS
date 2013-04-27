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

   with open("data/gameref/skills.csv",'r') as fp:
       skillreader = csv.reader( fp, delimiter=',')
       # Gobble header
       header = skillreader.next()
       for idx,val in enumerate( skillreader ):
           if( len( val ) == 5):
               john.AddSkillCSV( val )
           else:
               pass

   print john


   john.Main()
