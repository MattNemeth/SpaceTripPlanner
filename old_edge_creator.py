# Creates edges between galaxies where a space ship could travel between

import csv
import math

MAXIMUM_DISTANCE = 1 # The maximum number of light years a spaceship can travel before needing a refuel
TEXT_OUTPUT = False

# Get the X, Y, Z cordinates of a galaxy
# TODO - calculate this once and save the value
def getCord(gal):
    theta = 15 * (int(gal['RA'].split(" ")[0]) + float(gal['RA'].split(" ")[1])/60)
    phi = int(gal['DEC'].split(" ")[0]) + int(gal['DEC'].split(" ")[1])/60
    x = float(gal['LY']) * math.cos(math.radians(theta)) * math.cos(math.radians(phi))
    y = float(gal['LY']) * math.sin(math.radians(theta)) * math.cos(math.radians(phi))
    z = float(gal['LY']) * math.sin(math.radians(phi))
    cord = (x, y, z)
    return cord


# Calculates the distance between 2 galaxies
def calcDistance(startGal, endGal):
    startCord = getCord(startGal)
    endCord = getCord(endGal)
    return math.sqrt(
        (startCord[0] - endCord[0]) ** 2 +
        (startCord[1] - startCord[1]) ** 2 +
        (startCord[2] - startCord[2]) ** 2
    )

# Cleans up galaxy name so it will work with DOT
def cleanName(name):
    replacements = [
        (".", ""),
        ("/", "_"),
        ("'", ""),
        ("=", "_"),
        ("-", ""),
        (" ", "_"),
        (" ", "_"),
        ("_", "")
    ]
    for repl in replacements:
        while repl[0] in name:
            name = name.replace(repl[0], repl[1])
    return name



# Prints a dictionary in a more readable format
def prettyPrint(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         prettyPrint(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

# Read in galaxy data
galaxies = {}
with open('GalaxiesWithDistancesAndNumbers.csv', 'r') as file:
    reader = csv.reader(file)
    firstRow = True
    for row in reader:
        if firstRow:
            firstRow = False
            continue
        galaxies[row[0]] = {'RA': row[1], "DEC": row[2], "LY": row[3]}

# Print Galaxies
print ("Galaxy data")
prettyPrint(galaxies)

# Calculate edges
edges = []
for startKey in galaxies:
    for endKey in galaxies:
        print (startKey, " TO ", endKey, calcDistance(galaxies[startKey], galaxies[endKey]))
        if calcDistance(galaxies[startKey], galaxies[endKey]) < MAXIMUM_DISTANCE and startKey != endKey:
            if TEXT_OUTPUT:
                s = '"' + startKey + '"' + " to " + '"' + endKey + '"'
            else:
                s = cleanName(startKey)+ " -- " + cleanName(endKey)
            edges.append(s)

print ("\n\n ********** \n EDGES \n******* \n ")
for edge in edges:
    print (edge)
