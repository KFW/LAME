# for adafruit circuit playground express
# flash w or w/o buzz morse for "lame" or "SOS"
"""
The dot duration is the basic unit of time measurement in code transmission. 
The duration of a dash is three times the duration of a dot. 
Each dot or dash is followed by a short silence, equal to the dot duration. 
The letters of a word are separated by a space equal to three dots (one dash), 
and the words are separated by a space equal to seven dots. (from Wikipedia)
some code from AdaFruit examples
updated with new library - cpx
"""

import time
from adafruit_circuitplayground.express import cpx


CODE = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
        
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' 
        }

DOT = 0.05 # 100 ms
DASH = 3 * DOT
GAP = 2 * DOT  # needed if we've already waited one dot
SPACE = 4 * DOT  # would be 7 but will have already waited one DOT and one GAP
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# prep neopixels
cpx.pixels.brightness = 0.05  # control overall brightness here
                             # could have done it with the color settings
cpx.pixels.fill(GREEN)
time.sleep(2)
cpx.pixels.fill(BLACK)


TONE = 1047


word = "LAME"  # set initial condition
color = BLUE

while 1:
    # toggle between words; will set to whichever button pressed most recently
    if cpx.button_a:
        word = 'LAME'
        color = BLUE
    elif cpx.button_b:
        word = 'SOS'
        color = RED

    for letter in word:
        for c in CODE[letter]:
            if c == '.':
                cpx.pixels.fill(color)
                if not cpx.switch:  # want tone if switch to right, which is 'False'
                    cpx.play_tone(TONE, DOT)
                time.sleep(DOT)
                cpx.pixels.fill(BLACK)
                time.sleep(DOT)
            else:  # must be dash
                cpx.pixels.fill(color)
                if not cpx.switch:   
                    cpx.play_tone(TONE, DASH)
                time.sleep(DASH)
                cpx.pixels.fill(BLACK)
                time.sleep(DOT)
        time.sleep(GAP)     # wait additional GAP ms between characters
    time.sleep(SPACE)       # wait additional SPACE ms for word spacing
