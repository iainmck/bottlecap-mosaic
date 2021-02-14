import math
from scipy import misc
import matplotlib.pyplot as plt
import numpy as np
import urllib
import io

import util
import createColorMap as ccm
from Errors import *

from config import *

def makeCapMosaic(capsList, imagePath, capWidth, startingBinWidth=STARTING_BIN_WIDTH, backgroundHue=BACKGROUND_HUE, imagePathIsUrl=True):
    #startingBinWidth 0 to 255, 10 is good
    #backgroundHue is the shade of the background 0-255 black-white

    # open image
    if imagePathIsUrl is True:
        try:
            url = urllib.urlopen(imagePath)
        except: # url lib cant process path
            raise BadImageLinkError()

        fileInfo = url.info()
        print 'Image to be processed:'
        print fileInfo

        filetype = fileInfo['Content-Type']
        if "png" not in filetype and "jpeg" not in filetype:
            raise BadImageFiletypeError()

        filesize = int(fileInfo['Content-Length'])
        if filesize > MAX_FILESIZE:
            raise FilesizeError()

        f = io.BytesIO(url.read())
        targetImage = misc.imread(f)
    else:
        targetImage = misc.imread(imagePath)  # image from path

    plt.imshow(targetImage)
    plt.show()

    (height, width, rgb) = targetImage.shape
    print "Image Width: " + str(width) + "px"
    print "Image Height: " + str(height) + "px"

    if rgb != 3:
        raise BadImageError() # not valid rgb; image may have fourth dimension (alpha)

    CAPS_WIDE = capWidth  # CONTROL PARAMETER
    pixelRadius = width/(2.0*CAPS_WIDE + 1)
    CAPS_HIGH = int((height - 2.0*pixelRadius)/(math.sqrt(3)*pixelRadius) + 1)

    print "Caps Needed: " + str(CAPS_WIDE*CAPS_HIGH)

    # go through image and save image rgb for each circular region
    imagePoints = []
    imageColors = []

    for row in range(CAPS_HIGH):
        y = int(pixelRadius + row*math.sqrt(3)*pixelRadius)
        for col in range(CAPS_WIDE):
            x = int(pixelRadius * (row%2 + col*2 + 1))
            imagePoints.append((x,y))
            colorsInRegion = []

            for i in range(int(x-pixelRadius), int(x+pixelRadius)):
                for j in range(int(y-pixelRadius), int(y+pixelRadius)):
                    if util.distance2d((x,y),(i,j)) <= pixelRadius:
                        colorsInRegion.append(targetImage[j,i]) # j and i flipped for rows and columns
            imageColors.append(colorsInRegion)

    # take average of each circular region rgbs
    imageColorAvgs = []

    for colors in imageColors:
        avg = np.zeros(3)

        for color in colors:
            avg += color
        avg /= len(colors)
        avg = avg.astype("uint8")
        imageColorAvgs.append(tuple(avg))

    # draw ideal mosaic
    mosaic = np.ones((height, width, rgb), dtype="uint8")*backgroundHue  # 0-255 = black-white background

    for index, point in enumerate(imagePoints):
        (x,y) = point
        for i in range(int(x-pixelRadius), int(x+pixelRadius)):
            for j in range(int(y-pixelRadius), int(y+pixelRadius)):
                if util.distance2d((x, y), (i, j)) <= pixelRadius:
                    mosaic[j,i] = np.array(imageColorAvgs[index], dtype="uint8")

    # ideal mosaic
    plt.imshow(mosaic)
    plt.show()

    # make mosaic from bottle caps
    capMosaic = np.ones((height, width, rgb), dtype="uint8")*backgroundHue  # background
    colorMap = ccm.createColorMap(imageColorAvgs, capsList, imagePoints, startingBinWidth=startingBinWidth)

    for index, point in enumerate(colorMap["coords"]):
        (x,y) = point
        for i in range(int(x-pixelRadius), int(x+pixelRadius)):
            for j in range(int(y-pixelRadius), int(y+pixelRadius)):
                if util.distance2d((x, y), (i, j)) <= pixelRadius:
                    capMosaic[j,i] = np.array(colorMap["caps"][index], dtype="uint8")

    plt.imshow(capMosaic)
    plt.show()

    img_io = io.BytesIO()
    plt.imsave(img_io, capMosaic, format='png')
    img_io.seek(0)
    return img_io # file object containing png image output
