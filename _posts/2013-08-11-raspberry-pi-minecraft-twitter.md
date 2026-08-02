---
title: 'Raspberry Pi - Minecraft Twitter'
date: 2013-08-11 22:27:00 +01:00
tags: [minecraft, python, raspberry-pi, social-networking]
redirect_from:
  - /2013/08/raspberry-pi-minecraft-twitter.html
---

![](/assets/img/2013/08/minecraft-twitter.jpg)I was at [Young Rewired State](https://www.google.co.uk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&ved=0CDIQFjAA&url=https%3A%2F%2Fyoungrewiredstate.org%2F&ei=XfcHUu6qEsiZO--1gbAL&usg=AFQjCNHoJLwzZk0KO_jYyO6jOop_QWJNgg&sig2=EhRWyPUlgc47gcCn5f3W7Q&bvm=bv.50500085,d.ZWU)'s (YRS) festival of code this weekend, mentoring a group of young coders from BBC Birmingham, when I saw a tweet from [Raspberry Pi](http://raspberrypi.org/) about it being Minecraft day on Monday, so I thought, I'm surrounded by coders, we have a weekend ahead of us, we must be able to create something...

We came up with Twitter for Minecraft, a python script which connects to a live user stream on twitter and waits for tweets to arrive, when they do, the text is rendered into blocks using a simple typeface we created in which each letter is a 3x5 collection of blocks.

{% include youtube.html id="kW74GQtdUeg" %}

This is the team I was mentoring at YRS, a particular mention needs to go to Steve, who gave his time to help me create the typeface and learn about how to code in Minecraft.

![](/assets/img/2013/08/20130811_114316.jpg)

**Install**

***Create a twitter app***
 You need to create a twitter app using your twitter id, you can do this by visiting [dev.twitter.com](http://dev.twitter.com/), signing on, and clicking create app; if you are having problems see a previous blog post of mine, [automatically posting updates to twitter](/posts/automatically-posting-updates-to/), which has some in-depth instructions.

***Install python oauth & pycurl***
 We need a couple of python modules to get the twitter feed working. If you have never installed python modules before you are going to need to install the python setup tools module, distribute, see blog post, [python - installing modules](/posts/raspberry-pi-python-installing-modules/), for info on how to do this.

```bash
sudo apt-get install git-core
git clone https://github.com/leah/python-oauth.git
cd python-oauth
sudo python setup.py install
sudo apt-get install python-pycurl
```

***Download code***

```bash
cd ~
git clone https://github.com/martinohanlon/minecraft-twitter.git
cd minecraft-twitter
```

***Update twitter keys***
 You will need to get the twitter keys you were given when you created your twitter app and put them into minecraft-twitter.py. Open minecraft-twitter.py and scroll down till you find:

```text
# twitter oauth keys, get yours from dev.twitter.com
CONSUMER_KEY = '#############'
CONSUMER_SECRET = '###############'
ACCESS_TOKEN = '###############
ACCESS_TOKEN_SECRET = '###############'
```

And replace the hashes with your access keys.

***Run***
 Start up minecraft

```bash
python minecraft-twitter.py
```

**Code**
 Its a bit hacky (as you might expect from a hack weekend), but I've include it for reference below. If you want to get it running though I would suggest you download it from github using the instructions above.

```python
#www.stuffaboutcode.com
#Raspberry Pi, Minecraft Twitter

#import the minecraft.py module from the minecraft directory
import minecraft.minecraft as minecraft
#import minecraft block module
import minecraft.block as block
#import time, so delays can be used
import time
#import oauth for twitter security
from oauth.oauth import OAuthRequest, OAuthSignatureMethod_HMAC_SHA1
from hashlib import md5
#required by twitter stream class
import json, random, math, urllib, urllib2, pycurl

#Letters used in the program, hashes are turned into blocks
letters = {"a":
"###" + "\n" +
"# #" + "\n" +
"###" + "\n" +
"# #" + "\n" +
"# #" + "\n",
"b":
"###" + "\n" +
"# #" + "\n" +
"###" + "\n" +
"# #" + "\n" +
"###" + "\n",
"c":
"###" + "\n" +
"#" + "\n" +
"#" + "\n" +
"#" + "\n" +
"###" + "\n",
"d":
"##" + "\n" +
"# #" + "\n" +
"# #" + "\n" +
"# #" + "\n" +
"##" + "\n",
"e":
"###" + "\n" +
"#" + "\n" +
"###" + "\n" +
"#" + "\n" +
"###" + "\n",
"f":
"###" + "\n" +
"#" + "\n" +
"###" + "\n" +
"#" + "\n" +
"#" + "\n",
"g":
"###" + "\n" +
"# #" + "\n" +
"###" + "\n" +
"  #" + "\n" +
"###" + "\n",
"h":
"# #" + "\n" +
"# #" + "\n" +
"###" + "\n" +
"# #" + "\n" +
"# #" + "\n",
"i":
"###" + "\n" +
" #" + "\n" +
" #" + "\n" +
" #" + "\n" +
"###" + "\n",
"j":
"###" + "\n" +
" #" + "\n" +
" #" + "\n" +
" #" + "\n" +
"##" + "\n",
"k":
"# #" + "\n" +
"##" + "\n" +
"#" + "\n" +
"##" + "\n" +
"# #" + "\n",
"l":
"#" + "\n" +
"#" + "\n" +
"#" + "\n" +
"#" + "\n" +
"###" + "\n",
"m":
"# #" + "\n" +
"###" + "\n" +
"###" + "\n" +
"# #" + "\n" +
"# #" + "\n",
"n":
"###" + "\n" +
"# #" + "\n" +
"# #" + "\n" +
"# #" + "\n" +
"# #" + "\n",
"o":
"###" + "\n" +
"# #" + "\n" +
"# #" + "\n" +
"# #" + "\n" +
"###" + "\n",
"p":
"###" + "\n" +
"# #" + "\n" +
"###" + "\n" +
"#" + "\n" +
"#" + "\n",
"q":
"###" + "\n" +
"# #" + "\n" +
"###" + "\n" +
"  #" + "\n" +
"  #" + "\n",
"r":
"###" + "\n" +
"# #" + "\n" +
"##" + "\n" +
"# #" + "\n" +
"# #" + "\n",
"s":
"###" + "\n" +
"#" + "\n" +
"###" + "\n" +
"  #" + "\n" +
"###" + "\n",
"t":
"###" + "\n" +
" #" + "\n" +
" #" + "\n" +
" #" + "\n" +
" #" + "\n",
"u":
"# #" + "\n" +
"# #" + "\n" +
"# #" + "\n" +
"# #" + "\n" +
"###" + "\n",
"v":
"# #" + "\n" +
"# #" + "\n" +
"# #" + "\n" +
"# #" + "\n" +
" #" + "\n",
"w":
"# #" + "\n" +
"# #" + "\n" +
"# #" + "\n" +
"###" + "\n" +
"###" + "\n",
"x":
"# #" + "\n" +
" #" + "\n" +
" #" + "\n" +
" #" + "\n" +
"# #" + "\n",
"y":
"# #" + "\n" +
"# #" + "\n" +
"###" + "\n" +
"  #" + "\n" +
"###" + "\n",
"z":
"###" + "\n" +
"  #" + "\n" +
" #" + "\n" +
"#" + "\n" +
"###" + "\n",
" ":
" ",
"1":
" #" + "\n" +
"##" + "\n" +
" #" + "\n" +
" #" + "\n" +
"###" + "\n",
"2":
"###" + "\n" +
"  #" + "\n" +
"###" + "\n" +
"#" + "\n" +
"###" + "\n",
"3":
"###" + "\n" +
"  #" + "\n" +
"###" + "\n" +
"  #" + "\n" +
"###" + "\n",
"4":
"#" + "\n" +
"#" + "\n" +
"# #" + "\n" +
"###" + "\n" +
"  #" + "\n",
"5":
"###" + "\n" +
"#" + "\n" +
"###" + "\n" +
"  #" + "\n" +
"###" + "\n",
"6":
"###" + "\n" +
"#" + "\n" +
"###" + "\n" +
"# #" + "\n" +
"###" + "\n",
"7":
"###" + "\n" +
"  # " + "\n" +
" #" + "\n" +
" #" + "\n" +
"#" + "\n",
"8":
"###" + "\n" +
"# #" + "\n" +
"###" + "\n" +
"# #" + "\n" +
"###" + "\n",
"9":
"###" + "\n" +
"# #" + "\n" +
"###" + "\n" +
"  #" + "\n" +
"###" + "\n",
"0":
"###" + "\n" +
"# #" + "\n" +
"# #" + "\n" +
"# #" + "\n" +
"###" + "\n",
"!":
" # " + "\n" +
" # " + "\n" +
" # " + "\n" +
"   " + "\n" +
" # " + "\n",
"?":
"###" + "\n" +
"  #" + "\n" +
" ##" + "\n" +
"   " + "\n" +
" # " + "\n",
".":
"   " + "\n" +
"   " + "\n" +
"   " + "\n" +
"   " + "\n" +
" # " + "\n",
",":
"   " + "\n" +
"   " + "\n" +
"   " + "\n" +
"  #" + "\n" +
" # " + "\n",
"/":
"  #" + "\n" +
"  #" + "\n" +
" # " + "\n" +
"# " + "\n" +
"# " + "\n",
":":
"   " + "\n" +
" # " + "\n" +
"   " + "\n" +
" # " + "\n" +
"   " + "\n",
"@":
"###" + "\n" +
"# #" + "\n" +
"## " + "\n" +
"#  " + "\n" +
"###" + "\n",
"'":
" # " + "\n" +
" # " + "\n" +
"   " + "\n" +
"   " + "\n" +
"   " + "\n",
"#":
" # " + "\n" +
"###" + "\n" +
" # " + "\n" +
"###" + "\n" +
" # " + "\n"
}

# twitter oauth keys, get yours from dev.twitter.com
CONSUMER_KEY = '#############'
CONSUMER_SECRET = '###############'
ACCESS_TOKEN = '###############
ACCESS_TOKEN_SECRET = '###############'

# constants to position the text lines in minecraft
LETTERBLOCKID = block.COBBLESTONE.id
LETTERBLOCKDATA = 0
#These are the lines where the tweets will be written
TEXTLINES = {0:[[minecraft.Vec3(-95, 55, -95), minecraft.Vec3(+95, 55, -95)],
                [minecraft.Vec3(+95, 55, -95), minecraft.Vec3(+95, 55, +95)],
                [minecraft.Vec3(+95, 55, +95), minecraft.Vec3(-95, 55, +95)],
                [minecraft.Vec3(-95, 55, +95), minecraft.Vec3(-95, 55, -95)]],
             1:[[minecraft.Vec3(-95, 47, -95), minecraft.Vec3(+95, 47, -95)],
                [minecraft.Vec3(+95, 47, -95), minecraft.Vec3(+95, 47, +95)],
                [minecraft.Vec3(+95, 47, +95), minecraft.Vec3(-95, 47, +95)],
               [minecraft.Vec3(-95, 47, +95), minecraft.Vec3(-95, 47, -95)]],
             2:[[minecraft.Vec3(-95, 39, -95), minecraft.Vec3(+95, 39, -95)],
                [minecraft.Vec3(+95, 39, -95), minecraft.Vec3(+95, 39, +95)],
                [minecraft.Vec3(+95, 39, +95), minecraft.Vec3(-95, 39, +95)],
                [minecraft.Vec3(-95, 39, +95), minecraft.Vec3(-95, 39, -95)]]
             }
LINEHEIGHT = 5
LETTERWIDTH = 3

#Class for creating text in minecraft
class MinecraftText:
    def __init__(self, mc):
        self.mc = mc
        self.currentLine = 0
        self.currentTopLeft = LINETOPLEFTS[self.currentLine]

    #writes a line to minecraft at the next position
    def writeNextLine(self, line):
        #Output message
        self.clearLine(self.currentLine)
        self.writeLineToMC(line, self.currentLine)
        self.currentLine+=1
        #if I have reached the top line, reset it
        if self.currentLine == 4: self.currentLine = 0

    #writes a line of text into minecraft
    def writeLineToMC(self, line, lineNumber):
        #get the textlines
        textlines = TEXTLINES[lineNumber]
        #current testline
        currentTextLine = 0
        #set the cursor position
        currentCursor = minecraft.Vec3(textlines[currentTextLine][0].x,
                                       textlines[currentTextLine][0].y,
                                       textlines[currentTextLine][0].z)
        #setup x and z directions
        xDirection, zDirection = 1, 0
        nextTextLine = False
        #make line lower case
        line = line.lower()
        #write the line to minecraft
        for character in line:
            #create the character in minecraft
            self.writeLetterToMC(character, currentCursor, xDirection, zDirection)
            #move the 'cursor' on
            # check if the current cursor pos is outside the textLine,
            # if so move to the next text line
            if currentTextLine == 0:
                currentCursor.x = currentCursor.x + LETTERWIDTH + 1
                if currentCursor.x > textlines[currentTextLine][1].x: nextTextLine = True
            if currentTextLine == 1:
                currentCursor.z = currentCursor.z + LETTERWIDTH + 14
                if currentCursor.z > textlines[currentTextLine][1].z:
                    nextTextLine = True
            if currentTextLine == 2:
                currentCursor.x = currentCursor.x - LETTERWIDTH + 14
                if currentCursor.x < textlines[currentTextLine][1].x: nextTextLine = True
            if currentTextLine == 3:
                currentCursor.z = currentCursor.z - LETTERWIDTH + 14
                #if currentCursor.z < textlines[currentTextLine][1].z: nextTextLine = True
            if nextTextLine == True:
                nextTextLine = False
                #next testline
                currentTextLine+=1
                #set the cursor position
                currentCursor = minecraft.Vec3(textlines[currentTextLine][0].x,
                                               textlines[currentTextLine][0].y,
                                               textlines[currentTextLine][0].z)
                #setup x and z diections
                if currentTextLine == 1: xDirection, zDirection = 0, 1
                if currentTextLine == 2: xDirection, zDirection = -1, 0
                if currentTextLine == 3: xDirection, zDirection = 0, -1

    #create a letter in minecraft
    def writeLetterToMC(self, character, cursorTopLeft, xDirection, zDirection):
        # the current position is where we have reached in creating the letter
        currentPos = minecraft.Vec3(cursorTopLeft.x, cursorTopLeft.y, cursorTopLeft.z)

        # is the character in my letter list?
        if (character in letters.keys()):
            # get the hashes for the character
            letterString = letters[character]
            #loop through all the hashes, creating block
            for digit in letterString:
                if digit == "#":
                    #print "create block x = " + str(currentPos.x) + " y = " + str(currentPos.y)
                    self.mc.setBlock(currentPos.x, currentPos.y, currentPos.z, LETTERBLOCKID, LETTERBLOCKDATA)
                    currentPos.x = currentPos.x + xDirection
                    currentPos.z = currentPos.z + zDirection
                if digit == " ":
                    self.mc.setBlock(currentPos.x, currentPos.y, currentPos.z, block.AIR.id)
                    currentPos.x = currentPos.x + xDirection
                    currentPos.z = currentPos.z + zDirection
                if digit == "\n":
                    currentPos.y = currentPos.y - 1
                    currentPos.x = cursorTopLeft.x
                    currentPos.z = cursorTopLeft.z

    #clears a line of text in minecraft
    def clearLine(self, lineNumber):
        for textline in TEXTLINES[lineNumber]:
            self.mc.setBlocks(textline[0].x,
                              textline[0].y,
                              textline[0].z,
                              textline[1].x,
                              textline[1].y - LINEHEIGHT,
                              textline[1].z,
                              block.AIR.id)

# class for managing oauth tokens
class Token(object):
    def __init__(self,key,secret):
        self.key = key
        self.secret = secret

    def _generate_nonce(self):
        random_number = ''.join(str(random.randint(0, 9)) for i in range(40))
        m = md5(str(time.time()) + str(random_number))
        return m.hexdigest()

# twitter client
class MinecraftTwitterStreamClient:
    def __init__(self, streamURL):
        #Connect to minecraft by creating the minecraft object
        # - minecraft needs to be running and in a game
        self.mc = minecraft.Minecraft.create()
        #Post a message to the minecraft chat window
        self.mc.postToChat("Minecraft twitter stream active")
        #create my minecraft text screen object
        self.mcText = MinecraftText(self.mc)
        #setup connection to twitter stream
        self.streamURL = streamURL
        self.buffer = ""
        self.conn = pycurl.Curl()
        self.conn.setopt(pycurl.URL, self.streamURL)
        self.conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)
        self.conn.perform()

    #this method is called each time some data arrives on the stream
    def on_receive(self, data):
        # debug - to see when this is called sys.stdout.write(".")
        self.buffer += data
        if data.endswith("\n") and self.buffer.strip():
            content = json.loads(self.buffer)
            self.buffer = ""
            #debug - output json from buffer print content

            #friends data - store for later
            if "friends" in content:
                self.friends = content["friends"]

            #text (tweet) arrives
            if "text" in content:
                print u"{0[user][name]}: {0[text]}".format(content).encode('utf-8')
                tweet = u"{0[user][name]}: {0[text]}".format(content).encode('utf-8')
                self.mcText.writeNextLine(tweet)

# get the url needed to open the twitter user stream, including signature after authentication
def getTwitterUserStreamURL():
    STREAM_URL = "https://userstream.twitter.com/2/user.json"

    access_token = Token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    consumer = Token(CONSUMER_KEY,CONSUMER_SECRET)

    parameters = {
        'oauth_consumer_key': CONSUMER_KEY,
        'oauth_token': access_token.key,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': str(int(time.time())),
        'oauth_nonce': access_token._generate_nonce(),
        'oauth_version': '1.0',
    }

    oauth_request = OAuthRequest.from_token_and_callback(access_token,
                    http_url=STREAM_URL,
                    parameters=parameters)
    signature_method = OAuthSignatureMethod_HMAC_SHA1()
    signature = signature_method.build_signature(oauth_request, consumer, access_token)

    parameters['oauth_signature'] = signature
    data = urllib.urlencode(parameters)
    return "%s?%s" % (STREAM_URL,data)

if __name__ == "__main__":

    #Create minecraft twitter
    mcTwitter = MinecraftTwitterStreamClient(getTwitterUserStreamURL())
```
