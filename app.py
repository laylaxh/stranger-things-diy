import code, string, time, random, re
from flask import Flask
from flask import request
from neopixel import *

"""
code.interact(local=dict(globals(), **locals()))
TODO:
  Scary While Loop
"""



app = Flask(__name__)

# Start random seed
random.seed()

# LED strip configuration
LED_COUNT      = 50      # Number of LED pixels
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!)
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Predefined colors
OFF            = Color(0,0,0)
WHITE          = Color(255,255,255)
RED            = Color(255,0,0)
GREEN          = Color(0,255,0)
BLUE           = Color(0,0,255)
PURPLE         = Color(128,0,128)
YELLOW         = Color(255,255,0)
ORANGE         = Color(255,50,0)
TURQUOISE      = Color(64,224,208)
RANDOM         = Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))

# Other vars
LIGHTSHIFT     = 0  # Shift the lights down the strand to the other end
FLICKERLOOP    = 3  # Number of loops to flicker
COLORS         = [YELLOW,GREEN,RED,BLUE,ORANGE,TURQUOISE,GREEN,
                  YELLOW,PURPLE,RED,GREEN,BLUE,YELLOW,RED,TURQUOISE,GREEN,RED,BLUE,GREEN,ORANGE,
                  YELLOW,GREEN,RED,BLUE,ORANGE,TURQUOISE,RED,BLUE,
                  ORANGE,RED,YELLOW,GREEN,PURPLE,BLUE,YELLOW,ORANGE,TURQUOISE,RED,GREEN,YELLOW,PURPLE,
                  YELLOW,GREEN,RED,BLUE,ORANGE,TURQUOISE,GREEN,BLUE,ORANGE]
                  
lines          = [list(range(33,50)),list(reversed(range(15,32))), list(range(0,14))] # NEW EDIT was 13
textID         = []  # Attempting to use unique text IDs to perform a while loop. Still in progress  

friendNumberMap = {
  '+13603493405': 'steve rocks',          # Steve
  '+18182697821': 'layla turn around',   # Layla
  '+13233636062': 'icu zach',             # Zach
  '+13233957777': 'brian do a handstand', # Brian
  '+18183954507': 'xxxander',             # Xander
  '+19734627230': 'dale is that u',       # Dale
  '+18598015371': 'luke i m ur father'    # Luke 
  }

@app.route("/")
def run():
  demogorgonMessage = getTwilioMessage()
  preMessageDisplay()
  responseChooser(demogorgonMessage)
  turnOffLights()
  return ""

def lightOneUp(sleepTime):
  strip.show()
  time.sleep(sleepTime)

def getTwilioMessage():
  global textID
  textID = request.args.getlist('SmsMessageSid')  # Updating most recent textID
  rawSms      = request.args.getlist('Body')
  sms         = rawSms[0].encode("utf-8").lower()
  modifiedSms = re.sub('[^a-zA-Z0-9\n\s]', '', sms)[0:30].split()
  return modifiedSms 

def preMessageDisplay():
  totalPixels  = range(strip.numPixels())

  # All LEDs turn on in one of the predefined COLORS
  for i in range(0,2):
    for i in totalPixels:
      strip.setPixelColor(i, COLORS[i])
    lightOneUp(.5)
  
    turnOffLights()
    time.sleep(.2)

def responseChooser(message):
  
  #print(request.args.getlist('DateSent').encode("utf-8"))
  
  if len(message) == 1 and message[0] == 'run':
    runEasterEgg()
  elif len(message) == 1 and message[0] == 'spooky':
    spookyScary(5)
  elif len(message) == 1 and message [0] == 'demogorgon':
    demoEasterEgg()
  elif len(message) == 1 and message[0] == 'line':
    rainbowOn(.05)
  elif len(message) == 1 and message [0] == 'rainbow':
    realRainbow()
  else:
    normalMessage(message)

  # For numbers we know
  friendNumber = request.args.getlist('From')[0].encode("utf-8")
  if friendNumber in friendNumberMap and random.randint(0,10) >= 10:
    displayMessage(friendNumberMap[friendNumber].split())


def normalMessage(message):
  displayMessage(message)


