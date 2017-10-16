import code, string, time, random, re
from flask import Flask
from flask import request
from neopixel import *
app = Flask(__name__)

# LED strip configuration:
LED_COUNT      = 50      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

#Predefined Colors
OFF = Color(0,0,0)
WHITE = Color(255,255,255)
RED = Color(255,0,0)
GREEN = Color(0,255,0)
BLUE = Color(0,0,255)
PURPLE = Color(128,0,128)
YELLOW = Color(255,255,0)
ORANGE = Color(255,50,0)
TURQUOISE = Color(64,224,208)
RANDOM = Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))

# Other vars
LIGHTSHIFT = 0  #shift the lights down the strand to the other end 
FLICKERLOOP = 3  #number of loops to flicker

#list of colors, tried to match the show as close as possible
COLORS = [YELLOW,GREEN,RED,BLUE,ORANGE,TURQUOISE,GREEN,
          YELLOW,PURPLE,RED,GREEN,BLUE,YELLOW,RED,TURQUOISE,GREEN,RED,BLUE,GREEN,ORANGE,
          YELLOW,GREEN,RED,BLUE,ORANGE,TURQUOISE,RED,BLUE, 
          ORANGE,RED,YELLOW,GREEN,PURPLE,BLUE,YELLOW,ORANGE,TURQUOISE,RED,GREEN,YELLOW,PURPLE,
          YELLOW,GREEN,RED,BLUE,ORANGE,TURQUOISE,GREEN,BLUE,ORANGE] 

@app.route("/")
def getTwilioMessage():
    rawSms = request.args.getlist('Body')
    sms = rawSms[0].encode("utf-8").lower()
    modifiedSms = re.sub('[^a-zA-Z0-9\n\.]', ' ', sms)

    # look up address value for eachLetter key and light up
    for eachLetter in modifiedSms:
      result = mapLetterToLed(eachLetter, len(COLORS))
      position = result[0]
      color = result[1]
      strip.setPixelColor(position, color)
      strip.show()
      time.sleep(2)
      strip.setPixelColor(position, OFF)
      strip.show()
      time.sleep(1)

    for led in range(len(26)): #TODO:remove hardcode
      strip.setPixelColor(led, OFF)
    strip.show()

# Map a lower case char to an LED
def mapLetterToLed(letter, colorLen): 
    letterPosColor = {
    'a': (0+LIGHTSHIFT, COLORS[0%colorLen]),
    'b': (1+LIGHTSHIFT, COLORS[1%colorLen]),
    'c': (2+LIGHTSHIFT, COLORS[2%colorLen]),
    'd': (3+LIGHTSHIFT, COLORS[3%colorLen]),
    'e': (4+LIGHTSHIFT, COLORS[4%colorLen]),
    'f': (5+LIGHTSHIFT, COLORS[5%colorLen]),
    'g': (6+LIGHTSHIFT, COLORS[6%colorLen]),
    'h': (7+LIGHTSHIFT, COLORS[7%colorLen]),
    'i': (8+LIGHTSHIFT, COLORS[8%colorLen]),
    'j': (9+LIGHTSHIFT, COLORS[9%colorLen]),
    'k': (10+LIGHTSHIFT, COLORS[10%colorLen]),
    'l': (11+LIGHTSHIFT, COLORS[11%colorLen]),
    'm': (12+LIGHTSHIFT, COLORS[12%colorLen]),
    'n': (13+LIGHTSHIFT, COLORS[13%colorLen]),
    'o': (14+LIGHTSHIFT, COLORS[14%colorLen]),
    'p': (15+LIGHTSHIFT, COLORS[15%colorLen]),
    'q': (16+LIGHTSHIFT, COLORS[16%colorLen]),
    'r': (17+LIGHTSHIFT, COLORS[17%colorLen]),
    's': (18+LIGHTSHIFT, COLORS[18%colorLen]),
    't': (19+LIGHTSHIFT, COLORS[19%colorLen]),
    'u': (20+LIGHTSHIFT, COLORS[20%colorLen]),
    'v': (21+LIGHTSHIFT, COLORS[21%colorLen]),
    'w': (22+LIGHTSHIFT, COLORS[22%colorLen]),
    'x': (23+LIGHTSHIFT, COLORS[23%colorLen]),
    'y': (24+LIGHTSHIFT, COLORS[24%colorLen]),
    'z': (25+LIGHTSHIFT, COLORS[25%colorLen]),
    ' ': (26+LIGHTSHIFT, COLORS[26%colorLen]),
    }
    return letterPosColor[letter]


if __name__ == "__main__":
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    app.run()
