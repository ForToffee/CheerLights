import urllib2
import json
import time
import ws2812, atexit

lastID = 0      #most recent entry_id
refresh = 15    #refresh time in secs
urlRoot = "http://api.thingspeak.com/channels/1417/"
pixels = []    #list of pixels and their colours
maxPixels = 64

namesToRGB = {'red': [0xFF, 0, 0],
                'green': [0, 0x80, 0],
                'blue': [0, 0, 0xFF],
                'cyan': [0, 0xFF, 0xFF],
                'white': [0xFF, 0xFF, 0xFF],
                'warmwhite': [0xFD, 0xF5, 0xE6],
                'purple': [0x80, 0, 0x80],
                'magenta': [0xFF, 0, 0xFF],
                'yellow': [0xFF, 0xFF, 0],
                'orange': [0xFF, 0xA5, 0],
                'pink': [0xFF, 0xC0, 0xCB],
                'oldlace': [0xFD, 0xF5, 0xE6]}


#borrowed from https://github.com/pimoroni/UnicornHat/blob/master/python/UnicornHat/unicornhat.py
#c/o Gadgetoid
def clean_shutdown():
  '''
  Registered at exit to ensure ws2812 cleans up after itself
  and all pixels are turned off.
  '''
  off()
  ws2812.terminate(0)

atexit.register(clean_shutdown)

#retrieve and load the JSON data into a JSON object
def getJSON(url):
    jsonFeed = urllib2.urlopen(urlRoot + url)
    feedData = jsonFeed.read()
    #print feedData
    jsonFeed.close()

    data = json.loads(feedData)
    return data

#use the JSON object to identify the colour in use,
#update the last entry_id processed
def parseColour(feedItem):
    global lastID
    #print feed["created_at"], feed["field1"]
    for name in namesToRGB.keys():
        if feedItem["field1"] == name:
            pixels.insert(0, namesToRGB(name)    #add the colour to the head
    lastID = getEntryID(feed)

#read the last entry_id
def getEntryID(feedItem):
    return int(feedItem["entry_id"])

#refresh the displayed pixels
def showColours():
    index = 0
    for pixel in pixels:
        ws2812.setPixelColor(index, pixel[0], pixel[1], pixel[2])
        index += 1
        if index >= maxPixels:
            pixels = pixels[maxPixels-1]    #trim the list as we've maxed out
    ws2812.show()
                  
#main program
ws2812.init(maxPixels)

#process the currently available list of colours
data = getJSON("feed.json")
for feedItem in data["feeds"]:
    parseColour(feedItem)
showColours()

#check for new colour requests
while True:
    data = getJSON("field/1/last.json")
    
    if getEntryID(data) > lastID:   #Has this entry_id been processed before?
        parseColour(data)
        showColours()
    time.sleep(refresh)