def displayMessage(message):
  for word in message:
    displayWord(word)
    time.sleep(.5)

def displayWord(word):
  # Look up address value for eachLetter key and display
  for eachLetter in word:
    result = mapLetterToLed(eachLetter, len(COLORS))
    position = result[0]
    color = result[1]
    strip.setPixelColor(position, color)
    lightOneUp(1)
    strip.setPixelColor(position, OFF)
    lightOneUp(.2)

def turnOffLights():
  for led in range(strip.numPixels()):
    strip.setPixelColor(led, OFF)
  strip.show()

def runEasterEgg():
  displayWord('ru')
  result = mapLetterToLed('n', len(COLORS))
  position = result[0]
  color = result[1]
  strip.setPixelColor(position, color)
  time.sleep(.5)
  lightOneUp(3)

  # White Flash, Red Remains
  for led in range(strip.numPixels()):
    if led == position:
      continue  # Skip Red
    else:
      strip.setPixelColor(led, WHITE)
  lightOneUp(.5)
  
  # Bleed Red loop
  counter = 1
  for led in range(strip.numPixels()):
    if strip.getPixelColor(led) == RED:
      strip.setPixelColor(led+1, RED)
      strip.setPixelColor(led-counter, RED)
      counter = counter + 2
    lightOneUp(.05)

  # Flash Red
  for i in range(20):
    for led in range(strip.numPixels()):
      if strip.getPixelColor(led) == RED:
        strip.setPixelColor(led, WHITE)
      else:
        strip.setPixelColor(led, RED)
    lightOneUp(.2)
  turnOffLights()
  
def mapLetterToLed(letter, colorLen):
  letterPosColor = {
  'a': (33+LIGHTSHIFT,  COLORS[0%colorLen]),
  'b': (35+LIGHTSHIFT,  COLORS[1%colorLen]),
  'c': (38+LIGHTSHIFT,  COLORS[2%colorLen]),
  'd': (40+LIGHTSHIFT,  COLORS[3%colorLen]),
  'e': (41+LIGHTSHIFT,  COLORS[4%colorLen]),
  'f': (43+LIGHTSHIFT,  COLORS[5%colorLen]),
  'g': (44+LIGHTSHIFT,  COLORS[6%colorLen]),
  'h': (46+LIGHTSHIFT,  COLORS[7%colorLen]),
  'i': (47+LIGHTSHIFT,  COLORS[8%colorLen]),
  'j': (49+LIGHTSHIFT,  COLORS[9%colorLen]),
  'k': (30+LIGHTSHIFT, COLORS[10%colorLen]),
  'l': (28+LIGHTSHIFT, COLORS[11%colorLen]),
  'm': (26+LIGHTSHIFT, COLORS[12%colorLen]),
  'n': (24+LIGHTSHIFT, RED),                # COLORS[13%colorLen]
  'o': (22+LIGHTSHIFT, COLORS[14%colorLen]),
  'p': (20+LIGHTSHIFT, COLORS[15%colorLen]),
  'q': (18+LIGHTSHIFT, COLORS[16%colorLen]),
  'r': (16+LIGHTSHIFT, TURQUOISE),          # COLORS[17%colorLen]
  's': (0+LIGHTSHIFT, COLORS[18%colorLen]),
  't': (2+LIGHTSHIFT, COLORS[19%colorLen]),
  'u': (4+LIGHTSHIFT, BLUE),                # COLORS[20%colorLen]
  'v': (6+LIGHTSHIFT, COLORS[21%colorLen]),
  'w': (8+LIGHTSHIFT, COLORS[22%colorLen]),
  'x': (9+LIGHTSHIFT, COLORS[23%colorLen]),
  'y': (11+LIGHTSHIFT, COLORS[24%colorLen]),
  'z': (13+LIGHTSHIFT, COLORS[25%colorLen]),
  }
  return letterPosColor[letter]
  
