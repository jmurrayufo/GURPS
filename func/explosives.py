import math

def weightREF2Dmg( weight = 0, REF = 1 ):
   # Back Calculate damageStr
   n = math.sqrt( (4*REF) * weight )
   if( n < 1 ):
      return "0"
   return "6dx%d"%( int( n ) )

def dmgREF2Weight( dmg = 0, REF = 1 ):
   """
   Take the given damage and REF, and give the pounds of explosive needed
   dmg: intiget multipuls of 6d
   REF: Relative Explosive factor as a float/int
   """

   return ( dmg * dmg )/( 4.0 * REF )

if __name__ == '__main__':
   print weightREF2Dmg( 20, 1.4 )
   print dmgREF2Weight( 1, 1 )