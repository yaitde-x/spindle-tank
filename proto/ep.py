#!flask/bin/python
from flask import Flask
from flask import request

import time
import math
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 7       # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

app = Flask(__name__)
@app.route('/')

def index():
    return "Hello, World!"

@app.route('/postjson', methods=['POST'])
def post():
    print(request.is_json)
    content = request.get_json()
    #print(content)
    print(content['id'])
    print(content['name'])
    return 'JSON posted'

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    app.run(debug=True, host='0.0.0.0')