def demoEasterEgg():
  offset0   = (len(lines[1])-len(lines[0]))
  offset2   = (len(lines[1])-len(lines[2]))

  for i in range(0,max(len(lines[0]),len(lines[1]),len(lines[2]))):
    strip.setPixelColor(lines[1][i],COLORS[lines[1][i]])
    if len(lines[0]) >= len(lines[1])-i:
      strip.setPixelColor(lines[0][i-offset0],COLORS[lines[1][i-offset0]])
    if len(lines[2]) >= len(lines[1])-i:
      strip.setPixelColor(lines[2][i-offset2],COLORS[lines[2][i-offset2]])
    flickerAll(.5, flashTime=0.03)
    turnOffLights()
  turnOffLights()

def flickerAll(sleeptime, flickerTimes=6, flashTime=0.05):
  colorList = []
  for i in range(0,LED_COUNT):
    colorList.append(strip.getPixelColor(i))
  for i in range(1,random.randint(2,flickerTimes)):
    strip.show()
    time.sleep(flashTime)
    turnOffLights()
    strip.show()
    time.sleep(flashTime)
    for led in range(len(colorList)):
      strip.setPixelColor(led, colorList[led])
  lightOneUp(sleeptime)
  
def flickerOne(position, currentColor, flickerTimes=10, flashTime=0.05):
   for i in range(1,random.randint(2,flickerTimes)):
    strip.setPixelColor(position, OFF)
    strip.show()
    time.sleep(flashTime)
    strip.setPixelColor(position, currentColor)
    strip.show()
    time.sleep(flashTime)
  
def rainbowOn(speed, hold=2):
  for row in range(len(lines)):  
    for led in range(len(lines[row])):
      strip.setPixelColor(lines[row][led], COLORS[(lines[row][led])])
      strip.show()
      time.sleep(speed)
  time.sleep(hold)
  turnOffLights()

def spookyScary(times):
  # Turn all lights on
  for row in range(len(lines)):  
    for led in range(len(lines[row])):
      strip.setPixelColor(lines[row][led], COLORS[(lines[row][led])])
  strip.show()
  if times >= 2:
    for i in range(0,times):
      randomRow = random.randint(0,2)
      randomLed = random.randint(0,len(lines[randomRow])-1)
      currentColor = strip.getPixelColor(randomLed)
      flickerOne(randomLed, currentColor)
      time.sleep(random.uniform(.5, 2.5))
  turnOffLights()
  
  
def realRainbow():
  offset0   = (len(lines[1])-len(lines[0]))
  offset2   = (len(lines[1])-len(lines[2]))
  rainbowColors = [Color(255,0,255),Color(255,0,255),Color(255,0,255),
                   Color(75,0,130),Color(75,0,130),Color(0,0,255),Color(0,0,255),
                   Color(0,255,0),Color(0,255,0),Color(0,255,0),Color(255,255,0),Color(255,255,0),
                   Color(255,127,0),Color(255,127,0),Color(255,127,0),Color(255,0,0),
                   Color(255,0,0)]
  for i in range(0,max(len(lines[0]),len(lines[1]),len(lines[2]))):
    strip.setPixelColor(lines[1][i],rainbowColors[i])
    if len(lines[0]) >= len(lines[1])-i:
      strip.setPixelColor(lines[0][i-offset0],rainbowColors[i])
    if len(lines[2]) >= len(lines[1])-i:
      strip.setPixelColor(lines[2][i-offset2],rainbowColors[i])
    lightOneUp(.05)
  for i in range(0,max(len(lines[0]),len(lines[1]),len(lines[2]))):
    strip.setPixelColor(lines[1][i],OFF)
    if len(lines[0]) >= len(lines[1])-i:
      strip.setPixelColor(lines[0][i-offset0],OFF)
    if len(lines[2]) >= len(lines[1])-i:
      strip.setPixelColor(lines[2][i-offset2],OFF)
    lightOneUp(.05)
  turnOffLights()
  
"""  
# Work in Progress
def meantimeLooper():
  while textID == request.args.getlist('SmsMessageSid'):
    chooser = random.randint(0,2)
    if chooser == 0:
      spookyScary(5)
    elif chooser == 1:
      rainbowOn(.3)
    else:
      demoEasterEgg()
    time.sleep(5)
"""
  
if __name__ == "__main__":
  # Create NeoPixel object with appropriate configuration
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
  # Initialize the library (must be called once before other functions)
  strip.begin()
  rainbowOn(.01)
  turnOffLights()
  app.run()
