import math
import numpy as np
import util

MAX_VALUE = 255

def pickRandomMaxObject(numpyArray, maxValue, points):
    randPoints = np.random.choice(range(len(points)), size=len(points), replace=False)

    for i in randPoints:
        (r,g,b) = points[i]
        if numpyArray[r,g,b] == maxValue:
            return (r,g,b)
    print "No max value found!"
    return False


def calculateNumBins(binWidth):
    max = float(MAX_VALUE)
    return int(math.ceil(max/binWidth + 1/max))

def makeBins(binWidth, numBins, image):
    histogram = np.zeros((numBins, numBins, numBins))
    bins = [[[[] for i in range(numBins)] for j in range(numBins)] for k in range(numBins)]
    points = []

    for P in image:
        (r, g, b) = P
        rBin = int(math.floor(r / binWidth))
        gBin = int(math.floor(g / binWidth))
        bBin = int(math.floor(b / binWidth))

        histogram[rBin, gBin, bBin] += 1
        bins[rBin][gBin][bBin].append(P)
        if (rBin, gBin, bBin) not in points:
            points.append((rBin, gBin, bBin))

    return histogram, bins, points

def findClosest(point, points):
    # points =
    #   [ {
    #       cap_id: str
    #       amount: int
    #       color: [int, int, int]
    #   }, {..}, {..} ]
    closest = None
    minDistance = math.pow(MAX_VALUE,3) # longer than any possible distance
    indexOfClosest = -1
    for index, testPoint in enumerate(points):
        color = tuple(testPoint["color"])
        distance = util.distance3d(point, color)
        if distance < minDistance:
            minDistance = distance
            closest = color
            indexOfClosest = index
    return closest, indexOfClosest

# DOESNT WORK WITH TRANSPARENT IMAGES
def createColorMap(image, caps, coords, startingBinWidth=10):
    print "CAPS"
    print caps
    # image is a list of 3d rgb tuples representing pixels in an image ("image points")

    # caps represents available colors
    #   [ {
    #       cap_id: str
    #       amount: int
    #       color: [int, int, int]
    #   }, {..}, {..} ]

    # coords is a list of 2d tuples corresponding to the xy location of each point

    # startingBinWidth is ("random") parameter from 1-255 controlling cap matching;
    #   - ~10 is good, lower numbers reduce speed
    #   - change to see variability in output

    colorMap = {
        "image": [], # original image colors
        "caps": [], # selected caps to match image colors
        "coords": [], # coordinates of each color
        "capIDs": [] # id of selected caps for physical re-creation
    }
    binWidth = startingBinWidth

    while binWidth <= MAX_VALUE and len(image) > 1 and len(caps) > 0:
        numBins = calculateNumBins(binWidth)
        histogram, bins, points = makeBins(binWidth, numBins, image)
        # histogram = frequency of image points in each color bin
        # bins = image points in their respective bins [[[(221, 12, 310), ...], ], ]
        # points = list of image point coordinates [(1,2,4), (4,4,1), (3,4,1)...]

        maxFreq = histogram.max() # find the frequency of the most populated bin(s)

        while maxFreq > 1 and len(caps) > 0: # once the maxFreq is 1, we need to make bins wider (encompassing more points)
            (rMax, gMax, bMax) = pickRandomMaxObject(histogram, maxFreq, points) # randomly pick a bin that has the maxFreq

            bin = bins[rMax][gMax][bMax]
            randBin = np.random.choice(len(bin)) # randomly take image point in the bin
            imageColor = bin[randBin]
            del bins[rMax][gMax][bMax][randBin] # remove from bins array
            histogram[rMax, gMax, bMax] -= 1 # decrease frequency

            index = image.index(imageColor) # track the index of the selected image point
            colorMap["image"].append(imageColor) # put image point in output
            image.remove(imageColor)

            coord = coords[index] # put correspending coord in output
            colorMap["coords"].append(coord)
            coords.remove(coord)

            capColor, capIndex = findClosest(imageColor, caps) # put closest bottlecap in output
            colorMap["caps"].append(capColor)
            colorMap["capIDs"].append(caps[capIndex]["cap_id"])
            # caps array is a histogram so removal is different
            numCapsAvailable = caps[capIndex]["amount"]
            if numCapsAvailable == 1:
                del caps[capIndex]
            else:
                caps[capIndex]["amount"] = numCapsAvailable - 1

            maxFreq = histogram.max()

        binWidth += 1

    return colorMap


if __name__ == "__main__":
    # test case
    image = [(10, 10, 10), (50, 50, 50), (200, 200, 200), (241, 241, 241)]
    caps = [(0, 0, 0), (10, 10, 10), (100, 100, 100), (241, 241, 241)]
    coords = [(1,1), (2,1), (1,2), (2,2)]
    print createColorMap(image, caps, coords)
