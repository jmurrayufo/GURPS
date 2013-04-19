import json
from collections import OrderedDict

print "Name of file"
fileName = raw_input( ">" ) + '.json'
with open( fileName ,'w' ) as fp:
    jsonDict = OrderedDict()

    print "\nEnter TL"
    jsonDict['TL'] = input('>')

    print "\nEnter Gun Name"
    jsonDict['Name'] = raw_input('>')

    print "\n**Damage subsection**"
    jsonDict['Damage'] = OrderedDict()

    print "\nEnter base Damage"
    jsonDict['Damage']['Base'] = raw_input('>')

    print "\nEnter armor divisor"
    jsonDict['Damage']['Divisor'] = raw_input('>')

    print "\nEnter damage type"
    jsonDict['Damage']['Type'] = raw_input('>')

    print "\nEnter Acc"
    jsonDict['Acc'] = input('>')

    print "\n**Range subsection**"
    jsonDict['Range'] = OrderedDict()

    print "\nEnter minimum range"
    jsonDict['Range']['Min'] = input('>')

    print "\nEnter maximum range"
    jsonDict['Range']['Max'] = input('>')

    print "\n**Weight subsection**"
    jsonDict['Weight'] = OrderedDict()

    print "\nEnter base weight"
    jsonDict['Weight']['Base'] = input('>')

    print "\nEnter maximum range"
    jsonDict['Weight']['Misc'] = raw_input('>')

    print "\nEnter rate of fire"
    jsonDict['RoF'] = input('>')

    print "\n**Shots subsection**"
    jsonDict['Shots'] = OrderedDict()

    print "\nEnter base shots"
    jsonDict['Shots']['Base'] = input('>')

    print "\nEnter reload number"
    jsonDict['Shots']['Reload'] = input('>')

    print "\nEnter ST"
    jsonDict['ST'] = input('>')

    print "\nEnter Bulk"
    jsonDict['Bulk'] = input('>')

    print "\nEnter Recoil"
    jsonDict['Rcl'] = input('>')

    print "\nEnter Cost"
    jsonDict['Cost'] = input('>')

    print "\nEnter LC"
    jsonDict['LC'] = input('>')

    print "\nEnter Notes"
    jsonDict['Notes'] = raw_input('>')






    json.dump( jsonDict, fp, indent=3 )

