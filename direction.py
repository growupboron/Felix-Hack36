import urllib
import json
import requests
from gtts import *
import os
import geocoder
from Code import dest


#to tun python3 direction.py

# Your Bing Maps Key 
bingMapsKey = "AoD12M8p7T6itLwPExdTce4zsvll79X-vaqL3fp50CSOZAmgWVjpfKh9FDwWLoLx" 

g = geocoder.ip('me')
gps = g.latlng
# input information
# start location

print(gps[0])
print(gps[1])
longitude = gps[1]
latitude = gps[0]
#latitude = gps[0]
#longitude = gps[1]
# end location
#destination = "1427 Alderbrook Ln San Jose CA 95129"
destination =  dest
encodedDest = urllib.parse.quote(destination, safe='')

routeUrl = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + str(latitude) + "," + str(longitude) + "&wp.1=" + encodedDest + "&key=" + bingMapsKey
print(routeUrl)
request = urllib.request.Request(routeUrl)
response = urllib.request.urlopen(request)

r = response.read().decode(encoding="utf-8")
result = json.loads(r)
itineraryItems = result["resourceSets"][0]["resources"][0]["routeLegs"][0]["itineraryItems"]
f=open("dir.txt","w+")
for item in itineraryItems:
    dir = item["instruction"]["text"]
    #print(dir)
    f.write(dir+"\r")
    
#os.system("python3 speech_dir.py")
