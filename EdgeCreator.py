# Creates edges between galaxies where a space ship could travel between
# Outputs the graph data into CUDA code

import csv
import math

MAXIMUM_DISTANCE = 1 # The maximum number of light years a spaceship can travel before needing a refuel
DEBUG = True # This will print more verbose. IT WILL NOT OUTPUT VALID CUDA CODE WHEN THIS IS TRUE. USE ONLY WHEN DEBUGGING

# Get the X, Y, Z cordinates of a galaxy
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

# Counts the number of edges with the given start node
# This is used for outputting the length in cuda
def getStartCount(edges, start):
    count = 0
    for edge in edges:
        if edge['start'] == start:
            count += 1
    return count


# Read in galaxy data
galaxies = []
with open('GalaxiesWithDistancesAndNumbers.csv', 'r') as file:
    reader = csv.reader(file)
    first = True
    for row in reader:
        if first:
            first = False
            continue
        galaxies.append({'Name': row[0], 'RA': row[1], "DEC": row[2], "LY": row[3]})


# Calculate edges
edges = []
for startGalIndex in range(len(galaxies)):
    for endGalIndex in range(len(galaxies)):
        if startGalIndex != endGalIndex and calcDistance(galaxies[startGalIndex], galaxies[endGalIndex]) < MAXIMUM_DISTANCE:
            edge = {'start':"{0:0=2d}".format(startGalIndex), 'end':"{0:0=2d}".format(endGalIndex)}
            edges.append(edge)

# Output
if DEBUG:
    print ("********** \n EDGES \n******* \n ")
    for edge in edges:
        print (edge)

# Print graph in CUDA code
print ("Node node[", len(galaxies), "];")

if DEBUG:
    print ("********** \n START AND LENGTH CU OUTPUT \n******* \n ")

completedStart = []
for i in range(len(edges)):
    if edges[i]['start'] not in completedStart:
        completedStart.append(edges[i]['start'])
        startS = "node[" + str(edges[i]['start']) + "].start = " + str(i) + ";"
        print (startS)
        lengthS = "node[" + str(edges[i]['start']) + "].length = " + str(getStartCount(edges, edges[i]['start'])) + ";"
        print (lengthS)

if DEBUG:
    print ("********** \n Galaxy names \n******* \n ")

for i in range(len(galaxies)):
    nameS = "node[" + str(i) + "].name = '" + galaxies[i]['Name'].replace("'", "") + "';"
    print (nameS)
    id0 = str( (int)((i - (i%10))/10))
    id1 = str(i % 10)
    idS = "node[" + str(i) + "].id[0] = '" + id0 + "'; node[" + str(i) + "].id[1] = '" + id1 + "';"
    print (idS)


if DEBUG:
    print ("********** \n EDGES CU OUTPUT \n******* \n ")

print ("int edges[", len(edges), "];")

for i in range(len(edges)):
    edgeS = "edges[" + str(i) + "] = " + str(edges[i]['end']) + ";"
    print (edgeS)

for edge in edges:
    print(edge)
