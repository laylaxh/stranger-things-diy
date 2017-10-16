import code
import re
import random
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

#Predefined Colors and Masks
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
ALPHABET = '*******abcdefghijklm********zyxwvutsrqpon*********'  #alphabet that will be used
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

    colorLen = len(COLORS)
    # #Initialize all LEDs
    # for i in range(len(ALPHABET)):
    #   strip.setPixelColor(i+LIGHTSHIFT, COLORS[i%colorLen])
    # strip.show()
    for eachLetter in modifiedSms:
      lightUpLetter(eachLetter) # look up address value for eachLetter key and light up
    strip.show()
    # code.interact(local=dict(globals(), **locals()))

# Map a lower case char to an LED
def lightUpLetter(letter): 
  letterToLEDAddress = {
    'a': strip.setPixelColor(0+LIGHTSHIFT, COLORS[0%colorLen]),
    'b': strip.setPixelColor(1+LIGHTSHIFT, COLORS[1%colorLen]),
    'c': strip.setPixelColor(2+LIGHTSHIFT, COLORS[2%colorLen]),
    # 'd': 4,
    # 'e': 5,
    # 'f': 6,
    # 'g': 7,
    # 'h': 8,
    # 'i': 9,
    # 'j': 10,
    # 'k': 11,
    # 'l': 12,
    # 'm': 13,
    # 'n': 14,
    # 'o': 15,
    # 'p': 16,
    # 'q': 17,
    # 'r': 18,
    # 's': 19,
    # 't': 20,
    # 'u': 21,
    # 'v': 22,
    # 'w': 23,
    # 'x': 24,
    # 'y': 25,
    # 'z': 26,
    # ' ': 27,
    }
  return letterToLEDAddress[letter]


if __name__ == "__main__":
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    app.run()
