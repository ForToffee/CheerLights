import urllib2
import json
import time

global lastID
lastID = 0
refresh = 15    #refresh time in secs
urlRoot = "http://api.thingspeak.com/channels/1417/"

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
def parseColour(feed):
    global lastID
    print feed["created_at"], feed["field1"]
    lastID = getEntryID(feed)

#read the last entry_id
def getEntryID(feed):
    return int(feed["entry_id"])

#main program

#process the currently available list of colours
data = getJSON("feed.json")
for feed in data["feeds"]:
    parseColour(feed)

#check for new colour requests
while True:
    data = getJSON("field/1/last.json")
    
    if getEntryID(data) > lastID:   #Have processed this entry_id before?
        parseColour(data)
    time.sleep(refresh)
