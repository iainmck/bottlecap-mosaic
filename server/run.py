import requests
import shutil

from caps import capsList
import main


#print capsList

totalCaps = sum(cap['amount'] for cap in capsList)
print "Caps Owned:", totalCaps

# run directly
print main.makeCapMosaic(capsList,
    #"https://s-media-cache-ak0.pinimg.com/originals/68/86/da/6886da9dd04a24959005f577e3940c06.png",
	"./target_images/audrey.jpg",
    capWidth=21, imagePathIsUrl=False)

# run through local flask app
#data = {
	#"image_url": "https://s-media-cache-ak0.pinimg.com/originals/68/86/da/6886da9dd04a24959005f577e3940c06.png",
	#"image_url": "./target_images/face.png",
	#"caps_wide": 25,
    #"starting_bin_width": 9,
#"caps_list": capsList
#}

#r = requests.post("http://127.0.0.1:5000/process", json=data)
#with open('img.png', 'wb') as out_file:
#    shutil.copyfileobj(r.raw, out_file)
#del r
