# for adafruit circuit playground express
# flash w or w/o buzz morse for "lame" or "SOS"
"""
The dot duration is the basic unit of time measurement in code transmission. 
The duration of a dash is three times the duration of a dot. 
Each dot or dash is followed by a short silence, equal to the dot duration. 
The letters of a word are separated by a space equal to three dots (one dash), 
and the words are separated by a space equal to seven dots. (from Wikipedia)

some code from AdaFruit examples
"""

import board
import time
from digitalio import DigitalInOut, Direction, Pull
import audioio
import math
import array
import neopixel


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

DOT = 0.15 # 150 ms
DASH = 3 * DOT
GAP = 2 * DOT # needed if we've already waited one dot
SPACE = 4 * DOT # would be 7 but will have already waited one DOT and one GAP
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255,0)

buttonA = DigitalInOut(board.BUTTON_A)
buttonA.direction = Direction.INPUT
buttonA.pull = Pull.DOWN

buttonB = DigitalInOut(board.BUTTON_B)
buttonB.direction = Direction.INPUT
buttonB.pull = Pull.DOWN

switch = DigitalInOut(board.SLIDE_SWITCH)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

# prep neopixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1)
pixels.fill(GREEN)
pixels.show()  # confirm working
time.sleep(2)
pixels.fill(BLACK)
pixels.show

# prep tone
FREQUENCY = 440    # 440 Hz middle 'A'
SAMPLERATE = 8000  # 8000 samples/second, recommended!
 
# Generate one period of sine wav.
length = SAMPLERATE // FREQUENCY
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / 18) * (2 ** 15) + 2 ** 15)

spkrenable = DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = Direction.OUTPUT
spkrenable.value = True
 
sample = audioio.AudioOut(board.SPEAKER, sine_wave)
sample.frequency = SAMPLERATE

## end tone portion

word = "LAME" # set initial condition
color = BLUE

while 1:
    # toggle between words; will set to whichever button pressed most recently
    if buttonA.value == True:
        word = 'LAME'
        color = BLUE
    elif buttonB.value == True:
        word = 'SOS'
        color = RED

    for letter in word:
        for c in CODE[letter]:
            if c == '.':
                pixels.fill(color)
                pixels.show()
                if not switch.value: # want tone if switch to right, which is 'False'
                    sample.play(loop=True) 
                time.sleep(DOT)
                pixels.fill(BLACK)
                pixels.show()
                sample.stop()
                time.sleep(DOT)
            else: # must be dash
                pixels.fill(color)
                pixels.show()
                if not switch.value:   
                    sample.play(loop=True) 
                time.sleep(DASH)
                pixels.fill(BLACK)
                pixels.show()
                sample.stop()
                time.sleep(DOT)
        time.sleep(GAP)     # wait additional GAP ms between characters
    time.sleep(SPACE)       # wait additional SPACE ms for word spacing
