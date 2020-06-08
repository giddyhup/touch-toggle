#!/usr/bin/python3
# needs to be run with sudo rights
# package evdev must be installed globally:
# sudo -H pip3 install evdev

from evdev import InputDevice, ecodes, categorize
import time

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

# function to toggle screen state
def screentoggle(wantedstate):
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
            if debug: print(f'Touch detected and screen state = {scrstate}'.format(scrstate))
            # act on touch events within the defined region when the screen is on
            if scrstate == '0':
                # turn screen off
                screentoggle('1')
                # reset variable
                BTNstate = "0"
                # debounce
                time.sleep(.1)
            # act on touch events anywhere when the screen is off
            if (scrstate == '1'):
                # turn screen on and let events pass
                screentoggle('0')
                # reset variables
                BTNstate = "0"
                # debounce
                time.sleep(.1)
    # debounce
    time.sleep(.1)
