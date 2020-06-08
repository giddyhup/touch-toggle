#!/usr/bin/python3
# needs to be run with sudo rights
# package evdev must be installed globally:
# sudo -H pip3 install evdev

from evdev import InputDevice, ecodes, categorize
import time

# coordinates, where touch events cause action
# top y, top x, width, height
topy,topx,w,h = 0,450,574,139

# coordinates converted to ranges
hrange = range(topx, topx + w)
vrange = range(topy, topy + h)

# debug flag, no script output when False
debug = True
if debug: print('debug is on')

# touch screen device 
dev = InputDevice('/dev/input/event0')

# screen state, "0" is on; "1" is off, only root can write
screenstatefile = '/sys/class/backlight/rpi_backlight/bl_power'

# read screen state at start
f = open(screenstatefile, 'r')
scrstate = f.read().rstrip('\n')
f.close()

# init vars
BTNstate = 0
X = -1
Y = -1

# grab screen events when it is off
if (scrstate == '1'):
    if debug: print("screen is off, grabbing input")
    dev.grab()

# function to toggle screen state and to grab input
def grabandscreentoggle(wantedstate):
    if wantedstate == '1': # screen should be turned be off
        # all input will be grabbed
        dev.grab()
    else:
        dev.ungrab()
    # actually toggling the screen by writing to file
    f = open(screenstatefile, 'w')
    f.write(wantedstate)
    f.close()

# read events and categorize
for event in dev.read_loop():
    absevent = categorize(event)
    if ecodes.bytype[absevent.event.type][absevent.event.code] == 'BTN_TOUCH':
        BTNstate = absevent.event.value
        # read screen state when touch is detected
        if BTNstate == 1:
            f = open(screenstatefile, 'r')
            scrstate = f.read().rstrip('\n')
            f.close()
        # reset X and Y when there was no touch
        if BTNstate == 0:
            X = -1
            Y = -1
    # get coordinates
    if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Y':
        Y = absevent.event.value
    if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_X':
        X = absevent.event.value
    # check if touch was detected and there are valid coordinates
    if (BTNstate == 1) and (X > -1) and (Y > -1 ):
        if debug: print(f'Touch at {X}/{Y} and screen state = {scrstate}'.format(X,Y,scrstate))
        # act on touch events within the defined region when the screen is on
        if (X in hrange) and (Y in vrange) and (scrstate == '0'):
            # turn screen off and activate events grabbing
            grabandscreentoggle('1')
            # reset variables
            BTNstate = "0"
            X = -1
            Y = -1
            # debounce
            time.sleep(.1)
        # act on touch events anywhere when the screen is off
        if (scrstate == '1'):
            # turn screen on and let events pass
            grabandscreentoggle('0')
            # reset variables
            BTNstate = "0"
            X = -1
            Y = -1
            # debounce
            time.sleep(.1)
    # debounce
    time.sleep(.1)
