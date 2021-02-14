# color averages from https://www.photopea.com/

from config import BACKGROUND_HUE

capsDict = {
    "pink": {
        "color": (255, 203, 199),
        "amount": 17
    },
    "light red": {
        "color": (255, 112, 102),
        "amount": 24
    },
    "red": {
        "color": (230, 15, 0),
        "amount": 257
    },
    "maroon": {
        "color": (150, 10, 0),
        "amount": 33
    },
    "light orange": {
        "color": (255, 190, 69),
        "amount": 24
    },
    "orange": {
        "color": (242, 133, 0),
        "amount": 13
    },
    "yellow": {
        "color": (255, 247, 23),
        "amount": 5
    },
    "yellow orange": {
        "color": (212, 183, 19),
        "amount": 12
    },
    "green yellow": {
        "color": (217, 237, 0),
        "amount": 26
    },
    "light green": {
        "color": (157, 255, 0),
        "amount": 5
    },
    "green": {
        "color": (17, 207, 0),
        "amount": 70
    },
    "dark green": {
        "color": (8, 99, 0),
        "amount": 9
    },
    "turquoise (anchor)": {
        "color": (5, 126, 150),
        "amount": 24
    },
    "light blue": {
        "color": (31, 236, 240),
        "amount": 26
    },
    "teal (blue green)": {
        "color": (81, 196, 175),
        "amount": 10
    },
    "navy blue": {
        "color": (0, 80, 199),
        "amount": 106
    },
    "midnight blue": {
        "color": (0, 26, 92),
        "amount": 18
    },
    "purple": {
        "color": (58, 2, 224),
        "amount": 1
    },
    "white": {
        "color": (245, 245, 245),
        "amount": 145
    },
    "light silver": {
        "color": (222, 222, 222),
        "amount": 61
    },
    "silver": {
        "color": (189, 189, 189),
        "amount": 50
    },
    "dark silver": {
        "color": (125, 125, 125),
        "amount": 9
    },
    "black": {
        "color": (28, 28, 28),
        "amount": 77
    },
    "light gold": {
        "color": (224, 215, 128),
        "amount": 58
    },
    "dark gold": {
        "color": (168, 159, 71),
        "amount": 55
    },
    "bronze": {
        "color": (140, 118, 52),
        "amount": 61
    },
    "background": {
        "color": (BACKGROUND_HUE+10, BACKGROUND_HUE+10, BACKGROUND_HUE+10),
        "amount": 999
    }
}

capsList = []

for beer in capsDict.keys():
    capsList.append({
        "cap_id": beer,
        "amount": capsDict[beer]["amount"],
        "color": capsDict[beer]["color"]
    })