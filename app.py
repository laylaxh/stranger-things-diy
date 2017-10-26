import code, string, time, random, re
from flask import Flask
from flask import request
from neopixel import *

"""
code.interact(local=dict(globals(), **locals()))
TODO:
 Demogorgon walk
 Message charcter limit
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
                  
lines = [list(range(34,50)),list(reversed(range(15,32))), list(range(0,13))]


friendNumberMap = {
  '+13603493405': 'steve rocks', # Steve
  '+18182697821': 'layla is sexy', # Layla
  '+13233636062': 'icu zach', # Zach
  '+13233957777': 'brian do a handstand' # Brian
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
  rawSms      = request.args.getlist('Body')
  sms         = rawSms[0].encode("utf-8").lower()
  modifiedSms = re.sub('[^a-zA-Z0-9\n\s]', '', sms).split()
  return modifiedSms 

def preMessageDisplay():
  totalPixels  = range(strip.numPixels())

  # All LEDs turn on in one of the predefined COLORS
  for i in totalPixels:
    strip.setPixelColor(i, COLORS[random.randint(0,(len(COLORS)-1))])
  lightOneUp(.5)

  # Kill lights off in random order
  pixelIndices = list(totalPixels)
  random.shuffle(pixelIndices)

  for led in totalPixels:
    strip.setPixelColor(pixelIndices[led], OFF)
    lightOneUp(random.randint(1,30)/1000.0)

  # Flash on/off
  for i in totalPixels:
    strip.setPixelColor(i, COLORS[random.randint(0,(len(COLORS)-1))])
  lightOneUp(.5)

  turnOffLights()

def responseChooser(message):
  
  #print(request.args.getlist('DateSent').encode("utf-8"))
  
  if len(message) == 1 and message[0] == 'run':
    runEasterEgg()
  else:
    normalMessage(message)
    
##  code.interact(local=dict(globals(), **locals()))

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
    lightOneUp(.1)

  # Flash Red
  for i in range(20):
    for led in range(strip.numPixels()):
      if strip.getPixelColor(led) == RED:
        strip.setPixelColor(led, WHITE)
      else:
        strip.setPixelColor(led, RED)
    lightOneUp(.2)

def mapLetterToLed(letter, colorLen):
  letterPosColor = {
  'a': (34+LIGHTSHIFT,  COLORS[0%colorLen]),
  'b': (36+LIGHTSHIFT,  COLORS[1%colorLen]),
  'c': (38+LIGHTSHIFT,  COLORS[2%colorLen]),
  'd': (40+LIGHTSHIFT,  COLORS[3%colorLen]),
  'e': (42+LIGHTSHIFT,  COLORS[4%colorLen]),
  'f': (44+LIGHTSHIFT,  COLORS[5%colorLen]),
  'g': (46+LIGHTSHIFT,  COLORS[6%colorLen]),
  'h': (48+LIGHTSHIFT,  COLORS[7%colorLen]),
  'i': (49+LIGHTSHIFT,  COLORS[8%colorLen]),
  'j': (31+LIGHTSHIFT,  COLORS[9%colorLen]),
  'k': (29+LIGHTSHIFT, COLORS[10%colorLen]),
  'l': (27+LIGHTSHIFT, COLORS[11%colorLen]),
  'm': (25+LIGHTSHIFT, COLORS[12%colorLen]),
  'n': (23+LIGHTSHIFT, RED),                # COLORS[13%colorLen]
  'o': (21+LIGHTSHIFT, COLORS[14%colorLen]),
  'p': (19+LIGHTSHIFT, COLORS[15%colorLen]),
  'q': (17+LIGHTSHIFT, COLORS[16%colorLen]),
  'r': (15+LIGHTSHIFT, TURQUOISE),          # COLORS[17%colorLen]
  's': (0+LIGHTSHIFT, COLORS[18%colorLen]),
  't': (2+LIGHTSHIFT, COLORS[19%colorLen]),
  'u': (4+LIGHTSHIFT, BLUE),               # COLORS[20%colorLen]
  'v': (6+LIGHTSHIFT, COLORS[21%colorLen]),
  'w': (8+LIGHTSHIFT, COLORS[22%colorLen]),
  'x': (10+LIGHTSHIFT, COLORS[23%colorLen]),
  'y': (11+LIGHTSHIFT, COLORS[24%colorLen]),
  'z': (12+LIGHTSHIFT, COLORS[25%colorLen]),
  }
  return letterPosColor[letter]
  
def demoEasterEgg():
  offset0 = (len(lines[1])-len(lines[0]))
  offset2 = (len(lines[1])-len(lines[2]))

  for i in range(0,max(len(lines[0]),len(lines[1]),len(lines[2]))):
    strip.setPixelColor(lines[1][i],COLORS[lines[1][i]])
    if len(lines[0]) >= len(lines[1])-i:
      strip.setPixelColor(lines[0][i-offset0],COLORS[lines[1][i-offset0]])
    if len(lines[2]) >= len(lines[1])-i:
      strip.setPixelColor(lines[2][i-offset2],COLORS[lines[2][i-offset2]])
    flickerOn(.5)
    turnOffLights()
  turnOffLights()

# Work in progress  
def flickerOn(sleeptime, flickerTimes=6, flashTime=0.05):
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


if __name__ == "__main__":
  # Create NeoPixel object with appropriate configuration
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
  # Initialize the library (must be called once before other functions)
  strip.begin()
  demoEasterEgg()
  app.run()
